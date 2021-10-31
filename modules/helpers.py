import re
from typing import Sequence

from modules.obj import Entity, Attribute, ATTR

_ATTR_TYPE_REGEX = re.compile(r"\s*([*+~]*)\s*(.+?)\s*(\[\s*\])?\s*")


def _split_attribute_type(name: str) -> tuple[str, ATTR]:
    """Given an attribute string (without subcomponents), determine then return the attribute name and type"""
    match = _ATTR_TYPE_REGEX.fullmatch(name)
    prefix, name, postfix = match.groups()

    if "*" in prefix:
        return name, ATTR.KEY_ATTRIBUTE
    elif "+" in prefix:
        return name, ATTR.WEAK_KEY_ATTRIBUTE
    elif postfix is not None:
        return name, ATTR.MULTIVALUE
    elif "~" in prefix:
        return name, ATTR.DERIVED
    else:
        return name, ATTR.NORMAL


def parse_attribute(definition: str):
    """Parse a string to an `Attribute`. Supported string formats:

    - `*name`: key attribute
    - `+name`: weak key attribute
    - `~name`: derived attribute
    - `name[]`: multi-value attribute
    - `name: a b c`: composite key with subattributes

    ```
    Attribute.parse("name: first_name last_name")
    Attribute.parse("*id")
    Attribute.parse("+staff_id")
    Attribute.parse("~age")
    Attribute.parse("addresses[]")
    ```

    :param definition: a string to parse
    :return: an Attribute
    """
    name = definition
    subattrs = None

    # check if it has subattributes
    if ":" in name:
        # this will error if there are multiple ":"'s in the name
        name, subattrs = name.split(":")
        name = name.strip()
        # split attributes by space then parse each string
        subattrs = subattrs.split()
        subattrs = [parse_attribute(x) for x in subattrs]

    # check if it starts with * or +
    name, type = _split_attribute_type(name)

    return Attribute(name, type=type, components=subattrs)


def parse_attributes(definitions: Sequence[str]):
    """Parse a list of strings to `Attributes`, see documentation for `parse_attribute`"""
    return [parse_attribute(d) for d in definitions]


def quick_entity(name: str, attrs: Sequence[str]):
    """Create an entity from a string name and a string list of attributes"""
    return Entity(name, attributes=parse_attributes(attrs))


def print_attr(attr: Attribute, indent: int = 0):
    print(
        f"{indent * ' '}{attr.name}: {attr.type} {'[composite]' if attr.is_composite() else ''}"
    )
    for sub in attr.subattrs:
        print_attr(sub, indent + 2)
