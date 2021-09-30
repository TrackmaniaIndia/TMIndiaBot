from base64 import b64encode


def b64encode_string(string: str):
    strBytes = str(string).encode("ascii")
    b64Bytes = b64encode(strBytes)

    return b64Bytes.decode("ascii")
