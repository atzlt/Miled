from math import sqrt, gcd

from primality import primality as prime


def prime_factors(n: int, option: str = "multi"):
    if type(n) != int or n <= 0:
        raise ValueError("Cannot factorize n = " + str(n))
    i = 0
    if option == "set":
        s = []
        while (p := prime.nthprime(i)) <= sqrt(n):
            if n % p == 0:
                s.append(p)
            i += 1
        return s
    if option == "multi":
        s = []
        while n > 1:
            while n % (p := prime.nthprime(i)) == 0:
                n /= p
                s.append(p)
            i += 1
        return s
    if option == "exp":
        s: list[tuple[int, int]] = []
        while n > 1:
            p = prime.nthprime(i)
            r = 0
            while n % p == 0:
                n /= p
                r += 1
            if r > 0:
                s.append((p, r))
            i += 1
        return s


def divisors(n: int):
    s = []
    for i in range(1, n + 1):
        if n % i == 0:
            s.append(i)
    return s


def divisor_tau(n: int):
    s = 0
    for i in range(1, n + 1):
        if n % i == 0:
            s += 1
    return s


def divisor_sigma(n: int):
    s = 0
    for i in range(1, n + 1):
        if n % i == 0:
            s += i
    return s


def euler_phi(n: int):
    s = 0
    for i in range(2, n):
        if gcd(i, n) == 1:
            s += 1
    return s


def coprime_numbers(n: int):
    s = []
    for i in range(2, n):
        if gcd(i, n) == 1:
            s.append(i)
    return s
