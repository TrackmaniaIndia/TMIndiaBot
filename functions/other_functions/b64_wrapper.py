from base64 import b64encode

def b64encodeStr(string: str):
    strBytes = str(string).encode('ascii')
    b64Bytes = b64encode(strBytes)

    return b64Bytes.decode('ascii')