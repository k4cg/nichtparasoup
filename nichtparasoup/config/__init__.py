from os.path import dirname, join as path_join
from typing import Any

_schema_file = path_join(dirname(__file__), "schema.yaml")


def validate_yaml_file(file_path: str) -> bool:
    import yamale
    schema = yamale.make_schema(_schema_file)
    data = yamale.make_data(file_path)
    return yamale.validate(schema, data) is not None  # throws all the errors


def parse_yaml_file(file_path: str) -> Any:
    from ruamel.yaml import safe_load as yaml_import   # type: ignore
    return yaml_import(open(file_path, "r"))

