import vector
from vector import VectorObject2D
from helper_methods import normalize


class RigidBody:
    ZERO = vector.obj(x=0, y=0)
    pos = ZERO
    velocity = ZERO
    mass = 1
    top_speed = 10
    net_force = ZERO

    min_speed = 0.1
    max_force = 1
    drag = 0.1

    def add_force(self, force: VectorObject2D):
        self.net_force = self.net_force + force

    def apply_forces(self):
        acc = self.net_force.scale(self.mass)
        self.velocity = self.velocity.add(acc)
        if abs(self.velocity) > self.top_speed:
            self.velocity = normalize(self.velocity).scale(self.top_speed)
        self.pos = self.pos.add(self.velocity)
        self.net_force = self.ZERO

    def get_gravity_force(self, target):
        diff = target - self.pos
        dist = abs(diff)
        G = 30
        force_mag = G * self.mass / (dist * dist)
        force = normalize(diff).scale(force_mag)
        if abs(force) < self.min_speed:
            force = normalize(force).scale(self.min_speed)
        return force

    def get_drag_force(self):
        return self.velocity.scale(-self.drag)
