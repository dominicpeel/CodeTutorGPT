def cache(func):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            print(args, "Not in cache")
            res = func(*args)
            cache[args] = res
        else:
            print(args, "Returning from cache")
        return cache[args]

    return wrapper

@cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

fib(10)
fib(10)
fib(5)