__messageHUB__ = []

def addMessage(sMessage):
    __messageHUB__.append(sMessage)

def getMessages():
    p = __messageHUB__.copy()
    __messageHUB__.clear()
    return p