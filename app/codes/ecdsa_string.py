from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.publicKey import PublicKey
from ellipticcurve.signature import Signature
from ellipticcurve.utils.compatibility import *

def generate_KeyPair():
    privateKey = PrivateKey()
    publicKey = privateKey.publicKey()
    a = str(privateKey.toPem())
    b = str(publicKey.toPem())
    a = a.replace('-----BEGIN EC PRIVATE KEY-----\n','')
    a = a.replace('\n-----END EC PRIVATE KEY-----\n','')
    b = b.replace('-----BEGIN PUBLIC KEY-----\n','')
    b = b.replace('\n-----END PUBLIC KEY-----\n','')
    return a,b

def create_Signature(message,privateKey_input):
    privateKey_input = '-----BEGIN EC PRIVATE KEY-----\n' + privateKey_input + '\n-----END EC PRIVATE KEY-----\n'
    privateKey = PrivateKey().fromPem(privateKey_input)
    signature = Ecdsa.sign(message, privateKey)
    return str(signature.toBase64())

def verify_Signature(message, signature_input, publicKey_input):
    publicKey_input = '-----BEGIN PUBLIC KEY-----\n' + publicKey_input + '\n-----END PUBLIC KEY-----\n'
    signature = Signature.fromBase64(signature_input)
    publicKey = PublicKey.fromPem(publicKey_input)
    return (Ecdsa.verify(message, signature, publicKey))


pr1,pb1 = generate_KeyPair()
pr2,pb2 = generate_KeyPair()
message = "chandan bond"
sign1 = create_Signature(message,pr1)
sign2 = create_Signature(message, pr2)
print(pr1)
print(pb1)
#print(sign1)
print(verify_Signature(message,sign1,pb1))
print(verify_Signature(message,sign2,pb2))
