import os
import datetime


# No set literals because we support Python 2.6.
TRUE_VALUES = set((
    True,
    'True',
    'true',
))


class empty(object):
    """
    We use this sentinel object, instead of None, as None is a plausible value
    for a default in real Python code.
    """
    pass


def get_env_value(name, required=False, default=empty):
    """
    Core function for extracting the environment variable.

    Enforces mutual exclusivity between `required` and `default` keywords.

    The `empty` sentinal value is used as the default `default` value to allow
    other function to handle default/empty logic in the appropriate way.
    """
    if required and default is not empty:
        raise ValueError("Using `default` with `required=True` is invalid")
    elif required:
        try:
            value = os.environ[name]
        except KeyError:
            raise KeyError(
                "Must set environment variable {0}".format(name)
            )
    else:
        value = os.environ.get(name, default)
    return value


def env_int(name, required=False, default=empty):
    """Pulls an environment variable out of the environment and casts it to an
    integer. If the name is not present in the environment and no default is
    specified then a ``ValueError`` will be raised. Similarly, if the
    environment value is not castable to an integer, a ``ValueError`` will be
    raised.

    :param name: The name of the environment variable be pulled
    :type name: str

    :param required: Whether the environment variable is required. If ``True``
    and the variable is not present, a ``KeyError`` is raised.
    :type required: bool

    :param default: The value to return if the environment variable is not
    present. (Providing a default alongside setting ``required=True`` will raise
    a ``ValueError``)
    :type default: bool
    """
    value = get_env_value(name, required=required, default=default)
    if value is empty:
        raise ValueError(
            "`env_int` requires either a default value to be specified, or for "
            "the variable to be present in the environment"
        )
    return int(value)


def env_bool(name, truthy_values=TRUE_VALUES, required=False, default=empty):
    """Pulls an environment variable out of the environment returning it as a
    boolean. The strings ``'True'`` and ``'true'`` are the default *truthy*
    values. If not present in the environment and no default is specified,
    ``None`` is returned.

    :param name: The name of the environment variable be pulled
    :type name: str

    :param truthy_values: An iterable of values that should be considered
    truthy.
    :type truthy_values: iterable

    :param required: Whether the environment variable is required. If ``True``
    and the variable is not present, a ``KeyError`` is raised.
    :type required: bool

    :param default: The value to return if the environment variable is not
    present. (Providing a default alongside setting ``required=True`` will raise
    a ``ValueError``)
    :type default: bool
    """
    value = get_env_value(name, required=required, default=default)
    if value is empty:
        return None
    return value in TRUE_VALUES


def env_string(name, required=False, default=empty):
    """Pulls an environment variable out of the environment returning it as a
    string. If not present in the environment and no default is specified, an
    empty string is returned.

    :param name: The name of the environment variable be pulled
    :type name: str

    :param required: Whether the environment variable is required. If ``True``
    and the variable is not present, a ``KeyError`` is raised.
    :type required: bool

    :param default: The value to return if the environment variable is not
    present. (Providing a default alongside setting ``required=True`` will raise
    a ``ValueError``)
    :type default: bool
    """
    value = get_env_value(name, default=default, required=required)
    if value is empty:
        value = ''
    return value


def env_list(name, separator=',', required=False, default=empty):
    """Pulls an environment variable out of the environment, splitting it on a
    separator, and returning it as a list. Extra whitespace on the list values
    is stripped. List values that evaluate as falsy are removed. If not present
    and no default specified, an empty list is returned.

    :param name: The name of the environment variable be pulled
    :type name: str

    :param separator: The separator that the string should be split on.
    :type separator: str

    :param required: Whether the environment variable is required. If ``True``
    and the variable is not present, a ``KeyError`` is raised.
    :type required: bool

    :param default: The value to return if the environment variable is not
    present. (Providing a default alongside setting ``required=True`` will raise
    a ``ValueError``)
    :type default: bool
    """
    value = get_env_value(name, required=required, default=default)
    if value is empty:
        return []
    # wrapped in list to force evaluation in python 3
    return list(filter(bool, [v.strip() for v in value.split(separator)]))


def env_timestamp(name, required=False, default=empty):
    """Pulls an environment variable out of the environment and parses it to a
    ``datetime.datetime`` object. The environment variable is expected to be a
    timestamp in the form of a float.

    If the name is not present in the environment and no default is specified
    then a ``ValueError`` will be raised.

    :param name: The name of the environment variable be pulled
    :type name: str

    :param required: Whether the environment variable is required. If ``True``
    and the variable is not present, a ``KeyError`` is raised.
    :type required: bool

    :param default: The value to return if the environment variable is not
    present. (Providing a default alongside setting ``required=True`` will raise
    a ``ValueError``)
    :type default: bool
    """
    if required and default is not empty:
        raise ValueError("Using `default` with `required=True` is invalid")

    value = get_env_value(name, required=required, default=empty)
    # change datetime.datetime to time, return time.struct_time type
    if default is not empty and value is empty:
        return default
    if value is empty:
        raise ValueError(
            "`env_timestamp` requires either a default value to be specified, "
            "or for the variable to be present in the environment"
        )

    timestamp = float(value)
    return datetime.datetime.fromtimestamp(timestamp)


def env_iso8601(name, required=False, default=empty):
    """Pulls an environment variable out of the environment and parses it to a
    ``datetime.datetime`` object. The environment variable is expected to be an
    iso8601 formatted string.

    If the name is not present in the environment and no default is specified
    then a ``ValueError`` will be raised.

    :param name: The name of the environment variable be pulled
    :type name: str

    :param required: Whether the environment variable is required. If ``True``
    and the variable is not present, a ``KeyError`` is raised.
    :type required: bool

    :param default: The value to return if the environment variable is not
    present. (Providing a default alongside setting ``required=True`` will raise
    a ``ValueError``)
    :type default: bool
    """
    try:
        import iso8601
    except ImportError:
        raise ImportError(
            'Parsing iso8601 datetime strings requires the iso8601 library'
        )

    if required and default is not empty:
        raise ValueError("Using `default` with `required=True` is invalid")

    value = get_env_value(name, required=required, default=empty)
    # change datetime.datetime to time, return time.struct_time type
    if default is not empty and value is empty:
        return default
    if value is empty:
        raise ValueError(
            "`env_iso8601` requires either a default value to be specified, or "
            "for the variable to be present in the environment"
        )
    return iso8601.parse_date(value)
