from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def add_item(self, title, qnt):
        pass

    @abstractmethod
    def remove(self, title, qnt):
        pass

    @abstractmethod
    def get_free_space(self):
        pass

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def get_unique_items_count(self):
        pass


class Item:
    def __init__(self, title, quantity):
        self.title = title
        self.quantity = quantity

    def get_title(self):
        return self.title

    def get_qnt(self):
        return self.quantity

    def get_items(self):
        return {self.title: self.quantity}


class Store(Storage):
    capacity = 100

    def __init__(self):
        self.items = {}

    @classmethod
    def _get_total(cls):
        return cls.capacity

    @classmethod
    def _set_total(cls, qnt):
        cls.capacity = qnt

    @classmethod
    def get_free_space(cls):
        return cls.capacity

    def add_item(self, title, qnt):
        if qnt < self._get_total():
            value = self.items.get(title, 0) + qnt  # Извлекает кол-во товара по ключу и прибавляет новое поступление

            item = Item(title=title, quantity=value)
            self.items[title] = value
            self._set_total(self._get_total() - qnt)
            self.capacity = qnt

        else:
            value = self.items.get(title, 0) + self._get_total()
            self.items[title] = value
            self.capacity = self._get_total()
            self._set_total(0)

    def more(self, qnt):
        if qnt < self._get_total():
            self._set_total(self._get_total() - qnt)
            self.capacity += qnt
        else:
            self.capacity = self._get_total()
            self._set_total(0)

    def remove(self, title, qnt):
        if self.items.get(title) is not None:
            if qnt < self.items.get(title):
                value = self.items.get(title) - qnt
                item = Item(title=title, quantity=value)
                self.items[title] = value
                self._set_total(self._get_total() + qnt)
                self.capacity -= qnt
            elif qnt >= self.items.get(title):
                # self.items[title] = 0
                self.capacity -= self.items.get(title)
                self._set_total(self._get_total() + self.items.get(title))
                value = self.items.pop(title, 0)
        else:
            print('Товар не найден')

    def get_items(self):
        return self.items

    def get_unique_items_count(self):
        return len(self.items)


class Shop(Store):
    capacity = 20
    items_count = 5

    def add_item(self, title, qnt):
        if len(self.items) < Shop.items_count or self.items.get(title) is not None:
            if qnt < self._get_total():
                value = self.items.get(title,
                                       0) + qnt  # Извлекает кол-во товара по ключу и прибавляет новое поступление

                item = Item(title=title, quantity=value)
                self.items[title] = value
                self._set_total(self._get_total() - qnt)
                self.capacity = qnt

            elif qnt >= self._get_total():
                value = self.items.get(title, 0) + self._get_total()
                self.items[title] = value
                self.capacity = self._get_total()
                self._set_total(0)
        else:
            print("Нет места на складе")
            print(list(self.get_items().keys()))


class Request:

    def __init__(self, _from, _to, amount, product):
        self._from = _from
        self._to = _to
        self.amount = amount
        self.product = product

    def get_request(self):
        return {
            'from': self._from,
            'to': self._to,
            'amount': self.amount,
            'product': self.product

        }
