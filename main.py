import pygame
import random
import sys

# Инициализация pygame
pygame.init()

# Определяем размеры окна игры
WIDTH = 1800
HEIGHT = 1080

meteor_counter = 0

# Создаем окно игры
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Игра с самолетом")

# Задаем цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Загружаем изображения самолета, метеорита и лазера
airplane_img = pygame.image.load("plane.png")
meteor_img = pygame.image.load("meteor.png")
laser_img = pygame.image.load("laser.png")

# Размеры самолета, метеорита и лазера
airplane_width = 80
airplane_height = 60
meteor_width = 50
meteor_height = 50
laser_width = 5
laser_height = 20

# Начальные координаты самолета
airplane_x = 350
airplane_y = 500

# Начальные координаты метеорита
meteor_x = random.randint(200, 900)  # Меняем диапазон спавна метеорита по оси X
meteor_y = -meteor_height
meteor_speed = 5 / 2.5  # Уменьшаем скорость в 1,5 раза

# Начальные координаты лазера
lasers = []  # Список для хранения активных лазеров
laser_speed = 10

# Функция для отрисовки самолета
def draw_airplane(x, y):
    screen.blit(airplane_img, (x, y))

# Функция для отрисовки метеорита
def draw_meteor(x, y):
    screen.blit(meteor_img, (x, y))

# Функция для отрисовки лазера
def draw_laser(x, y):
    screen.blit(laser_img, (x, y))

# Класс для лазера
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = laser_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

# Класс для метеорита
class Meteor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = meteor_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

# Создание спрайтов
meteor = Meteor(meteor_x, meteor_y)
lasers = pygame.sprite.Group()  # Группа для хранения спрайтов лазеров

# Основной цикл игры
running = True
while running:
    # Задаем цвет фона
    screen.fill(BLACK)

    keys = pygame.key.get_pressed()  # Получаем состояние клавиш
    if keys[pygame.K_LEFT]:
        airplane_x -= 10
    if keys[pygame.K_RIGHT]:
        airplane_x += 10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обработка нажатия на клавиши
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Стрельба - создание нового лазера
                laser_x = airplane_x + airplane_width / 2 - laser_width / 2  # Центрируем лазер относительно самолета
                laser_y = airplane_y
                lasers.add(Laser(laser_x, laser_y))  # Добавляем новый спрайт лазера в группу
            if event.key == pygame.K_q:
                pygame.display.iconify()  # Сворачиваем окно
            if event.key == pygame.K_ESCAPE:
                running = False  # Выход из игры

    # Движение самолета по горизонтали
    if airplane_x < 0:
        airplane_x = 0
    if airplane_x > WIDTH - airplane_width:
        airplane_x = WIDTH - airplane_width

    # Движение метеорита сверху вниз
    meteor.rect.y += meteor_speed
    if meteor.rect.y > HEIGHT:
        print(f"Вы сбили метеоритов: {meteor_counter}")  # Выводим сообщение о конце игры
        pygame.display.iconify()  # Сворачиваем окно
        running = False  # Завершаем игру

    # Движение лазера снизу вверх
    for laser in lasers:
        laser.rect.y -= laser_speed
        if laser.rect.y < 0:
            lasers.remove(laser)

    # Проверка столкновения самолета и метеорита
    if pygame.Rect(airplane_x, airplane_y, airplane_width, airplane_height).colliderect(meteor.rect):
        print(f"Игра окончена, Вы сбили {meteor_counter} метеоритов")  # Выводим сообщение о конце игры и количество сбитых метеоритов
        pygame.display.iconify()  # Сворачиваем окно
        running = False  # Завершаем игру

    # Проверка столкновения лазера и метеорита
    if pygame.sprite.spritecollide(meteor, lasers, True, pygame.sprite.collide_mask):
        meteor.rect.topleft = (random.randint(200, 900), -meteor_height)  # Спавним новый метеорит только при столкновении с лазером
        meteor_counter += 1
        print(f"Вы сбили метеоритов: {meteor_counter}")

    # Отрисовка самолета, метеорита и лазера
    draw_airplane(airplane_x, airplane_y)
    if meteor.rect.y < HEIGHT:  # Отрисовываем метеорит только если он в пределах экрана
        draw_meteor(meteor.rect.x, meteor.rect.y)
    for laser in lasers:
        draw_laser(laser.rect.x, laser.rect.y)

    # Обновление экрана
    pygame.display.flip()

# Завершение игры
pygame.quit()

