from random import choices
from string import ascii_lowercase

from .config import DEFAULT_PORT


def get_url(url: str) -> str:
    """Ranomdly generates a url for use in requests.
    Generates a hostname with the port and the provided suffix url provided
    :param url: A url fragment to use in the creation of the master url
    """
    sub = "{0}.spotilocal.com".format("".join(choices(ascii_lowercase, k=10)))
    return "http://{0}:{1}{2}".format(sub, DEFAULT_PORT, url)
