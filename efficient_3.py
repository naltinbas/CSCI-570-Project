from utils import *
from basic_3 import SequenceAlignment

class MemoryEfficientSA:
    def __init__(self, seq1: str, seq2: str, gap_penalty: int = 30, mismatch_table: dict = None):
        self.seq1 = list(seq1)
        self.seq2 = list(seq2)
        self.gap_penalty = gap_penalty
        if mismatch_table is None:
            mismatch_table = {
                'A': {'A': 0,   'C': 110, 'G': 48,  'T': 94},
                'C': {'A': 110, 'C': 0,   'G': 118, 'T': 48},
                'G': {'A': 48,  'C': 118, 'G': 0,   'T': 110},
                'T': {'A': 94,  'C': 48,  'G': 110, 'T': 0}
            }
        self.mismatch = mismatch_table

    def compute_last_row(self, x, y):
        prev = [j * self.gap_penalty for j in range(len(y) + 1)]
        for i in range(1, len(x) + 1):
            curr = [0] * (len(y) + 1)
            curr[0] = i * self.gap_penalty
            for j in range(1, len(y) + 1):
                cost = self.mismatch[x[i - 1]][y[j - 1]]
                curr[j] = min(prev[j - 1] + cost,
                              prev[j] + self.gap_penalty,
                              curr[j - 1] + self.gap_penalty)
            prev = curr
        return prev

    def alignment(self, x, y):
        if len(x) == 0:
            return ('_' * len(y), ''.join(y))
        if len(y) == 0:
            return (''.join(x), '_' * len(x))
        # Base case: if either sequence is very short, use full DP
        if len(x) <= 1 or len(y) <= 1:
            sa = SequenceAlignment(''.join(x), ''.join(y),
                                   gap_penalty=self.gap_penalty,
                                   mismatch_table=self.mismatch)
            _, aligned_x, aligned_y = sa.run()
            return aligned_x, aligned_y

        mid = len(x) // 2
        x_left = x[:mid]
        x_right = x[mid:]

        # Compute cost from left part
        left_cost = self.compute_last_row(x_left, y)
        # Compute cost from right part (using reversed sequences)
        right_cost = self.compute_last_row(x_right[::-1], y[::-1])[::-1]

        # Find the best split point in y.
        min_cost = float('inf')
        split_index = 0
        for k in range(len(y) + 1):
            if left_cost[k] + right_cost[k] < min_cost:
                min_cost = left_cost[k] + right_cost[k]
                split_index = k

        left_alignment = self.alignment(x_left, y[:split_index])
        right_alignment = self.alignment(x_right, y[split_index:])

        return (left_alignment[0] + right_alignment[0],
                left_alignment[1] + right_alignment[1])

    def run(self):
        if len(self.seq1)>len(self.seq2):
            aligned_seq2, aligned_seq1 = self.alignment(self.seq2, self.seq1)
            cost = self.compute_last_row(self.seq2, self.seq1)[-1]
        else:
            aligned_seq1, aligned_seq2 = self.alignment(self.seq1, self.seq2)
            cost = self.compute_last_row(self.seq1, self.seq2)[-1]
        return cost, aligned_seq1, aligned_seq2
        

def main(input_file, output_file):
    s1_base, indices1, s2_base, indices2 = parse_input_file(input_file)
    s1_generated = generate_string(s1_base, indices1)
    s2_generated = generate_string(s2_base, indices2)
    
    mem_before = process_memory()
    
    aligner = MemoryEfficientSA(s1_generated, s2_generated)
    (alignment_cost, aligned_seq1, aligned_seq2), time_taken = time_wrapper(aligner.run)
    
    mem_after = process_memory()
    memory_used = mem_after - mem_before
    
    with open(output_file, 'w') as f:
        f.write(f'{alignment_cost}\n')
        f.write(aligned_seq1 + "\n")
        f.write(aligned_seq2 + "\n")
        f.write(f'{time_taken}\n')
        f.write(f'{memory_used}')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python efficient_3.py <input_file> <output_file>")
    else:
        main(sys.argv[1], sys.argv[2])