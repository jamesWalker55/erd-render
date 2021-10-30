from helpers import quick_entity, print_attr, parse_attributes
from obj import Relation, COUNT

employee = quick_entity(
    "Employee",
    [
        "Name: Fname Lname",
        "Address",
        "*NINumber",
        "Salary",
        "Sex",
        "Birthdate",
    ],
)
department = quick_entity(
    "Department",
    [
        "*Name",
        "*Number",
        "Locations[]",
    ],
)
project = quick_entity(
    "Project",
    [
        "*Name",
        "*Number",
        "Location",
    ],
)
dependent = quick_entity(
    "Dependent",
    [
        "+Name",
        "Sex",
        "Birthdate",
        "Relationship",
    ],
)
entities = [employee, department, project, dependent]

relations = [
    Relation(
        (employee, COUNT.ANY, "Supervisee"),
        (employee, COUNT.ZERO_OR_ONE, "Supervisor"),
        name="Supervises",
    ),
    Relation(
        (dependent, COUNT.ANY),
        (employee, 1),
        name="Dependents-Of",
        is_identifying=True,
    ),
    Relation(
        (employee, COUNT.AT_LEAST_ONE),
        (project, COUNT.AT_LEAST_ONE),
        name="Works-On",
        attributes=parse_attributes(["Hours"]),
    ),
    Relation(
        (project, COUNT.ANY),
        (department, COUNT.ZERO_OR_ONE),
        name="Controls",
    ),
    Relation(
        (employee, 1),
        (department, COUNT.ZERO_OR_ONE),
        name="Manages",
    ),
    Relation(
        (employee, COUNT.AT_LEAST_ONE),
        (department, 1),
        name="Works-For",
    ),
]

if __name__ == "__main__":
    for ent in entities:
        print(ent)
        if ent.is_weak():
            print(f"{ent.name} is fucking weak")
        for attr in ent.attrs:
            print_attr(attr, indent=2)
        print()

    for rel in relations:
        print(rel)
