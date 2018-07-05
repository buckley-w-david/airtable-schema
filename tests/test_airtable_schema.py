import os.path
import pytest

from airtable_schema import __version__
from airtable_schema import schema


def test_version():
    assert __version__ == "0.1.0"


@pytest.fixture
def airtable_schema_str() -> str:
    with open(os.path.join(os.path.dirname(__file__), "example.schema"), "r") as file:
        return file.read()


@pytest.fixture
def airtable_schema(airtable_schema_str: str) -> schema.AirtableSchema:
    return schema.AirtableSchema.from_str(airtable_schema_str)


def test_parse_schema_str(airtable_schema_str: str) -> None:
    result = schema.AirtableSchema.from_str(airtable_schema_str)
    assert len(result.tables) == 2
    table = result.tables[0]
    assert table.id == "tblarQuh3cAiHvwX9"
    assert len(table.columns) == 3
    column = table.columns[0]
    assert column.id == "fld4iwaQPKPHEc2FB"


def test_serialization_preserves_data(airtable_schema: schema.AirtableSchema) -> None:
    assert schema.AirtableSchema.from_dict(airtable_schema.to_dict()) == airtable_schema
