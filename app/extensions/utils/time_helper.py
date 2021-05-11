from sqlalchemy import func


def get_utc_timestamp_for_model() -> func:
    return func.timezone("UTC", func.current_timestamp())
