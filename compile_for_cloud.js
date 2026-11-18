// Docker build: Solidity 0.8.20 --> ABI + bytecode for the online demo.
// This is compiled from the exact same two-contract source used locally.
const fs = require('fs');
const crypto = require('crypto');
const path = require('path');
const solc = require('solc');

const solPath = path.join(__dirname, 'solidity', 'Tanusitvanyok.sol');
const artifactPath = path.join(__dirname, 'solidity', 'compiled_contracts.json');
const sourceBuffer = fs.readFileSync(solPath);
const source = sourceBuffer.toString('utf8');
const version = solc.version();
if (!version.startsWith('0.8.20')) throw new Error('Expected Solidity 0.8.20, got ' + version);
const input = {
  language: 'Solidity',
  sources: { 'Tanusitvanyok.sol': { content: source } },
  settings: {
    optimizer: { enabled: true, runs: 200 },
    outputSelection: { '*': { '*': [ 'abi', 'evm.bytecode.object' ] } }
  }
};
const output = JSON.parse(solc.compile(JSON.stringify(input)));
const errors = output.errors || [];
for (const err of errors) console.log((err.severity || 'info') + ': ' + err.formattedMessage);
if (errors.some(err => err.severity === 'error')) process.exit(1);
const compiled = {};
const contracts = output.contracts['Tanusitvanyok.sol'];
for (const [name, contract] of Object.entries(contracts)) {
  compiled['<stdin>:' + name] = { abi: contract.abi, bin: contract.evm.bytecode.object };
}
for (const name of ['TanusitvanyKezelo', 'TanusitvanyTarolo']) {
  if (!compiled['<stdin>:' + name]) throw new Error('Missing compiled contract ' + name);
}
fs.writeFileSync(artifactPath, JSON.stringify({
  source_sha256: crypto.createHash('sha256').update(sourceBuffer).digest('hex'),
  solc_version: version,
  compiled
}, null, 2) + '\n');
console.log('Solidity 0.8.20 compiled and cached for Render.');
