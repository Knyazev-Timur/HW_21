from classes import Request, Store, Shop

def get_product(invoice):
    if invoice.get('from') == 'магазин' and check_in_shop(invoice):
        value = get_value_shop(invoice)
        print(f'В магазине имеется {storage.get_items().get(invoice["product"])} {invoice.get("product")}')
        storage.remove(invoice.get("product"), value)
        print(f'Курьер забирает из магазина {value} {invoice.get("product")}')
        set_product(invoice, value)

    elif invoice.get("from") == 'склад' and check_in_store(invoice):
        value = get_value_store(invoice)
        print(f'На складе имеется {stock.get_items().get(invoice["product"])} {invoice.get("product")}')
        stock.remove(invoice.get("product"), value)
        print(f'Курьер забирает со склада {value} {invoice.get("product")}')
        set_product(invoice, value)

    else:
        print('Будьте внимательны! Запрос не может быть обработан!')

def set_product(invoice, value):
    if invoice.get('to') == 'склад':
        delivery_to_store(invoice, value)
    elif invoice.get('to') == 'магазин':
        delivery_to_shop(invoice, value)
    else:
        print(f"Место доставки было указано некорректно. {value} {invoice.get('product')} остаются у курьера.")

def delivery_to_store(invoice, value):
    if stock.get_free_space() >= value:
        stock.add_item(invoice.get("product"), value)
        print(f"Курьер доставил на склад {value} {invoice.get('product')}")

    elif stock.get_free_space() < value:
        value_free = stock.get_free_space()
        print(f"На складе место только для {value_free} {invoice.get('product')}")
        stock.add_item(invoice.get("product"), value_free)
        print(f"Курьер доставил на склад {value_free} {invoice.get('product')}")
        print(f"Курьер вернул {value - value_free} {invoice.get('product')} в {invoice['from']}")
        invoice['to'] = invoice['from']
        invoice['from'] = None
        value -= value_free
        set_product(invoice, value)

def delivery_to_shop(invoice, value):
    if invoice.get('product') in list(storage.get_items().keys()) or storage.get_unique_items_count() < 5:
        if value <= storage.get_free_space():
            storage.add_item(invoice.get("product"), value)
            print(f"Курьер доставил в магазин {value} {invoice.get('product')}")
        elif value > storage.get_free_space():
            value_free = storage.get_free_space()
            print(f"В магазине место только для {value_free} {invoice.get('product')}")
            storage.add_item(invoice.get("product"), value_free)
            print(f"Курьер вернул {value - value_free} {invoice.get('product')} в {invoice['from']}")
            invoice['to'] = invoice['from']
            invoice['from'] = None
            value -= value_free
            set_product(invoice, value)
    else:
        print(
            f'В магазине нет свободных витрин. {value} {invoice.get("product")} будут возвращены на {invoice.get("from")}')
        invoice['to'] = invoice['from']
        invoice['from'] = None
        set_product(invoice, value)


def check_in_shop(invoice):
    if invoice.get('product') in list(storage.get_items().keys()):
        return True
    else:
        return False


def check_in_store(invoice):
    if invoice.get('product') in list(stock.get_items().keys()):
        return True
    else:
        return False


def get_value_shop(invoice):
    if storage.get_items().get(invoice['product']) >= invoice.get('amount'):
        return invoice.get('amount')
    else:
        return storage.get_items().get(invoice['product'])


def get_value_store(invoice):
    if stock.get_items().get(invoice['product']) >= invoice.get('amount'):
        return invoice.get('amount')
    else:
        return storage.get_items().get(invoice['product'])


#######################################################################################################
if __name__ == '__main__':

    store = {"печенье": 5, "конфеты": 4, "халва": 3, "шоколад": 6, "мороженное": 2}
    warehouse = {"коробка": 35, "лента": 10, "скотч": 20, "бумага": 10, "пленка": 20}

    storage = Shop()
    for item, value in store.items():
        storage.add_item(item, value)

    stock = Store()
    for item, value in warehouse.items():
        stock.add_item(item, value)

    while True:

        print(f'\nв магазине хранится:')
        for item, value in storage.get_items().items():
            print(f'{value} {item}')

        print(f'\nна складе хранится:')
        for item, value in stock.get_items().items():
            print(f'{value} {item}')

        print(f'\nВведите запрос в формате "Доставить 3 бумага из склад в магазин"\n'
              f'(для выхода введите "stop")')
        question = input().lower()

        if question == "stop":
            break

        quest = question.split()
        if len(quest) != 7:
            print('Запрос не корректен')
        else:
            _from = quest[4]
            _to = quest[6]
            amount = int(quest[1])
            product = quest[2]
            order = Request(_from, _to, amount, product)

        invoice = order.get_request()
        get_product(invoice)
        input()
