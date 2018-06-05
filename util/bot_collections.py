"""
Iterator for a Linked List

Single use iterator for linked list.

"""
class LList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
        
    def begin(self):
        return self.head
    
    def end(self):
        return self.tail
    
    def isEmpty(self):
        return self.length == 0
    
    """Adds a value to the front of the linked list"""
    def push(self, newValue):
        if self.head == None:
            self.head = self.tail = LLNode(newValue)
        else:
            self.head = self.head.insertPrev(newValue)
        self.length += 1
        
    """Adds a value to the end of the linked list"""
    def pushEnd(self, newValue):
        if self.head == None:
            self.head = self.tail = LLNode(newValue)
        else:
            self.tail = self.tail.insertNext(newValue)
        self.length += 1
    
    """Removes and returns the first value from the linked list"""
    def pop(self):
        if self.length == 0:
            return None
        temp = self.head
        self.head = self.head.delete()
        if self.length > 0:
            self.length -= 1
            if self.length == 0:
                self.tail = None
        return temp.getValue()
    
    """Removes and returns the last value from the linked list"""
    def popEnd(self):
        if self.length == 0:
            return None
        temp = self.tail
        self.tail = self.tail.head
        temp.delete()
        if self.length > 0:
            self.length -= 1
            if self.length == 0:
                self.head = None
        return temp.getValue()
    
"""Linked List Node"""
class LLNode:
    
    """Returns new Linked List Node with no head or tail"""
    def __init__(self, value, head = None, tail = None):
        self.head = head
        self.tail = tail
        self.value = value

    def hasNext(self):
        return self.tail is not None
    
    def hasPrev(self):
        return self.head is not None
    
    def getNext(self):
        return self.tail
    
    def getPrev(self):
        return self.head
    
    def getValue(self):
        return self.value
    
    def setValue(self, newValue):
        self.value = newValue
    
    """Interts the value as a new node after this one. Returns the new node"""
    def insertNext(self, newValue):
        temp = LLNode(newValue, head = self, tail = self.tail)
        if self.hasNext():
            self.tail.head = temp
        self.tail = temp
        return temp
        
    """Interts the value as a new node before this one. Returns the new node"""
    def insertPrev(self, newValue):
        temp = LLNode(newValue, head = self.head, tail = self)
        if self.hasPrev():
            self.head.tail = temp
        self.head = temp
        return temp
        
    """Interts the value as a new node on the end of the list. Returns the new node."""
    def insertEnd(self, newValue):
        if self.hasNext:
            return self.tail.insertEnd(newValue)
        else:
            return self.insertNext(newValue)
    
    """Removes this node from the list. Returns the next node."""
    def delete(self):
        # Setting the previous and next nodes to point to each other
        if self.hasPrev():
            self.head.tail = self.tail
        if self.hasNext():
            self.tail.head = self.head
        return self.tail
    
    
# You can run this in a run() if you need it for the tests 
def testLinkedLists():
    try:
        ## Testing node
        
        rootNode = LLNode("root")
        assert rootNode.hasNext() == False
        assert rootNode.hasPrev() == False
        assert rootNode.getValue() == "root"
        
        node12 = rootNode.insertNext("123")
        assert rootNode.hasNext() == True
        assert node12.hasPrev() == True
        
        node6 = rootNode.insertNext("234")
        assert node12.getPrev().getValue() == "234"
        assert node6.getNext().getValue() == "123"
        
        delNode = node6.delete()
        assert delNode.getValue() == node12.getValue()
        assert rootNode.hasNext() == True
        assert rootNode.getNext().getValue() == node12.getValue()
        assert node12.hasPrev() == True
        
        assert rootNode.getNext().value == node12.value
        assert rootNode.value == node12.getPrev().value
        
        node9 = node12.insertPrev("345")
        temp = node9.delete()
        assert node12.getPrev().getValue() == rootNode.getValue()
        assert temp.value == node12.value
        
        ## Testing list
        
        llist = LList()
        assert llist.begin() == None
        assert llist.end() == None
        assert llist.length == 0
        assert llist.isEmpty() == True
        
        assert llist.pop() == None
        assert llist.popEnd() == None
        
        llist.push("1")
        assert llist.length == 1
        assert llist.begin().getValue() == "1"
        assert llist.end().getValue() == "1"
        
        llist.push("2")
        assert llist.length == 2
        assert llist.begin().getValue() == "2"
        assert llist.end().getValue() == "1"
        
        llist.pushEnd("0")
        assert llist.length == 3
        assert llist.begin().getValue() == "2"
        assert llist.end().getValue() == "0"
        
        poppedNode = llist.pop()
        assert llist.length == 2
        assert poppedNode == "2"
        assert llist.begin().getValue() == "1"
        assert llist.end().getValue() == "0"
        
        poppedNode = llist.popEnd()
        assert llist.length == 1
        assert poppedNode == "0"
        assert llist.begin().getValue() == "1"
        assert llist.end().getValue() == "1"
        
        poppedNode = llist.pop()
        assert llist.length == 0
        assert poppedNode == "1"
        assert llist.begin() == None
        assert llist.end() == None
        
        testList = LList()
        testList.push(3)
        testList.push(2)
        testList.push(1)
        testList.push(0)
        
        iterator = testList.begin()
        c = 0
        while iterator != None:
            assert iterator.getValue() == c
            c += 1
            iterator = iterator.getNext()
        
        return "What horrific chain of events led to this outcome"
    except MemoryError:
        return "Wow how did this happen"
    
#print testLinkedLists()
    