"""Support custom filters for jinja"""
import urllib.parse
import base64
import zlib

from random import Random, SystemRandom, shuffle

import logging
from homeassistant.helpers import template

_LOGGER = logging.getLogger(__name__)

_TemplateEnvironment = template.TemplateEnvironment


def deflate(string):
    return zlib.decompress(string)


def inflate(string):
    return zlib.compress(string.encode("utf-8"))


def decode_base64_and_inflate(string):
    data = base64.b64decode(string)
    return zlib.decompress(data).decode("utf-8")


def deflate_and_base64_encode(string):
    data = zlib.compress(string.encode("utf-8"))
    return base64.b64encode(data).decode("utf-8")


def decode_valetudo_map(string):
    """ Currently, this function is equivalent to deflate_and_base64_encode. """
    """ But it may be changed in the future. """
    return decode_base64_and_inflate(string)


def unquote(string):
    return urllib.parse.unquote(string)


def ternary(value, true_val, false_val, none_val=None):
    """  value ? true_val : false_val """
    if value is None and none_val is not None:
        return none_val
    elif bool(value):
        return true_val
    else:
        return false_val


def randomize_list(mylist, seed=None):
    try:
        mylist = list(mylist)
        if seed:
            r = Random(seed)
            r.shuffle(mylist)
        else:
            shuffle(mylist)
    except Exception:
        pass
    return mylist


def init(*args):
    env = _TemplateEnvironment(*args)

    env.filters["unquote"] = unquote
    env.filters["urldecode"] = unquote
    env.filters["ternary"] = ternary
    env.filters["shuffle"] = randomize_list
    env.filters["deflate"] = deflate
    env.filters["inflate"] = inflate
    env.filters["deflate_and_base64_encode"] = deflate_and_base64_encode
    env.filters["decode_base64_and_inflate"] = decode_base64_and_inflate
    env.filters["decode_valetudo_map"] = decode_valetudo_map

    return env


template.TemplateEnvironment = init
template._NO_HASS_ENV.filters["unquote"] = unquote
template._NO_HASS_ENV.filters["urldecode"] = unquote
template._NO_HASS_ENV.filters["ternary"] = ternary
template._NO_HASS_ENV.filters["shuffle"] = randomize_list
template._NO_HASS_ENV.filters["deflate"] = deflate
template._NO_HASS_ENV.filters["inflate"] = inflate
template._NO_HASS_ENV.filters["deflate_and_base64_encode"] = deflate_and_base64_encode
template._NO_HASS_ENV.filters["decode_base64_and_inflate"] = decode_base64_and_inflate
template._NO_HASS_ENV.filters["decode_valetudo_map"] = decode_valetudo_map


async def async_setup(hass, hass_config):
    return True
