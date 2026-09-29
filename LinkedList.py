from collections.abc import Iterator

# Узел связного списка
class LinkedListItem:

    # Инциализация элемента
    # Вместо track по схеме используется data
    # Поскольку требуется реализация нескольких плейлистов
    def __init__(self, data = None):
        self._data = data
        self._next = None
        self._previous = None

    @property
    def next_item(self):
        return self._next

    @next_item.setter
    def next_item(self, value):
        self._next = value
        if value.previous_item != self:
            value.previous_item = self

    @property
    def previous_item(self):
        return self._previous

    @previous_item.setter
    def previous_item(self, value):
        self._previous = value
        if value.next_item != self:
            value.next_item = self

    @property
    def data(self):
        return self._data

    def __repr__(self):
        return repr(self.data)

    def __eq__(self, other):
        """
        Переопределяем __eq__ под тест, сравнивая значение со значением
        Если в сравнение передается не LinkedListItem
        (Тест reversed)
        """
        if isinstance(other, LinkedListItem):
            return self is other
        else:
            return self.data == other


# Итератор для двусвязного списка
class LinkedListIterator(Iterator):

    def __init__(self, first_item: LinkedListItem, is_reversed: bool = False):
        if is_reversed:
            if first_item is not None:
                self.current_item = first_item.previous_item
            else:
                self.current_item = first_item
        else:
            self.current_item = first_item

        self.start = self.current_item
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
    def append_left(self, item):
        new_list_item = LinkedListItem(item)
        if self.first_item is None:
            self.__init_first_item(new_list_item)
        else:
            self.__append_new_item(new_list_item)
            # Для добавления "слева" устанавливаем первым новый элемент
            self.first_item = new_list_item

    # Добавить справа
    def append_right(self, item):
        new_list_item = LinkedListItem(item)
        if self.first_item is None:
            self.__init_first_item(new_list_item)
        else:
            self.__append_new_item(new_list_item)

    # Добавить справа
    def append(self, item):
        self.append_right(item)

    # Удалить элемент
    def remove(self, item):
        current_item = self.first_item
        # Проверка на наличие хотя бы одного элемента
        if current_item is None:
            raise ValueError("Удаляемого объекта нет в списке")

        # Удаление единственного элемента
        if (current_item == self.first_item
            and self.first_item.next_item == self.first_item
            and current_item.data == item):
            self.first_item = None
            return

        while True:
            if current_item.data == item:
                previous_item = current_item.previous_item
                next_item = current_item.next_item
                previous_item.next_item = current_item.next_item
                next_item.previous_item = previous_item
                # Если удален первый элемент коллекции, устанавливаем новый
                if current_item == self.first_item:
                    self.first_item = next_item
                break
            else:
                current_item = current_item.next_item
                # Если обошли все элементы, вызываем ошибку
                if current_item == self.first_item:
                    raise ValueError("Удаляемого объекта нет в списке")

    # Вставка справа от указанного элемента
    def insert(self, previous: LinkedListItem, item):
        new_list_item = LinkedListItem(item)
        current_item = self.first_item
        while True:
            if current_item.data == previous:
                next_item = current_item.next_item
                current_item.next_item = new_list_item
                new_list_item.previous_item = current_item
                new_list_item.next_item = next_item
                next_item.previous_item = new_list_item
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

    """ 
    Получение элемента по индексу
    Тоже адаптировано под тест, возможно такая методология для связных списков?
    Но список имеющий 1 элемент с 0 индексом = длина 1
    Должен возвращать ошибку при получении на вход индекса 1 - за границей
    И не выдавать ошибку при получении на вход индекса -1? Это не за границей?
    """
    def __getitem__(self, index: int) -> LinkedListItem:
        list_length = self.__len__()
        if index >= list_length or index < -list_length:
            raise IndexError("Индекс выходит за границу списка")
        if index == 0:
            return self.first_item.data
        current_item = self.first_item
        if index > 0:
            for i in range(index + 1):
                if i == index:
                    break
                current_item = current_item.next_item
        else:
            for i in range(0, index - 1, -1):
                if i == index:
                    break
                current_item = current_item.previous_item
        return current_item.data

    def __contains__(self, item) -> bool:
        current_item = self.first_item
        if current_item is not None:
            while True:
                if current_item.data == item:
                    return True
                current_item = current_item.next_item
                if current_item is self.first_item:
                    break
        return False

    def __reversed__(self):
        return LinkedListIterator(self.first_item, True)

