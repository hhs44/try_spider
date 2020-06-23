from functools import lru_cache


@lru_cache()
def foo(num):
    if num in (1, 2):
        return 1
    return foo(num - 1) + foo(num - 2)


for x in range(1, 10000):
    print(f"{x} :{foo(x)}\n")