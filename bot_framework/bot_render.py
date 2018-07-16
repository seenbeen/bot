import pygame

from util.bot_math import *
from util.pattern.bot_singleton import Singleton
from util.bot_collections import DictUtil

class RectUtil:
    @staticmethod
    def findAABB(pts):
        if len(pts) == 0:
            raise Exception("Please provide at least one point to method findAABB")

        minX, minY = pts[0].x, pts[0].y
        maxX, maxY = pts[0].x, pts[0].y
        
        for p in pts:
            minX = min(minX, p.x)
            minY = min(minY, p.y)
            maxX = max(maxX, p.x)
            maxY = max(maxY, p.y)

        return pygame.Rect(map(int, [minX, minY, maxX - minX, maxY - minY]))

    @staticmethod
    def genRectPts(rect):
        p = Vector2(rect.x, rect.y)
        w = Vector2(rect.w, 0)
        h = Vector2(0, rect.h)
        return [p, p+w, p+w+h, p+h]

class BOTRenderer:
    def __init__(self, screenWidth, screenHeight):
        self.__screenWidth = screenWidth
        self.__screenHeight = screenHeight
        self.__screen = pygame.display.set_mode((screenWidth, screenHeight))

        # configuration-related
        self.__compositingChain = [] # TODO: Use LL for iteration
        self.__renderables = {}
        self.__scenes = {}
        self.__cameras = {}
        self.__viewports = {}
        self.__compositingCache = BOTCompositingCache(self.__screen)

    ''' Shutdown of the renderer, called by Singleton shutdown. '''
    def __del__(self):
        pass

    # Component Accessors
    ''' Returns a tuple containing the screen dimensions. '''
    def getScreenDimensions(self):
        return (self.__screenWidth, self.__screenHeight)

    '''
        Returns the renderable matching the given name.
        Raises an exception if no such renderable exists.
    '''
    def getRenderable(self, renderableName):
        return DictUtil.tryFetch(self.__renderables, renderableName,
                                  ('Attempting to fetch non-existent '
                                   'renderable %s from renderer!')%renderableName)

    '''
        Returns the scene matching the given name.
        Raises an exception if no such scene exists.
    '''
    def getScene(self, sceneName):
        return DictUtil.tryFetch(self.__scenes, sceneName,
                                  ('Attempting to fetch non-existent '
                                   'scene %s from renderer!')%sceneName)

    '''
        Returns the camera matching the given name.
        Raises an exception if no such camera exists.
    '''
    def getCamera(self, cameraName):
        return DictUtil.tryFetch(self.__cameras, cameraName,
                                  ('Attempting to fetch non-existent '
                                   'camera %s from renderer!')%cameraName)

    '''
        Returns the viewport matching the given name.
        Raises an exception if no such viewport exists.
    '''
    def getViewport(self, viewportName):
        return DictUtil.tryFetch(self.__viewports, viewportName,
                                  ('Attempting to fetch non-existent '
                                   'viewport %s from renderer!')%viewportName)

    # Configuration Registration Methods
    ''' Chains a compositor onto the current compositing chain. '''
    def chainCompositor(self, compositor):
        compositor.init(self.__compositingCache)
        self.__compositingChain.append(compositor)

    ''' Adds a Renderable to the current state of the renderer. '''
    def registerRenderable(self, renderable):
        name = renderable.getName()
        DictUtil.tryStrictInsert(self.__renderables, name, renderable,
                                  ('Attempting to override existing '
                                   'renderable %s in renderer!')%name)

    ''' Adds a Scene to the current state of the renderer. '''
    def registerScene(self, scene):
        name = scene.getName()
        DictUtil.tryStrictInsert(self.__scenes, name, scene,
                                  ('Attempting to override existing '
                                   'scene %s in renderer!')%name)

    ''' Adds a Viewport to the current state of the renderer. '''
    def registerViewport(self, viewport):
        name = viewport.getName()
        DictUtil.tryStrictInsert(self.__viewports, name, viewport,
                                  ('Attempting to override existing '
                                   'viewport %s in renderer!')%name)

    ''' Adds a Camera to the current state of the renderer. '''
    def registerCamera(self, camera):
        name = camera.getName()
        DictUtil.tryStrictInsert(self.__cameras, name, camera,
                                  ('Attempting to override existing '
                                   'camera %s in renderer!')%name)

    # Configuration Unregistration Methods
    '''
        Clears the entire compositing chain.
        Note: Renderer compositing will have to be reconfigured
        or nothing will display.
    '''
    def clearCompositingChain(self):
        for compositor in self.__compositingChain:
            compositor.cleanup(self.__compositingCache)
        del self.__compositingChain[:]

    '''
        Attempts to unregister renderable from renderer.
        Note that before this happens, the renderable must
        be removed from all scenes.
    '''
    def unregisterRenderable(self, renderable):
        name = renderable.getName()
        removed = DictUtil.tryRemove(self.__renderables, name,
                                     ('Attempting to unregister non-existent '
                                      'Renderable %s from renderer!')%name)
        if removed != renderable:
            raise Exception('FATAL: Unregistered Renderable does not match provided Renderable despite sharing name "%s"'%name)

    '''
        Attempts to remove scene from renderer.
    '''
    def unregisterScene(self, scene):
        name = scene.getName()
        removed = DictUtil.tryRemove(self.__scenes, name,
                                     ('Attempting to unregister non-existent '
                                      'Scene %s from renderer!')%name)
        if removed != scene:
            raise Exception('FATAL: Unregistered Scene does not match provided Scene despite sharing name "%s"'%name)
    
    '''
        Attempts to remove camera from renderer.
    '''
    def unregisterCamera(self, camera):
        name = camera.getName()
        removed = DictUtil.tryRemove(self.__cameras, name,
                                     ('Attempting to unregister non-existent '
                                      'Camera %s from renderer!')%name)
        if removed != camera:
            raise Exception('FATAL: Unregistered Camera does not match provided Camera despite sharing name "%s"'%name)

    '''
        Attempts to remove viewport from renderer.
    '''
    def unregisterViewport(self, viewport):
        name = viewport.getName()
        removed = DictUtil.tryRemove(self.__viewports, name,
                                     ('Attempting to unregister non-existent '
                                      'Viewport %s from renderer!')%name)
        if removed != viewport:
            raise Exception('FATAL: Unregistered Viewport does not match provided Viewport despite sharing name "%s"'%name)

    def update(self, deltaTime):
        for renderableKey in self.__renderables:
            self.__renderables[renderableKey]._onUpdate(deltaTime)

        self.__screen.fill((255, 255, 255))
        for compositor in self.__compositingChain:
            compositor.composite(self.__compositingCache)
        pygame.display.flip()

    # Render Methods, to be called by compositors
    def renderSceneTo(self, sceneName, cameraName, viewportName, targetSurface):
        scene = self.getScene(sceneName)
        camera = self.getCamera(cameraName)
        viewport = self.getViewport(viewportName)
        renderables = scene.query(camera)

        # finally render to surface
        targetSurface.set_clip(viewport.position.toIntTuple() + viewport.dimensions.toIntTuple())

        vcMatrix = viewport.getMatrix() * camera.getMatrix()
        for renderable in renderables:
            renderable._render(vcMatrix * renderable.transform.getMatrix(), targetSurface)

        targetSurface.set_clip(None)

