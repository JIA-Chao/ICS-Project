"""
Author: Jia Zhao
"""

import RSA_Prime
import en_de


def RSA_encrypt(text, pub):
    """RSA Encryption: m^e = c (mod n)"""
    RSA_encry = []
    for each in text:
        # print('EACH:', each)
        RSA_encry.append(RSA_Prime.quick_pow_mod(each, pub[1], pub[0]))
    return RSA_encry


def RSA_decrypt(RSA_en, pri):
    """RSA Decryption: c^d = m (mod n)"""
    RSA_decry = []
    for each in RSA_en:
        RSA_decry.append(RSA_Prime.quick_pow_mod(each, pri[1], pri[0]))
    return RSA_decry


def RSA_key():
    key = {}
    prime_pair = RSA_Prime.prime_pair()
    p = prime_pair[0]
    q = prime_pair[1]
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537   # by default
    d = RSA_Prime.mod_inverse(e, phi)
    # print("p = ", p, "q = ", q)
    # print("n = ", n)
    # print("e = ", e, "d = ", d)
    pub = [n, e]
    pri = [n, d]
    key['pub'] = pub
    key['pri'] = pri
    # print('key pair:', key)
    return key


# if __name__ == '__main__':
#     key = RSA_key()
#     # print('key length:', len(str(key['pub'][0])))
#     text = 'HIIIIII I love you!'
#     print('Plain Text:', text)
#     en_text = en_de.encrypt(text)
#     print('en_text:', en_text)
#     RSA_en = RSA_encrypt(en_text, key['pub'])
#     RSA_de = RSA_decrypt(RSA_en, key['pri'])
#     print('RSA_en:', RSA_en)
#     print('RSA_de:', RSA_de)
#     de_text = en_de.decrypt(RSA_de)
#     print('SUCCESS!!!', de_text)
#
#     print('TEST:')
#     test = RSA_decrypt([12764483985865285200809457049972], key['pri'])
#     print(test)
