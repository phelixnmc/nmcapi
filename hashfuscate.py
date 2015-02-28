import hashlib
import base64
import itertools
import traceback

hash_func = hashlib.sha256
digestSize = len(hash_func("").digest())

class HashfuscateDecodeError(Exception):
    pass

def b64_enc(s):
    return base64.b64encode(s, ["-", "_"])

def b64_dec(s):
    return base64.b64decode(s, ["-", "_"])

def ixor(s, x):
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s, itertools.cycle(x)))

def encode(v):
    h = hash_func(v).digest()
    return b64_enc(h) + "+" + b64_enc(ixor(v, h))

def decode(s, returnHash=False):
    try:
        h64, v64 = s.split("+")
        h = b64_dec(h64)
        if len(h) != digestSize:
            raise Exception("Wrong digest size: " + str(len(h)))
        vx = b64_dec(v64)    
        v = ixor(vx, h)
    except Exception as e:
        raise HashfuscateDecodeError(traceback.format_exc())
    if hash_func(v).digest() != h:
        raise HashfuscateDecodeError("Hash mismatch.")
    if returnHash:
        return v, h
    return v

if __name__ == "__main__":
    x = encode("It was a bright cold day in April...")
    print "obfuscated:", x
    try:
        x = "b" + x[1:]
        print "deobfuscated:", decode(x)[0]
    except HashfuscateDecodeError as e:
        print type(e), str(e)
        raise
