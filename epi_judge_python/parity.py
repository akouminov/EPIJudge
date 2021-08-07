from test_framework import generic_test


def parity(x: int) -> int:
    # TODO - you fill in here.
    count = 0
    while x:
        count ^= 1 # flips count from 1 to 0, if 1 then odd number, if 0 even
        x &= x-1 #clear the lowest bit
    return count

# brute force
def parity_brute_force(x: int) -> int:
    # TODO - you fill in here.
    count = 0
    while x:
        count ^= x & 1 # and number with 1 to see if first bit is 1 and then exclusive or with count
        x >>= 1 # shift by 1 for next bit
    return count


if __name__ == '__main__':
    exit(generic_test.generic_test_main('parity.py', 'parity.tsv', parity))
