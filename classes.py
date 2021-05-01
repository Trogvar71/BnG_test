# в этом модуле будет самописный класс для IP-адреса, чтобы удобнее
# было абстрагировать операции с адресами. Я намеренно написал свой класс
# вместо использования готового решения, чтобы продемонстрировать ради проекта
# технологию создания классов и собственных модулей

class IPaddress():
    # адрес инициализируется, принимая на вход строку
    # если адрес корректный, задаем значения атрибутов
    def __init__(self, addr):
        self.addr = addr
        if self.is_correct():
            self.string = addr
            self.octs = [int(i) for i in addr.split('.')]
            # октеты адреса, начиная от старшего
            self.o1 = self.octs[0]
            self.o2 = self.octs[1]
            self.o3 = self.octs[2]
            self.o4 = self.octs[3]
        else:
            self.string = None

    def is_correct(self):
        # print('проверка адреса')
        oct = self.addr.split('.')
        if not all(i.isdigit() for i in oct):
            print('Некорректные символы в адресе', self.addr)
            return False
        elif len(oct) != 4:
            print('Неверный формат адреса', self.addr)
            return False
        elif not all(0 <= int(i) <= 255 for i in oct):
            print('Выход за допустимый диапазон', self.addr)
            return False
        else:
            # print('OK')
            return True

    def __str__(self):
        return self.string

    def get_octs(self):
        return self.octs

    def get_o1(self):
        return self.o1

    def get_o2(self):
        return self.o2

    def get_o3(self):
        return self.o3

    def get_o4(self):
        return self.o4

    # реализовал операции сравнения адресов для проверки правильного ввода, ну и просто чтобы были на будущее
    def __gt__(self, other):
        if self.o1 > other.o1:
            return True
        elif self.o1 == other.o1:
            if self.o2 > other.o2:
                return True
            elif self.o2 == other.o2:
                if self.o3 > other.o3:
                    return True
                elif self.o3 == other.o3:
                    if self.o4 > other.o4:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def __lt__(self, other):
        if self.o1 < other.o1:
            return True
        elif self.o1 == other.o1:
            if self.o2 < other.o2:
                return True
            elif self.o2 == other.o2:
                if self.o3 < other.o3:
                    return True
                elif self.o3 == other.o3:
                    if self.o4 < other.o4:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    # для проверки четкого равенства достаточно сравнить строковые представления
    def __eq__(self, other):
        return self.string == other.string

    def __ne__(self, other):
        return self.string != other.string

    def __ge__(self, other):
        return self > other or self == other

    def __le__(self, other):
        return self < other or self == other