Singleton.transformToSingleton(BOTRenderer)

'''
    RenderEntity is just a simple wrapper facilitating
    naming.
    
    It provides a constructor which generates arbitrary
    unique names when a name isn't important.
'''
class BOTRenderEntity(object):
    __EntCount = 0

    def __init__(self, name=None):
        if name != None:
            self.__name = name
        else:
            self.__name = "%s-%i"%(self.__class__.__name__, BOTRenderEntity.__EntCount)
            BOTRenderEntity.__EntCount += 1

    def getName(self):
        return self.__name

'''
    A scene is essentially a container of renderables that will be
    potentially rendered together by a camera.

    Scene must support:
    - insertion and deletion of renderables
    - querying of all renderables which overlap a given rectangle (may not be axis-aligned).
'''
class BOTScene(BOTRenderEntity):
    def __init__(self, name=None):
        super(BOTScene, self).__init__(name)
        self.__renderables = []

    def addRenderable(self, renderable):
        self.__renderables.append(renderable)

    def removeRenderable(self, renderable):
        self.__renderables.remove(renderable)

    def query(self, camera):
        # TODO: Perform an optimized query
        #       - Maybe use Separating Axis to test non AABB overlap so we don't have to do this...
        result = []
        camRect = RectUtil.findAABB(map(lambda v: camera.transform.getMatrix() * v, camera._genBounds()))
        for renderable in self.__renderables:
            objRect = RectUtil.findAABB(map(lambda v: renderable.transform.getMatrix() * v, renderable._genBounds()))
            if camRect.colliderect(objRect):
                result.append(renderable)
        return result

    # TODO: update the scene manager so that querying returns accurate results if
    # objects shifted around since last frame

