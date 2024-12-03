from itertools import islice

# Slides through iterable each `n` elements.
#
# Sample usage:
#
#   >>> list(sliding_window([1, 2, 3, 4]))
#   [(1, 2), (2, 3), (3, 4)]
#
#   >>> list(sliding_window([1, 2, 3]))
#   [(1, 2), (2, 3)]
#
#   >>> list(sliding_window([1, 2, 3, 4], n=3))
#   [(1, 2, 3), (2, 3, 4)]
#
def sliding_window(iterable, n=2):
    args = [islice(iter(iterable), i, None) for i in range(n)]
    return zip(*args)


class Report:

    def __init__(self, line):
        self.levels = [int(i) for i in line.split()]

    def __repr__(self):
        return f'Report(levels={self.levels}, _is_sorted={self._is_sorted()}, _is_delta_safe={self._is_delta_safe()})'

    def is_safe(self):
        return self._is_sorted() and self._is_delta_safe()

    def _is_sorted(self):
        sorted_levels = sorted(self.levels)
        reverse_sorted_levels = sorted(self.levels, reverse=True)
        
        return self.levels in [sorted_levels, reverse_sorted_levels]

    def _is_delta_safe(self):
        for a, b in sliding_window(self.levels):
            if abs(a - b) not in range(1, 4):
                return False

        return True


with open('input.txt') as f:
    reports = [Report(line) for line in f.readlines()]

safe_reports_total = sum(report.is_safe() for report in reports)
print(safe_reports_total)
