import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Вредные Соседи")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# FPS
clock = pygame.time.Clock()
fps = 60

class Fence(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((80, 60))  # Размеры квадрата
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100

    def damage(self, amount, all_sprites, fences, neighbor):
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Удаляем забор, если его здоровье исчерпано
            if self.rect.x + 80 < screen_width:  # Проверяем, не выходим ли за правый край экрана
                new_fence = Fence(self.rect.x + 80, self.rect.y)
                fences.add(new_fence)
                all_sprites.add(new_fence)

class Character(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.moving = True

    def update(self):
        if self.moving:
            self.rect.x += 1  # Сосед двигается вправо

    def restart_movement(self):
        self.moving = True  # Возобновить движение соседа

    def stop_movement(self):
        self.moving = False  # Остановить движение соседа

def main():
    all_sprites = pygame.sprite.Group()
    fences = pygame.sprite.Group()

    # Инициализация заборов на сетке
    for i in range(0, screen_width, 80):  # Создаем сетку заборов с шагом 80 пикселей по горизонтали
        for j in range(0, screen_height, 60):  # и 60 пикселей по вертикали
            if i == 400 and j == 300:  # Поместим начальный забор в центр
                fence = Fence(i, j)
                fences.add(fence)
                all_sprites.add(fence)

    # Инициализация персонажей
    neighbor = Character(RED, 400, 300)  # Сосед начинает по центру сетки
    all_sprites.add(neighbor)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        neighbor.update()  # Обновляем позицию соседа
        collision = pygame.sprite.spritecollideany(neighbor, fences)  # Проверяем столкновение с любым забором
        if collision:
            neighbor.stop_movement()  # Остановить соседа при столкновении
            collision.damage(1, all_sprites, fences, neighbor)  # Наносим урон забору

        screen.fill(WHITE)  # Очищаем экран
        all_sprites.draw(screen)  # Отрисовываем все спрайты
        pygame.display.flip()  # Обновляем экран
        clock.tick(fps)  # Удерживаем FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
