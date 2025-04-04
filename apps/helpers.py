from dataclasses import dataclass

from django.http import HttpRequest

from apps.user.models import User


class AuthenticatedHttpRequest(HttpRequest):
    user: User


@dataclass(kw_only=True)
class BaseResult:
    """
    Base result object that is used for all results returned from a service function.

    If `success` is True, then `message` will always be a message that is show-able
    to the user relating the success of the operation.

    Otherwise, `message` will contain an error string that is show-able to the user
    """

    success: bool
    message: str = ""


@dataclass(kw_only=True)
class BaseData:
    """
    Base data object for any attributes that will be common for all data objects
    For now its empty. More of a 'just in case' which doesn't hurt.
    """

    pass
