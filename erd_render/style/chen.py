from typing import Sequence, Union

from erd_render.modules.obj import Entity, Relation, COUNT, Attribute, ATTR
from erd_render.modules.render import ObjGraph


def render(
    entities: Sequence[Entity],
    relations: Sequence[Relation],
    filename=None,
    format="pdf",
    k=0.4,
    repulsive_force=4,
    overlap_scaling=-4,
    use_neato=False,
):
    """
    render the given Entities and Relations to an ER diagram using Chan's notation, defaults to using the `sfdp` engine

    :param entities: a list of Entities. all entities that are part of a relation must appear here
    :param relations: a list of Relations
    :param filename: the path to output the generated graphviz source and diagram
    :param format: the output format, like "png" or "pdf"
    :param k: spring constant for node placement: https://graphviz.org/docs/attrs/K/
    :param repulsive_force: the repulsive force for node placement: https://graphviz.org/docs/attrs/repulsiveforce/
    :param use_neato: use `neato` as the node placement engine instead of `sfdp`, this disables the parameters `k`
           and `repulsive_force`
    """
    if use_neato:
        g = ObjGraph(
            "graph",
            engine="neato",
            graph_attr=(("overlap", "false"),),
        )
    else:
        g = ObjGraph(
            "graph",
            engine="sfdp",
            graph_attr=(
                ("overlap_scaling", str(overlap_scaling)),
                ("K", str(k)),
                ("repulsiveforce", str(repulsive_force)),
            ),  # space out elements a bit
        )
    id_map = {}

    # create the entities
    g.node_style(shape="box")
    for entity in entities:
        assert entity not in id_map
        draw_entity(g, id_map, entity)

    # create the relations
    g.node_style(shape="diamond")
    for rel in relations:
        assert rel not in id_map
        draw_relation(g, id_map, rel)

    # draw attributes
    attr_holders: Sequence[Union[Entity, Relation]] = [*entities, *relations]
    g.node_style(shape="oval")
    for obj in attr_holders:
        for attr in obj.attrs:
            draw_attribute(g, id_map, id_map[obj], attr)

    g.render(filename=filename, format=format)


def draw_attribute(
    graph: ObjGraph,
    id_map: dict[Union[Entity, Relation], str],
    parent_id: str,
    attr: Attribute,
):
    label = attr.name
    kwargs = {}
    if attr.type == ATTR.KEY_ATTRIBUTE:
        # add a underline to the label
        label = f"<<U>{label}</U>>"
    elif attr.type == ATTR.WEAK_KEY_ATTRIBUTE:
        # there is no dotted underline in graphviz
        # we can only underline every other letter
        is_even = True
        label_parts = []
        for letter in label:
            if is_even:
                label_parts.append(f"<U>{letter}</U>")
            else:
                label_parts.append(letter)
            is_even = not is_even
        label = "".join(label_parts)
        label = f"<{label}>"
    elif attr.type == ATTR.DERIVED:
        kwargs["style"] = "dashed"
    elif attr.type == ATTR.MULTIVALUE:
        kwargs["peripheries"] = "2"

    a_id = graph.node(label, **kwargs)
    graph.edge(a_id, parent_id)
    id_map[attr] = a_id

    for subattr in attr.subattrs:
        draw_attribute(graph, id_map, a_id, subattr)


def prev_letter(letter: str):
    # uppercase: 65..90
    # lowercase: 97..122
    code = ord(letter)
    lower_bound = 65 if 65 <= code <= 90 else 97
    # increment code by 1, wrapping to lower_bound if it exceeds 26
    code = (code - 1 - lower_bound) % 26 + lower_bound
    return chr(code)


def draw_relation(
    graph: ObjGraph, id_map: dict[Union[Entity, Relation], str], rel: Relation
):
    # always draw a diamond no matter what
    if rel.is_identifying:
        rid = graph.node(rel.name, peripheries="2")
    else:
        rid = graph.node(rel.name)

    # guess total participation
    total_parti_map = guess_total_participation(rel)

    # draw the connecting lines
    many_letter = "N"
    for e_info in rel.entity_infos:
        # get count of this entity
        if isinstance(e_info.count, COUNT):
            if e_info.count in (COUNT.ANY, COUNT.AT_LEAST_ONE):
                count = many_letter
                many_letter = prev_letter(many_letter)
            elif e_info.count == COUNT.ZERO_OR_ONE:
                count = "1"
            else:
                raise NotImplementedError("Unknown COUNT value")
        elif e_info.count is None:
            count = None
        else:
            count = str(e_info.count)

        # get role of this entity
        role = e_info.role
        # if total participation, then draw a double line
        color = "black:invis:black" if total_parti_map[e_info] else None

        eid = id_map[e_info.entity]
        graph.edge(
            eid,
            rid,
            headlabel=count,
            labeldistance="1.5",
            label=role,
            color=color,
        )

    id_map[rel] = rid


def guess_total_participation(rel):
    # guess which entity types require total participation
    total_parti_map = dict((x, True) for x in rel.entity_infos)
    for e_info in rel.entity_infos:
        # if this entity count's min value is 0,
        # then all other entities will be single lines (i.e. total participation = False)
        if e_info.count not in (None, 0, COUNT.ZERO_OR_ONE, COUNT.ANY):
            continue

        for x in total_parti_map:
            if x == e_info:
                continue
            total_parti_map[x] = False
    return total_parti_map


def draw_entity(
    graph: ObjGraph, id_map: dict[Union[Entity, Relation], str], entity: Entity
):
    if entity.is_weak():
        # draw double boxes
        id_map[entity] = graph.node(entity.name, peripheries="2")
    else:
        id_map[entity] = graph.node(entity.name)
