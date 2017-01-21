# Compose.py

def curry(uncurried, *args):
    if len(args) == 0:
        return uncurried
    ori_args = args
    return lambda *args: uncurried(*(ori_args + args))

def compose(*fxns):
    if len(fxns) == 2:
        return lambda x: fxns[0](fxns[1](x))
    return lambda x: fxns[0](compose(*fxns[1:])(x))

def if_else(condition, callback, args):
    """
    Executes `callback` on the first element of a two-element-long `args` list
    if `condition` evaluates to `True`. If not, the second element of `args` is
    used.
    ------
    Parameters:
        condition: Conditional statement. Must be either `True` or `False`
        callback : Function which calls `args[0]` if `condition(obj) == True`.
                   Otherwise, `args[1]` is used instead.
        args     : A two-element-long list. First element will be used
                   in `callback` if `condition(obj) == True`. If not,
                   the second element will be used instead.
    """
    return callback(args[0]) if condition else callback(args[1])

if __name__ == "__main__":
    pass
