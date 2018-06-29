from pygame import Rect as pygame_Rect
from util.bot_collections import DictUtil
from util.bot_math import *
from util.pattern.bot_singleton import Singleton

class BOTPhysicsSpace:
    def __init__(self):
        self.__rigidBodies = {}
        self.__resolvers = {}

    def addRigidBody(self, rigidBody):
        name = rigidBody.getName()
        DictUtil.tryStrictInsert(self.__rigidBodies, name, rigidBody,
                                 ("Attempting to override existing "
                                  "'BOTRigidBody' '%s' in 'BOTPhysicsSpace'!") % name)

    def removeRigidBody(self, rigidBody):
        name = rigidBody.getName()
        removed = DictUtil.tryRemove(self.__rigidBodies, name, rigidBody,
                                     ("Attempting to remove non-existent "
                                      "'BOTRigidBody' '%s' from 'BOTPhysicsSpace'!") % name)

        if removed is not rigidBody:
            raise Exception("FATAL: Unregistered 'BOTRigidBody' does not match provided "
                            "'BOTRigidBody' despite sharing name '%s'" % name)

    def update(self, deltaTime):
        for rboKey in self.__rigidBodies:
            self.__rigidBodies[rboKey].update(deltaTime)

        n = len(self.__objects)
        for i in range(n):
            objA = self.__objects[i]
            for j in range(i+1, n):
                objB = self.__objects[j]
                if objA._collidesWith(objB):
                    resolverTuple = PhysicsCollisionResolverTuple(objA.getTag(), objB.getTag())
                    if resolverTuple in self.__resolvers:
                        self.__resolvers[resolverTuple]._resolve(objA, objB)

    def lateUpdate(self):
        self.pump()

Singleton.transformToSingleton(BOTPhysicsSpace)

def __BOTPhysicsSpaceQueue():
    QUEUED_METHODS = [BOTPhysicsSpace.addRigidBody, BOTPhysicsSpace.removeRigidBody]
    # I really don't care how this order goes, though this may matter later
    EventQueue.enQueueify(BOTPhysicsSpace, QUEUED_METHODS, lambda eventA, eventB: 0)

__BOTPhysicsSpaceQueue()

class BOTPhysicsRigidBody:
    def __init__(self, collider, tag):
        if not isinstance(collider, PhysicsCollider):
            raise Exception("Collider provided to 'BOTPhysicsRigidBodyObject' must be of type 'BOTPhysicsCollider', got '%s'."%collider.__class__.__name__)
        if not isinstance(tag, str):
            raise Exception("Tag provided to 'BOTPhysicsRigidBodyObject' must be of type 'str', got '%s'."%tag.__class__.__name__)

        self.__transform = Transform()
        self.__collider = collider
        self.__tag = tag
        self.__boundObject = None

    def getTransform(self):
        return self.__transform

    def setBoundObject(self, obj):
        self.__boundObject = obj

    def getBoundObject(self):
        return self.__boundObject

    def getTag(self):
        return self.__tag

    def _collidesWith(self, rbo):
        return self.__collider.collidesWith(rbo.__collider)

    def _update(self, deltaTime):
        self.__collider._applyTransform(self.__transform)

class BOTPhysicsCollider(object):
    def __init__(self, vertices):
        self.__vertices = vertices # note vertices are in local space
        self._applyTransform(self, Transform())

    def _applyTransform(self, transform):
        self.__worldVertices = map(lambda x: transform.getMatrix() * x, self.__vertices)

        # temporarily just compute the bounding rectangle here, and call it a day
        # we can use Separating Axis Test later if we really need to
        self.__AABB = pygame_Rect(reduce(lambda x, y: x + y, map(Vector2.toIntTuple, RectUtil.findAABB(self.__worldVertices)), []))
        
    def _collidesWith(self, collider):
        return self.__AABB.colliderect(collider.__AABB)

class BOTBoxCollider(BOTPhysicsCollider):
    def __init__(self, dimensions):
        wVector = Vector2(dimensions.x, 0)/2
        hVector = Vector2(0, dimensions.y)/2
        super(BOTBoxCollider, self).__init__([wVector + hVector, -wVector + hVector, -wVector + -hVector, wVector + -hVector])

class BOTPhysicsCollisionResolverTuple:
    def __init__(self, tagA, tagB):
        if not isinstance(tagA, str) or not isinstance(tagB, str):
            raise Exception("Tags provided to 'BOTPhysicsCollisionResolverTuple' must be of type 'str', got ('%s', '%s')." %
                            (tagA.__class__.__name__, tagB.__class__.__name__))
        self.__tagA = tagA
        self.__tagB = tagB

    def __hash__(self, other):
        if self.__tagA < self.__tagB:
            return hash((self.__tagA, self.__tagB))
        return hash((self.__tagB, self.__tagA))

    def __eq__(self, other):
        return ((self.__tagA == other.__tagA and self.__tagB == other.__tagB) or
                (self.__tagA == other.__tagB and self.__tagB == other.__tagA))
    
class BOTPhysicsCollisionResolver:
    def __init__(self, tagA, tagB):
        self.__tagA = tagA
        self.__tagB = tagB

    def _resolve(self, objectA, objectB):
        if self.__tagA == objA.getTag() and self.__tagB == objB.getTag():
            return self.onResolve(objectA, objectB)
        elif self.__tagA == objB.getTag() and self.__tagB == objA.getTag():
            return self.onResolve(objectB, objectA)
        else:
            raise Exception("Trying to resolve objs of tags ('%s', '%s') with BOTPhysicsCollisionResolver expecting ('%s', '%s')" %
                            (objectA.getTag(), objectB.getTag(), self.__tagA, self.__tagB))

    def onResolve(self, objectA, objectB):
        raise Exception("BOTPhysicsCollisionResolver %s must define 'onResolve'"%self.__class__.__name__)
