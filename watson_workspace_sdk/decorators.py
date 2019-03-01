from flask import request, Response
import hmac
import json
import hashlib
import logging
import timeit
from watson_workspace_sdk.config import Config


logging.basicConfig(level=Config.log_level)
logger = logging.getLogger(__name__)


def verify_workspace_origin(webhook_secret: str):
    """
    Checks incoming flask requests and ensures message came from Watson Workspace.
    If request does not originate from workspace it is logged and dropped.

    :param webhook_secret: Webhook secret - Found in Watson Workspace application page.
    :return: Incoming request

    """
    def real_wrapper(func: request):
        def wrapper():
            logger.info(f""" Message-Received: Space {request.json.get("spaceId")} received Message Id {request.json.get("messageId")} """)
            header_token = hmac.new(bytes(webhook_secret, "utf-8"), msg=request.data, digestmod=hashlib.sha256).hexdigest()
            if header_token == request.headers.get('X-OUTBOUND-TOKEN'):
                logger.info(f""" Message-Integrity: Confirmed for Message Id {request.json.get("messageId")} """)
                logger.info(f""" Message-Owner: User {request.json.get("userName")} ({request.json.get("userId")}) with message id {request.json.get("messageId")}""")
                return func()
            else:
                logger.error(f" Questionable message recieved by verify_workspace_origin. Message dropped.")
                logger.error(f" Message is as follows : {request.data}")
                return "verify_workspace_origin failed"  # Nothing will happen from here - func won't be called
        wrapper.__name__ = func.__name__
        return wrapper
    real_wrapper.__name__ = real_wrapper.__name__
    return real_wrapper


def handle_verification(webhook_secret: str):  # has to be done every hour with Workspace
    """
    Checks if incoming request is a periodic Watson Workspace Verification message and replies to the challenge.

    :param webhook_secret: Webhook secret - Found in Watson Workspace application  page.
    :return: Incoming request
    """
    def real_wrapper(func):
        def wrapper():
            if request.json.get("type") == "verification":
                try:
                    challenge = json.loads(request.data.decode("utf-8")).get("challenge")
                    response = json.dumps({"response": challenge})
                    response_header_token = hmac.new(bytes(webhook_secret, "utf-8"), msg=bytes(response, "utf-8"),
                                                     digestmod=hashlib.sha256).hexdigest()
                    resp = Response(response=response, status=200)
                    resp.headers['X-Outbound-Token'] = response_header_token
                    resp.headers['content_type'] = 'application/json'
                    logger.info(f""" Webhook-Verification: Succeeded""")
                except Exception as e:
                    logger.error(f" Webhook-Verification: Failed")
                    logger.error(f"Request : {request}")
                    logger.error(f"Response : {response}")
                    return "handle_verification failed"
                return resp
            else:  # do nothing
                return func()
        wrapper.__name__ = func.__name__
        return wrapper
    real_wrapper.__name__ = real_wrapper.__name__
    return real_wrapper


def filter_workspace_annotations(whitelist=[], blacklist=[]):
    """
    Drops and/or allows through specific annotations.
    Useful to cut out the Watson annotation calls that are not too informative.

        blacklist = [toscana-words]  # Drop these annotations.

        whitelist = ["generic"]      # These are standard chat messages from users

        whitelist = ["actionSelected", "generic"  # Allows user chat messages and action events such as clicking a
        button, slash command or clicking on a focus annotation.

    :param whitelist: List of annotations to allow
    :param blacklist: List of annotations to drop
    :return: Incoming request


    Use:
    After a user creates a message, Workspace will annotate the message extracting Workspace Moment data.
    This is a message-annotation-edited event, and the annotation type will be a conversation-moment. My app has no use
    for this information so will be dropped.
    """
    def real_wrapper(func):
        def wrapper():
            if request.json.get("annotationType") in whitelist:
                logger.info(f""" Annotation-Filter: Forwarding message {request.json.get("messageId")} as {request.json.get("annotationType")} is in whitelist {whitelist} """)
                return func()
            else:
                logger.info(f""" Annotation-Filter: Dropping message {request.json.get("messageId")} as {request.json.get("annotationType")} isn't in whitelist {whitelist} \n""")
                return ""
        wrapper.__name__ = func.__name__
        return wrapper
    real_wrapper.__name__ = real_wrapper.__name__
    return real_wrapper


def user_blacklist(blacklist):  # has to be done every hour with Workspace
    """
        Ignores messages from a blacklist of user ids
    """
    def real_wrapper(func):
        def wrapper():
            if request.json.get("userId") in blacklist:
                logger.info(f""" User-Filter: Dropping message {request.json.get("messageId")} ({request.json.get("type")}) as {request.json.get("userId")} is in blacklist {blacklist} """)
                return ""
            if request.json.get("userId") not in blacklist:
                logger.info(f""" User-Filter: Forwarding message {request.json.get("messageId")} ({request.json.get("type")}) as {request.json.get("userId")} is not blacklisted {blacklist} """)
                return func()
            return func()
        wrapper.__name__ = func.__name__
        return wrapper
    real_wrapper.__name__ = real_wrapper.__name__
    return real_wrapper


def user_whitelist(whitelist):  # has to be done every hour with Workspace
    """
        Ignore all messages unless a user is on a whitelist of user ids
    """
    def real_wrapper(func):
        def wrapper():
            if request.json.get("userId") not in whitelist:
                logger.info(f""" User-Filter: Dropping message {request.json.get("messageId")} ({request.json.get("type")}) as {request.json.get("userId")} isn't in whitelist {whitelist} \n""")
                return ""
            if request.json.get("userId") in whitelist:
                logger.info(f""" User-Filter: Forwarding message {request.json.get("messageId")} ({request.json.get("type")}) as {request.json.get("userId")} is in whitelist {whitelist} """)
                return func()
            return func()
        wrapper.__name__ = func.__name__
        return wrapper
    real_wrapper.__name__ = real_wrapper.__name__
    return real_wrapper


def ignore_bots():  # has to be done every hour with Workspace
    """
        Ignore all messages from Watson Workspace bots/Apps
    """
    def real_wrapper(func):
        def wrapper():
            if request.json.get("userName") is "None":
                logger.info(f""" Ignore-bots: Dropping message {request.json.get("messageId")} ({request.json.get("type")}) as {request.json.get("userId")} is a bot/app \n""")
                return ""
            elif request.json.get("userId") is not "None":  # elif for now - unsure of other values - for instance oauth apps
                logger.info(f""" Ignore-bots: Forwarding message {request.json.get("messageId")} ({request.json.get("type")}) as {request.json.get("userName")} ({request.json.get("userId")}) is not a bot/app """)
                return func()
            return func()
        wrapper.__name__ = func.__name__
        return wrapper
    real_wrapper.__name__ = real_wrapper.__name__
    return real_wrapper


def timer():  # has to be done every hour with Workspace

    def real_wrapper(func):
        def timed():
            ts = timeit.timeit()
            print(ts)
            return func()
        timed.__name__ = func.__name__
        return timed
    real_wrapper.__name__ = real_wrapper.__name__
    return real_wrapper

