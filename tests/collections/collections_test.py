
from util.bot_collections import *
    
def run():
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
    assert llist.tail.getValue() == "1"
    
    llist.push("2")
    assert llist.length == 2
    assert llist.begin().getValue() == "2"
    assert llist.tail.getValue() == "1"
    
    llist.pushEnd("0")
    assert llist.length == 3
    assert llist.begin().getValue() == "2"
    assert llist.tail.getValue() == "0"
    
    poppedNode = llist.pop()
    assert llist.length == 2
    assert poppedNode == "2"
    assert llist.begin().getValue() == "1"
    assert llist.tail.getValue() == "0"
    
    poppedNode = llist.popEnd()
    assert llist.length == 1
    assert poppedNode == "0"
    assert llist.begin().getValue() == "1"
    assert llist.tail.getValue() == "1"
    
    poppedNode = llist.pop()
    assert llist.length == 0
    assert poppedNode == "1"
    assert llist.begin() == None
    assert llist.tail == None
    
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
