from SHA256 import SHA256


# class Block(db.Model){

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     payer = Column(String)
#     recipient = Column(String)
#     amount = Column(Float)
#     prevHash = Column(String)

# }

class Block():
    def __init__(self,id, payer, recipient, amount, prevHash):
        self.id = id
        self.payer = payer
        self.recipient = recipient
        self.amount = amount
        self.prevHash = prevHash

def printBlockContents(Block):
    print(Block.id, Block.payer, Block.recipient, Block.amount, Block.prevHash)