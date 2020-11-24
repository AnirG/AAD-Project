from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.publicKey import PublicKey
from ellipticcurve.signature import Signature
from ellipticcurve.utils.compatibility import *
from ellipticcurve.point import Point
from ellipticcurve.curve import curvesByOid, supportedCurves, secp256k1

def generate_KeyPair():
    privateKey = PrivateKey()
    publicKey = privateKey.publicKey()

    return [str(privateKey.secret),str(publicKey.point.x) + '.' + str(publicKey.point.y) + '.' + str(publicKey.point.z)]

def create_Signature(message,privateKey_input):
    privateKey = PrivateKey(secret = int(privateKey_input))
    signature = Ecdsa.sign(message, privateKey)
    return str(signature.toBase64())

def verify_Signature(message, sign64, publicKey_input):
    signature = Signature.fromBase64(sign64)
    a = publicKey_input.split(".")
    pt = Point(int(a[0]), int(a[1]), int(a[2]))
    publicKey = PublicKey(point = pt, curve = secp256k1)
    return (Ecdsa.verify(message, signature, publicKey))


# p1 = generate_KeyPair()
# p2 = generate_KeyPair()
# print(len(p1[0]))
# print(len(p1[1]))
# message = "chandan bond"

# a = input()
# b = input()

# sign = create_Signature(message, a)
# print(sign)

# print(verify_Signature(message, sign, b))
