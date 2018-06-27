from pygame import *
from util.bot_math import *
import math

def run():
    screen = display.set_mode((800, 600))

    running = True

    def rotatePt(r, ang):
        a = math.radians(ang)
        return [r * math.cos(a), r * math.sin(a)]

    def genStar(sides):
        return [map(int, rotatePt([100/3, 100][i%2], i*360/sides)) for i in range(sides)]

    def genCrossHair(crossHairSize):
        xLine = Vector2(crossHairSize, 0)
        yLine = Vector2(0, crossHairSize)
        return [-xLine, xLine, -yLine, yLine]

    camTransform = Transform()
    camTransform.scale = Vector2(0.75, 0.75)
    camDims = Vector2(800,600)

    vpPos = camDims * 0.25/2
    vpDims = camDims * 0.75

    center = Vector2()
    vecStar = map(lambda pt: Vector2(*pt), genStar(10))

    starTransform = Transform()
    myClock = time.Clock()

    ctr = 0
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False

        # controls to move the viewport around
        keys = key.get_pressed()
        deltaVector = Vector2()
        vel = 200/60.0 # 200 px / 60 frames

        # remember viewport coords are given in screen space (up is negative)
        if keys[K_UP]:
            deltaVector.y = -vel
        elif keys[K_DOWN]:
            deltaVector.y = vel
        if keys[K_LEFT]:
            deltaVector.x = -vel
        elif keys[K_RIGHT]:
            deltaVector.x = vel

        vpPos += deltaVector
        
        ctr = (ctr + 1)%360
        camTransform.position = Vector2(*rotatePt(150, ctr))
        starTransform.rotation = (starTransform.rotation + 2) % 360
        starTransform.position = Vector2(*rotatePt(100, -starTransform.rotation))
        
        vMat = Mat33Util.getViewportMatrix(vpPos, vpDims)
        cMat = Mat33Util.getCamMatrix(camTransform, camDims)

        mMat = starTransform.getMatrix()
        
        starRes = map(lambda v: vMat * cMat * mMat * v, vecStar)
        starResPt = map(Vector2.toIntTuple, starRes)

        centerRes = vMat * cMat * center # mMat is just Identity for center
        centerResPt = centerRes.toIntTuple()

        crossHairRes = map(lambda v: vMat * cMat * camTransform.getMatrix() * v, genCrossHair(10))
        crossHairResPt = map(Vector2.toIntTuple, crossHairRes)

        vpRect = Rect(*map(int, [vpPos.x, vpPos.y, vpDims.x, vpDims.y]))

        screen.fill((0, 0, 0))

        # clip to VP Rect to not render outside
        screen.set_clip(vpRect)
        
        draw.polygon(screen, (0, 255, 0), starResPt, 2)
        
        # we have to account for the camera's scale when showing paths
        draw.circle(screen, (255, 0, 255), centerResPt, int(150 / 0.75 * 0.75), 1)
        draw.circle(screen, (0, 255, 0), centerResPt, int(100 / 0.75 * 0.75), 1)

        # origin
        draw.circle(screen, (255, 0, 0), centerResPt, 5)

        # camera cross-hair
        draw.line(screen, (0, 255, 255), crossHairResPt[0], crossHairResPt[1], 2)
        draw.line(screen, (0, 255, 255), crossHairResPt[2], crossHairResPt[3] , 2)

        # draw the viewport rect
        draw.rect(screen, (255, 255, 255), vpRect, 2)

        # free up the screen clipping
        screen.set_clip(None)

        display.flip()
        
        myClock.tick(60)
    quit()
