from utils import *

class SequenceAlignment:
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
        self.OPT = None
        
    def bottom_up(self):
        rows, cols = len(self.seq1) + 1, len(self.seq2) + 1
        
        OPT = [[0 for _ in range(cols)] for _ in range(rows)]
        
        # Base Case
        for i in range(rows):
            OPT[i][0] = i * self.gap_penalty
        
        for j in range(cols):
            OPT[0][j] = j * self.gap_penalty
            
        
        # Bottom Up Pass
        for i in range(1, rows):
            for j in range(1, cols):
                cost = self.mismatch[self.seq1[i-1]][self.seq2[j-1]]
                match_mismatch = OPT[i-1][j-1] + cost
                insert_gap = OPT[i-1][j] + self.gap_penalty
                delete_gap = OPT[i][j-1] + self.gap_penalty

                OPT[i][j] = min(match_mismatch, insert_gap, delete_gap)

        self.OPT = OPT
        return OPT
    
    def traceback(self):
        if self.OPT is None:
            raise ValueError("Run bottom_up() first to compute the alignment matrix!")

        i, j = len(self.seq1), len(self.seq2)
        aligned_seq1 = []
        aligned_seq2 = []

        while i > 0 or j > 0:
            if i > 0 and j > 0 and self.OPT[i][j] == self.OPT[i-1][j-1] + self.mismatch[self.seq1[i-1]][self.seq2[j-1]]:
                aligned_seq1.append(self.seq1[i-1])
                aligned_seq2.append(self.seq2[j-1])
                i -= 1
                j -= 1
            elif i > 0 and self.OPT[i][j] == self.OPT[i-1][j] + self.gap_penalty:
                # Upward move (gap in seq2)
                aligned_seq1.append(self.seq1[i-1])
                aligned_seq2.append('_')  # Gap in seq2
                i -= 1
            else:
                # Left move (gap in seq1)
                aligned_seq1.append('_')  # Gap in seq1
                aligned_seq2.append(self.seq2[j-1])
                j -= 1

        return ''.join(aligned_seq1[::-1]), ''.join(aligned_seq2[::-1])
    
    def run(self):
        self.bottom_up()
        aligned_seq1, aligned_seq2 = self.traceback()
        return self.OPT[-1][-1], aligned_seq1, aligned_seq2


def main(input_file, output_file):
    s1_base, indices1, s2_base, indices2 = parse_input_file(input_file)
    
    j = len(indices1)
    k = len(indices2)
    if j > 10 or k > 10:
        with open(output_file, 'w') as f:
            f.write("Cannot process")
        return
    
    s1_generated = generate_string(s1_base, indices1)
    s2_generated = generate_string(s2_base, indices2)
    
    if len(s1_generated) < 1 or len(s1_generated) > 2000 or len(s2_generated) < 1 or len(s2_generated) > 2000:
        with open(output_file, 'w') as f:
            f.write("Cannot process")
        return
    
    mem_before = process_memory()
    
    aligner = SequenceAlignment(s1_generated, s2_generated)
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
        print("Usage: python basic_3.py <input_file> <output_file>")
    else:
        main(sys.argv[1], sys.argv[2])