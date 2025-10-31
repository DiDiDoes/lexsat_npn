import argparse
import os
import random
import time

from lexsat_npn import Formula, npn


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Profile NPN Methods")
    parser.add_argument(
        "--method",
        type=str,
        choices=["brute_force_tt", "flip_swap_tt", "sifting_tt", "flip_swap_lexsat", "sifting_lexsat"],
        required=True,
        help="NPN method to profile"
    )
    parser.add_argument(
        "--num-bit",
        type=int,
        default=4,
        help="Bit-width of the benchmarks to profile"
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=10,
        help="Number of repeats for averaging"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for selecting benchmarks"
    )
    args = parser.parse_args()
    assert args.num_bit in [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
    random.seed(args.seed)

    all_files = []
    root = os.path.expanduser(f"~/data/epfl_{args.num_bit}")
    benchmarks = os.listdir(root)
    for benchmark in benchmarks:
        aig_dir = os.path.join(root, benchmark)
        aig_files = [f for f in os.listdir(aig_dir) if f.endswith(".aig")]
        all_files.extend([os.path.join(aig_dir, f) for f in aig_files])

    total_time = 0.0
    total_trial = 0
    total_call = 0
    for _ in range(args.repeats):
        aig_file = random.choice(all_files)
        formula = Formula(aig_file)
        formula.build_cnf()
        start_time = time.time()
        best_truth_table, num_trial, num_call = npn(formula, args.method)
        end_time = time.time()
        total_time += end_time - start_time
        total_trial += num_trial
        total_call += num_call
    print(f"Bit-width: {args.num_bit}, Method: {args.method}, Repeats: {args.repeats}")
    print(f"Total Time: {total_time:.4f}s, Average Time: {total_time/args.repeats:.4f}s")
    print(f"Average Trials: {total_trial/args.repeats}, Average Speed: {total_time/total_trial*1000:.2f}ms")
    if total_call > 0:
        print(f"Average SAT Calls: {total_call/args.repeats}, Average Speed: {total_time/total_call*1000:.2f}ms")
