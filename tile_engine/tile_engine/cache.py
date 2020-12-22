from functools import wraps

'''
http://book.pythontips.com/en/latest/function_caching.html
'''
def memoize(function):
    memo = {}
    @wraps(function)
    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv
    return wrapper
