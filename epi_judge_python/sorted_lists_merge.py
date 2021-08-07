from typing import Optional

from list_node import ListNode
from test_framework import generic_test


def merge_two_sorted_lists(L1: Optional[ListNode],
                           L2: Optional[ListNode]) -> Optional[ListNode]:
    # TODO - you fill in here.
    if L1 == None:
        return L2
    if L2 == None:
        return L1
    if L1.data > L2.data:
        node = L2
        node1 = L1
        head = L2
    else:
        node = L1
        node1 = L2
        head = L1
    while node.next:
        if node1 and node1.data >= node.data and node1.data < node.next.data:
            node1_next = node1.next
            node1.next = node.next
            node.next = node1
            node = node1
            node1 = node1_next
        else:
            node = node.next
    if node1:
        node.next = node1
    return head

# the other approach is to pick one or the other


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('sorted_lists_merge.py',
                                       'sorted_lists_merge.tsv',
                                       merge_two_sorted_lists))
