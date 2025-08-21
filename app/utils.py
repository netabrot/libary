

def filters(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}

def changed_fields(payload):
    return payload.model_dump(exclude_unset=True, exclude_none=True)
