import heapq
import os
import tempfile
import time
from datetime import datetime
from typing import List, Tuple


class Sorter:
    def __init__(self, chunk_size_mb: int = 200):
        self.chunk_size = chunk_size_mb * 1024 * 1024
        self.temp_dir = tempfile.mkdtemp()
        print(f"Using temp directory: {self.temp_dir}")
        print(f"Chunk size: {chunk_size_mb}MB")

    def parse_line(self, line: str) -> Tuple[str, int, str]:
        try:
            number_str, text = line.strip().split('.', 1)
            return (text.strip(), int(number_str), line)
        except ValueError as e:
            print(f"Error parsing line: {line!r}")
            raise e

    def sort_chunk(self, lines: List[str]) -> List[str]:
        try:
            parsed = [self.parse_line(line) for line in lines if line.strip()]
            parsed.sort()
            return [item[2] for item in parsed]
        except Exception as e:
            print(f"Error sorting chunk: {e}")
            raise e

    def split_into_sorted_chunks(self, input_path: str) -> List[str]:
        start_time = time.time()
        chunk_files = []
        current_chunk = []
        current_size = 0
        total_size = os.path.getsize(input_path)
        processed_size = 0
        last_progress_time = start_time

        try:
            with open(input_path, 'r') as f:
                for line in f:
                    line_size = len(line.encode('utf-8'))
                    processed_size += line_size

                    if current_size + line_size > self.chunk_size and current_chunk:
                        # Sort and write current chunk
                        chunk_start_time = time.time()
                        sorted_chunk = self.sort_chunk(current_chunk)
                        chunk_path = os.path.join(self.temp_dir, f"chunk_{
                                                  len(chunk_files)}.txt")
                        with open(chunk_path, 'w') as chunk_file:
                            chunk_file.writelines(sorted_chunk)
                        chunk_files.append(chunk_path)
                        current_chunk = []
                        current_size = 0

                        # Progress report every 5 seconds
                        current_time = time.time()
                        if current_time - last_progress_time >= 5:
                            elapsed = current_time - start_time
                            progress = processed_size / total_size * 100
                            print(f"Splitting progress: {progress:.1f}% "
                                  f"({len(chunk_files)} chunks) in {self.format_time(elapsed)} ")
                            last_progress_time = current_time

                    current_chunk.append(line)
                    current_size += line_size

            # Handle last chunk
            if current_chunk:
                sorted_chunk = self.sort_chunk(current_chunk)
                chunk_path = os.path.join(self.temp_dir, f"chunk_{
                                          len(chunk_files)}.txt")
                with open(chunk_path, 'w') as chunk_file:
                    chunk_file.writelines(sorted_chunk)
                chunk_files.append(chunk_path)

            total_time = time.time() - start_time
            print(f"\nSplit complete:")
            print(f"Created {len(chunk_files)} chunks")
            print(f"Total time: {self.format_time(total_time)}")

            return chunk_files

        except Exception as e:
            print(f"Error during splitting: {e}")
            # Cleanup any created chunks
            for chunk_file in chunk_files:
                if os.path.exists(chunk_file):
                    os.remove(chunk_file)
            raise e

    def merge_chunks(self, chunk_files: List[str], output_path: str):
        start_time = time.time()
        last_progress_time = start_time
        try:
            print("Opening chunk files and initializing heap...")
            chunk_handles = []
            heap = []

            for i, chunk_path in enumerate(chunk_files):
                handle = open(chunk_path, 'r')
                chunk_handles.append(handle)
                first_line = handle.readline()
                if first_line.strip():
                    parsed = self.parse_line(first_line)
                    heap.append((parsed[0], parsed[1], i, first_line))

            heapq.heapify(heap)

            written_lines = 0
            total_bytes = 0

            print("Starting merge process...")
            with open(output_path, 'w') as out:
                while heap:
                    # Get smallest item
                    _, _, chunk_idx, line = heapq.heappop(heap)
                    bytes_written = len(line.encode('utf-8'))
                    out.write(line)
                    written_lines += 1
                    total_bytes += bytes_written

                    # Progress update every 5 seconds
                    current_time = time.time()
                    if current_time - last_progress_time >= 5:
                        elapsed = current_time - start_time
                        print(f"Merged {written_lines:,} lines in {
                              self.format_time(elapsed)} ")
                        last_progress_time = current_time

                    # Read next line from same chunk
                    next_line = chunk_handles[chunk_idx].readline()
                    if next_line.strip():
                        parsed = self.parse_line(next_line)
                        heapq.heappush(
                            heap, (parsed[0], parsed[1], chunk_idx, next_line))

            total_time = time.time() - start_time
            print(f"\nMerge complete:")
            print(f"Total lines: {written_lines:,}")
            print(f"Total time: {self.format_time(total_time)}")

        finally:
            # Clean up
            print("\nCleaning up temporary files...")
            cleanup_start = time.time()
            for handle in chunk_handles:
                handle.close()
            for chunk_path in chunk_files:
                if os.path.exists(chunk_path):
                    os.remove(chunk_path)
            if os.path.exists(self.temp_dir):
                os.rmdir(self.temp_dir)
            print(f"Cleanup took {self.format_time(
                time.time() - cleanup_start)}")

    def sort_file(self, input_path: str, output_path: str):
        overall_start = time.time()
        try:
            print(f"Input file size: {os.path.getsize(
                input_path)/(1024*1024*1024):.2f}GB")

            print("\nPhase 1: Splitting into sorted chunks...")
            chunk_files = self.split_into_sorted_chunks(input_path)

            print("\nPhase 2: Merging chunks...")
            self.merge_chunks(chunk_files, output_path)

            total_time = time.time() - overall_start
            print(f"\nSort complete at {
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:")
            print(f"Output file size: {os.path.getsize(
                output_path)/(1024*1024*1024):.2f}GB")
            print(f"Total processing time: {self.format_time(total_time)}")

        except Exception as e:
            print(f"Error during sorting: {e}")
            raise e

    def format_time(self, seconds):
        """Convert seconds to human readable format"""
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f} minutes"
        else:
            hours = seconds / 3600
            return f"{hours:.1f} hours"
