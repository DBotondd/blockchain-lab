"""Ismételhető PoW-kísérlet; CSV-be menti a mért kimenetet."""
import csv
from blockchain import Blockchain

with open('pow_meres_eredmenyek.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['nehezseg','ismetles','probalkozasok','futasido_ms'])
    for diff in (0,1,2):
        for trial in range(1, 11):
            chain = Blockchain(diff)
            block, attempts, seconds = chain.add_block(f'meres-{diff}-{trial}')
            writer.writerow([diff, trial, attempts, f'{seconds*1000:.4f}'])
print('30 PoW mérés CSV-be mentve.')
