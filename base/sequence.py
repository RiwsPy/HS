from .utils import Card_list
from .enums import Type


class Sequence:
    """
        _START (myself)
        _ON (all except myself)
        Effects (myself)
        _OFF (all except myself)
        _END (myself)
    """
    TURN_ON = 'turn_on'

    def __init__(self, name: str, source, **kwargs):
        self.name = name
        self.phase_name = name
        self.source = source
        self.is_valid = True
        self.target = None
        self._repops = Card_list()

        for kv in kwargs.items():
            setattr(self, *kv)

        self._methods = []
        self._args = []
        self._kwargs = []

    def add_target(self, target):
        # TODO: rename to set_target ?
        if self.target:
            print('target is not None:', self.target)
        self.target = target

    @property
    def method_name(self) -> str:
        return getattr(self.__class__, self.phase_name, self.phase_name.lower())

    def purge_methods(self):
        self._methods = []
        self._args = []
        self._kwargs = []

    def start_and_close(self) -> None:
        self.__enter__()
        self.__exit__()

    def phase_range(self) -> list:
        # TODO: Can be simplest
        end_param = self.phase_name.rpartition('_')[-1]
        if end_param in ('START', 'END'):
            return self.source
        elif self.name in ('TURN', 'FIGHT'):
            return self.source.game
        elif self.source.controller is self.source:
            return self.source
        else:  # sometimes, self.source doesn't have a controller
            return self.source.controller.field

    def __call__(self, method, *args, **kwargs):
        self._methods.append(method)
        self._args.append(args)
        self._kwargs.append(kwargs)

    def execute_effect(self) -> None:
        for met, args, kwargs in zip(self._methods, self._args, self._kwargs):
            if not self.is_valid:
                break
            met(*args, **kwargs)
        self.purge_methods()

    def copy_and_add_last_method(self) -> None:
        if self._methods:
            self._methods.append(self._methods[-1])
            self._args.append(self._args[-1])
            self._kwargs.append(self._kwargs[-1])

    def __enter__(self):
        if self.name in ('TURN', 'FIGHT'):
            self.source.game.current_sequence = self.name

        self.active_phase('_START', self.source)
        if self.is_valid:
            self.active_phase('_ON')
            self.execute_effect()
            self.active_phase('', self.source)

        return self
    start = __enter__

    def __exit__(self, *args):
        self.active_phase('_OFF')
        self.execute_effect()
        self.active_phase('_END', self.source)
    close = __exit__

    def active_phase(self, end_name: str, source=None):
        self.phase_name = self.name + end_name
        source = source or self.phase_range()
        getattr(source, self.method_name, source.no_method)(self)
        for entity in self._iter_seq(source):
            method = getattr(entity, self.method_name, None)
            if method:
                method(self)

    def is_ally(self, target) -> bool:
        return self.source.controller is target.controller

    def _iter_seq(self, entity, *args):
        next_entities = Card_list()
        for ent in args or entity.entities:
            if ent.type != Type.ZONE or ent.phase == 'ALL':
                next_entities += ent.entities
            yield ent
        # ON / OFF phase inaccessible pour la source de la séquence
        # sauf si source.valid_for_myself == True
        if self.phase_name.rpartition('_')[-1] in ('ON', 'OFF') and\
                not getattr(self.source, 'valid_for_myself', False):
            next_entities = next_entities.exclude(self.source)
        if next_entities:
            yield from self._iter_seq(entity, *next_entities)
