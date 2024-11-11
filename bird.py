# 이것은 각 상태들을 객체로 구현한 것임.

import random
from pico2d import get_time, load_image
from state_machine import *
import game_world
import game_framework

PIXEL_PER_METER = (1.0 / 0.1)
RUN_SPEED_KMPH = 100.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

FRAMES_PER_ACTION = 14
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

class Run:
    @staticmethod
    def enter(bird, e):
        bird.dir = 1
        bird.action = 2
        bird.frame = random.randint(0, 4)
        bird.temp = 0
        bird.face_dir = random.randint(0, 1)

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        if not bird.action == 0:
            bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
            bird.temp = bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
            if bird.temp > 4:
                bird.frame = 0.0
                bird.temp = 0.0
                bird.action -= 1
        elif bird.action == 0:
            bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
            bird.temp = bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
            if bird.temp > 3:
                bird.frame = 0.0
                bird.temp = 0.0
                bird.action = 2
        if bird.face_dir == 0:
            bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time
            if bird.x > 1600:
                bird.face_dir = 1
        elif bird.face_dir == 1:
            bird.x -= bird.dir * RUN_SPEED_PPS * game_framework.frame_time
            if bird.x < 0:
                bird.face_dir = 0

    @staticmethod
    def draw(bird):
        if bird.face_dir == 0:
            bird.image.clip_draw(int(bird.frame) * 182, bird.action * 168, 182, 168, bird.x, bird.y)
        elif bird.face_dir == 1:
            bird.image.clip_composite_draw(int(bird.frame) * 182, bird.action * 168, 182, 168, 0, 'h', bird.x, bird.y, 182, 168)

class Bird:
    def __init__(self):
        self.x, self.y = random.randint(400, 1200), random.randint(100, 500)
        self.face_dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Run)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()