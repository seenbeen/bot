from bot_framework.bot_physics import *
from util.bot_math import *

def run():
    class Calculator:
        @staticmethod
        def calculateDamageWithResistance(damage, resistence):
            return max(damage - resistence, 0)

    class MyDude:
        def __init__(self, hp, resistence):
            self.__hp = hp
            self.__resistence = resistence

        def getResistence(self):
            return self.__resistence

        def takeDamage(self, n):
            self.__hp = max(0, self.__hp - n)

        def printStatus(self):
            print "MyDude has %i HP." % self.__hp

    class Fireball:
        def __init__(self, damage):
            self.damage = damage

        def getDamage(self):
            return self.damage

    class Tags:
        PROJECTILE = 'PROJECTILE'
        LIFEFORM = 'LIFEFORM'

    class LifeformProjectileResolver(BOTPhysicsCollisionResolver):
        def __init__(self):
            super(LifeformProjectileResolver,
                  self).__init__(Tags.LIFEFORM, Tags.PROJECTILE)

        def onResolve(self, lifeform, projectile):
            print "Projectile bashes lifeform"
            life = lifeform.getBoundObj()
            proj = projectile.getBoundObj()
            life.printStatus()
            dmg = Calculator.calculateDamageWithResistance(proj.getDamage(), life.getResistence())
            print ("Projectile does %i dmg." % dmg)
            life.takeDamage(dmg)
            life.printStatus()

            # pretend during this update fireball obj also went peace due to collision
            physx.removeRigidBody(rbFireball)
    
    BOTPhysicsSpace.initialize()
    physx = BOTPhysicsSpace.instance()

    # relevant game objects...
    myDude = MyDude(100, 15)
    fireBall = Fireball(50)

    # RBOs
    rbMyDude = BOTPhysicsRigidBody(myDude, BOTBoxCollider(Vector2(100,100)), Tags.LIFEFORM)
    rbFireball = BOTPhysicsRigidBody(fireBall, BOTBoxCollider(Vector2(50,50)), Tags.PROJECTILE)

    # Set Up A Resolver
    resolver = LifeformProjectileResolver()

    # now start to add stuff in
    physx.addResolver(resolver)
    physx.addRigidBody(rbMyDude)
    physx.addRigidBody(rbFireball)
    physx.pump() # pump the add ops through (might need a cleaner way to do this)

    # simulate our game loop thing

    # quick pointCast to see if we can pin both fireball and mydude
    pointCastPoint = Vector2(0,0)
    ptCastResult = physx.pointCast(pointCastPoint)
    print "Hit [%s] with pointCast %s" % (", ".join(map(lambda x: str(x.getBoundObj().__class__.__name__),
                                                        ptCastResult)),
                                          pointCastPoint)
    
    physx.update(0)
    physx.lateUpdate() # recall this flushes add/remove ops
    
    physx.update(0) # no more collision cuz fireball went peace
    physx.lateUpdate()

    BotPhysicsSpace.shutdown()
