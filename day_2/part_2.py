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
        return f'Report(levels={self.levels}, is_safe={self.is_safe()})'

    def is_safe(self):
        if self._is_sorted(self.levels) and self._is_delta_safe(self.levels):
            return True

        for level_index, _ in enumerate(self.levels):
            levels = self.levels[:level_index] + self.levels[level_index + 1:]

            if self._is_sorted(levels) and self._is_delta_safe(levels):
                return True

        return False

    def _is_sorted(self, levels):
        sorted_levels = sorted(levels)
        reverse_sorted_levels = sorted(levels, reverse=True)
        
        return levels in [sorted_levels, reverse_sorted_levels]

    def _is_delta_safe(self, levels):
        for a, b in sliding_window(levels):
            if abs(a - b) not in range(1, 4):
                return False

        return True


with open('input.txt') as f:
    reports = [Report(line) for line in f.readlines()]

safe_reports_total = sum(report.is_safe() for report in reports)
print(safe_reports_total)