'''
    Your everyday viewport class is essentially a glorified
    int rectangle, which defines a region on a surface to render to.

    Note that since this is in screen space, (0,0) corresponds to the
    top-left corner.
'''
class BOTViewport(BOTRenderEntity):
    def __init__(self, width, height, name=None):
        super(BOTViewport, self).__init__(name)
        self.position = Vector2()
        self.dimensions = Vector2(width, height)

    def getMatrix(self):
        # TODO: Store this so it isn't generated every time
        return Mat33Util.getViewportMatrix(self.position, self.dimensions)

'''
    The Camera class tracks a few things other than a transform.
    The Camera has a Width and Height specified in Rendering-World units,
    which are used for culling.
'''
class BOTCamera(BOTRenderEntity):
    def __init__(self, width, height, name=None):
        super(BOTCamera, self).__init__(name)
        self.transform = Transform()
        self.dimensions = Vector2(width, height)
        self.__rectPts = RectUtil.genRectPts(pygame.Rect(-width/2, -height/2, width, height))

    '''
        Find the corresponding minimum AABB which covers
        the camera's (possibly rotated) frustum.
    '''
    def _genBounds(self):
        return self.__rectPts

    def getMatrix(self):
        # TODO: Store this so it isn't generated every time
        return Mat33Util.getCamMatrix(self.transform, self.dimensions)

'''
    The renderer generates images to the screen by via a series of
    rendering steps called compositing steps.

    A compositor is responsible for one such step in the rendering process.
    For instance, the CameraCompositor is responsible for rendering the scene
    from a given Camera's POV, onto a target surface.
    
    The CompositingCache (CC) allows compositors to, during initialization,
    allocate the resources needed to execute. Compositors use the CC for
    communication, if multiple steps, or any post-processing is needed.

    The BOTCompositingCache.SCREEN_KEY surface is reserved as the surface corresponding
    to the window's screen, and is always available in the compositing cache. 

    During execution, a compositor can also request a query [from the renderer] to
    a particular scene (or multiple for that matter) and directly render using said
    objects. (In fact, the CameraCompositor does just this).
'''
class BOTCompositor(object):
    def init(self, compositingCache):
        raise Exception('Error: [BOTCompositor]%s.init not implemented.'%(self.__class__.__name__))
    
    def composite(self, compositingCache):
        raise Exception('Error: [BOTCompositor]%s.composite not implemented.'%(self.__class__.__name__))

    def cleanup(self, compositingCache):
        raise Exception('Error: [BOTCompositor]%s.cleanup not implemented.'%(self.__class__.__name__))

'''
    To make life a bit easier, the CameraCompositor is a Compositor
    implementing rendering functionality, which draws the given Camera's
    POV onto a given surface identified by a passed-in CC key.

    Note: This means that the CameraCompositor assumes the resource has already
    been pre-allocated.
'''
class BOTCameraCompositor(BOTCompositor):
    def __init__(self, sceneName, cameraName, viewportName, surfKey):
        self.__sceneName = sceneName
        self.__cameraName = cameraName
        self.__viewportName = viewportName
        self.__surfKey = surfKey

    def init(self, compositingCache):
        pass

    def composite(self, compositingCache):
        BOTRenderer.instance().renderSceneTo(self.__sceneName, self.__cameraName,
                                          self.__viewportName,
                                          compositingCache.getCachedSurface(self.__surfKey))

    def cleanup(self, compositingCache):
        pass
        
