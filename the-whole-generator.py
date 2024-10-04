from random import randint
from random import choice
import csv
import time


def shop_dict_builder(in_file):
    source = open(f'A:/educ/algos/dataset-generation/input-data/shops/{in_file}.txt', "r", encoding="utf8")
    shoplist = {}
    for pstring in source:
        current_shop = list(pstring.split(' == '))
        current_shop[2] = current_shop[2].split(', ')
        current_shop[2][0] = int(current_shop[2][0])
        current_shop[2][1] = int(current_shop[2][1])

        current_shop[1] = current_shop[1].split(', ')
        current_shop[1][0] = round(float(current_shop[1][0]), 8)
        current_shop[1][1] = round(float(current_shop[1][1]), 8)

        current_shop[3] = current_shop[3].replace('\n', '')

        shoplist[current_shop[0]] = current_shop[1:4]
    source.close()
    return shoplist
# возвращает словарь с элементами вида 'магазин': [[xx.xxxxxxxx, yy.yyyyyyyy], [z, w], 'группа категорий']
# где х, у - широта и долгота соответственно; z, w - время открытия и закрытия магазина в секундах считая от полуночи


def dependencies_builder(in_file):
    source = open(f'A:/educ/algos/dataset-generation/input-data/categories/{in_file}.txt', "r", encoding="utf8")
    dependencies = {}
    for elem in source:
        dependency = elem.split(' == ')
        if dependencies.get(dependency[0]) is None:
            dependencies[dependency[0]] = [dependency[1].rstrip()]
        else:
            current = dependencies[dependency[0]]
            current.append(dependency[1].rstrip())
            dependencies[dependency[0]] = current
    source.close()
    return dependencies
# возвращает словарь с элементами вида 'категория товаров': ['товар 1', 'товар 2', ..., 'товар n']


def goods_builder(in_file):
    source = open(f'A:/educ/algos/dataset-generation/input-data/goods/{in_file}.txt', "r", encoding="utf8")
    dependencies = {}
    for elem in source:
        dependency = elem.split(' == ')
        if dependencies.get(dependency[0]) is None:
            price = dependency[2].rstrip()
            try:
                price = int(price)
            except ValueError:
                good = dependency[1]
                print(f'В вашем файле отсутствует цена товара {good}, проверьте файл, исправьте ошибку и перезапустите '
                      'программу, установлена цена 1\n')
                price = 1
            if price == 0:
                good = dependency[1]
                print(f'В вашем файле установлена нулевая цена товара {good}, проверьте файл, исправьте ошибку и '
                      'перезапустите программу, установлена цена 1\n')
                price = 1
            dependencies[dependency[0]] = [(dependency[1], price)]
        else:
            current = dependencies[dependency[0]]
            price = dependency[2].rstrip()
            try:
                price = int(price)
            except ValueError:
                good = dependency[1]
                print(f'В вашем файле отсутствует цена товара {good}, проверьте файл, исправьте ошибку и перезапустите '
                      'программу, установлена цена 1\n')
                price = 1
            price = int(price)
            current.append((dependency[1], price))
            dependencies[dependency[0]] = current
    source.close()
    return dependencies
# возвращает словарь с элементами вида 'товар': [('бренд 1', int 1), ('бренд 2', int 2), ..., ('бренд n', int n)],
# где int i - цена товара i-того бренда


def system_and_bank_settinger():
    system_probs, bank_probs = [100, 0, 0], [100, 0, 0]
    while True:
        probs = (input('Введите через пробел вероятность (в процентах) использования платёжных систем МИР, MC,'
                       ' Visa соответственно,\n сумма значений должна составить 100. Пример: 40 30 30: ')).split(' ')
        if len(probs) != 3:
            print('\nВведите три числа.\n')
            continue
        else:
            try:
                mir_prob, mc_prob, visa_prob = int(probs[0]), int(probs[1]), int(probs[2])
            except ValueError:
                print('\nВводите целые числа, пожалуйста.\n')
                continue

            if mir_prob + mc_prob + visa_prob == 100:
                system_probs = [mir_prob, mc_prob, visa_prob]
                break
            else:
                print('\nСумма ввёденных чисел должна составлять 100.\n')
                continue

    while True:
        probs = (input('Введите через пробел вероятность (в процентах) использования карт банков СБЕР, ВТБ, Т-БАНК'
                       ' соответственно,\n сумма значений должна составить 100. Пример: 40 30 30: ')).split(' ')
        if len(probs) != 3:
            print('\nВведите три числа.\n')
            continue
        else:
            try:
                sber_prob, vtb_prob, tink_prob = int(probs[0]), int(probs[1]), int(probs[2])
            except ValueError:
                print('\nВводите целые числа, пожалуйста.\n')
                continue

            if sber_prob + vtb_prob + tink_prob == 100:
                bank_probs = [sber_prob, vtb_prob, tink_prob]
                break
            else:
                print('\nСумма ввёденных чисел должна составлять 100.\n')
                continue
    return system_probs, bank_probs


