from collections.abc import Iterator

# Узел связного списка
class LinkedListItem:

    # Инциализация элемента
    def __init__(self, data = None):
        self.data = data
        self._next = None
        self._previous = None

    @property
    def next_item(self):
        return self._next

    @next_item.setter
    def next_item(self, value):
        self._next = value

    @property
    def previous_item(self):
        return self._previous

    @previous_item.setter
    def previous_item(self, value):
        self._previous = value

    def __repr__(self):
        return repr(self.data)


# Итератор для двусвязного списка
class LinkedListIterator(Iterator):

    def __init__(self, first_item: LinkedListItem, is_reversed: bool = False):
        self.current_item = first_item
        self.start = first_item
        self.has_yielded_start = False
        self.is_reversed = is_reversed

    def __next__(self):
        if self.current_item is None:
            raise StopIteration()
        # Проверка, что обошли весь список
        if self.current_item == self.start and self.has_yielded_start:
            raise StopIteration()

        item_to_return = self.current_item
        if self.is_reversed:
            self.current_item = self.current_item.previous_item
        else:
            self.current_item = self.current_item.next_item
        self.has_yielded_start = True
        return item_to_return


# Кольцевой двусвязный список
class LinkedList:

    # Инциализация
    def __init__(self, first_item: LinkedListItem = None):
        self.first_item = first_item
        self.current_item = first_item

    # Добавить слева
    def append_left(self, item: LinkedListItem):
        new_list_item = LinkedListItem(item)
        if self.first_item is None:
            self.__init_first_item(new_list_item)
        else:
            self.__append_new_item(new_list_item)
            # Для добавления "слева" устанавливаем первым новый элемент
            self.first_item = new_list_item

    # Добавить справа
    def append_right(self, item: LinkedListItem):
        new_list_item = LinkedListItem(item)
        if self.first_item is None:
            self.__init_first_item(new_list_item)
        else:
            self.__append_new_item(new_list_item)

    # Добавить справа
    def append(self, item: LinkedListItem):
        self.append_right(item)

    # Удалить элемент
    def remove(self, item: LinkedListItem):
        current_item = self.first_item
        # Проверка на наличие хотя бы одного элемента
        if current_item is None:
            raise ValueError("Удаляемого объекта нет в списке")

        while True:
            if current_item == item:
                previous_item = current_item.previous_item
                current_item.previous_item = current_item.next_item
                current_item.next_item = previous_item
                break
            else:
                current_item = current_item.next_item
                # Если обошли все элементы, вызываем ошибку
                if current_item == self.first_item:
                    raise ValueError("Удаляемого объекта нет в списке")

    # Вставка справа от указанного элемента
    def insert(self, previous: LinkedListItem, item: LinkedListItem):
        current_item = self.first_item
        while True:
            if current_item == previous:
                next_item = current_item.next_item
                current_item.next_item = item
                item.previous_item = current_item
                item.next_item = next_item
                next_item.previous_item = item
                break
            else:
                current_item = current_item.next_item
            # Элемент не найден - выход из метода
            if current_item == self.first_item:
                return

    # Последний элемент
    @property
    def last(self):
        if self.first_item is not None:
            return self.first_item.previous_item
        else:
            return None

   # Служебный метод для добавления нового элемента, если список пустой
    def __init_first_item(self, new_item: LinkedListItem):
        self.first_item = new_item
        new_item.next_item = new_item
        new_item.previous_item = new_item

    # Служебный метод для добавления нового элемента, если в списке есть элементы
    def __append_new_item(self, new_item: LinkedListItem):
        last_item = self.first_item.previous_item
        last_item.next_item = new_item
        new_item.previous_item = last_item
        new_item.next_item = self.first_item
        self.first_item.previous_item = new_item

    # Получение размера списка
    def __len__(self) -> int:
        len = 0
        current_item = self.first_item
        if current_item is None:
            return len

        while True:
            len += 1
            current_item = current_item.next_item
            if current_item == self.first_item:
                break
        return len

    # Итератор
    def __iter__(self) -> Iterator[LinkedListItem]:
        return LinkedListIterator(self.first_item)

    # Получение элемента по индексу
    def __getitem__(self, index: int) -> LinkedListItem:
        if index >= self.__len__():
            raise ValueError("Индекс выходит на границу списка")
        if index == 0:
            return self.first_item
        current_item = self.first_item
        for i in range(index + 1):
            if i == index:
                break
            current_item = current_item.next_item
        return current_item

    def __contains__(self, item: LinkedListItem) -> bool:
        current_item = self.first_item
        if current_item is not None:
            while True:
                if current_item == item:
                    return True
                current_item = current_item.next_item
                if current_item is self.first_item:
                    break
        return False

    def __reversed__(self):
        return LinkedListIterator(self.first_item, True)