class BOTCompositingCache:
    '''
        The CompositingCache is the glue used to allow input/output
        communication between the different Compositing steps.
    '''
    __SCREEN_KEY = 'SCREEN'
    
    @staticmethod
    def getScreenKey():
        return BOTCompositingCache.__SCREEN_KEY

    def __init__(self, screen):
        self.__cache = {}
        self.__cache[BOTCompositingCache.__SCREEN_KEY] = screen
        self.__screen = screen

    def cacheSurface(self, key, surface):
        DictUtil.tryStrictInsert(self.__scenes, key, surface,
                                  ('Attempting to override existing '
                                   'surface %s in CompositingCache!')%key)

    def getCachedSurface(self, key):
        return DictUtil.tryFetch(self.__cache, key,
                                  ('Attempting to fetch non-existent '
                                   'surface %s from CompositingCache!')%key)

    '''
        Clears all compositor-stored information within
        the cache. Does not remove BOTCompositingCache.__SCREEN_KEY.

        WARNING: Do not call this unless you are 150%
        sure you know what you're doing. This will
        invalidate all surface references loaded in by
        compositors during initialization, potentially
        borking rendering.
    '''
    def clearCache(self):
        self.__cache.clear()
        self.__cache[BOTCompositingCache.__SCREEN_KEY] = self.__screen

class BOTRenderable(BOTRenderEntity):
    def __init__(self, name=None):
        super(BOTRenderable, self).__init__(name)
        self.transform = Transform()
        self.layer = 0
        self.debug = False

    def destroy(self):
        BOTRenderer.instance().unregisterRenderable(self)

    def _genBounds(self):
        raise Exception('Error: [BOTRenderable]%s._genBounds not implemented.'%(self.__class__.__name__))

    def _onUpdate(self, deltaTime):
        raise Exception('Error: [BOTRenderable]%s._onUpdate not implemented.'%(self.__class__.__name__))

    '''
        Wrapper render method called by internals. Allows
        insertion of debug information
    '''
    def _render(self, vcmMatrix, targetSurface):
        self._onRender(vcmMatrix, targetSurface)
        if self.debug:
            rect = RectUtil.findAABB(map(lambda v: vcmMatrix * v, self._genBounds()))
            pygame.draw.rect(targetSurface, (255, 0, 255), rect, 1)
            p1, p2, p3 = map(lambda p: (vcmMatrix * Vector2(*p)).toIntTuple(), [(0, 0), (20, 0), (0, 20)])

            # outline
            pygame.draw.line(targetSurface, (0, 0, 0), p1, p2, 4)
            pygame.draw.line(targetSurface, (0, 0, 0), p1, p3, 4)
            # axes
            pygame.draw.line(targetSurface, (255, 0, 0), p1, p2, 2)
            pygame.draw.line(targetSurface, (0, 255, 0), p1, p3, 2)
    '''
        Notes:
        - vcmMatrix is the matrix which applies everything needed
          to a coordinate in local space to get it into the proper screen
          space, taking into account this object's transform.
        - simply use it to determine location when rendering
    '''
    def _onRender(self, vcmMatrix, targetSurface):
        raise Exception('Error: [BOTRenderable]%s._onRender not implemented.'%(self.__class__.__name__))

    # 'into' the screen is positive
    def __cmp__(self, renderable):
        return self.layer > renderable.layer

