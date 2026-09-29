from LinkedList import LinkedList, LinkedListItem

# Музыкальная композиция
class Composition:

    def __init__(self, title: str, path: str):
        self.title = title
        self.path = path

    def __repr__(self) -> str:
        return f"Composition({self.title}, {self.path})"


# Плейлист
class PlayList(LinkedList):

    def __init__(self):
        super().__init__()
        self.current_item = None

    # Запуск проигрывания с выбранной композиции
    def play_all(self, start_from: LinkedListItem = None):

        if self.first_item is None:
            return
        if start_from is not None and start_from in self:
            # Поиск стартового элемента
            current = self.first_item
            while current.track != start_from:
                current = current.next_item
            self.current_item = current
        else:
            self.current_item = self.first_item

    # Переход к следующей композиции
    def next_track(self) -> Composition:
        if self.current_item is not None:
            self.current_item = self.current_item.next_item
            return self.current_item.data()
        else:
            if self.first_item is None:
                return None
            return self.first_item.data()

    # Переход к предыдущей композиции
    def previous_track(self) -> Composition:
        if self.current_item is not None:
            self.current_item = self.current_item.previous_item
            return self.current_item.data()
        else:
            if self.first_item is None:
                return None
            return self.first_item.data()

    @property
    # Получение текущей композиции
    def current(self) -> Composition:
        return self.current_item.data()