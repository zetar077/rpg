import json 
from settings import *
def load_json(path):
    with open(path,"r",encoding = "utf-8") as file:
        return json.load(file)
class Timer:
    def __init__(self, duration, repeat=False, autostart=False, func=None):
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.repeat = repeat
        self.func = func
        if autostart:
            self.activate()

    def __bool__(self):
        return self.active

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()

    def update(self):
        if not self.active:
            return
        passed = pygame.time.get_ticks() - self.start_time
        if passed >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()
def folder_importer(*path):
    surfs = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            if file_name.startswith('.'):
                continue
            full_path = join(folder_path, file_name)
            key = file_name.split('.')[0]
            surfs[key] = pygame.image.load(full_path).convert_alpha()
    return surfs