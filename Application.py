import sys
import pygame
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog
from PlayList import PlayList, Composition

pygame.init()  # 🎵 Подготовка библиотеки Pygame для воспроизведения звука.


class PlayerUI(QWidget):
    """Графический интерфейс плеера."""

    def __init__(self):
        super().__init__()
        self.playlist = PlayList()
        self.current_file_label = QLabel('Нет файла')
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Список композиций
        list_layout = QHBoxLayout()
        self.list_widget = QListWidget()
        add_button = QPushButton('Добавить композицию')
        add_button.clicked.connect(self.add_composition)
        list_layout.addWidget(self.list_widget)
        list_layout.addWidget(add_button)
        layout.addLayout(list_layout)

        # Текущая композиция
        layout.addWidget(QLabel('Текущий файл'))
        layout.addWidget(self.current_file_label)

        # Управление воспроизведением
        control_layout = QHBoxLayout()
        prev_btn = QPushButton('<< Предыдущая')
        prev_btn.clicked.connect(self.prev_track)
        play_btn = QPushButton('► Воспроизвести')
        play_btn.clicked.connect(self.play_current)
        next_btn = QPushButton('Следующая >>')
        next_btn.clicked.connect(self.next_track)
        control_layout.addWidget(prev_btn)
        control_layout.addWidget(play_btn)
        control_layout.addWidget(next_btn)
        layout.addLayout(control_layout)

        self.setLayout(layout)
        self.resize(450, 300)
        self.setWindowTitle('Музыка ♫️')

    def update_list_view(self):
        """Обновляет отображаемый список композиций."""
        self.list_widget.clear()
        for idx, item in enumerate(self.playlist):
            self.list_widget.insertItem(idx, item.track.title)

    def add_composition(self):
        """Открывает диалог выбора файла и добавляет его в плейлист."""
        file_path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Выберите музыкальный файл',
            filter="MP3 файлы (*.mp3);;Все файлы (*.*)"
        )
        if file_path:
            comp = Composition(file_path.split('/')[-1], file_path)
            self.playlist.append_right(comp)
            self.update_list_view()

    def play_current(self):
        """Начинает или продолжает воспроизведение текущего трека."""
        if self.playlist.current_item is not None:
            pygame.mixer.music.load(self.playlist.current_item.path)
            pygame.mixer.music.play()
            self.current_file_label.setText(f'Сейчас играет: {self.playlist.current_item.title}')

    def next_track(self):
        """Переходит к следующей композиции и запускает её."""
        track = self.playlist.next_track()
        if track is not None:
            self.current_file_label.setText(f'Сейчас играет: {track.title}')
            pygame.mixer.music.load(track.path)
            pygame.mixer.music.play()

    def prev_track(self):
        """Переходит к предыдущей композиции и запускает её."""
        track = self.playlist.previous_track()
        if track is not None:
            self.current_file_label.setText(f'Сейчас играет: {track.title}')
            pygame.mixer.music.load(track.path)
            pygame.mixer.music.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlayerUI()
    window.show()
    sys.exit(app.exec())