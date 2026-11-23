"""Optional inputs use their public row/serialization interfaces."""

from datetime import date

import pytest

from tabulate import SEPARATING_LINE, tabulate


@pytest.fixture
def polars():
    return pytest.importorskip("polars")


@pytest.mark.parametrize("headers", [(), "keys", "firstrow", ["Label", "Quantity"]])
@pytest.mark.parametrize("showindex", ["default", "always", "never", ["a", "b", "c"]])
def test_polars_rows_headers_and_index(polars, headers, showindex):
    frame = polars.DataFrame({"name": ["one", "two", "three"], "quantity": [1.5, None, 3.0]})
    expected_headers = frame.columns if headers == "keys" else headers
    options = {"floatfmt": ".2f", "missingval": "?", "showindex": showindex, "tablefmt": "grid"}
    # firstrow removes a row before an explicit index is applied.
    if headers == "firstrow" and isinstance(showindex, list):
        options["showindex"] = showindex[1:]
    assert tabulate(frame, headers=headers, **options) == tabulate(
        frame.rows(), headers=expected_headers, **options
    )
    assert frame.columns == ["name", "quantity"]
    assert frame.shape == (3, 2)


def test_polars_empty_schema_and_dates(polars):
    empty = polars.DataFrame(schema={"name": polars.String, "count": polars.Int64})
    assert tabulate(empty, headers="keys") == tabulate([], headers=["name", "count"])
    assert tabulate(polars.DataFrame(), headers="keys") == ""
    frame = polars.DataFrame({"date": [date(2024, 1, 1)], "name": ["雪"]})
    assert tabulate(frame, headers="keys") == tabulate(frame.rows(), headers=frame.columns)


@pytest.fixture(params=["pydantic", "pydantic.v1"])
def pydantic(request):
    return pytest.importorskip(request.param)


def test_pydantic_serialization_and_header_mapping(pydantic):
    class Row(pydantic.BaseModel):
        name: str
        value: float | None = None
        password: str = pydantic.Field(default="private", exclude=True)

    rows = [Row(name="one", value=1.25), Row(name="two")]
    expected = [{"name": "one", "value": 1.25}, {"name": "two", "value": None}]
    for headers in [(), "keys", "firstrow", {"name": "Label", "value": "Amount"}]:
        assert tabulate(iter(rows), headers=headers, floatfmt=".1f", showindex=True) == tabulate(
            expected, headers=headers, floatfmt=".1f", showindex=True
        )
    assert rows[0].password == "private"


def test_pydantic_nested_models_separators_and_mixed_fields(pydantic):
    class Address(pydantic.BaseModel):
        city: str

    class User(pydantic.BaseModel):
        name: str
        address: Address

    class Total(pydantic.BaseModel):
        count: int

    rows = [User(name="one", address=Address(city="Paris")), SEPARATING_LINE, Total(count=1)]
    expected = [{"name": "one", "address": {"city": "Paris"}}, SEPARATING_LINE, {"count": 1}]
    # The dictionary adapter needs separators left in place while discovering keys.
    assert tabulate(rows, headers="keys", tablefmt="grid") == tabulate(
        expected, headers="keys", tablefmt="grid"
    )


def test_pydantic_v2_serializer_computed_and_root():
    pydantic = pytest.importorskip("pydantic")
    if not hasattr(pydantic, "RootModel"):
        pytest.skip("Pydantic 2 serializer and root-model API")

    class Row(pydantic.BaseModel):
        amount: int

        @pydantic.field_serializer("amount")
        def format_amount(self, value):
            return f"{value} units"

        @pydantic.computed_field
        @property
        def double(self) -> int:
            return self.amount * 2

    assert tabulate([Row(amount=3)], headers="keys") == tabulate(
        [{"amount": "3 units", "double": 6}], headers="keys"
    )
    root = pydantic.RootModel[list[int]]([1, 2])
    assert tabulate([root], headers="keys") == tabulate([{"root": [1, 2]}], headers="keys")

    class Scalar(pydantic.BaseModel):
        @pydantic.model_serializer
        def serialize(self):
            return "not a row"

    with pytest.raises(TypeError, match="serialize to a mapping"):
        tabulate([Scalar()], headers="keys")
