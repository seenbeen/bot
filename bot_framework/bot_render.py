import pygame

from util.bot_math import *
from util.pattern.bot_singleton import Singleton

# dict manipulation utils with throw
class DictUtil:
    @staticmethod
    def tryFetch(d, key, failMessage=None):
        if key in d:
            return d[key]
        raise Exception(['Trying to fetch non-existent key %s from Dict.'%key, failMessage][failMessage != None])

    @staticmethod
    def tryStrictInsert(d, key, val, failMessage=None):
        if key in d:
            raise Exception(['Trying to insert existing key %s into Dict.'%key, failMessage][failMessage != None])
        d[key] = val

    @staticmethod
    def tryRemove(d, key, failMessage=None):
        if key in d:
            return d.pop(key)
        raise Exception(['Trying to remove non-existent key %s from Dict.'%key, failMessage][failMessage != None])

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

        return [Vector2(minX, minY), Vector2(maxX - minX, maxY - minY)]

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
        for renderable in self.__renderables:
            renderable._onUpdate(deltaTime)

        self.__screen.fill((255, 255, 255))
        for compositor in self.__compositingChain:
            compositor.composite(self.__compositingCache)
        pygame.display.flip()

    # Render Methods, to be called by compositors
    def renderSceneTo(self, sceneName, cameraName, viewportName, targetSurface):
        scene = self.getScene(sceneName)
        camera = self.getCamera(cameraName)
        viewport = self.getViewport(viewportName)
        renderables = scene.query(camera._genBoundingRect())

        # finally render to surface
        targetSurface.set_clip(viewport.position.toIntTuple() + viewport.dimensions.toIntTuple())

        vcMatrix = viewport.getMatrix() * camera.getMatrix()
        for renderable in renderables:
            renderable._onRender(vcMatrix * renderable.transform.getMatrix(), targetSurface)

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

    # TODO: Perform an optimized query
    def query(self, boundingRect):
        result = []
        for renderable in self.__renderables:
            if boundingRect.colliderect(renderable._genBoundingRect()):
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

    '''
        Find the corresponding minimum AABB which covers
        the camera's (possibly rotated) frustum.
    '''
    def _genBoundingRect(self):
        # TODO: Probably cache this as it's not the cheapest computation
        l = Vector2(self.dimensions.x / 2.0, 0.0)
        h = Vector2(0.0, self.dimensions.y / 2.0)
        p = self.transform.position

        intRect = map(Vector2.toIntTuple, RectUtil.findAABB([p-l-h, p-l+h, p+l+h, p+l-h]))

        return pygame.Rect(intRect[0] + intRect[1])

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

    def destroy(self):
        BOTRenderer.instance().unregisterRenderable(self)

    def _genBoundingRect(self):
        raise Exception('Error: [BOTRenderable]%s._genBoundingRect not implemented.'%(self.__class__.__name__))

    def _onUpdate(self, deltaTime):
        raise Exception('Error: [BOTRenderable]%s._onUpdate not implemented.'%(self.__class__.__name__))

    '''
        Notes:
        - vcmMatrix is the matrix which applies everything needed
          to a coordinate in local space to get it into the proper screen
          space, taking into account this object's transform.
        - simply use it to determine location when rendering
    '''
    def _onRender(self, vcmMatrix, surface):
        raise Exception('Error: [BOTRenderable]%s._onRender not implemented.'%(self.__class__.__name__))

    # 'into' the screen is positive
    def __cmp__(self, renderable):
        return self.layer > renderable.layer

class BOTPolygon(BOTRenderable):
    def __init__(self, pts, color, name=None):
        super(BOTPolygon, self).__init__(name)
        self.__pts = pts
        self.__color = color
        self.debug = False # trades some performance to show the computed AABB

    def _genBoundingRect(self):
        rect = RectUtil.findAABB(map(lambda pt: self.transform.getMatrix() * pt, self.__pts))
        intRect = map(Vector2.toIntTuple, rect)
        return pygame.Rect(intRect[0] + intRect[1])
    
    def _onUpdate(self, deltaTime):
        pass

    def _onRender(self, vcmMatrix, surface):
        newPts = map(lambda pt: (vcmMatrix * pt).toIntTuple(), self.__pts)
        pygame.draw.polygon(surface, self.__color, newPts)
        pygame.draw.polygon(surface, (0, 0, 0), newPts, 2) # outline

        # debug rect, rather expensive... we'll probably want to improve this
        if self.debug:
            p, d = RectUtil.findAABB(map(lambda pt: self.transform.getMatrix() * pt, self.__pts))
            l = Vector2(d.x, 0.0)
            h = Vector2(0.0, d.y)

            intRect = map(lambda v: Vector2.toIntTuple(vcmMatrix * self.transform.getInverseMatrix() * v), [p, p+l, p+l+h, p+h])

            pygame.draw.polygon(surface, (255, 0, 255), intRect, 2)

