from settings import *
class All_sprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()
        self.camera_speed = 0.1
        self.camera_init = False  # в первом кадре камера сразу ставится на игрока
        self.shake_strength = 0
        self.shake_offset = pygame.Vector2()
    def shake(self,power):
        self.shake_strength = power
    def draw(self, target_pos):
        # считаем смещение камеры: оно должно быть числом, а не объектом экрана.
        # target_pos - это позиция игрока (например, player.rect.center)
        target_offset = pygame.Vector2()
        target_offset.x = -(target_pos[0] - SCREEN_WIDTH // 2)
        target_offset.y = -(target_pos[1] - SCREEN_HEIGHT // 2)
        if not self.camera_init:  # первый кадр - камера сразу в нужном месте
            self.offset.update(target_offset)
            self.camera_init = True
        else:
            self.offset += (target_offset - self.offset) * self.camera_speed
        if self.shake_strength > 0:
            self.shake_offset.x = random.uniform(-self.shake_strength, self.shake_strength)
            self.shake_offset.y = random.uniform(-self.shake_strength, self.shake_strength)
            self.shake_strength *= 0.9
            if self.shake_strength < 0.1:
                self.shake_strength = 0
        else:
            self.shake_offset = pygame.Vector2()

        # отрисовка должна происходить ВСЕГДА, а не только когда нет тряски
        ground_sprites = [sprite for sprite in self if getattr(sprite, 'ground', False)]
        object_sprites = [sprite for sprite in self if not getattr(sprite, 'ground', False)]
        object_sprites.sort(key=lambda sprite: sprite.rect.centery)
        for sprite in ground_sprites + object_sprites:
            pos = sprite.rect.topleft + self.offset + self.shake_offset
            self.display_surface.blit(sprite.image, pos)

            if hasattr(sprite, 'draw_health'):
                sprite.draw_health(self.display_surface, self.offset + self.shake_offset)  # hp
                