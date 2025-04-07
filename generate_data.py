from pathlib import Path
import re
from utils import *
import basic_3
import efficient_3

datapoints_dir = Path("./datapoints")
output_dir = Path("./outputs")
results_file = Path("./results.txt")

output_dir.mkdir(exist_ok=True)

input_files = sorted([f for f in datapoints_dir.glob("*.txt")], key=lambda x: int(re.search(r'(\d+)', x.name).group(1)) if re.search(r'(\d+)', x.name) else 0)

results = []

for input_file in input_files:
    input_name = input_file.name
    basic_output = output_dir / f"basic_{input_name}"
    efficient_output = output_dir / f"efficient_{input_name}"
    
    print(f"Processing {input_name}...")
    
    s1_base, indices1, s2_base, indices2 = parse_input_file(input_file)
    s1_generated = generate_string(s1_base, indices1)
    s2_generated = generate_string(s2_base, indices2)
    
    m_plus_n = len(s1_generated) + len(s2_generated)
    
    basic_3.main(str(input_file), str(basic_output))
    print(f"  basic_3.py executed successfully for {input_name}")
    
    efficient_3.main(str(input_file), str(efficient_output))
    print(f"  efficient_3.py executed successfully for {input_name}")
    
    basic_time = "N/A"
    basic_memory = "N/A"
    if basic_output.exists():
        try:
            with open(basic_output, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 5:
                    basic_time = lines[3].strip()
                    basic_memory = lines[4].strip()
        except Exception as e:
            print(f"Error reading {basic_output}: {e}")
    
    efficient_time = "N/A"
    efficient_memory = "N/A"
    if efficient_output.exists():
        try:
            with open(efficient_output, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 5:
                    efficient_time = lines[3].strip()
                    efficient_memory = lines[4].strip()
        except Exception as e:
            print(f"Error reading {efficient_output}: {e}")
    
    results.append((m_plus_n, basic_time, efficient_time, basic_memory, efficient_memory))

try:
    results.sort(key=lambda x: int(x[0]))
except ValueError:
    results.sort(key=lambda x: str(x[0]))


row_format = "{:<10}{:<20}{:<20}{:<20}{:<20}\n"

with open(results_file, 'w') as f:
    f.write(row_format.format("M+N", "Time in MS", "Time in MS", "Memory in KB", "Memory in KB"))
    f.write(row_format.format("", "(Basic)", "(Efficient)", "(Basic)", "(Efficient)"))
    f.write("-" * 90 + "\n")
    
    for m_plus_n, basic_time, efficient_time, basic_memory, efficient_memory in results:
        f.write(row_format.format(m_plus_n, basic_time, efficient_time, basic_memory, efficient_memory))

print(f"Results saved to {results_file}")