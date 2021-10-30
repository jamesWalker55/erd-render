prefix_counter = {}


def new(prefix=None):
    """generate a unique string for the current session. an optional prefix can be provided."""
    count = prefix_counter.get(prefix, 0)
    count += 1
    prefix_counter[prefix] = count
    if prefix is not None:
        return f"{prefix}-{count}"
    else:
        return f"{count}"
