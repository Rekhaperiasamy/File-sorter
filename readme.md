# External Merge Sort Implementation

Sorting is done with 'External Merge Sort' algorithm.

## Table of Contents

- [How to Run](#how-to-run)
- [Implementation Details](#implementation-details)

## How to Run

### 1. Generate Test File

```
python generate_test_file.py -s 0.1 -o test_file.txt
```

-s is the size of the file in GB.
-o is the output file name.

### 2. Sort File

```
python sort_test_file.py -i test_file.txt -o sorted_test_file.txt
```

-i is the input file name.
-o is the output file name.

## Implementation Details

### 1. File Generation (Generator class)

- Generates random numbers and strings
- Maintains some common strings to ensure duplicates
- Reports progress during generation
- Tracks generation time

### 2. Sorting Process (Sorter class)

#### Phase 1: Split

1. Reads input file in chunks of specified size (default 100MB)
2. For each chunk:
   - Loads it into memory
   - Parses lines into (string, number, original_line) tuples
   - Sorts the chunk
   - Writes to temporary file
3. Creates multiple sorted chunk files

#### Phase 2: Merge

1. Opens all chunk files simultaneously
2. Uses a min-heap to efficiently merge chunks:
   - Heap contains one line from each chunk
   - Always extracts minimum element
   - Replaces extracted element with next line from same chunk
3. Writes merged result to output file

### Sorting Logic

1. Primary sort key: String part (text after the number)
2. Secondary sort key: Number part
3. Example sort order:

```
1. Apple
415. Apple
2. Banana is yellow
32. Cherry is the best
30432. Something something something
```

### Memory Usage

- Chunk size determines memory footprint
- Default 100MB chunks work well for most systems
- Can be adjusted based on available RAM:

### Progress Monitoring

- Regular progress updates (every 5 seconds)
- Shows:
  - Percentage complete
  - Elapsed time
  - Estimated remaining time

### Temporary Files

- Created in system's temp directory
- Automatically cleaned up after sorting
- Each chunk file is approximately chunk_size_mb in size
