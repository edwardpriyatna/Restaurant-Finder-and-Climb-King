""" Heap implemented using an array"""
__author__ = "Brendon Taylor"
__docformat__ = 'reStructuredText'

from typing import Generic
from referential_array import ArrayR, T


class MinHeap(Generic[T]):
    MIN_CAPACITY = 1

    def __init__(self, max_size: int) -> None:
        self.length = 0
        self.the_array = ArrayR(max(self.MIN_CAPACITY, max_size) + 1)

    def __len__(self) -> int:
        return self.length

    def is_full(self) -> bool:
        return self.length + 1 == len(self.the_array)

    def rise(self, k: int) -> None:
        """
        Rise element at index k to its correct position
        :pre: 1 <= k <= self.length
        """
        item = self.the_array[k]
        while k > 1 and item < self.the_array[k // 2]:
            self.the_array[k] = self.the_array[k // 2]
            k = k // 2
        self.the_array[k] = item

    def add(self, element: T) -> None:
        """
        Swaps elements while rising
        """
        if self.is_full():
            raise IndexError

        self.length += 1
        self.the_array[self.length] = element
        self.rise(self.length)

    def smallest_child(self, k: int) -> int:
        """
        Returns the index of k's child with smallest value.
        :pre: 1 <= k <= self.length // 2
        """

        if 2 * k == self.length or \
                self.the_array[2 * k] < self.the_array[2 * k + 1]:
            return 2 * k
        else:
            return 2 * k + 1

    def sink(self, k: int) -> None:
        """ Make the element at index k sink to the correct position.
            :pre: 1 <= k <= self.length
            :complexity: ???
        """
        item = self.the_array[k]

        while 2 * k <= self.length:
            min_child = self.smallest_child(k)
            if self.the_array[min_child] >= item:
                break
            self.the_array[k] = self.the_array[min_child]
            k = min_child

        self.the_array[k] = item

    def get_min(self):
        """ Remove (and return) the minimum element from the heap. """
        if self.length == 0:
            raise IndexError

        min_elt = self.the_array[1]
        self.length -= 1
        if self.length > 0:
            self.the_array[1] = self.the_array[self.length+1]
            self.sink(1)
        return min_elt

if __name__ == '__main__':
    items = [int(x) for x in input('Enter a list of numbers: ').strip().split()]
    heap = MinHeap(len(items))

    for item in items:
        heap.add(item)

    for i in heap.the_array:
        print(i)
