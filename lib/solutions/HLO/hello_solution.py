"""hello_solution challenge."""


# noinspection PyUnusedLocal
# friend_name = unicode string
def hello(friend_name: str) -> str:
    """Input friend name. Return a string containing a message.

    :param friend_name: name of friend
    :return: string containing a message
    """
    if not isinstance(friend_name, str):
        raise TypeError("friend_name must be a string.")
    return f"Hello, {friend_name}!"