def card_generator(sys_prob, bank_prob):
    sys_value = randint(1, 100)
    if sys_value <= sys_prob[0]:
        system = '2'
    elif sys_prob[0] < sys_value <= (sys_prob[0] + sys_prob[1]):
        system = '5'
    else:
        system = '4'

    bank_value = randint(1, 100)
    if bank_value <= bank_prob[0]:
        if system == '2':
            bank = '202'
        elif system == '5':
            bank = '469'
        else:
            bank = '276'
    elif bank_prob[0] < bank_value <= (bank_prob[0] + bank_prob[1]):
        if system == '2':
            bank = '204'
        elif system == '5':
            bank = '278'
        else:
            bank = '475'
    else:
        if system == '2':
            bank = '200'
        elif system == '5':
            bank = '213'
        else:
            bank = '377'

    remainder = ''
    for i in range(12):
        remainder += str(randint(0, 9))

    card_number = system + bank + remainder
    return card_number


def buyer(card_n, shopsl, conns, goodsl):
    card = card_n
    stroka = '\n'
    shop = choice(list(shopsl))

    cords = shopsl[shop][0]
    cordx = str(cords[0])
    cordy = str(cords[1])
    cords = cordx + ', ' + cordy

    date = str(randint(1, 30)) + '/' + str(randint(3, 11)) + '/' + '2024'
    borders = shopsl[shop][1]
    time = randint(borders[0], borders[1])
    hours = str(time // 3600)
    time %= 3600
    minutes = time // 60
    if minutes < 10:
        minutes = '0' + str(minutes)
    else:
        minutes = str(minutes)
    secs = time % 60
    if secs < 10:
        secs = '0' + str(secs)
    else:
        secs = str(secs)
    time = hours + ':' + minutes + ':' + secs

    group = shopsl[shop][2]
    group = conns[group]
    grouplen = len(group) - 1
    quantity = randint(5, 32)
    check = ''
    summ = 0
    for i in range(quantity):
        category = group[randint(0, grouplen)]
        if goodsl.get(category) is not None:
            goods = goodsl[category]
            goodslen = len(goods) - 1
            good = goods[randint(0, goodslen)]

            summ += int(good[1])
            check += category + ': ' + good[0] + ', '

    return [shop, cords, date, time, card, quantity, check, summ]


print('Приветствую вас в программе, генерирующей данные. Чтобы настроить датасет, перейдите в папку'
      '\n A:/educ/algos/dataset-generation/input-data'
      '\nи добавьте входные данные согласно примерам и инструкциям в файлах input-sample.txt,'
      '\nназовите все свои файлы одинаковыми именами согласно примерам в папках.')  # Инструкция
in_filename = input('\nВведите имя своих файлов без указания расширения (пример - input-sample, не input-sample.txt): ')

shops = shop_dict_builder(in_filename)
connections = dependencies_builder(in_filename)
goods = goods_builder(in_filename)

sys_probs, bank_probs = system_and_bank_settinger()  # Пользователь вводит вероятности оплаты картами определённых ПС и банков

cards_list = []

ite = 0
iters = 10
while iters < 50000:
    try:
        iters = int(input('Введите размер датасета (целое число): '))
    except ValueError:
        continue
    break
# Ввод количества покупок в файле

curtime = str(time.time())

with open(f'A:/educ/algos/dataset-generation/output/{curtime}.csv', 'a+', newline='') as mycsvfile:
    writer = csv.writer(mycsvfile, dialect='excel', delimiter=';', quotechar='\'')
    while ite < (iters + 1):
        while True:
            card = card_generator(sys_probs, bank_probs)
            if card in cards_list:
                continue
            else:
                cards_list.append(card)
                break
        card_util = randint(1, 5)
        ite += card_util
        if ite > iters:
            card_util -= (ite - iters)
        for ut in range(card_util):
            writer.writerow(buyer(card, shops, connections, goods))
mycsvfile.close()
