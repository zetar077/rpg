from settings import *
from support import Timer

class Sprite(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surf, ground=False):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        # ground=True - тайлы земли (рисуются первыми, без сортировки)
        self.ground = ground

class Player(Sprite):
    def __init__(self,groups,pos,frames,collision_rects,bounds):
        self.frames = frames
        self.state = 'down'
        self.frame_index = 1
        self.last_state = 'down'
        super().__init__(groups,pos,self.frames[self.state][int(self.frame_index)],ground=False)
        self.direction = pygame.Vector2()
        self.speed = 100
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-30, -50)
        # квадраты с карты (слой Collisions), с которыми нельзя сталкиваться
        self.collision_rects = collision_rects
        # границы карты, чтобы не выйти за её край
        self.bounds = bounds
    def input(self):
        keys = pygame.key.get_pressed()
        # D даёт 1, A даёт 1, вместе выходит 0. То же самое для S и W.
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        # вектор (1, 1) длиннее вектора (1, 0). После normalize длина снова 1.
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()
    def move(self, dt):
        #вычисляем скорость и направление
        displacement = self.direction * self.speed * dt

        # двигаем хитбокс по X и разрешаем столкновения
        self.hitbox_rect.centerx += displacement.x
        for rect in self.collision_rects:
            if self.hitbox_rect.colliderect(rect):
                if displacement.x > 0:
                    self.hitbox_rect.right = rect.left
                elif displacement.x < 0:
                    self.hitbox_rect.left = rect.right

        # двигаем хитбокс по Y и разрешаем столкновения
        self.hitbox_rect.centery += displacement.y
        for rect in self.collision_rects:
            if self.hitbox_rect.colliderect(rect):
                if displacement.y > 0:
                    self.hitbox_rect.bottom = rect.top
                elif displacement.y < 0:
                    self.hitbox_rect.top = rect.bottom

        # не даём выйти за границы карты
        self.hitbox_rect.clamp_ip(self.bounds)

        # возвращаем видимый rect на место хитбокса
        self.rect.move_ip(
            self.hitbox_rect.centerx - self.rect.centerx,
            self.hitbox_rect.centery - self.rect.centery,
        )
    def update(self,dt):
        self.input()
        self.move(dt)
        self.animate(dt)
    def get_state(self):
        # сначала проверяем диагонали (более конкретные случаи),
        # иначе они перехватываются простыми проверками x<0 / x>0
        x = self.direction.x
        y = self.direction.y
        if x == 0 and y == 0:
            return self.last_state
        if x > 0 and y < 0:
            return 'right_up'
        if x > 0 and y > 0:
            return 'right_down'
        if x < 0 and y < 0:
            return 'left_up'
        if x < 0 and y > 0:
            return 'left_down'
        if x > 0:
            return 'right'
        if x < 0:
            return 'left'
        if y > 0:
            return 'down'
        return 'up'
    def animate(self, dt):
        state = self.get_state()
        moving = self.direction.length_squared() > 0
        if moving:
            self.frame_index += 10 * dt
            self.last_state = state
        else:
            self.frame_index = 1
            state = self.last_state

        frames = self.frames[state]
        self.image = frames[int(self.frame_index) % len(frames)]
        self.rect = self.image.get_frect(center=self.rect.center)
        self.state = state
        
