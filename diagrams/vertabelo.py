from erd_render.modules.helpers import quick_entity
from erd_render.modules.obj import Relation, COUNT
from erd_render.style.chen import render

# https://vertabelo.com/blog/chen-erd-notation/

prod = quick_entity(
    "PRODUCT",
    [
        "NAME",
        "*SKU",
        "PRICE EXCL. VAT",
        "VAT RATE",
        "~PRICE INCL. VAT",
    ],
)

student = quick_entity(
    "STUDENT",
    [
        "*STUDENT ID",
        "LAST NAME",
        "FIRST NAME",
        "~AGE",
        "DATE OF BIRTH",
        "EMAIL[]",
        "MAJOR",
        "ADDRESS: COUNTRY STATE CITY ZIPCODE STREETNAME STREETNO APARTMENTNO",
    ],
)

book = quick_entity(
    "BOOK",
    [
        "*BOOK ID",
        "TITLE",
    ],
)

chapter = quick_entity(
    "CHAPTER",
    [
        "+CHAPTER ID",
        "TITLE",
    ],
)

contains = Relation(
    (book, 1),
    (chapter, COUNT.ANY),
    name="CONTAINS",
    is_identifying=True,
)

if __name__ == "__main__":
    render(
        [prod, student, book, chapter],
        [contains],
        filename="vertabelo.gv",
        use_neato=True
    )
