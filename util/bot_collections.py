class LLNode:
    
    def __init__(self, value, head = None, tail = None):
        self.head = head
        self.tail = tail
        self.value = value

    def hasNext(self):
        return not self.tail is None
    
    def hasPrev(self):
        return not self.head is None
    
    def getNext(self):
        return self.tail
    
    def getPrev(self):
        return self.head
    
    def getValue(self):
        return self.value
    
    def setValue(self, newValue):
        self.value = newValue
    
    def insert(self, newValue):
        temp = LLNode(newValue, self, self.tail)
        if self.hasNext():
            self.tail.tail = tempNode
        self.tail = temp
            
    def deleteNext(self):
        if self.hasNext():
            temp = self.tail.pop()
            self.tail = temp.tail
            return temp
        return None
    
    def pop(self):
        if self.hasPrev():
            self.head.tail = self.tail
        if self.hasNext():
            self.tail.head = self.head
        self.head = self.tail = None
        return self
        