import os


def get_env(variable_name: str) -> str:
    """Returns a environment variable"""
    try:
        var = os.environ[variable_name]
        if not var:
            raise RuntimeError(f"Variable is null, Check {variable_name}.")
        return var
    except KeyError:
        raise RuntimeError(f"Variable is not set, Check {variable_name}.")


ENV = {
    # Apigee
    "environment": get_env("ENVIRONMENT"),
    "missing_ods_client_id": get_env("INTERNAL_TESTING_WITHOUT_ODS_KEY"),
    "missing_ods_client_secret": get_env("INTERNAL_TESTING_WITHOUT_ODS_SECRET"),
    "missing_asid_client_id": get_env("INTERNAL_TESTING_WITHOUT_ASID_KEY"),
    "missing_asid_client_secret": get_env("INTERNAL_TESTING_WITHOUT_ASID_SECRET")
}
