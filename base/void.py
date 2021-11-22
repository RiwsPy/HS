from .enums import Type, Zone, Race

class Void:
    def __init__(self) -> None:
        self.temp_list = []

    @property
    def type(self) -> int:
        return Type.ZONE

    @property
    def zone(self) -> int:
        return Zone.NONE

    @property
    def race(self) -> int:
        return Race('NONE')
    synergy = race

    def __getattr__(self, attr) -> None:
        return None

    def remove(self, *args, **kwargs) -> None:
        pass
    #append = remove

    def append(self, entity, **kwargs) -> None:
        self.temp_list.append(entity)

    @property
    def owner(self) -> 'Void':
        return self
