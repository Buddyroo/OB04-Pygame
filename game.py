import pygame
import time

pygame.init()

window_size = (800, 800)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Вредные соседи")

image_full = pygame.image.load("img/harry1 (magick converted).png")
image = pygame.transform.scale(image_full, (110, 110))
image_rect = image.get_rect()

image2=pygame.image.load("img/broom.png")
image2 = pygame.transform.scale(image2, (120, 80))
image2_rect = image2.get_rect()

# FPS
clock = pygame.time.Clock()
fps = 60

class Fence(с):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, screen_height))  # Создаем поверхность для забора
        self.image.fill(GREEN)  # Заполняем забор зеленым цветом
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))  # Позиционируем забор
        self.health = 100  # Устанавливаем начальное здоровье забора

    def move(self, offset):
        """ Перемещение забора по горизонтали. """
        self.rect.x += offset  # Сдвигаем забор на заданное количество пикселей

    def damage(self, amount):
        """ Уменьшение здоровья забора при ударе. """
        self.health -= amount  # Уменьшаем здоровье забора
        if self.health <= 0:
            self.kill()  # Удаляем забор, если его здоровье исчерпано
class Character(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))

    def move(self, dx=0, dy=0):
        self.rect.x += dx
        self.rect.y += dy


speed = 1

run = True

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            image_rect.center = mouse_x, mouse_y

    if image_rect.colliderect(image2_rect):
        print("collision")
        time.sleep(1)#чтобы не писало Столкновение 50 раз за секунду

    # keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT]:
        #     image_rect.x -= speed
        # if keys[pygame.K_RIGHT]:
        #     image_rect.x += speed
        # if keys[pygame.K_UP]:
        #     image_rect.y -= speed
        # if keys[pygame.K_DOWN]:
        #     image_rect.y += speed




    screen.fill((0, 0, 0))
    screen.blit(image,image_rect)
    screen.blit(image2, image2_rect)
    pygame.display.flip()


pygame.quit()
