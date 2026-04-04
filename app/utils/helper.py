def map_to_schema(schema, data):
    return [schema.model_validate(item) for item in data]