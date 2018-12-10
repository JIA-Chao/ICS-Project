"""
Author: Jia Zhao
"""

def encrypt(s):
    """
    Use ASCII to encrypt and only remains the last two digits as str; if the first is zero, add it.
    Store each word as one str in the return list.
    """
    to_return = []
    s_l = s.split()
    for each in s_l:
        temp_s = ''
        for char in each:
            temp = str(ord(char))
            if len(temp) == 2:
                temp_s += temp
            else:
                temp_s += temp[1:]
        to_return.append(temp_s)
    return to_return


def decrypt(en_l):
    """Opposite to encryption"""
    to_return = ''
    for encry in en_l:
        s = str(encry)
        for i in range(len(s)//2):
            i1 = s[2 * i]
            i2 = s[2 * i + 1]
            if i1 == '0' or i1 == '1' or i1 == '2':
                char_ord = int('1' + i1 + i2)
            else:
                char_ord = int(i1 + i2)
            to_return += chr(char_ord)
        to_return += ' '
    return to_return


# print(encrypt('HIIIIII I love you!'))
# l =['72737373737373', '73', '08111801', '21111733']
# print(type(str(l)))

