"""Linked List"""
class LList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
        
    def begin(self):
        return self.head
    
    def end(self):
        return None
    
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
