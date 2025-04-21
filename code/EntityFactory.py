from code.Enemy import Enemy

class EntityFactory:
    @staticmethod
    def create_enemy():
        return Enemy()
