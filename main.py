import logging
import sys
import functions_framework

# from google.cloud import error_reporting
from utils.box_client_ccg import (
    ConfigCCG,
    get_ccg_enterprise_client,
)
from box_sdk_gen import BoxAPIError


@functions_framework.http
def hello_get(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    Note:
        For more information on how Flask integrates with Cloud
        Functions, see the `Writing HTTP functions` page.
        <https://cloud.google.com/functions/docs/writing/http#http_frameworks>
    """
    return "Hello, World!"


@functions_framework.http
def whoami(request):
    client = get_ccg_enterprise_client(ConfigCCG())
    try:
        me = client.users.get_user_me()
        # return f"\nHello, I'm {me.name} ({me.login}) [{me.id}]"
        return me.to_dict()
    except BoxAPIError as e:
        return (e.response_info.body, e.response_info.status_code)


@functions_framework.http
def init(request):
    # only allow POST
    if request.method != "POST":
        return "Method not allowed", 405

    # get the request data
    request_json = request.get_json()
    if request_json and "folder_id" in request_json:
        folder_id = request_json["folder_id"]
    else:
        return "Bad request", 400

    # folder id cannot be empty, 0 or None
    if not folder_id or folder_id == 0 or folder_id == "0" or folder_id == "":
        return (
            "Bad request, folder_id is a string, and cannot be 0, or empty",
            400,
        )

    client = get_ccg_enterprise_client(ConfigCCG())

    # make sure folder exists
    try:
        folder = client.folders.get_folder_by_id(folder_id)
    except BoxAPIError as e:
        return (e.response_info.body, e.response_info.status_code)

    return folder.to_dict()
