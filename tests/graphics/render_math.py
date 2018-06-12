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

    center = Vector2()

    camTransform = Transform()
    camTransform.scale = Vector2(0.75, 0.75)
    camDims = Vector2(800,600)
    vpDims = Vector2(800,600)

    vecStar = map(lambda pt: Vector2(*pt), genStar(10))

    starTransform = Transform()
    myClock = time.Clock()

    ctr = 0
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
        ctr = (ctr + 1)%360
        camTransform.position = Vector2(*rotatePt(150, ctr))
        starTransform.rotation = (starTransform.rotation + 2) % 360
        starTransform.position = Vector2(*rotatePt(100, -starTransform.rotation))
        
        vMat = Mat33Util.getCamToViewportMatrix(camDims, vpDims)
        cMat = camTransform.getInverseMatrix()
        mMat = starTransform.getMatrix()
        
        res = map(lambda v: vMat * cMat * mMat * v, vecStar)
        resPt = map(lambda v: map(int, [v.x, v.y]), res)

        centerRes = vMat * cMat * center # note that mMat is just Identity for center
        centerResPt = map(int, [centerRes.x, centerRes.y])
        
        screen.fill((0, 0, 0))
        draw.polygon(screen, (0, 255, 0), resPt, 2)
        
        # we have to account for the camera's scale when showing paths
        draw.circle(screen, (255, 0, 255), centerResPt, int(150/0.75), 1)
        draw.circle(screen, (0, 255, 255), centerResPt, int(100/0.75), 1)

        # origin
        draw.circle(screen, (255, 0, 0), centerResPt, 5)

        # camera cross-hair
        crossHairSize = 10
        draw.line(screen, (0, 255, 0), (400, 300 - crossHairSize), (400, 300 + crossHairSize), 2)
        draw.line(screen, (0, 255, 0), (400 - crossHairSize, 300), (400 + crossHairSize, 300) , 2)
        
        display.flip()
        
        myClock.tick(60)
    quit()
