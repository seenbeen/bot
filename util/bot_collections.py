"""Iterator for a Linked List"""
class LLIterator:
    
    """Creates a new LLIterator using an existing linked list node as the root"""
    def __init__(self, node):
        self.head = node
        self.node = node
    
    def reset(self):
        self.node = self.head
    
    """Returns false if this is the last value"""
    def hasNext(self):
        return self.node is not None and self.node.hasNext()
    
    """Returns the next value or None if there are no more values"""
    def next(self):
        if self.node is not None and self.node.hasNext():
            self.node = self.node.getNext()
            return self.node.getValue()
        return None
    
    """Removes the current value"""
    def delete(self):
        if self.node is not None:
            self.node.delete()
            if self.node.hasPrev() == False:
                self.head = self.node.tail
                
    """Inserts a new LLNode after the current one"""
    def insert(self, value):
        if self.head is None:
            self.head = self.node = LLNode(value)
        elif self.node is not None:
            self.node.insertNext(value)

    """Returns the value of the current node"""
    def getValue(self):
        return self.node.getValue()
    
    """Returns the current node"""
    def getNode(self):
        return self.node

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
    
    """Interts the value as a new node after this one."""
    def insertNext(self, newValue):
        temp = LLNode(newValue, head = self, tail = self.tail)
        if self.hasNext():
            self.tail.head = temp
        self.tail = temp
        return temp
        
    """Interts the value as a new node before this one."""
    def insertPrev(self, newValue):
        temp = LLNode(newValue, head = self.head, tail = self)
        if self.hasPrev():
            self.head.tail = temp
        self.head = temp
        return temp
        
    """Interts the value as a new node on the end of the list"""
    def insertEnd(self, newValue):
        if self.hasNext:
            return self.tail.insertEnd(newValue)
        else:
            return self.insertNext(newValue)
    
    """Removes the next node in the list and returns that node"""
    def deleteNext(self):
        if self.hasNext():
            temp = self.tail
            self.tail = self.tail.delete()
            return temp
        return None
    
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
        print("pass 1")
        
        node12 = rootNode.insertNext("123")
        assert rootNode.hasNext() == True
        assert node12.hasPrev() == True
        print("pass 2")
        
        node6 = rootNode.insertNext("234")
        assert node12.getPrev().getValue() == "234"
        assert node6.getNext().getValue() == "123"
        print("pass 3")
        
        delNode = node6.delete()
        assert delNode.getValue() == node12.getValue()
        assert rootNode.hasNext() == True
        assert node12.hasPrev() == True
        print ("pass 4")
        
        assert rootNode.getNext().value == node12.value
        assert rootNode.value == node12.getPrev().value
        print("pass 5")
        
        node9 = node12.insertPrev("345")
        temp = node9.deleteNext()
        assert node9.hasNext() == False
        assert temp.value == node12.value
        print("pass 6")
        
        ## Testing iterator
        
        it = LLIterator(LLNode("root"))
        
        it.delete()
        it.insert("1")
        it.insert("3")
        it.insert("2")
        assert it.getValue() == "1"
        assert it.hasNext()
        assert it.next() == "2"
        it.delete()
        assert it.next() == "3"
        it.reset()
        assert it.head is not None
        assert it.next() == "3"
        assert it.next() == None        
        return True
    
    except MemoryError:
        return "wow how did this happen"
    
print testLinkedLists()
    