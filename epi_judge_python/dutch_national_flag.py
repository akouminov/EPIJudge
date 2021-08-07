import functools
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

RED, WHITE, BLUE = range(3)


def dutch_flag_partition(pivot_index: int, A: List[int]) -> None:
    # TODO - you fill in here.
    pivot = A[pivot_index]
    pointer_1 = 0
    pointer_2 = 0
    pointer_3 = len(A)
    while pointer_2 < pointer_3:
        if A[pointer_2] == pivot:
            pointer_2 += 1
        elif A[pointer_2] > pivot:
            pointer_3 -= 1
            A[pointer_3], A[pointer_2] = A[pointer_2],  A[pointer_3]
        elif A[pointer_2] < pivot:
            A[pointer_1], A[pointer_2] = A[pointer_2], A[pointer_1]
            pointer_1, pointer_2 = pointer_1 + 1, pointer_2 + 1
    return


@enable_executor_hook
def dutch_flag_partition_wrapper(executor, A, pivot_idx):
    count = [0, 0, 0]
    for x in A:
        count[x] += 1
    pivot = A[pivot_idx]

    executor.run(functools.partial(dutch_flag_partition, pivot_idx, A))

    i = 0
    while i < len(A) and A[i] < pivot:
        count[A[i]] -= 1
        i += 1
    while i < len(A) and A[i] == pivot:
        count[A[i]] -= 1
        i += 1
    while i < len(A) and A[i] > pivot:
        count[A[i]] -= 1
        i += 1

    if i != len(A):
        raise TestFailure('Not partitioned after {}th element'.format(i))
    elif any(count):
        raise TestFailure('Some elements are missing from original array')


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('dutch_national_flag.py',
                                       'dutch_national_flag.tsv',
                                       dutch_flag_partition_wrapper))
