import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # РЕКОМЕНДАЦИЯ : Лучше записать проще: if not date.
        self.date = (
            dt.datetime.now().date() if
            not
            # РЕКОМЕНДАЦИЯ : если передать дату '31.02.2026', возникнет ValueError.
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        # РЕКОМЕНДАЦИЯ : здесь создаётся лишний список. В sum можно передать генератор без квадратных скобок.
        return sum([rec.amount for rec in self.records if rec.date == dt.datetime.now().date()])

    def get_week_stats(self):
        today = dt.datetime.now().date()
        # РЕКОМЕНДАЦИЯ : запись 7 > ... >= 0 немного путает. Проще читать как 0 <= (today - rec.date).days < 7.
        return sum([rec.amount for rec in self.records if 7 > (today - rec.date).days >= 0])


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        # РЕКОМЕНДАЦИЯ : x не очень понятное имя переменной. Лучше назвать её calories_left, сразу ясно, что там хранится.
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return ('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # ОШИБКА: курсы в параметрах сохраняются в момент создания метода. Лучше брать значения через self.USD_RATE и self.EURO_RATE.
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        cash_remained = self.limit - self.get_today_stats()

        # РЕКОМЕНДАЦИЯ : название d ничего не объясняет. Можно назвать словарь rates, чтобы было понятнее.
        d = {'usd': (USD_RATE, 'USD'), 'eur': (EURO_RATE, 'Euro'), 'rub': (1.0, 'руб')}

        rate = d.get(currency)
        if rate is None:
            return f'Неизвестная валюта {currency}'

        # ОШИБКА: если вызвать метод с USD_RATE=0 и currency="usd", программа упадёт с ZeroDivisionError. Перед делением нужно проверять, что курс больше нуля.
        cash_remained /= rate[0]
        # РЕКОМЕНДАЦИЯ : курс уже найден в переменной rate. Лучше взять название валюты из rate[1], чтобы не искать то же самое в словаре ещё раз.
        currency_type = d.get(currency)[1]

        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        # ОШИБКА: забыли return. 
        super().get_week_stats()
