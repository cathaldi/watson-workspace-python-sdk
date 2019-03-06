

def _http_status_handler(json_body, response_status_code) -> str:
    """

    :param json_body:  JSON response from Watson Workspace
    :param response_status_code: Response code from Watson Workspace
    :return: A parsed payload
    :raises: _throw_http_400
    """
    if response_status_code < 400:
        given_status_code = json_body.get("message", response_status_code)
    else:
        json_body = {}
        given_status_code = response_status_code

    if given_status_code == 200:
        return ""
    elif given_status_code == 201:
        return ""
    elif given_status_code == 204:
        return ""
    elif given_status_code >= 400:
        _throw_http_400(json_body.get("errors", f"Received a {response_status_code} from Watson Workspace"))
    else:
        raise Exception(f"Unexpected exception. Received a {given_status_code}")


def _throw_http_400(bss_message_string: str):
    raise Exception(bss_message_string)


def _throw_http_404(bss_message_string: str):
    raise Exception(bss_message_string)


def _throw_http_500(bss_message_string: str):
    raise Exception(bss_message_string)
