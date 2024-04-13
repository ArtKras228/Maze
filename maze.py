from pygame import *
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self, img, speed, x, y):
        super().__init__()
        self.img = transform.scale(image.load(img), (100, 100))
        self.speed = speed
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 'right'
    def reset(self):
        win.blit(self.img, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self, key_pressed):
        if key_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= 5
        if key_pressed[K_s] and self.rect.y < 400:
            self.rect.y += 5
        if key_pressed[K_a] and self.rect.x > 0:
            if self.direction == 'left':
                pass
            else:
                self.img = transform.flip(self.img, True, False)
                self.direction = 'left'
            self.rect.x -= 5
        if key_pressed[K_d] and self.rect.x < 600:
            if self.direction == 'right':
                pass
            else:
                self.img = transform.flip(self.img, True, False)
                self.direction = 'right'
            self.rect.x += 5
        if key_pressed[K_w] and key_pressed[K_LSHIFT] and self.rect.y > 0:
            self.rect.y -= 7
        if key_pressed[K_s] and key_pressed[K_LSHIFT] and self.rect.y < 400:
            self.rect.y += 7
        if key_pressed[K_a] and key_pressed[K_LSHIFT] and self.rect.x > 0:
            if self.direction == 'left':
                pass
            else:
                self.img = transform.flip(self.img, True, False)
                self.direction = 'left'
            self.rect.x -= 7
        if key_pressed[K_d] and key_pressed[K_LSHIFT] and self.rect.x < 600:
            if self.direction == 'right':
                pass
            else:
                self.img = transform.flip(self.img, True, False)
            self.direction = 'right'
            self.rect.x += 7

class Enemy(GameSprite):
    def move(self, key_pressed):
        self.rect.x -= self.speed
        if self.rect.x < 400:
            self.speed *= -1
            self.img = transform.flip(self.img, True, False)
        if self.rect.x > 600:
            self.speed *= -1
            self.img = transform.flip(self.img, True, False)

class Wall(sprite.Sprite):
    def __init__(self, color, w, h, x, y):
        super().__init__()
        self.color = color
        self.img = Surface((w, h))
        self.img.fill(self.color)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw_wall(self):
        win.blit(self.img, (self.rect.x, self.rect.y))

hero = Player('hero.png', 10, 0, 0)
enemy = Enemy('cyborg.png', 5, 600, 120)
enemy.img = transform.flip(enemy.img, True, False)
target = GameSprite('exit.png', 1, 500, 0)
wall1 = Wall((13, 0, 13), 15, 380, 100, 0)
wall2 = Wall((13, 0, 13), 15, 400, 230, 100)
wall3 = Wall((13, 0, 13), 15, 380, 360, 0)
wall4 = Wall((13, 0, 13), 215, 15, 360, 380)

win = display.set_mode((700,500))
display.set_caption('Лабиринт')

clock = time.Clock()
run = True
finish = False
mixer.init()
mixer.music.load('main-menu-2.ogg')
kick = mixer.Sound('game-lost.ogg')
won = mixer.Sound('game-won.ogg')
mixer.music.play()

bg = transform.scale(image.load('background.jpg'), (700,500))

while run:
    key_pressed = key.get_pressed()
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not(finish):
        win.blit(bg, (0,0))

        wall1.draw_wall()
        wall2.draw_wall()
        wall3.draw_wall()
        wall4.draw_wall()
        target.reset()

        hero.move(key_pressed)
        hero.reset()
        enemy.move(key_pressed)
        enemy.reset()

        if sprite.collide_rect(hero, target):
            won.play()
            finish = True
            message = font.SysFont('arial', 70).render('ТЫ ВЫИГРАЛ', True, (0,255,0))
            win.blit(message, (200,200))

        if (
            sprite.collide_rect(hero, wall1) or
            sprite.collide_rect(hero, wall2) or
            sprite.collide_rect(hero, wall3) or
            sprite.collide_rect(hero, wall4) or
            sprite.collide_rect(hero, enemy)):
            kick.play()
            finish = True
            message = font.SysFont('arial', 70).render('ТЫ ПРОИГРАЛ', True, (255,0,0))
            win.blit(message, (250,200))

    display.update()
    clock.tick(60)