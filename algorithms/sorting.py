from typing import List, Generator, Dict, Any

Step = Dict[str, Any]

def _snapshot(arr: List[int]) -> List[int]:
    return arr.copy()

# --- Bubble Sort ---
def bubble_sort_steps(arr: List[int]) -> Generator[Step, None, None]:
    a = arr.copy()
    n = len(a)
    for end in range(n-1, 0, -1):
        for i in range(end):
            j = i+1
            yield {'type': 'compare', 'i': i, 'j': j, 'array': _snapshot(a)}
            if a[i] > a[j]:
                a[i], a[j] = a[j], a[i]
                yield {'type': 'swap', 'i': i, 'j': j, 'array': _snapshot(a)}
    yield {'type': 'finished', 'array': _snapshot(a)}

# --- Selection Sort ---
def selection_sort_steps(arr: List[int]) -> Generator[Step, None, None]:
    a = arr.copy()
    n = len(a)
    for i in range(n-1):
        min_idx = i
        yield {'type': 'select_min', 'i': i, 'min_idx': min_idx, 'array': _snapshot(a)}
        for j in range(i+1, n):
            yield {'type': 'compare', 'i': min_idx, 'j': j, 'array': _snapshot(a)}
            if a[j] < a[min_idx]:
                min_idx = j
                yield {'type': 'select_min', 'i': i, 'min_idx': min_idx, 'array': _snapshot(a)}
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            yield {'type': 'swap', 'i': i, 'j': min_idx, 'array': _snapshot(a)}
    yield {'type': 'finished', 'array': _snapshot(a)}

# --- Insertion Sort ---
def insertion_sort_steps(arr: List[int]) -> Generator[Step, None, None]:
    a = arr.copy()
    n = len(a)
    for i in range(1, n):
        key = a[i]
        j = i-1
        yield {'type': 'key_pick', 'i': i, 'key': key, 'array': _snapshot(a)}
        while j >= 0 and a[j] > key:
            yield {'type': 'compare', 'i': j, 'key': key, 'array': _snapshot(a)}
            a[j+1] = a[j]
            yield {'type': 'overwrite', 'k': j+1, 'value': a[j], 'array': _snapshot(a)}
            j -= 1
        a[j+1] = key
        yield {'type': 'insert', 'i': j+1, 'key': key, 'array': _snapshot(a)}
    yield {'type': 'finished', 'array': _snapshot(a)}

# --- Quick Sort ---
def quick_sort_steps(arr: List[int]) -> Generator[Step, None, None]:
    a = arr.copy()
    def _quick_sort(low, high):
        if low < high:
            pivot_index = high
            pivot = a[pivot_index]
            i = low
            for j in range(low, high):
                yield {'type': 'compare', 'i': j, 'pivot': pivot_index, 'array': _snapshot(a)}
                if a[j] < pivot:
                    a[i], a[j] = a[j], a[i]
                    yield {'type': 'swap', 'i': i, 'j': j, 'array': _snapshot(a)}
                    i += 1
            a[i], a[high] = a[high], a[i]
            yield {'type': 'swap', 'i': i, 'j': high, 'array': _snapshot(a)}
            yield from _quick_sort(low, i-1)
            yield from _quick_sort(i+1, high)
    yield from _quick_sort(0, len(a)-1)
    yield {'type': 'finished', 'array': _snapshot(a)}

# --- Merge Sort ---
def merge_sort_steps(arr: List[int]) -> Generator[Step, None, None]:
    a = arr.copy()
    def _merge_sort(l, r):
        if l < r:
            m = (l+r)//2
            yield from _merge_sort(l, m)
            yield from _merge_sort(m+1, r)
            # merge step
            left = a[l:m+1]
            right = a[m+1:r+1]
            i = j = 0
            k = l
            while i < len(left) and j < len(right):
                yield {'type': 'compare', 'i': l+i, 'j': m+1+j, 'array': _snapshot(a)}
                if left[i] <= right[j]:
                    a[k] = left[i]
                    yield {'type': 'overwrite', 'k': k, 'value': left[i], 'array': _snapshot(a)}
                    i += 1
                else:
                    a[k] = right[j]
                    yield {'type': 'overwrite', 'k': k, 'value': right[j], 'array': _snapshot(a)}
                    j += 1
                k += 1
            while i < len(left):
                a[k] = left[i]
                yield {'type': 'overwrite', 'k': k, 'value': left[i], 'array': _snapshot(a)}
                i += 1
                k += 1
            while j < len(right):
                a[k] = right[j]
                yield {'type': 'overwrite', 'k': k, 'value': right[j], 'array': _snapshot(a)}
                j += 1
                k += 1
    yield from _merge_sort(0, len(a)-1)
    yield {'type': 'finished', 'array': _snapshot(a)}
