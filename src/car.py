import pygame
import random
import time

import brain_device as device

device.start()
device.prepare()
pygame.init()

W = 600
H = 700
screen = pygame.display.set_mode([W, H])

WHITE = (255, 255, 255)
GREY = (160, 160, 160)

car_w = 75
car_h = 100
x = W // 2 - car_w // 2
y = H - 225

pol1_x = W // 3 - 10
pol1_y = 0
pol2_x = 2 * W // 3 - 10
pol2_y = 0

money_w = 75
money_h = 75

mashinka_x = 0
DRIFT = 1


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (car_w, car_h))
        self.rect = self.image.get_rect(
            topleft=(x, y))
        self.default_x = x
        self.default_y = y

    def draw(self):
        screen.blit(self.image, self.rect)

    def default_pos(self):
        self.rect.x = self.default_x
        self.rect.y = self.default_y

    def move_right(self):
        self.rect.x += W // 3
        if self.rect.x > W:
            self.rect.x -= W // 3

    def move_left(self):
        self.rect.x -= W // 3
        if self.rect.x < 0:
            self.rect.x += W // 3

    def set_state(slef, kak):
        if kak == -1:
            slef.move_left()
            slef.move_left()
        if kak == 1:
            slef.move_right()
            slef.move_right()
        if kak == 0:
            slef.move_left()
            slef.move_left()
            slef.move_right()


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (car_w, car_h))
        self.rect = self.image.get_rect(
            topleft=(x, y))
        self.y = y
        self.speed = 0.3

    def update(self):
        self.rect.y = self.y
        self.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)


class Money(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (money_w, money_h))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(
            topleft=(x, y))
        self.y = y
        self.speed = random.choice((0.3, 0.5, 0.6))

    def update(self):
        self.rect.y = self.y
        self.y += self.speed
        if self.rect.y > H:
            self.kill()

    def draw(self):
        screen.blit(self.image, self.rect)


class Pol(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = random.choice((0.3,))

    def update(self):
        self.y += self.speed
        if self.y > H:
            self.y = -100

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, 20, 100))


font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


car = Player(x, y, '../assets/Sprites/Car_we.png')

t = 0
col = 0

moneys = pygame.sprite.Group()
cars = pygame.sprite.Group()
pols = pygame.sprite.Group()

cur_y = 0
while cur_y < H:
    pol_1 = Pol(pol1_x, cur_y)
    pols.add(pol_1)
    pol_2 = Pol(pol2_x, cur_y)
    pols.add(pol_2)
    cur_y += 200

score = 0

running = True
read_cnt = 0
start_time = time.time()
while running:
    if time.time() - t > 5:
        t = time.time()
        col = random.randint(0, 2)
        typ = random.randint(1, 6)
        if typ < 4:
            car1 = Car(W // 3 * col + (W - 40) // 6 - car_w / 2 + col // 2 * 10 + (col == 1) * 7, -car_h,
                       '../assets/Sprites/Car' + str(typ) + '.png')
            cars.add(car1)
        if typ >= 4:
            money = Money(W // 3 * col + (W - 40) // 6 - car_w / 2 + col // 2 * 10 + (col == 1) * 7, -money_h,
                          '../assets/Sprites/Money.png')

            moneys.add(money)

    hits_money = pygame.sprite.spritecollide(car, moneys, True)
    hits_car = pygame.sprite.spritecollide(car, cars, True)

    if hits_car:
        score = 0

    for hit in hits_money:
        score += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    car.set_state(device.get_data())
    """
    if device.ready_to_get_data():
        window = device.get_window(4)
        sum = 0
        for a in window:
            sum += a
        if sum == 0:
            read_cnt = 0
        print(read_cnt)
        if read_cnt % 4 == 0:
            if sum == 1 or sum == 2:
                mashinka_x = -1
            if sum >= 3:
                mashinka_x = 1
            if sum == 0:
                mashinka_x = 0
            car.set_state(mashinka_x)
        read_cnt += 1
    """
    screen.fill(GREY)

    for pol in pols:
        pol.draw()
    car.draw()
    cars.draw(screen)
    moneys.draw(screen)

    cars.update()
    moneys.update()
    pols.update()

    draw_text(screen, 'Score: ' + str(score), 18, 30, 5)
    draw_text(screen, 'Time: ' + str(int(time.time()-start_time)), 18, 50, 5)

    pygame.display.flip()

    # pygame.time.delay(20)
device.stop()
pygame.quit()