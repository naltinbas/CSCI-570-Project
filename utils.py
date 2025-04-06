import sys
import time
import psutil

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def time_wrapper(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    time_taken = (end_time- start_time)*1000
    return result, time_taken

def parse_input_file(filepath: str):
    """
    Parses the input file.
    Expected format:
      Line 1: Base string for the first sequence.
      Next several lines: Numeric indices for the first sequence.
      Next line: Base string for the second sequence.
      Remaining lines: Numeric indices for the second sequence.
    """
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip() != '']
    
    s1 = lines[0]
    indices1 = []
    i = 1
    while i < len(lines) and lines[i].isdigit():
        indices1.append(int(lines[i]))
        i += 1
    s2 = lines[i]
    i += 1
    indices2 = []
    while i < len(lines) and lines[i].isdigit():
        indices2.append(int(lines[i]))
        i += 1
    return s1, indices1, s2, indices2

def generate_string(base: str, indices: list):
    """
    Generates the final string from the base string by iteratively inserting
    a copy of the current string after the given index.
    """
    s = base
    for idx in indices:
        s = s[:idx+1] + s + s[idx+1:]
    return s
