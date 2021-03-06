'''Linked List'''
class LList:
    def __init__(self):
        self.head = LLNode(None)
        self.tail = self.head.insertNext(None)
        self.length = 0
        
    def begin(self):
        return self.head.next()
    
    def end(self):
        return self.tail
    
    def rbegin(self):
        return self.tail.prev()
    
    def rend(self):
        return self.head
    
    def isEmpty(self):
        return self.length == 0
    
    '''Adds a value to the front of the linked list'''
    def push(self, newValue):
        self.head.insertNext(newValue)
        self.length += 1
        
    '''Adds a value to the end of the linked list'''
    def pushEnd(self, newValue):
        self.tail.insertPrev(newValue)
        self.length += 1
    
    '''Removes and returns the first value from the linked list'''
    def pop(self):
        if self.length == 0:
            raise Exception("Tried to pop from empty list")
        temp = self.head.next()
        temp.delete()
        self.length -= 1
        return temp.getValue()
    
    '''Removes and returns the last value from the linked list'''
    def popEnd(self):
        if self.length == 0:
            raise Exception("Tried to pop from empty list")
        temp = self.tail.prev()
        temp.delete()
        self.length -= 1
        return temp.getValue()
    
'''Linked List Node'''
class LLNode:
    
    '''Returns new Linked List Node with no head or tail'''
    def __init__(self, value, head = None, tail = None):
        self.head = head
        self.tail = tail
        self.value = value

    def hasNext(self):
        return self.tail is not None
    
    def hasPrev(self):
        return self.head is not None
    
    def next(self):
        if self.hasNext():
            return self.tail
        else:
            raise StopIteration
    
    def prev(self):
        if self.hasPrev():
            return self.head
        else:
            raise StopIteration
    
    def getValue(self):
        return self.value
    
    def setValue(self, newValue):
        self.value = newValue
    
    '''Interts the value as a new node after this one. Returns the new node'''
    def insertNext(self, newValue):
        temp = LLNode(newValue, head = self, tail = self.tail)
        if self.hasNext():
            self.tail.head = temp
        self.tail = temp
        return temp
        
    '''Interts the value as a new node before this one. Returns the new node'''
    def insertPrev(self, newValue):
        temp = LLNode(newValue, head = self.head, tail = self)
        if self.hasPrev():
            self.head.tail = temp
        self.head = temp
        return temp
        
    '''Interts the value as a new node on the end of the list. Returns the new node.'''
    def insertEnd(self, newValue):
        if self.hasNext:
            return self.tail.insertEnd(newValue)
        else:
            return self.insertNext(newValue)
    
    '''Removes this node from the list. Returns the next node.'''
    def delete(self):
        # Setting the previous and next nodes to point to each other
        if self.hasPrev():
            self.head.tail = self.tail
        if self.hasNext():
            self.tail.head = self.head
        return self.tail

'''Common Dictionary Manipulation Methods with safety throw'''
class DictUtil:
    @staticmethod
    def tryFetch(d, key, failMessage=None):
        if key in d:
            return d[key]
        raise Exception(["Trying to fetch non-existent key %s from Dict." % key, failMessage][failMessage != None])

    @staticmethod
    def tryStrictInsert(d, key, val, failMessage=None):
        if key in d:
            raise Exception(["Trying to insert existing key %s into Dict." % key, failMessage][failMessage != None])
        d[key] = val

    @staticmethod
    def tryRemove(d, key, failMessage=None):
        if key in d:
            return d.pop(key)
        raise Exception(["Trying to remove non-existent key %s from Dict." % key, failMessage][failMessage != None])

'''Common Entity Utilities'''
class EntityUtil:
    '''Generates a guaranteed-to-be-unique name for the obj using its class name and id'''
    @staticmethod
    def genName(obj):
        return "%s-%i"%(obj.__class__.__name__, id(obj))

'''Linked-List dict to support fast look-up and iteration'''
class LLDict:
    def __init__(self):
        self.__dict = {}
        self.__linkedList = LList()

    def insert(self, key, item, failMessage=None):
        self.__linkedList.pushEnd(item)
        it = self.__linkedList.end().prev()
        try:
            if failMessage == None:
                failMessage = "Trying to add existing key '%s' to LLDict" % key
            DictUtil.tryStrictInsert(self.__dict, key, it, failMessage)
        except Exception as e:
            # rollback and re-raise
            it.delete()
            raise e

    def remove(self, key, failMessage=None):
        if failMessage == None:
            failMessage = "Trying to remove non-existent key '%s' from LLDict" % key
        it = DictUtil.tryFetch(self.__dict, key, failMessage)
        val = it.getValue()

        del self.__dict[key] # guaranteed to exist at this point
        it.delete()

        return val

    def get(self, key, failMessage=None):
        if failMessage == None:
            failMessage = "Trying to fetch non-existent key '%s' from LLDict" % key
        it = DictUtil.tryFetch(self.__dict, key, failMessage)
        return it.getValue()

    def begin(self):
        return self.__linkedList.begin()

    def end(self):
        return self.__linkedList.end()
