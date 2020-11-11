from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.publicKey import PublicKey
from ellipticcurve.signature import Signature
from ellipticcurve.utils.compatibility import *

def generate_KeyPair():
    privateKey = PrivateKey()
    publicKey = privateKey.publicKey()
    return privateKey.toPem(),publicKey.toPem()

def create_Signature(message,str1):             # str1 private key
    privateKey = PrivateKey().fromPem(str1)
    signature = Ecdsa.sign(message, privateKey)
    return str(signature.toBase64())

def verify_Signature(message, sign64, str1):
    signature = Signature.fromBase64(sign64)
    publicKey = PublicKey.fromPem(str1)
    return (Ecdsa.verify(message, signature, publicKey))


# can change toPem() to toDer()-->add toBytes for this if used.



# pr1,pb1 = generate_KeyPair()
# pr2,pb2 = generate_KeyPair()
# message = "chandan bond"
# sign1 = create_Signature(message,pr1)
# sign2 = create_Signature(message, pr2)
# # print(generate_KeyPair())
# print("PVT: ", len(pr1), "PBLIC: ", pb1)
# print("PVT: ", len(pr2), "PBLIC: ", pb2)
# print(verify_Signature(message,sign1,pb1))
# print(verify_Signature(message,sign2,pb2))
