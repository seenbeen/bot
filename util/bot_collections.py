"""Linked List"""
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
    
    """Adds a value to the front of the linked list"""
    def push(self, newValue):
        self.head.insertNext(newValue)
        self.length += 1
        
    """Adds a value to the end of the linked list"""
    def pushEnd(self, newValue):
        self.tail.insertPrev(newValue)
        self.length += 1
    
    """Removes and returns the first value from the linked list"""
    def pop(self):
        if self.length == 0:
            raise Exception('Tried to pop from empty list')
        temp = self.head.next()
        temp.delete()
        self.length -= 1
        return temp.getValue()
    
    """Removes and returns the last value from the linked list"""
    def popEnd(self):
        if self.length == 0:
            raise Exception('Tried to pop from empty list')
        temp = self.tail.prev()
        temp.delete()
        self.length -= 1
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