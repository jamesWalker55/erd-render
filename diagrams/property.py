from helpers import quick_entity, parse_attributes
from modules.obj import Relation, COUNT
from style.chen import render

staff = quick_entity("Staff", ["*staffNo"])
branch = quick_entity("Branch", ["*branchNo"])
client = quick_entity("Client", ["*clientNo"])
lease = quick_entity("Lease", ["*leaseNo"])
preference = quick_entity("Preference", [])
rent_property = quick_entity("PropertyForRent", ["*propertyNo"])
private_owner = quick_entity("PrivateOwner", ["*ownerNo"])
business_owner = quick_entity("BusinessOwner", ["*bName"])
newspaper = quick_entity("Newspaper", ["*newspaperName"])

entities = [
    staff,
    branch,
    client,
    lease,
    preference,
    rent_property,
    private_owner,
    business_owner,
    newspaper,
]

relations = [
    Relation(
        (staff, COUNT.ZERO_OR_ONE, "Supervisor"),
        (staff, COUNT.ANY, "Supervisee"),
        name="Supervises",
    ),
    Relation(
        (staff, 1),
        (branch, COUNT.ZERO_OR_ONE),
        name="Manages",
        attributes=parse_attributes("mgrStartDate bonus".split()),
    ),
    Relation(
        (branch, 1),
        (staff, COUNT.AT_LEAST_ONE),
        name="Has",
    ),
    Relation(
        (staff, 1),
        (branch, 1),
        (client, COUNT.ANY),
        name="Registers",
        attributes=parse_attributes(["dateJoined"]),
    ),
    Relation(
        (client, 1),
        (preference, 1),
        name="States",
    ),
    Relation(
        (client, 1),
        (lease, COUNT.ANY),
        name="Holds",
    ),
    Relation(
        (lease, COUNT.ANY),
        (rent_property, 1),
        name="LeasedBy",
    ),
    Relation(
        (staff, COUNT.ZERO_OR_ONE),
        (rent_property, COUNT.ANY),
        name="Oversees",
    ),
    Relation(
        (branch, 1),
        (rent_property, COUNT.AT_LEAST_ONE),
        name="Offers",
    ),
    Relation(
        (private_owner, COUNT.ZERO_OR_ONE),
        (rent_property, COUNT.AT_LEAST_ONE),
        name="POwns",
    ),
    Relation(
        (business_owner, COUNT.ZERO_OR_ONE),
        (rent_property, COUNT.AT_LEAST_ONE),
        name="BOwns",
    ),
    Relation(
        (newspaper, COUNT.ANY),
        (rent_property, COUNT.AT_LEAST_ONE),
        name="Advertises",
        attributes=parse_attributes("dateAdvert cost".split()),
    ),
]

if __name__ == "__main__":
    render(entities, relations, filename="property.gv")
