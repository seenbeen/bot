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
    assert node12.prev().getValue() == "234"
    assert node6.next().getValue() == "123"
    
    delNode = node6.delete()
    assert delNode.value == node12.value
    assert rootNode.hasNext() == True
    assert rootNode.next().value == node12.value
    assert node12.hasPrev() == True
    
    assert rootNode.next().value == node12.value
    assert rootNode.value == node12.prev().value
    
    node9 = node12.insertPrev("345")
    temp = node9.delete()
    assert node12.prev().value == rootNode.value
    assert temp.value == node12.value
    
    ## Testing list
    
    llist = LList()
    assert llist.begin().value == None
    assert llist.end().value == None
    assert llist.length == 0
    assert llist.isEmpty() == True
    try:
        llist.pop()
        assert False
    except Exception:
        assert True
        
    try:
        llist.popEnd()
        assert False
    except Exception:
        assert True
    
    llist.push("1")
    assert llist.length == 1
    assert llist.begin().value == "1"
    assert llist.end().prev().value == "1"
    
    llist.push("2")
    assert llist.length == 2
    assert llist.begin().value == "2"
    assert llist.end().prev().value == "1"
    
    llist.pushEnd("0")
    assert llist.length == 3
    assert llist.begin().value == "2"
    assert llist.end().prev().value == "0"
    
    poppedNode = llist.pop()
    assert llist.length == 2
    assert poppedNode == "2"
    assert llist.begin().value == "1"
    assert llist.end().prev().value == "0"
    
    poppedNode = llist.popEnd()
    assert llist.length == 1
    assert poppedNode == "0"
    assert llist.begin().value == "1"
    assert llist.end().prev().value == "1"
    
    poppedNode = llist.pop()
    assert llist.length == 0
    assert poppedNode == "1"
    assert llist.begin().value == None
    assert llist.end().value == None
    
    testList = LList()
    testList.push(3)
    testList.push(2)
    testList.push(1)
    testList.push(0)
    
    iterator = testList.begin()
    c = 0
    while iterator != testList.end():
        assert iterator.value == c
        c += 1
        iterator = iterator.next()
