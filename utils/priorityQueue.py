import heapq


class PriorityQueue:
    """
    A priority queue class that uses heapq
    """

    def __init__(self):
        self.queue = []
        self.index = 0

    def push(self, item, priority):
        heapq.heappush(self.queue, (-priority, self.index, item))
        self.index += 1

    def pop(self):
        return heapq.heappop(self.queue)[-1]

    def notEmpty(self):
        return True if self.queue else False
