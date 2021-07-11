from enums import Event, General, Zone, State, Type

class Void:
    def __init__(self) -> None:
        self.temp_list = []

    @property
    def general(self):
        return General.ZONE

    @property
    def zone(self):
        return Zone.NONE

    @property
    def event(self):
        return Event.NONE

    @property
    def state(self):
        return State.NONE

    @property
    def type(self):
        return Type.NONE
    synergy = type

    def __getattr__(self, attr):
        return None

    def remove(self, *args, **kwargs):
        pass
    #append = remove

    def append(self, entity):
        self.temp_list.append(entity)

    @property
    def owner(self):
        return self