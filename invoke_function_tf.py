import logging
import os
import sys

from oci import config
from oci import functions
from oci import identity
from oci import pagination


from oci.identity import models as identityt_models
from oci.functions import models as fn_models


def get_compartment(oci_cfg, compartment_name: str,
                    tenancy_id: str) -> identityt_models.Compartment:
    """
    Identifies compartment ID by its name within the particular tenancy
    :param oci_cfg: OCI auth config
    :param compartment_name: OCI tenancy compartment name
    :param tenancy_id: OCI tenancy ID
    :return: OCI tenancy compartment
    """
    identity_client = identity.IdentityClient(oci_cfg)
    result = pagination.list_call_get_all_results(
        identity_client.list_compartments,
        tenancy_id,
        compartment_id_in_subtree=True,
        access_level="ACCESSIBLE",
    )
    for c in result.data:
        if compartment_name == c.name:
            print(type(c))
            return c

    raise Exception("compartment not found")


def get_app(
        functions_client: functions.FunctionsManagementClient,
        app_name: str, compartment: identityt_models.Compartment) -> fn_models.Application:
    """
    Identifies app ID by its name
    :param functions_client: OCI Functions client
    :param app_name: OCI Functions app name
    :param compartment: OCI tenancy compartment
    :return: OCI Functions app ID
    """
    result = pagination.list_call_get_all_results(
        functions_client.list_applications,
        compartment.id
    )
    for app in result.data:
        if app_name == app.display_name:
            print(type(app))
            return app

    raise Exception("app not found")


def get_function(functions_client: functions.FunctionsManagementClient,
                 app: fn_models.Application,
                 function_name: str) -> fn_models.Function:
    """
    Identifies function ID by its name
    :param functions_client: OCI Functions client
    :param app: OCI Functions app
    :param function_name: OCI Functions function name
    :return: OCI Functions function ID
    """
    functions_client.list_functions(app.id)
    result = pagination.list_call_get_all_results(
        functions_client.list_functions,
        app.id
    )
    for fn in result.data:
        if function_name == fn.display_name:
            print(type(fn))
            print(fn.invoke_endpoint)
            return fn

    raise Exception("function not found")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("usage: python invoke_function.py"
                        " <compartment-name> <app-name> "
                        "<function-name> <image-file-path>")

    compartment_name = sys.argv[1]
    app_name = sys.argv[2]
    fn_name = sys.argv[3]

    cfg = config.from_file(
        file_location=os.getenv(
            "OCI_CONFIG_PATH", config.DEFAULT_LOCATION),
        profile_name=os.getenv(
            "OCI_CONFIG_PROFILE", config.DEFAULT_PROFILE)
    )

    if int(os.getenv("DEBUG", "0")) > 0:
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
        cfg.update({
            "log_requests": True
        })
    functions_client = functions.FunctionsManagementClient(cfg)
    config.validate_config(cfg)

    compartment = get_compartment(cfg, compartment_name, cfg["tenancy"])

    app = get_app(functions_client, app_name, compartment)

    fn = get_function(functions_client, app, fn_name)

    invoke_client = functions.FunctionsInvokeClient(
        cfg, service_endpoint=fn.invoke_endpoint)
    with open(sys.argv[4], 'rb') as img_file:
        resp = invoke_client.invoke_function(fn.id, img_file.read())
        print(resp.data.text)
