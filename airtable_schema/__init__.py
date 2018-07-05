import typing

__version__ = "0.1.1"


class AirtableCredentials(typing.NamedTuple):
    username: str
    password: str
