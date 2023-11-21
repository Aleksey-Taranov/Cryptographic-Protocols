import random
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
    a = random.randint(2, p - 2)
    a = pow(a, 2 ** n, p)
    f = open('shared_keys.txt', 'w')
    f.write(str(p) + ' ' + str(q) + ' ' + str(a))
    f.close()
    print("p, q, a =", p, q, a)
    return 0


def create_keys():
    f = open('shared_keys.txt', 'r')
    p, q, a = map(int, f.read().split())
    f.close()
    if q == 2 or q == 3:
        s = 2
    else:
        s = random.randint(2, q - 1)
    v = pow(a, s, p)
    _, v, _ = extended_euclid(v, p)
    if v < 0:
        v += p
    f = open('close_keys.txt', 'w')
    f.write(str(s))
    f.close()
    f = open('open_keys.txt', 'w')
    f.write(str(v))
    f.close()
    print("s, v =", s, v)
    return 0


def first_step():
    f = open('shared_keys.txt', 'r')
    p, q, a = map(int, f.read().split())
    f.close()
    r = random.randint(2, q - 1)
    f = open('r.txt', 'w')
    f.write(str(r))
    f.close()
    x = pow(a, r, p)
    f = open('x.txt', 'w')
    f.write(str(x))
    f.close()
    print("r, x =", r, x)
    return 0


def second_step():
    print("Выберете t > 1\nt = ", end='')
    while True:
        t = int(input())
        if t > 1:
            break
        print("t введено неверно")
    e = random.randint(0, pow(2, t - 1))
    f = open('e.txt', 'w')
    f.write(str(e))
    f.close()
    print("e =", e)
    return 0


def third_step():
    f = open('close_keys.txt', 'r')
    s = int(f.read())
    f.close()
    f = open('shared_keys.txt', 'r')
    _, q, _ = map(int, f.read().split())
    f.close()
    f = open('r.txt', 'r')
    r = int(f.read())
    f.close()
    f = open('e.txt', 'r')
    e = int(f.read())
    f.close()
    y = (r + s * e) % q
    f = open('y.txt', 'w')
    f.write(str(y))
    f.close()
    print("y =", y)
    return 0


def last_step():
    f = open('x.txt', 'r')
    x = int(f.read())
    f.close()
    f = open('shared_keys.txt', 'r')
    p, _, a = map(int, f.read().split())
    f.close()
    f = open('open_keys.txt', 'r')
    v = int(f.read())
    f.close()
    f = open('e.txt', 'r')
    e = int(f.read())
    f.close()
    f = open('y.txt', 'r')
    y = int(f.read())
    f.close()
    x_last = (pow(a, y, p) * pow(v, e, p)) % p
    print("x_last =", x_last)
    return x == x_last


def main():
    print("Сгенерировать общие параметры заново? [Y - да/N - нет]")
    while True:
        f = input()
        if f == 'Y':
            create_p()
            break
        elif f == 'N':
            break
        else:
            print("Некорректный ввод")
    print("Сгенирировать ключи для Пегги? [Y - да/N - нет]")
    while True:
        f = input()
        if f == 'Y':
            create_keys()
            print("Ключи сгенерированы")
            break
        elif f == 'N':
            return 0
        else:
            print("Некорректный ввод")
    print("Вычислить и отправить х Виктору? [Y - да/N - нет]")
    while True:
        f = input()
        if f == 'Y':
            first_step()
            print("Пегги вычислила x и отправила Виктору")
            break
        elif f == 'N':
            return 0
        else:
            print("Некорректный ввод")
    print("Отправить Пегги случайное е? [Y - да/N - нет]")
    while True:
        f = input()
        if f == 'Y':
            second_step()
            print("Виктор отправил Пегги число e")
            break
        elif f == 'N':
            return 0
        else:
            print("Некорректный ввод")
    print("Вычислить и отправить у Виктору? [Y - да/N - нет]")
    while True:
        f = input()
        if f == 'Y':
            third_step()
            print("Пегги вычислила у и отправила Виктору")
            break
        elif f == 'N':
            return 0
        else:
            print("Некорректный ввод")
    print("Проверить подлинность? [Y - да/N - нет]")
    while True:
        f = input()
        if f == 'Y':
            if last_step():
                print("Подлинность подтверждена")
            else:
                print("Подлинность не подтверждена")
            break
        elif f == 'N':
            return 0
        else:
            print("Некорректный ввод")
    return 0


main()
