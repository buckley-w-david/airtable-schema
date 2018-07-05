import json
import typing


class TypeOptions:
    def __init__(self, obj) -> None:
        self.obj = obj

    def __eq__(self, other) -> bool:
        return isinstance(other, TypeOptions) and self.obj == other.obj

    def __repr__(self) -> str:
        return f"TypeOptions(obj={repr(self.obj)})"

    def to_dict(self) -> typing.Dict:
        return {"obj": self.obj}

    @staticmethod
    def from_dict(options) -> "TypeOptions":
        return TypeOptions(options.get('obj'))

    @staticmethod
    def from_obj(obj) -> "TypeOptions":
        return TypeOptions(obj)


class Aircolumn:
    def __init__(self, id, name, type, type_options) -> None:
        self.id = id
        self.name = name
        self.type = type
        self.type_options = type_options

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Aircolumn)
            and self.id == other.id
            and self.name == other.name
            and self.type == other.type
            and self.type_options == other.type_options
        )

    def __repr__(self) -> str:
        return f"Aircolumn(id={repr(self.id)}, name={repr(self.name)}, type={repr(self.type)}, type_options={repr(self.type_options)})"

    def to_dict(self) -> typing.Dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "type_options": self.type_options.to_dict(),
        }

    @staticmethod
    def from_dict(column: typing.Dict) -> "Aircolumn":
        type_options = TypeOptions.from_dict(column.get("type_options"))
        column["type_options"] = type_options
        return Aircolumn(**column)

    @staticmethod
    def from_schema(column: typing.Dict) -> "Aircolumn":
        return Aircolumn(
            id=column.get("id"),
            name=column.get("name"),
            type=column.get("type"),
            type_options=TypeOptions.from_obj(column.get("typeOptions")),
        )


class Airtable:
    def __init__(self, id, name, columns, primary_column_name) -> None:
        self.id = id
        self.name = name
        self.columns = columns
        self.primary_column_name = primary_column_name

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Airtable)
            and self.id == other.id
            and self.name == other.name
            and self.columns == other.columns
            and self.primary_column_name == other.primary_column_name
        )

    def __repr__(self) -> str:
        return f"Airtable(id={repr(self.id)}, name={repr(self.name)}, columns={repr(self.columns)}, primary_column_name={repr(self.primary_column_name)})"

    def to_dict(self) -> typing.Dict:
        return {
            "id": self.id,
            "name": self.name,
            "columns": [column.to_dict() for column in self.columns],
            "primary_column_name": self.primary_column_name,
        }

    @staticmethod
    def from_dict(schema: typing.Dict) -> "Airtable":
        columns = [Aircolumn.from_dict(column) for column in schema.get("columns")]
        schema["columns"] = columns
        return Airtable(**schema)

    @staticmethod
    def from_schema(schema: typing.Dict) -> "Airtable":
        return Airtable(
            id=schema.get("id"),
            name=schema.get("name"),
            columns=[Aircolumn.from_schema(column) for column in schema.get("columns")],
            primary_column_name=schema.get("primaryColumnName"),
        )


class AirtableSchema:
    def __init__(self, tables) -> None:
        self.tables = tables

    def __eq__(self, other) -> bool:
        return isinstance(other, AirtableSchema) and self.tables == other.tables

    def __repr__(self) -> str:
        return f"AirtableSchema(tables={repr(self.tables)})"

    def to_dict(self) -> typing.Dict:
        return {"tables": [table.to_dict() for table in self.tables]}

    @staticmethod
    def from_schema(schema_dict: typing.Dict) -> "AirtableSchema":
        return AirtableSchema(
            tables=[Airtable.from_schema(table) for table in schema_dict.values()]
        )

    @staticmethod
    def from_dict(schema: typing.Dict):
        tables = [Airtable.from_dict(d) for d in schema.get("tables")]
        schema["tables"] = tables

        return AirtableSchema(**schema)

    @staticmethod
    def from_str(schema_str: str) -> "AirtableSchema":
        schema = json.loads(schema_str)
        return AirtableSchema.from_schema(schema)
