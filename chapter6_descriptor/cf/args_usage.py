# sum_integers_args.py
def my_sum(*args):
    """ argument 로 iterable values 를 넣고 돌린다.

    :param args:
    :return:
    """
    result = 0
    # Iterating over the Python args tuple
    for x in args:
        result += x
    return result


print(my_sum(1, 2, 3))
