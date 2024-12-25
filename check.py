import argparse
import logging as log
import subprocess
import sys
import time
from itertools import zip_longest
from pathlib import Path

from tqdm import tqdm


def setupLogging():
    log.basicConfig(
        level=log.INFO,
        format="[%(levelname)s] %(message)s",
        handlers=[log.StreamHandler(sys.stdout)],
    )

    log.addLevelName(log.CRITICAL, "\033[91m%s\033[0m" % log.getLevelName(log.CRITICAL))
    log.addLevelName(log.ERROR, "\033[91m%s\033[0m" % log.getLevelName(log.ERROR))
    log.addLevelName(log.WARNING, "\033[93m%s\033[0m" % log.getLevelName(log.WARNING))
    log.addLevelName(log.INFO, "\033[94m%s\033[0m" % log.getLevelName(log.INFO))
    log.addLevelName(log.DEBUG, "\033[90m%s\033[0m" % log.getLevelName(log.DEBUG))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("program", type=Path, help="program to run")
    parser.add_argument("--input", "-i", type=Path, nargs="+", help="input files")
    parser.add_argument("--output", "-o", type=Path, nargs="+", help="output files")
    args = parser.parse_args()

    setupLogging()

    PROGRAM: Path = args.program
    INPUT: list[Path] = args.input
    OUTPUT: list[Path] = args.output

    if len(INPUT) == 1 and INPUT[0].is_dir():
        INPUTS = list(INPUT[0].glob("*"))

    if len(OUTPUT) == 1 and OUTPUT[0].is_dir():
        OUTPUTS = list(OUTPUT[0].glob("*"))

    if not len(INPUTS) == len(OUTPUTS):
        raise ValueError("Number of input files must be equal to number of output files")
    if not PROGRAM.exists():
        raise FileNotFoundError(f"Program {PROGRAM} not found")

    failed: list[tuple[Path, Path, str, str, str]] = []
    results: list[tuple[Path, Path, float]] = []

    INPUTS = sorted(INPUTS)
    OUTPUTS = sorted(OUTPUTS)

    for input_file, output_file in tqdm(zip(INPUTS, OUTPUTS), leave=False, desc="Checking inputs", total=len(INPUTS)):
        if not input_file.exists():
            failed.append((input_file, output_file, f"Input file {input_file} not found", None, None))
        if not output_file.exists():
            failed.append((input_file, output_file, f"Output file {output_file} not found", None, None))

        expected_output = output_file.read_text()

        # Run the program, then, the stdin is the input file, and the stdout is
        # to be compared with the output file
        with open(input_file, "r") as f:
            input_data = f.read()
        try:
            start = time.time()
            result = subprocess.run(
                [sys.executable, PROGRAM], input=input_data, text=True, capture_output=True, timeout=5
            )
            end = time.time()
        except subprocess.TimeoutExpired as e:
            failed.append(
                (input_file, output_file, f"Program {PROGRAM} timed out", expected_output, e.stdout + "\n" + e.stderr)
            )
            continue
        except subprocess.CalledProcessError as e:
            failed.append(
                (
                    input_file,
                    output_file,
                    f"Program {PROGRAM} failed with return code {e.returncode}",
                    expected_output,
                    e.stdout + "\n" + e.stderr,
                )
            )
            continue

        if result.stdout != expected_output:
            failed.append(
                (input_file, output_file, f"Output mismatch", expected_output, result.stdout + "\n" + result.stderr)
            )
        else:
            results.append((input_file, output_file, end - start))

    if failed:
        log.error("Failed tests:")
        for input_file, output_file, reason, expected_output, found_output in failed:
            log.error(f"  {reason} : (in) {input_file} > (out) {output_file}")
            if expected_output is not None and found_output is not None:
                # Print them in two columns
                expected_lines = ["Expected:"] + expected_output.splitlines()
                found_lines = ["Found:"] + found_output.splitlines()

                maxlen = max(len(line) for line in expected_lines)

                for expected_line, found_line in zip_longest(expected_lines, found_lines, fillvalue=""):
                    log.error(f"  {expected_line.ljust(maxlen)} | {found_line}")
    else:
        log.info("All tests passed")
        log.info("Results:")
        for input_file, output_file, time_taken in results:
            log.info(f"Input: {input_file}, Output: {output_file}, Time taken: {time_taken:.3f}s")
        log.info(f"Average time taken: {sum(time_taken for _, _, time_taken in results) / len(results):.3f}s")

    log.info(f"Passed: {len(results)}, Failed: {len(failed)}")
