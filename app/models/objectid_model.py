from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class PyObjectID(ObjectId):
    @classmethod
    def __get_pydantic_core_schema(cls, source_type, handlers: GetCoreSchemaHandler):
        return core_schema.no_info_after_validator_function(
            cls.validate, core_schema.str_schema()
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectID")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema(cls, schema, handlers):
        json_schema = handlers(schema)
        json_schema.update(type="string", examples=["64e4b8f4a0c1a2b3c4d5e6f7"])
        return json_schema
