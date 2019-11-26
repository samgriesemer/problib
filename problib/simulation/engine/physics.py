import random
import numpy as np

class Engine():
    '''Base physics engine, outlines simple tick and entity management methods'''
    def __init__(self, entities=[]):
        '''Register initial list of entities'''
        self.entities = {}
        for entity in entities:
            self.add(entity)

    def tick(self):
        '''Execute single gym tick'''
        # main entity loop
        for entity in self.entities.values():
            # update entity physics
            entity.update()

    def add(self, entity):
        '''Add an entity to for the engine to track'''
        self.entities[id(entity)] = entity

    def remove(self, eid):
        '''Remove an entity from the engine'''
        self.entities.pop(eid)

    def entity_arrays(self):
        return {eid: entity.to_array() for eid, entity in self.entities.items()}

class Entity():
    '''
    TODO: consider making this a numpy array based class for efficient updates
    '''
    def __init__(self, px=0, py=0, vx=0, vy=0, ax=0, ay=0):
        # set position
        self.px = px
        self.py = py

        # set velocity
        self.vx = vx
        self.vy = vy

        # set acceleration
        self.ax = ax
        self.ay = ay

    @classmethod
    def random(cls, pxrng, pyrng, vxrng, vyrng, axrng=None, ayrng=None):
        '''
        Constructor overload, return randomly initialized
        point object within the specified position, velocty,
        and acceleration bounds
        '''
        px = random.uniform(*pxrng)
        py = random.uniform(*pyrng)
        vx = random.uniform(*vxrng)
        vy = random.uniform(*vyrng)
        ax = random.uniform(*axrng) if axrng else 0
        ay = random.uniform(*ayrng) if ayrng else 0

        return cls(px, py, vx, vy, ax, ay)

    def to_array(self):
        return np.array(list(self.__dict__.values()))

    def update(self):
        '''Update point physics'''
        # update position
        self.px += self.vx
        self.py += self.vy

        # update velocity
        self.vx += self.ax
        self.vy += self.ay

class Vector():
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
