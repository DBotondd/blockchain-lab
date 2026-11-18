"""Ismételhető PoW-mérés az eredeti blockchain.py implementációval."""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
from blockchain import Blockchain


def main():
    parser = argparse.ArgumentParser(description="PoW mérések CSV-be")
    parser.add_argument("--min", dest="lowest", type=int, default=1)
    parser.add_argument("--max", dest="highest", type=int, default=4)
    parser.add_argument("--repeats", type=int, default=9)
    parser.add_argument("--output", default="pow_uj.csv")
    args = parser.parse_args()
    if args.lowest < 0 or args.highest > 5 or args.lowest > args.highest:
        parser.error("A nehézségi szintek 0 és 5 között legyenek, min <= max.")
    if args.repeats < 1:
        parser.error("Legalább egy ismétlés szükséges.")
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["nehezseg", "ismetles", "probalkozasok", "futasido_ms"])
        for difficulty in range(args.lowest, args.highest + 1):
            for repeat in range(1, args.repeats + 1):
                chain = Blockchain(difficulty)  # genesis blokkot is bányássza; azt nem mérjük itt
                _, attempts, seconds = chain.add_block(f"pow-meres-{difficulty}-{repeat}")
                writer.writerow([difficulty, repeat, attempts, f"{seconds * 1000:.6f}"])
                print(f"nehézség={difficulty}, ismétlés={repeat}, próbálkozás={attempts}", flush=True)
    print("CSV elkészült:", path.resolve())

if __name__ == "__main__":
    main()
