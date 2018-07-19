from util.bot_collections import DictUtil
from util.bot_math import *
from util.pattern.bot_singleton import Singleton
from util.pattern.bot_eventqueue import EventQueue

class BOTPhysicsSpace:
    def __init__(self):
        self.__rigidBodies = {}
        self.__resolvers = {}

    def addRigidBody(self, rigidBody):
        name = rigidBody.getName()
        DictUtil.tryStrictInsert(self.__rigidBodies, name, rigidBody,
                                 ("Attempting to override existing "
                                  "'BOTPhysicsRigidBody' '%s' in 'BOTPhysicsSpace'!") % name)

    def removeRigidBody(self, rigidBody):
        name = rigidBody.getName()
        removed = DictUtil.tryRemove(self.__rigidBodies, name,
                                     ("Attempting to remove non-existent "
                                      "'BOTPhysicsRigidBody' '%s' from 'BOTPhysicsSpace'!") % name)

        if removed is not rigidBody:
            raise Exception("FATAL: Unregistered 'BOTRigidBody' does not match provided "
                            "'BOTPhysicsRigidBody' despite sharing name '%s'" % name)
    def addResolver(self, resolver):
        resolverTuple = resolver.getResolverTuple()
        DictUtil.tryStrictInsert(self.__resolvers, resolverTuple, resolver,
                                 ("Attempting to override existing "
                                  "'BOTPhysicsResolver' with ResolverTuple '%s' in 'BOTPhysicsSpace'!") % resolverTuple)

    def removeResolver(self, resolver):
        resolverTuple = resolver.getResolverTuple()
        removed = DictUtil.tryRemove(self.__resolvers, resolverTuple,
                                     ("Attempting to remove non-existent "
                                      "'BOTPhysicsResolver' with ResolverTuple '%s' from 'BOTPhysicsSpace'!") % resolverTuple)

        if removed is not resolver:
            raise Exception("FATAL: Unregistered 'BOTPhysicsResolver' does not match provided "
                            "'BOTPhysicsResolver' despite sharing ResolverTuple '%s'" % resolverTuple)

    '''
        Takes a point in world space, and returns
        all RBO's whose collider overlaps the given pt.
    '''
    def pointCast(self, pt):
        result = []
        # optimizable, should cache the rbo keys, or iterate using a linked list
        for rboKey in self.__rigidBodies:
            rbo = self.__rigidBodies[rboKey]
            if rbo._collidesWithPointCast(pt):
                result.append(rbo)
        return result

    def update(self, deltaTime):
        for rboKey in self.__rigidBodies:
            self.__rigidBodies[rboKey]._update(deltaTime)

        n = len(self.__rigidBodies)
        keys = self.__rigidBodies.keys()
        for i in range(n):
            rbA = self.__rigidBodies[keys[i]]
            for j in range(i+1, n):
                rbB = self.__rigidBodies[keys[j]]
                if rbA._collidesWithCollider(rbB):
                    resolverTuple = BOTPhysicsCollisionResolverTuple(rbA.getTag(), rbB.getTag())
                    if resolverTuple in self.__resolvers:
                        self.__resolvers[resolverTuple]._resolve(rbA, rbB)

    def lateUpdate(self):
        self.pump()

Singleton.transformToSingleton(BOTPhysicsSpace)

def __BOTPhysicsSpaceQueue():
    QUEUED_METHODS = [BOTPhysicsSpace.addRigidBody, BOTPhysicsSpace.removeRigidBody, BOTPhysicsSpace.addResolver, BOTPhysicsSpace.removeResolver]
    # I really don't care how this order goes, though this may matter later
    EventQueue.enQueueify(BOTPhysicsSpace, QUEUED_METHODS, lambda eventA, eventB: 0)

__BOTPhysicsSpaceQueue()

class BOTPhysicsRigidBody:
    def __init__(self, boundObj, collider, tag):
        if not isinstance(collider, BOTPhysicsCollider):
            raise Exception("Collider provided to 'BOTPhysicsRigidBodyObject' must be of type 'BOTPhysicsCollider', got '%s'."%collider.__class__.__name__)
        if not isinstance(tag, str):
            raise Exception("Tag provided to 'BOTPhysicsRigidBodyObject' must be of type 'str', got '%s'."%tag.__class__.__name__)

        self.__transform = Transform()
        self.__boundObj = boundObj
        self.__collider = collider
        self.__tag = tag
        self.__boundObject = None
        self.__name = "BOTPhysicsRigidBody %i"%id(self)

    def getTransform(self):
        return self.__transform

    def getBoundObj(self):
        return self.__boundObj

    def setBoundObject(self, obj):
        self.__boundObject = obj

    def getBoundObject(self):
        return self.__boundObject

    def getTag(self):
        return self.__tag

    def _collidesWithCollider(self, rbo):
        return self.__collider._collidesWith(rbo.__collider)

    def _collidesWithPointCast(self, pt):
        return self.__collider._collidesWithPointCast(pt)

    def _update(self, deltaTime):
        self.__collider._applyTransform(self.__transform)

    def getName(self):
        return self.__name

class BOTPhysicsCollider(object):
    def __init__(self, vertices):
        self.__vertices = vertices # note vertices are in local space
        self._applyTransform(Transform())

    def _applyTransform(self, transform):
        self.__worldVertices = map(lambda x: transform.getMatrix() * x, self.__vertices)

        # temporarily just compute the bounding rectangle here, and call it a day
        # we can use Separating Axis Test later if we really need to
        self.__AABB = RectUtil.findAABB(self.__worldVertices)
        
    def _collidesWith(self, collider):
        return self.__AABB.colliderect(collider.__AABB)

    def _collidesWithPointCast(self, pt):
        return self.__AABB.collidepoint(pt.toIntTuple())

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

    def __hash__(self):
        if self.__tagA < self.__tagB:
            return hash((self.__tagA, self.__tagB))
        return hash((self.__tagB, self.__tagA))

    def __eq__(self, other):
        return ((self.__tagA == other.__tagA and self.__tagB == other.__tagB) or
                (self.__tagA == other.__tagB and self.__tagB == other.__tagA))
    
class BOTPhysicsCollisionResolver(object):
    def __init__(self, tagA, tagB):
        self.__tagA = tagA
        self.__tagB = tagB
        self.__resolverTuple = BOTPhysicsCollisionResolverTuple(self.__tagA, self.__tagB)

    def _resolve(self, rbA, rbB):
        if self.__tagA == rbA.getTag() and self.__tagB == rbB.getTag():
            return self.onResolve(rbA, rbB)
        elif self.__tagA == rbB.getTag() and self.__tagB == rbA.getTag():
            return self.onResolve(rbB, rbA)
        else:
            raise Exception("Trying to resolve objs of tags ('%s', '%s') with BOTPhysicsCollisionResolver expecting ('%s', '%s')" %
                            (rbA.getTag(), rbB.getTag(), self.__tagA, self.__tagB))

    def onResolve(self, rbA, rbB):
        raise Exception("BOTPhysicsCollisionResolver %s must define 'onResolve'"%self.__class__.__name__)

    def getResolverTuple(self):
        return self.__resolverTuple
