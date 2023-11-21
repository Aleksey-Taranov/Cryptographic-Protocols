# Здесь формируются секрет и раздаются его части участникам.
import random


class Dealer:

    def __init__(self):
        self.Secret = 0
        self.Coefs = []

    # Ввод секрета с проверкой на то, что введено число.
    def InputSecret(self):
        while True:
            try:
                self.Secret = int(input('Введите секрет: '))
                break
            except ValueError:
                print('Неверный ввод. Введите число!')

    # Генерация случайных коэффициентов полинома от 1 до p.
    def GenerateCoefs(self, polynom_degree, p):
        self.Coefs = [random.randint(1, p) for _ in range(polynom_degree)]

    # Обнуление коэффициентов полинома
    def ForgetCoefs(self):
        self.Coefs = []

    # Вычисление значения полинома в точке. Создание доли секрета для конкретного пользователя.
    def ShareOfThePartSecret(self, keeper_number, p):
        coefs_with_secret = self.Coefs + [self.Secret]
        degree = len(coefs_with_secret)

        # Значение полинома.
        f = sum(coef * keeper_number ** (degree - i - 1) for i, coef in enumerate(coefs_with_secret))
        return [keeper_number, f % p]
