import random
import hashlib
from sympy import isprime


def extended_euclid(x1, x2):
    o_r, r = x1, x2
    o_s, s = 1, 0
    o_t, t = 0, 1
    while r != 0:
        q = o_r // r
        o_r, r = r, o_r - q * r
        o_s, s = s, o_s - q * s
        o_t, t = t, o_t - q * t
    return o_r, o_s, o_t


def fast_exponentiation(base, exponent, mod):
    result = 1
    base = base % mod
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        exponent = exponent // 2
        base = (base * base) % mod
    return result


def create_p():
    print("Введите n - длина простого числа q\nn = ", end='')
    exp = int(input())
    q = random.randint(pow(2, exp - 1), pow(2, exp))
    while not isprime(q):
        q = random.randint(pow(2, exp - 1), pow(2, exp))
    n = 2
    while not isprime(q * (2 ** n) + 1):
        n += 1
    p = q * (2 ** n) + 1
    f = open('p_q.txt', 'w')
    f.write(str(p) + ' ' + str(q))
    f.close()
    print("p =", p)
    print("q =", q)
    return 0


def create_keys():
    f = open('p_q.txt', 'r')
    p, q = map(int, f.read().split())
    f.close()
    while True:
        h = random.randint(2, p - 2)
        g = fast_exponentiation(h, (p - 1) // q, p)
        if g > 1:
            break
    x = random.randint(2, q - 1)
    y = fast_exponentiation(g, x, p)
    f = open('close_keys.txt', 'w')
    f.write(str(x))
    f.close()
    f = open('open_keys.txt', 'w')
    f.write(str(p) + ' ' + str(q) + ' ' + str(g) + ' ' + str(y))
    f.close()
    print("g =", p)
    print("y =", p)
    return 0


def first_step():
    f = open('open_keys.txt', 'r')
    _, q, _, _ = map(int, f.read().split())
    f.close()
    k = random.randint(2, q - 1)
    f = open('k.txt', 'w')
    f.write(str(k))
    f.close()
    print("k =", k)
    return 0


def second_step():
    f = open('k.txt', 'r')
    k = int(f.read())
    f.close()
    f = open('open_keys.txt', 'r')
    p, q, g, _ = map(int, f.read().split())
    f.close()
    f = open('close_keys.txt', 'r')
    x = int(f.read())
    f.close()
    r = fast_exponentiation(g, k, p) % q
    _, rev_k, _ = extended_euclid(k, q)
    f = open('message.txt', 'r', encoding='utf-8')
    m = f.read()
    f.close()
    s = (rev_k * (int(hashlib.sha1(bytes(m, encoding='utf-8')).hexdigest(), 16) + x * r)) % q
    f = open('sign.txt', 'w')
    f.write(str(r) + ' ' + str(s))
    f.close()
    print("r =", r)
    print("s =", s)
    return 0


def third_step():
    f = open('open_keys.txt', 'r')
    p, q, g, y = map(int, f.read().split())
    f.close()
    f = open('sign.txt', 'r')
    r, s = map(int, f.read().split())
    print("r (из файла) =", r)
    _, w, _ = extended_euclid(s, q)
    f = open('message.txt', 'r', encoding='utf-8')
    m = f.read()
    f.close()
    u1 = (int(hashlib.sha1(bytes(m, encoding='utf-8')).hexdigest(), 16) * w) % q
    u2 = (r * w) % q
    v = (fast_exponentiation(g, u1, p) * fast_exponentiation(y, u2, p) % p) % q
    print("w =", w)
    print("u1 =", u1)
    print("u2 =", u2)
    print("v =", v)
    return v == r


def protocol_gen():
    print("Сгенерировать p и q заново? [Y - да/N - нет]")
    while True:
        f = input()
        if f == 'Y':
            create_p()
            break
        elif f == 'N':
            break
        else:
            print("Некорректный ввод")
    print("Сгенерировать новые ключи? [Y - да/N - нет]")
    while True:
        f = input()
        if f == 'Y':
            create_keys()
            print("Ключи сгенерированы, хотите подписать сообщение? [Y - да/N - нет]")
            break
        elif f == 'N':
            print("Хотите подписать сообщение? [Y - да/N - нет]")
            break
        else:
            print("Некорректный ввод")
    while True:
        f = input()
        if f == 'Y':
            first_step()
            break
        elif f == 'N':
            return 0
        else:
            print("Некорректный ввод")
    second_step()
    print("Сообщение подписано")


def protocol_check():
    print("Проверка подписи для файла message.txt")
    if third_step():
        print("Подпись корректна")
    else:
        print("Подпись некорректна")


def main():
    print("Подписать сообщение или проверить подпись? [1 - Подписать/2 - Проверить]")
    while True:
        f = input()
        if f == '1':
            protocol_gen()
            return 0
        elif f == '2':
            protocol_check()
            return 0
        else:
            print("Некорректный ввод")


main()
