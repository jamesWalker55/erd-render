from enum import Enum, auto
from typing import Union, Sequence


class ATTR(Enum):
    # note, foreign keys do not exist in an ER model
    NORMAL = auto()
    KEY_ATTRIBUTE = auto()
    # weak key attributes are for weak entities
    # they have no key attribute, so you pick an attribute in the model as a weak key
    WEAK_KEY_ATTRIBUTE = auto()
    MULTIVALUE = auto()
    DERIVED = auto()


class COUNT(Enum):
    AT_LEAST_ONE = auto()  # 1..*
    ZERO_OR_ONE = auto()  # 0..1
    ANY = auto()  # 0..*


class Attribute:
    """represents an attribute, only instantiated internally"""

    def __init__(
        self, name: str, type: ATTR = ATTR.NORMAL, components: "list[Attribute]" = None
    ):
        if components is None:
            components = []

        self.name = name
        self.type = type
        self.subattrs = components

    def __repr__(self) -> str:
        return f"""Attribute({self.name.__repr__()}, {self.type}, {self.subattrs})"""

    def is_composite(self):
        return len(self.subattrs) != 0


class Entity:
    """represents an entity, can be strong or weak"""

    def __init__(self, name: str, attributes: list[Attribute] = None) -> None:
        if attributes is None:
            attributes = []
        self.name = name
        self.attrs = attributes

    def __repr__(self) -> str:
        return f"""Entity({self.name}, {self.attrs})"""

    def is_weak(self):
        """check if an entity is weak (has no key attributes)"""
        for attr in self.attrs:
            if attr.type == ATTR.KEY_ATTRIBUTE:
                return False
        else:  # no break
            return True


class EntityInfo:
    """
    IMPORTANT: `count` refers to **"how many of this thing the other entities have"**

    e.g. people have many pens; each pen is owned by 1 person;
    (person, 1),
    (pen, COUNT.HAS_MANY),

    e.g.
    1. doctor with a patient can have **many** treatments;
    2. doctor with a treatment can have **many** patients;
    3. patient with a treatment can be from **one** doctor;
    (patient, COUNT.MANY)
    (treatment, COUNT.MANY)
    (doctor, 1),
    """

    def __init__(
        self, entity: Entity, count: Union[COUNT, int, None] = None, role: str = None
    ):
        self.entity = entity
        self.count = count
        self.role = role

    def __repr__(self):
        return f"""<{self.entity.name}{'' if self.role is None else f' AS {self.role}'} * {self.count}>"""


class Relation:
    def __init__(
        self,
        *entities: Union[Entity, EntityInfo, Sequence],
        name: Union[str, None] = None,
        is_identifying: bool = False,
        attributes: list[Attribute] = None,
    ):
        """create a relation between 2 entities

        :param entities: the entities that this relation connects to. you can provide a count and role for each entity
        by using a tuple
        :param name: the name of the relation
        :param is_identifying: whether this relation is used to identify a weak entity type
        :param attributes: attributes of this relation
        """
        if attributes is None:
            attributes = []

        if len(entities) < 2:
            raise ValueError("There must be at least 2 entities involved in a relation")

        self.entity_infos = [self.parse_entity(x) for x in entities]
        self.name = name
        self.is_identifying = is_identifying
        self.attrs = attributes

        self.raise_for_count()

    def __repr__(self) -> str:
        entities = ", ".join(str(entity_info) for entity_info in self.entity_infos)
        name = self.name
        is_identifying = self.is_identifying
        attrs = self.attrs
        return f"Relation({entities}, {name=}, {is_identifying=}, {attrs=})"

    @staticmethod
    def parse_entity(arg: Union[Entity, EntityInfo, Sequence]):
        """Given an ambiguous "entity" argument, try to convert the input into a `EntityInfo` object"""
        if isinstance(arg, Entity):
            return EntityInfo(arg)
        elif isinstance(arg, EntityInfo):
            return arg
        elif isinstance(arg, Sequence):
            if not isinstance(arg[0], Entity):
                raise ValueError(f"First entry must be an Entity: {arg}")
            if len(arg) == 2:
                # 2nd argument must be count
                # role cannot exist without count
                return EntityInfo(arg[0], count=arg[1])
            elif len(arg) == 3:
                # must be in this order: entity, count, role
                return EntityInfo(arg[0], count=arg[1], role=arg[2])
            else:
                raise ValueError(f"Invalid sequence length: {arg}")
        else:
            raise ValueError(f"Unknown entity specification: {arg}")

    def raise_for_count(self):
        """check if all entities have / don't have a count, raise error if not"""
        has_cardinality = self.has_cardinality()
        for entity_count in self.entity_infos:
            if (has_cardinality and entity_count.count is None) or (
                not has_cardinality and entity_count.count is not None
            ):
                msg = "Entity count must be provided for either all entities or no entities"
                raise ValueError(msg)

    def has_cardinality(self):
        return self.entity_infos[0].count is not None
