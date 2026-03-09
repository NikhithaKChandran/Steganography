def KSA(key):

    key_length = len(key)

    S = list(range(256))

    j = 0

    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]

    return S


def PRGA(S, data_len):

    i = 0
    j = 0

    keystream = []

    for _ in range(data_len):

        i = (i + 1) % 256
        j = (j + S[i]) % 256

        S[i], S[j] = S[j], S[i]

        K = S[(S[i] + S[j]) % 256]

        keystream.append(K)

    return keystream


def prepare_key(key):
    return [ord(c) for c in key]


def encrypt(data, key):

    key = prepare_key(key)

    S = KSA(key)

    keystream = PRGA(S, len(data))

    cipher = bytearray()

    for i in range(len(data)):
        cipher.append(data[i] ^ keystream[i])

    return bytes(cipher)


def decrypt(data, key):

    # RC4 decryption is identical to encryption
    return encrypt(data, key)