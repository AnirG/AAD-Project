from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.publicKey import PublicKey
from ellipticcurve.signature import Signature
from ellipticcurve.utils.compatibility import *

def generate_KeyPair():
    privateKey = PrivateKey()
    publicKey = privateKey.publicKey()
    return str(privateKey.toString()),str(publicKey.toString())

def create_Signature(message,str1):
    privateKey = PrivateKey().fromString(toBytes(str1))
    signature = Ecdsa.sign(message, privateKey)
    return str(signature.toBase64())

def verify_Signature(message, sign64, str1):
    signature = Signature.fromBase64(sign64)
    publicKey = PublicKey.fromString(toBytes(str1))
    return (Ecdsa.verify(message, signature, publicKey))


"""
pr1,pb1 = generate_KeyPair()
pr2,pb2 = generate_KeyPair()
message = "chandan bond"
sign1 = create_Signature(message,pr1)
sign2 = create_Signature(message, pr2)
print(generate_KeyPair())
print(sign1)
print(verify_Signature(message,sign1,pb1))
print(verify_Signature(message,sign2,pb2))
"""