from collections import deque


def sum_block(start, size):
    nth_term = start + size - 1
    total_sum = (size / 2) * (start + nth_term)
    
    return total_sum


def process_chunk(files, file_id, index, chunksize):
    total = file_id * sum_block(index, chunksize)
    files[file_id] -= chunksize

    return total


with open('input.txt') as f:
    disk_data = [int(i) for i in f.read().strip()]

files = {}
spaces = []
files_non_processed = deque()

for index, value in enumerate(disk_data):
    if index % 2 == 0:
        files[index // 2] = value
        if value > 0:
            files_non_processed.appendleft(index // 2)
    else:
        spaces.append(value)

total = 0
aux_counter = 0

for index, value in enumerate(disk_data):
    current_index = index // 2

    if index % 2 == 0:
        current_file_id = current_index
        current_filesize = files[current_file_id]
        
        total += process_chunk(files, current_file_id, aux_counter, current_filesize)
        aux_counter += current_filesize

        if files_non_processed:
            files_non_processed.pop()
    else:
        current_space_index = current_index
        current_space_size = spaces[current_space_index]
        
        if not files_non_processed:
            break

        current_file_id = files_non_processed[0]
        current_filesize = files[current_file_id]

        while current_space_size >= current_filesize:
            total += process_chunk(files, current_file_id, aux_counter, current_filesize)

            aux_counter += current_filesize
            current_space_size -= current_filesize

            files_non_processed.popleft()

            if not files_non_processed:
                break

            current_file_id = files_non_processed[0]
            current_filesize = files[current_file_id]
            
        if current_space_size == 0 or not files_non_processed:
            continue

        total += process_chunk(files, current_file_id, aux_counter, current_space_size)
        aux_counter += current_space_size

        if files[current_file_id] == 0:
            files_non_processed.popleft()

print(int(total))
