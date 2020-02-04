import random
import numpy as np


class Engine:
    """Base physics engine, outlines simple tick and entity management methods"""

    def __init__(self, entities=[]):
        """Register initial list of entities"""
        self.entities = {}
        for entity in entities:
            self.add(entity)

    def tick(self):
        """Execute single gym tick"""
        # main entity loop
        for entity in self.entities.values():
            # update entity physics
            entity.update()

    def add(self, entity):
        """Add an entity to for the engine to track"""
        self.entities[id(entity)] = entity

    def remove(self, eid):
        """Remove an entity from the engine"""
        self.entities.pop(eid)

    def entity_arrays(self):
        return {eid: entity.to_array() for eid, entity in self.entities.items()}
