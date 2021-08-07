from typing import List

from test_framework import generic_test


def buy_and_sell_stock_once(prices: List[float]) -> float:
    # TODO - you fill in here.
    if len(prices) < 2:
        return 0.0
    if len(prices) == 2:
        return max(float(prices[1]-prices[0]), 0.0)
    max_diff_so_far = 0
    min_so_far = prices[0]
    for i in range(1, len(prices)):
        current_diff = prices[i] - min_so_far
        if current_diff > max_diff_so_far:
            max_diff_so_far = current_diff
        if min_so_far > prices[i]:
            min_so_far = prices[i]
    return max_diff_so_far


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('buy_and_sell_stock.py',
                                       'buy_and_sell_stock.tsv',
                                       buy_and_sell_stock_once))
