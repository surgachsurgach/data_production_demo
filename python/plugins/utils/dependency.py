from functools import reduce

def sequential_dependency(xs: list, ys: list = None):
    if ys is None:
        return reduce(lambda x, y: x >> y, xs)

    else:
        def make_dependency():
            for x, y in zip(xs, ys):
                yield x >> y

        return tuple(make_dependency())
