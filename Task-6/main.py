from dealer import Dealer
from keeper import PartOfSecret
import sympy.ntheory as nt
from sympy import mod_inverse


# Проверка на то, что было введено число.
def CheckInput(Message):
    while True:
        try:
            Number = int(input(Message))
            return Number
        except ValueError:
            print('Неверный ввод. Введите число!')
            continue


def RecoverSecret(Group, p):
    # Номера хранителей (точки) отделяются от долей секрета (значений полинома в точке).
    ListOfX = []
    ListOfY = []
    for Keeper in Group:
        ListOfX.append(Keeper.PairKey[0])
        ListOfY.append(Keeper.PairKey[1])
    # Интерполяционный полином Лагранжа.
    LenX = len(ListOfX)
    InterPoly = 0
    # Вычисление li(x)
    for i in range(LenX):
        Yi = ListOfY[i]
        Part = 1
        for j in range(LenX):
            if j == i:
                continue
            InverseDenom = mod_inverse(ListOfX[j] - ListOfX[i], p)
            Part *= (ListOfX[j] % p) * InverseDenom
        # Вычисление значения полинома. Сумма li(x) * yi
        InterPoly += Yi * Part
    # После вычисления суммы - mod p
    Secret = InterPoly % p
    return Secret


# Создание группы участвующей в восстановлении секрета. Ввод через пробел.
# Проводится также проверка на то, что такие участники есть.
def CreateGroup(ListOfParticipants):
    while True:
        GroupOfParticipants = []
        try:
            input_message = 'Введите номера участников для восстановления секрета через пробел: '
            NumberOfParticipants = list(map(int, input(input_message).split()))
            for i in NumberOfParticipants:
                FindParticipant = next(j for j in ListOfParticipants if j.PairKey[0] == i)
                GroupOfParticipants.append(FindParticipant)
            if len(GroupOfParticipants) == len(NumberOfParticipants):
                return GroupOfParticipants
        except StopIteration:
            print('Один из участников не был найден. Повторите ввод!')
            continue


# Основной код.
def main():
    # Ввод секрета (число).
    Dealer1 = Dealer()
    Dealer1.InputSecret()
    # Ввод количества сторон.
    while 1:
        n = CheckInput('Введите количество хранителей части секрета: ')
        if n <= 1:
            print('Количество участников должно быть строго больше 1')
        else:
            break
    # Генерация простого числа p большего секрета и количества участников.
    if n > Dealer1.Secret:
        # Возвращает первое простое число, которое идет после переданного в функцию числа.
        p = nt.nextprime(n)
    else:
        p = nt.nextprime(Dealer1.Secret)
    print('Сгенерированное простое число: ' + str(p))
    # Ввод минимального числа сторон для восстановления секрета.
    while 1:
        k = CheckInput('Минимальное количество участников для расшифровки секрета: ')
        if k > n or k <= 1:
            print('Минимальное количество участников должно быть меньше или равно общему количеству участников (от '
                  '2-ух)')
        else:
            break
    # Генерация коэффициентов полинома и их вывод на экран.
    Dealer1.GenerateCoefs(k - 1, p)
    print('Сгенерированные коэф-ты полинома: ', Dealer1.Coefs)
    # Список хранителей частей секрета.
    ListOfKeepers = []
    # Вычисление координат различных точек.
    for i in range(1, n + 1):
        Keeper = PartOfSecret(Dealer1.ShareOfThePartSecret(i, p))
        ListOfKeepers.append(Keeper)
    # Стираем случайные коэффициенты.
    Dealer1.ForgetCoefs()
    # Вывод частей ключей.
    for KeeperKey in ListOfKeepers:
        print('Часть ключа участника ' + str(KeeperKey.PairKey[0]) + ': ', KeeperKey.PairKey)
    # Группа участников, которые будут восстанавливать секрет.
    GroupOfKeepers = CreateGroup(ListOfKeepers)
    # Восстановление секрета.
    GroupSecret = RecoverSecret(GroupOfKeepers, p)
    # Проверка на то, что изначальный секрет и восстановленный совпадают.
    print('Расшифрованный секрет: ' + str(GroupSecret))
    if Dealer1.Secret == GroupSecret:
        print('Секреты совпадают!')
    else:
        print('Секреты отличаются!')
    return 0


main()
