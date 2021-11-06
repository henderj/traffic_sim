from interfaces.interfaces import DrawableInterface, TickableInterface, PoolInterface
from random import randint
import pygame
from pygame import Vector2
import pytweening as tween
from helper_methods import normalize


class Orb(DrawableInterface, TickableInterface):
    COLOR = (255, 255, 255)
    TARGET_COLOR = (50, 168, 82)
    V_ZERO = Vector2(0, 0)

    starting_pos = Vector2(x=0, y=0)
    pos: Vector2 = Vector2(x=0, y=0)
    size = Vector2(x=10, y=10)
    target = Vector2(x=200, y=200)
    progress = 0
    speed = 2

    max_acc = 0.1
    max_velocity = 3
    velocity = V_ZERO

    target_threshold = 5
    slow_down_point = 20

    pool: PoolInterface

    def init(self, pos: Vector2, size: int, pool: PoolInterface):
        self.starting_pos = pos
        self.pos = self.starting_pos
        self.progress = 0
        self.size = Vector2(x=size, y=size)
        self.pool = pool
        self.velocity: Vector2 = Vector2(x=0, y=0)

    def set_target(self, target: Vector2 = None):
        if target is None:
            target = Vector2(x=randint(0, 700), y=randint(0, 500))
        self.target = target

    def is_at_target(self) -> bool:
        return self.dist_to_target() < self.target_threshold

    def dist_to_target(self) -> float:
        # return abs(self.target - self.pos)
        return Vector2(self.target - self.pos).magnitude()

    def dir_to_target(self) -> Vector2:
        return Vector2(self.target - self.pos).normalize()

    def tick(self, dt: int):
        # self.progress += dt / 1000.0
        if self.is_at_target():
            self.pool.despawn(self)
            return None

        # acc = self.dir_to_target() * self.max_acc
        # if abs(self.velocity) < self.max_velocity:
        #     acc = self.max_acc
        # if self.dist_to_target() < self.slow_down_point:
        #     perc = 1 - (self.dist_to_target() / self.slow_down_point)
        #     acc = self.velocity * -0.1
        # self.velocity = self.velocity + acc
        # if self.velocity.magnitude() > self.max_velocity:
        #     self.velocity = self.velocity.normalize() * self.max_velocity
        # self.pos = self.pos + self.velocity

        target_dir = self.target - self.pos
        interp_veloctiy = target_dir.magnitude() * 5
        target_pos = self.pos + (target_dir.normalize() * interp_veloctiy * (dt / 1000))
        self.pos = self.pos.lerp(target_pos, 0.25)

        #  interpVelocity = targetDirection.magnitude * 5f;

        #  targetPos = transform.position + (targetDirection.normalized * interpVelocity * Time.deltaTime);

        #  transform.position = Vector3.Lerp( transform.position, targetPos + offset, 0.25f);
        # tweened_progress = tween.easeInOutSine(self.progress / self.speed)
        # diff = self.target - self.starting_pos
        # self.pos = diff.scale(tweened_progress) + self.starting_pos

    def draw(self, screen: pygame.Surface):
        self.draw_circle(self.pos, self.size, self.COLOR, screen)
        self.draw_circle(self.target, self.size * 0.5, self.TARGET_COLOR, screen)

    def draw_circle(self, pos: Vector2, size: Vector2, color, screen):
        draw_pos = pos - (size / 2)
        pygame.draw.ellipse(screen, color, [draw_pos.x, draw_pos.y, size.x, size.y])
