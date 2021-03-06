from .enums import Type, Zone, Race

class Void:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

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
