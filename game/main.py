from settings import *
from sprites import * 
from support import folder_importer
from groups import *
from pytmx.util_pygame import load_pygame
class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()
        self.running = True 
        self.all_sprites = All_sprites()
        self.player_frames = self.load_player_frames()
        # сначала строим карту, потом игрока (нужна точка спавна и коллизии)
        spawn = self.setup_map('my_map.tmx')
        self.player = Player(
            self.all_sprites,
            spawn,
            self.player_frames,
            self.collision_rects,
            self.map_bounds,
        )
        # анимированные монстры на карте (класс Animated_sprite)
        self.monster_frames = self.load_monster_frames()
        monster_positions = [(1150, 950), (1420, 1180), (1550, 1000)]
        for pos in monster_positions:
            Animated_sprite(self.all_sprites, pos, self.monster_frames)

    def setup_map(self, map_name):
        tmx = load_pygame(data('maps', map_name), pixelalpha=True)

        # земля: либо слой тайлов (склеиваем в одну картинку), либо image-слой
        map_w = tmx.width * tmx.tilewidth
        map_h = tmx.height * tmx.tileheight
        for layer in tmx.layers:
            if hasattr(layer, 'tiles'):  # тайловый слой
                ground_srf = pygame.Surface((map_w, map_h), pygame.SRCALPHA)
                for x, y, image in layer.tiles():
                    if image is not None:
                        ground_srf.blit(image, (x * tmx.tilewidth, y * tmx.tileheight))
                Sprite(self.all_sprites, (0, 0), ground_srf, ground=True)
            elif getattr(layer, 'image', None) is not None:  # image-слой (готовая земля)
                Sprite(self.all_sprites, (0, 0), layer.image, ground=True)

        # слой Objects - деревья, камни и т.п. (рисуются с y-сортировкой)
        for obj in tmx.get_layer_by_name('Objects'):
            image = tmx.get_tile_image_by_gid(obj.gid)
            if image is not None:
                Sprite(self.all_sprites, (obj.x, obj.y), image)

        # слой Collisions - прямоугольники, через которые нельзя пройти
        self.collision_rects = [
            pygame.Rect(round(o.x), round(o.y), round(o.width), round(o.height))
            for o in tmx.get_layer_by_name('Collisions')
        ]

        # границы карты, чтобы игрок не вышел за пределы мира
        self.map_bounds = pygame.Rect(0, 0, map_w, map_h)

        # слой Entities - имя 'Player' задаёт точку появления
        spawn = next(o for o in tmx.get_layer_by_name('Entities') if o.name == 'Player')
        return pygame.Vector2(spawn.x, spawn.y)
        
    def load_player_frames(self):
        directions = [
            'down', 'left_down', 'left', 'left_up',
            'up', 'right_up', 'right', 'right_down',
        ]
        player_frames = {}
        for direction in directions:
            folder = folder_importer(asset('images', 'player', direction))
            names = sorted(folder, key=lambda name: int(name))
            frames = []
            for name in names:
                surf = folder[name]
                frames.append(pygame.transform.scale(
                    surf,
                    (surf.get_width() * 3, surf.get_height() * 3),
                ))
            player_frames[direction] = frames
        return player_frames

    def load_monster_frames(self):
        # кадры монстра лежат в одной папке: 0.png, 1.png, ...
        folder = folder_importer(asset('images', 'enemies', 'normal'))
        frames = {}
        for name, surf in folder.items():
            frames[name] = pygame.transform.scale(
                surf,
                (surf.get_width() * 2, surf.get_height() * 2),
            )
        return frames

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.all_sprites.update(dt)
            background = [0,0,0]
            self.display_surface.fill(background)
            # камера должна следовать за игроком, а не за экраном
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        pygame.quit()
if __name__ == '__main__':
    game = Game()
    game.run()
#дз закомитить изменения
