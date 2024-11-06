import random
import string
import time


class Generator:
    def __init__(self):
        self.common_strings = [
            "Apple", "Banana", "Cherry", "Date", "Elderberry",
            "Something something something", "Test string", "Random text",
            "Common phrase", "Repeated line"
        ]
    
    def generate_line(self, use_common: bool = True) -> str:
        number = random.randint(1, 10**18)
        if use_common and random.random() < 0.3:
            text = random.choice(self.common_strings)
        else:
            length = random.randint(1, 100)
            text = ''.join(random.choices(string.ascii_letters + ' ', k=length))
        return f"{number}. {text}\n"
    
    def generate_file(self, target_size_bytes: int, output_path: str):
        start_time = time.time()
        written_bytes = 0
        last_progress_time = start_time
        
        with open(output_path, 'w') as f:
            while written_bytes < target_size_bytes:
                line = self.generate_line()
                f.write(line)
                written_bytes += len(line.encode('utf-8'))
                
                # Progress update every 5 seconds
                current_time = time.time()
                if current_time - last_progress_time >= 5:
                    elapsed = current_time - start_time
                    progress = written_bytes / target_size_bytes * 100
                    speed = written_bytes / (1024*1024) / elapsed  # MB/s
                    print(f"Generated {written_bytes/(1024*1024*1024):.2f}GB "
                          f"({progress:.1f}%) in {self.format_time(elapsed)} ")
                    last_progress_time = current_time

        total_time = time.time() - start_time
        print(f"\nFile generation complete:")
        print(f"Final size: {written_bytes/(1024*1024*1024):.2f}GB")
        print(f"Total time: {self.format_time(total_time)}")

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