class BOTPolygon(BOTRenderable):
    def __init__(self, pts, color, name=None):
        super(BOTPolygon, self).__init__(name)
        self.__pts = pts
        self.__color = color

    def _genBounds(self):
        return self.__pts
    
    def _onUpdate(self, deltaTime):
        pass

    def _onRender(self, vcmMatrix, targetSurface):
        newPts = map(lambda pt: (vcmMatrix * pt).toIntTuple(), self.__pts)
        pygame.draw.polygon(targetSurface, self.__color, newPts)
        pygame.draw.polygon(targetSurface, (0, 0, 0), newPts, 2) # outline

class BOTSprite(BOTRenderable):
    class Frame:
        '''
            Constructs a sprite frame.
            surface - Can be a subsurface as well. This will be blit onto the target surface.
                    Note: Surface must be arranged in such a way that the origin is located at
                            width(surface)/2, height(surface)/2 due to the way pygame rotates

            localRect - The local rectangle boundaries of the sprite frame itself such that
                (0, 0) of the rect will be the frame's local origin, and the rectangle defines
                whether the frame is visible or not.
            frameDelay - How long this frame should stay active before a swap.
        '''
        def __init__(self, surface, localRect, frameDelay):
            self.__surface = surface
            self.__frameDelay  = frameDelay
            self.__dims = Vector2(surface.get_width(), surface.get_height())
            self.__rectPts = RectUtil.genRectPts(localRect)

        '''
            Returns how much more time must elapse before the frame is switched.
            If this number is negative, the absolute value is how much remaining time must pass.
            If this number is positive, the amount is how much time is left of the elapsedTime
        '''
        def getRemainingTime(self, elapsedTime):
            return elapsedTime - self.__frameDelay

        '''
            This is where things get slightly "hocus pocus". We need to recompute a higher
            level transformation, since we don't have the power of texture coordinates ;_;'.
        '''
        def onRender(self, vcmMatrix, targetSurface):
            transform = Transform.fromMat33(vcmMatrix)
            absScale = Vector2(abs(transform.scale.x), abs(transform.scale.y))
            surf = pygame.transform.scale(self.__surface, (absScale * self.__dims).toIntTuple())
            surf = pygame.transform.flip(surf, transform.scale.x < 0, transform.scale.y < 0)
            # Notes: we're essentially working from screen space and in
            # screen space, rotations are backwards since the y axis is
            # essentially inverted which is why -rotation OTL
            surf = pygame.transform.rotate(surf, -transform.rotation)
            offset = -Vector2(surf.get_width(), surf.get_height())/2.0
            targetSurface.blit(surf, (transform.position + offset).toIntTuple())

        def genBounds(self):
            return self.__rectPts

    def __getCurrentFrame(self):
        return self.__currentAnimation[self.__currentFrameId]

    def __init__(self, initAnimationKey, initAnimationFrames, name=None):
        super(BOTSprite, self).__init__(name)
        self.__animations = { initAnimationKey : initAnimationFrames }
        self.__currentAnimation = initAnimationFrames
        self.__currentFrameId = 0

        self.__timeCounter = 0

    def setCurrentAnimation(self, animationKey, animationFrame=0):
        self.__currentAnimation = DictUtil.tryFetch(self.__animations, animationKey,
                                                    ('Attempting to set non-existent '
                                                     'animation %s in %s!')
                                                    % (animationKey, self.getName()))
        self.__currentFrameId = animationFrame

    def addAnimation(self, animationKey, animationFrames):
        DictUtil.tryStrictInsert(self.__animations, animationKey, animationFrames,
                                 ('Attempting to override existing '
                                  'animation %s in %s!') % (animationKey, self.getName()))

    def _genBounds(self):
        return self.__getCurrentFrame().genBounds()

    def _onUpdate(self, deltaTime):
        self.__timeCounter += deltaTime
        tRemaining = self.__getCurrentFrame().getRemainingTime(self.__timeCounter)
        while tRemaining >= 0:
            self.__currentFrameId = (self.__currentFrameId + 1) % len(self.__currentAnimation)
            self.__timeCounter = tRemaining
            tRemaining = self.__getCurrentFrame().getRemainingTime(self.__timeCounter)

    def _onRender(self, vcmMatrix, targetSurface):
        self.__getCurrentFrame().onRender(vcmMatrix, targetSurface)
