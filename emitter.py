from particle import Particle

class Emitter:
    def __init__(self, color, lifeSpan, initVelMag = 0, frequency = 1) -> None:
        self.particles = []
        self.color = color
        self.lifeSpan = lifeSpan
        self.velMag = initVelMag
        self.frequency = frequency

    def update(self, m = 1):
        for particle in self.particles:
            particle.update(m)
            particle.draw()
            if particle.lifeSpan <= 0:
                self.particles.remove(particle)
    
    def applyForce(self, force):
        for particle in self.particles:
            particle.applyForce(force)
    
    def __call__(self, pos):
        for i in range(self.frequency):
            self.particles.append(Particle(pos, self.velMag, self.lifeSpan, self.color))