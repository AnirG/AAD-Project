from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey

def generate_KeyPair():
    privateKey = PrivateKey()
    publicKey = privateKey.publicKey()
    return privateKey,publicKey

def create_Signature(message,privateKey):
    signature = Ecdsa.sign(message, privateKey)
    return signature

def verify_Signature(message, signature, publicKey):
    return (Ecdsa.verify(message, signature, publicKey))


# redirect to this when user opts in for crypto-part.

"""
pr1,pb1 = generate_KeyPair()
print(pr1,pb1)
pr2,pb2 = generate_KeyPair()
message = "chandan bond"
sign1 = create_Signature(message,pr1)
sign2 = create_Signature(message, pr2)
print(sign1)
print(verify_Signature(message,sign1,pb1))
print(verify_Signature(message,sign2,pb2))
"""