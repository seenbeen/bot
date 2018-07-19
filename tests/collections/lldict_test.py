from util.bot_collections import LLDict

def run():
    lldict = LLDict()

    lldict.insert("foo", 1)
    try:
        lldict.insert("foo", 2)
        assert False, "LLDict double key-insertion failed."
    except:
        pass
    lldict.insert("bar", 2)

    assert lldict.get("foo") == 1
    assert lldict.get("bar") == 2

    it = lldict.begin()
    assert it.getValue() == 1
    it = it.next()
    assert it.getValue() == 2
    it = it.next()
    assert it == lldict.end()

    lldict.remove("foo")
    it = lldict.begin()
    assert it.getValue() == 2
    assert lldict.get("bar") == 2

    try:
        lldict.get("foo")
        assert False, "LLDict non-existent removal somehow succeeded."
    except:
        pass
