"""Solidity szerződések futtatása helyi Ganache Ethereum tesztláncon.

A Ganache külön Node.js folyamat, amelyet szükség esetén innen indítunk.
Nem használ eth-tester / py-evm / safe-pysha3 csomagot.
"""
from pathlib import Path
import atexit
import os
import subprocess
import time

SOLC_VERSION = '0.8.20'
ROOT = Path(__file__).resolve().parent
SOLIDITY_FILE = ROOT / 'solidity' / 'Tanusitvanyok.sol'
RPC_URL = 'http://127.0.0.1:18545'
GANACHE_PROCESS = None


class CertificateAlreadyExistsError(ValueError):
    """A megadott tanusitvany lenyomata mar szerepel a szerzodesben."""



def compile_contracts():
    # A felhős Docker-kép a Solidityt build időben fordítja solc-js 0.8.20-szal.
    # Ez csökkenti a futás közbeni memóriahasználatot; a helyi fejlesztői
    # példányban továbbra is működik az eredeti py-solc-x fordítás.
    import hashlib
    import json
    artifact_file = ROOT / 'solidity' / 'compiled_contracts.json'
    if artifact_file.is_file():
        artifact = json.loads(artifact_file.read_text(encoding='utf-8'))
        source_hash = hashlib.sha256(SOLIDITY_FILE.read_bytes()).hexdigest()
        if artifact.get('source_sha256') != source_hash:
            raise RuntimeError('A Solidity-forrás megváltozott a Docker build óta; új telepítés szükséges.')
        if not str(artifact.get('solc_version', '')).startswith(SOLC_VERSION):
            raise RuntimeError('A Solidity-fordító verziója eltér a várt 0.8.20-tól.')
        return artifact['compiled']
    from solcx import compile_source, get_installed_solc_versions, install_solc
    if SOLC_VERSION not in {str(v) for v in get_installed_solc_versions()}:
        install_solc(SOLC_VERSION)
    code = SOLIDITY_FILE.read_text(encoding='utf-8')
    return compile_source(code, output_values=['abi', 'bin'], solc_version=SOLC_VERSION,
                          optimize=True)


def _stop_ganache():
    global GANACHE_PROCESS
    if GANACHE_PROCESS is not None and GANACHE_PROCESS.poll() is None:
        GANACHE_PROCESS.terminate()
        try:
            GANACHE_PROCESS.wait(timeout=3)
        except subprocess.TimeoutExpired:
            GANACHE_PROCESS.kill()
    GANACHE_PROCESS = None


class CertificateAlreadyExistsError(ValueError):
    """A megadott tanusitvany lenyomata mar szerepel a szerzodesben."""



atexit.register(_stop_ganache)


def _ganache_executable():
    candidate = ROOT / 'node_modules' / '.bin' / ('ganache.cmd' if os.name == 'nt' else 'ganache')
    if not candidate.is_file():
        raise RuntimeError(
            'A Ganache még nincs telepítve. A projekt mappájában futtasd: npm install. '
            'Ha az npm parancs nem létezik: winget install OpenJS.NodeJS.LTS'
        )
    return str(candidate)


def start_local_chain():
    """Helyi lánc indítása; egy meglévő, működő szervert újra felhasználunk."""
    global GANACHE_PROCESS
    from web3 import Web3
    w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={'timeout': 8}))
    if w3.is_connected():
        return w3
    if GANACHE_PROCESS is not None and GANACHE_PROCESS.poll() is None:
        raise RuntimeError('A Ganache folyamat fut, de a tesztlánc nem válaszol.')
    executable = _ganache_executable()
    command = [executable, '--server.host', '127.0.0.1', '--server.port', '18545',
               '--wallet.totalAccounts', '3', '--logging.quiet']
    GANACHE_PROCESS = subprocess.Popen(command, cwd=str(ROOT), stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL)
    for _ in range(40):
        if GANACHE_PROCESS.poll() is not None:
            raise RuntimeError('A Ganache váratlanul leállt. Ellenőrizd az npm install telepítést.')
        try:
            if w3.is_connected():
                return w3
        except Exception:
            pass
        time.sleep(0.25)
    _stop_ganache()
    raise RuntimeError('A helyi Ganache tesztlánc nem indult el (127.0.0.1:18545).')


def new_demo():
    """Solidity fordítása és a két szerződés telepítése valódi helyi EVM-re."""
    compiled = compile_contracts()
    w3 = start_local_chain()
    account = w3.eth.accounts[0]
    w3.eth.default_account = account
    iface = compiled['<stdin>:TanusitvanyKezelo']
    factory = w3.eth.contract(abi=iface['abi'], bytecode=iface['bin'])
    receipt = w3.eth.wait_for_transaction_receipt(factory.constructor().transact({'from': account}), timeout=60)
    if receipt.status != 1:
        raise RuntimeError('A szerződés telepítése sikertelen tranzakcióval zárult.')
    manager = w3.eth.contract(address=receipt.contractAddress, abi=iface['abi'])
    storage_address = manager.functions.tarolo().call()
    return {'w3': w3, 'account': account, 'manager': manager,
            'manager_address': receipt.contractAddress, 'storage_address': storage_address,
            'events': [], 'deploy_tx': receipt.transactionHash.hex()}


def register(demo, value):
    if not value.strip():
        raise ValueError('Üres tanúsítvány nem regisztrálható.')
    # A varhato duplikatumot a tranzakcio elott jelezzuk.
    # Ez csak a felhasznaloi elmenyt javitja; a Solidity require tovabbra is ved.
    if verify(demo, value):
        raise CertificateAlreadyExistsError('Ez a tanúsítvány már regisztrálva van.')
    tx = demo['manager'].functions.regisztral(value).transact({'from': demo['account']})
    receipt = demo['w3'].eth.wait_for_transaction_receipt(tx, timeout=60)
    if receipt.status != 1:
        raise RuntimeError('A tanúsítvány regisztrációja sikertelen.')
    result = {'Tanúsítvány': value,
              'Hash (Keccak-256)': demo['w3'].to_hex(demo['manager'].functions.lenyomat(value).call()),
              'Tranzakció': receipt.transactionHash.hex(), 'Blokk': receipt.blockNumber,
              'Gázfelhasználás': receipt.gasUsed}
    demo['events'].append(result)
    return result


def verify(demo, value):
    return bool(demo['manager'].functions.ellenoriz(value).call())


def count(demo):
    return int(demo['manager'].functions.regisztraciokSzama().call())
