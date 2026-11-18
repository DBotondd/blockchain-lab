"""Kiegészítő automatikus vizsgálatok a Blockchain Lab Python-moduljához."""
import unittest
from blockchain import Block, Blockchain, hash_text


class TestReszletesBlockchain(unittest.TestCase):
    def test_hash_ismetelhetoseg(self):
        self.assertEqual(hash_text('teszt'), hash_text('teszt'))

    def test_hash_megvaltozik_adatvaltozaskor(self):
        self.assertNotEqual(hash_text('teszt'), hash_text('Teszt'))

    def test_hash_utf8(self):
        self.assertEqual(len(hash_text('árvíztűrő tükörfúrógép')), 64)

    def test_genesis_blokk(self):
        chain = Blockchain(0)
        self.assertEqual(len(chain.blocks), 1)
        self.assertEqual(chain.blocks[0].previous_hash, '0' * 64)
        self.assertTrue(chain.validate()[0])

    def test_tobb_blokk_lancolasa(self):
        chain = Blockchain(1)
        chain.add_block('A'); chain.add_block('B'); chain.add_block('C')
        self.assertEqual(len(chain.blocks), 4)
        self.assertTrue(chain.validate()[0])
        self.assertTrue(all(chain.blocks[i].previous_hash == chain.blocks[i-1].hash for i in range(1,4)))

    def test_manipulacio_azonositja_blokkot(self):
        chain = Blockchain(1)
        chain.add_block('A'); chain.add_block('B')
        chain.tamper(1, 'X')
        valid, msg, index = chain.validate()
        self.assertFalse(valid)
        self.assertEqual(index, 1)

    def test_rossz_index_felismerese(self):
        chain = Blockchain(0)
        chain.add_block('A')
        chain.blocks[1].index = 99
        valid, _, index = chain.validate()
        self.assertFalse(valid)
        self.assertEqual(index, 1)

    def test_hibas_elozo_hash_felismerese(self):
        chain = Blockchain(0)
        chain.add_block('A')
        chain.blocks[1].previous_hash = 'f' * 64
        chain.blocks[1].hash = chain.blocks[1].calculate_hash()
        valid, msg, index = chain.validate()
        self.assertFalse(valid)
        self.assertEqual(index, 1)
        self.assertIn('előző hash', msg)

    def test_pow_nehezseg_egy_es_ketto(self):
        for difficulty in (1, 2):
            with self.subTest(difficulty=difficulty):
                chain = Blockchain(difficulty)
                block, attempts, _ = chain.add_block('teszt')
                self.assertTrue(block.hash.startswith('0' * difficulty))
                self.assertGreaterEqual(attempts, 1)
                self.assertTrue(chain.validate()[0])

    def test_ervenytelen_nehezseg(self):
        for difficulty in (-1, 6):
            with self.subTest(difficulty=difficulty):
                with self.assertRaises(ValueError):
                    Blockchain(difficulty)

    def test_nemletezo_blokk_modositasa(self):
        chain = Blockchain(0)
        with self.assertRaises(IndexError):
            chain.tamper(55, 'X')

    def test_mentett_hash_elterese(self):
        chain = Blockchain(0)
        chain.add_block('A')
        chain.blocks[1].hash = 'f' * 64
        valid, msg, _ = chain.validate()
        self.assertFalse(valid)
        self.assertIn('hash', msg)


if __name__ == '__main__':
    unittest.main()
