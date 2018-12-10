"""
Author: Jia Zhao
"""

# -*- coding: UTF-8 -*-
import math
import random


def egcd(a, b):
    """Extended Euclidean algorithm; get int x and int y such that gcd(a，b) = ax + by."""
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x


def mod_inverse(b, n):
    """Modulo Multiplicative Inverse; find a "c" such that (bc - 1) | n, or say n % bc = 1."""
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n
    else:
        raise Exception('Modular inverse does not exist!')


def quick_pow_mod(a, b, c):
    """
    Quick power mod; convert b into binary, traverse its binary; to get the modulo
    Time complexity: O(logN)
    """
    cond1, cond2 = False, False  # set condition for text en/de; and if it starts with '0'.
    if type(a) is str:
        cond1 = True
        if a[0] == '0':
            cond2 = True
    a = int(a)
    # print('a:', a, 'c:', c)
    a = a % c
    result = 1
    while b != 0:
        if b & 1:
            result = (result * a) % c
        b >>= 1
        a = (a % c) * (a % c)
    # print('r:', result)
    if cond1 and not cond2:
        return str(result)
    if cond2:
        result = '0' + str(result)
        # print('result with 0:', result)
        return result
    return result


def miller_rabin(a, n):
    """Miller Rabin Algorithm; test if "n" is a prime."""
    if n == 1:
        return False
    if n == 2:
        return True
    k = n - 1
    q = int(math.floor(math.log(k, 2)))
    m = 0
    while q > 0:
        m = k / 2 ** q
        if k % 2 ** q == 0 and m % 2 == 1:
            break
        q = q - 1
    if quick_pow_mod(a, k, n) != 1:
        return False
    m = int(m)
    b1 = quick_pow_mod(a, m, n)
    for i in range(q):
        if b1 == n - 1 or b1 == 1:
            return True
        b2 = b1 ** 2 % n
        b1 = b2
    if b1 == 1:
        return True
    return False


def prime_test_mr(n, k=8):
    """Generally, test Miller Rabin 8 times."""
    for i in range(k):
        a = random.randint(1, n - 1)
        if not miller_rabin(a, n):
            return False
    return True


def prime_each(num, prime_l):
    """Test if num have no common factors with each prime in prime_list."""
    for prime in prime_l:
        r = num % prime  # r is remainder
        if r == 0:
            return False
    return True


def prime_l(start, end):
    """Return a prime list from start to end."""
    to_return = []
    for i in range(start, end+1):
        if is_prime(i):
            to_return.append(i)
    return to_return


def is_prime(num):
    """Return if num if a prime."""
    sqrt = int(math.sqrt(num))
    for i in range(2, sqrt + 1):
        if num % i == 0:
            return False
    return True


def prime_pair(count=2):
    """Generate a prime pair as pub and pri keys for RSA."""
    l = prime_l(2, 100000)
    prime_pair = []
    for i in range(count):
        num = random.randint(pow(10, 15), pow(10, 16))
        if num % 2 == 0:
            num += 1
        cond = True
        while cond:
            if prime_each(num, l) and prime_test_mr(num):
                if num not in prime_pair:
                    prime_pair.append(num)
                    cond = False
            num += 2
    return prime_pair
