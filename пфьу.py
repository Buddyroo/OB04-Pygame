import pygame
import sys

#SCREEN
pygame.init()
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Вредные Соседи")

#BACKGROUND
background_original = pygame.image.load("img/background.png")
background = pygame.transform.scale(background_original, (screen_width, screen_height))#resize background image to screen size

#COLOR
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#SCREEN REFRESHMENT RATE, FPS
clock = pygame.time.Clock()
fps = 60

#TILES_IN_THE_GAME
tile_size = 80 #размер в пикселях
num_tiles_width = screen_width // tile_size  # количество тайлов по ширине
num_tiles_height = screen_height // tile_size  # количество тайлов по высоте
print(num_tiles_width, num_tiles_height)#выводим количество тайлов, для себя
#нарисуем тайлы для демонстрации разбивки
# Цвет линий сетки
grid_color = (200, 200, 200)  # Серый цвет


#FENCE
class Fence(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.width = 10
        self.image = pygame.Surface((self.width, screen_height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topright=(x, 0))
        self.health = 100

    def damage(self, amount, all_sprites, fences, neighbor):
        self.health -= amount
        if self.health <= 0:
            self.kill()

            x_new = self.rect.x + tile_size+self.width #прибавляем 80(ширина тайла)+10(ширина забора), потому что входной атрибут забора - это левый правый угол на пересечении тайлов, а координаты  - это левый верхний угол

            new_fence = Fence(x_new)
            fences.add(new_fence)
            all_sprites.add(new_fence)
            neighbor.rect.x = self.rect.x + 15
            neighbor.restart_movement()

class Character(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect(topright=(x, y))
        self.moving = True

    def update(self):
        if self.moving:
            self.rect.x += 1

    def restart_movement(self):
        self.moving = True

    def stop_movement(self):
        self.moving = False

    def move(self, dx=0, dy=0):
        self.rect.x += dx
        self.rect.y += dy

fences = pygame.sprite.Group()
initial_fence = Fence(160)
fences.add(initial_fence)

neighbor = Character(RED, 60, 180)
player = Character(BLACK, 3 * screen_width // 4, screen_height // 2)

all_sprites = pygame.sprite.Group()
all_sprites.add(initial_fence, neighbor, player)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(dx=-5)
        if keys[pygame.K_RIGHT]:
            player.move(dx=5)
        if keys[pygame.K_UP]:
            player.move(dy=-5)
        if keys[pygame.K_DOWN]:
            player.move(dy=5)



        neighbor.update()
        collision = pygame.sprite.spritecollideany(neighbor, fences)
        if collision:
            neighbor.stop_movement()
            collision.damage(1, all_sprites, fences, neighbor)

        screen.blit(background, (0, 0))

        # Рисуем сетку
        for x in range(0, screen_width, tile_size):  # Вертикальные линии
            pygame.draw.line(screen, grid_color, (x, 0), (x, screen_height), width=1)
        for y in range(0, screen_height, tile_size):  # Горизонтальные линии
            pygame.draw.line(screen, grid_color, (0, y), (screen_width, y), width=1)

        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()