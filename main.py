import functions_framework

from utils.box_client_ccg import (
    ConfigCCG,
    get_ccg_enterprise_client,
)
from utils.box_webhook_validate import validate_webhook_signature
from utils.box_tasks import create_file_task

from box_sdk_gen import BoxAPIError

from box_sdk_gen.managers.webhooks import (
    Webhook,
    CreateWebhookTarget,
    CreateWebhookTargetTypeField,
    CreateWebhookTriggers,
)


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
        return "Bad request, folder_id is mandatory", 400

    if request_json and "url" in request_json:
        url = request_json["url"]
    else:
        return "Bad request, url is mandatory", 400

    # folder id cannot be empty, 0 or None
    if not folder_id or folder_id == 0 or folder_id == "0" or folder_id == "":
        return (
            "Bad request, folder_id is a string, and cannot be 0, or empty",
            400,
        )

    # get the client
    client = get_ccg_enterprise_client(ConfigCCG())

    # make sure folder exists
    try:
        folder = client.folders.get_folder_by_id(folder_id)
    except BoxAPIError as e:
        return (e.response_info.body, e.response_info.status_code)

    # create the webhook
    try:

        webhook: Webhook = client.webhooks.create_webhook(
            target=CreateWebhookTarget(
                id=folder.id, type=CreateWebhookTargetTypeField.FOLDER
            ),
            address=url,
            triggers=[CreateWebhookTriggers.FILE_UPLOADED],
        )
    except BoxAPIError as e:
        return (e.response_info.body, e.response_info.status_code)

    return webhook.to_dict()


@functions_framework.http
def echo(request):
    # only allow POST
    if request.method != "POST":
        return "Method not allowed", 405

    # get the request headers
    # request_headers = request.headers
    box_timestamp = request.headers.get("box-delivery-timestamp")
    signature1 = request.headers.get("box-signature-primary")
    signature2 = request.headers.get("box-signature-secondary")

    box_headers = {
        "box-delivery-timestamp": box_timestamp,
        "box-signature-primary": signature1,
        "box-signature-secondary": signature2,
    }
    # logger.log(logging.LogEntry(payload=box_headers))
    print(box_headers)

    # get the request data
    request_json = request.get_json()
    # logger.log(logging.LogEntry(payload=request_json))
    print(request_json)

    return ("OK", 200)


@functions_framework.http
def box_webhook(request):

    # only allow POST
    if request.method != "POST":
        return "Method not allowed", 405

    # get the request headers
    timestamp_header = request.headers.get("box-delivery-timestamp")
    signature1 = request.headers.get("box-signature-primary")
    signature2 = request.headers.get("box-signature-secondary")
    box_signature_version = request.headers.get("box-signature-version")
    box_signature_algorithm = request.headers.get("box-signature-algorithm")

    config = ConfigCCG()

    # validate the webhook signature
    is_valid = validate_webhook_signature(
        config.key_a,
        config.key_b,
        timestamp_header,
        signature1,
        signature2,
        request.data,
        box_signature_version,
        box_signature_algorithm,
    )

    if not is_valid:
        return ("Invalid signature", 401)

    payload = request.get_json()

    # get a box client
    client = get_ccg_enterprise_client(config)

    # file_id = (payload.get("source", {}).get("id"),)
    # user_id = (config.ccg_user_id,)

    task_assignment = create_file_task(
        client,
        file_id=payload.get("source", {}).get("id"),
        user_id=config.ccg_user_id,
        message="Please review this file",
    )

    print(task_assignment)

    return ("OK", 200)
