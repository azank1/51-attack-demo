# 51% Attack Demo

Blockchain security simulation with wallet cryptography, blockchain implementation, and consensus validation.

## Implementation

- **Wallet**: RSA and ECC key simulation with cracking attempts
- **Blockchain**: SHA-256 hashed blocks with transactions
- **Consensus Engine**: LEGACY_CBL and STAKE_CBL validation modes
- Two attack scenarios testing different security mechanisms

## How to Run

```bash
python3 sim.py
```

## Expected Output

```
==================================================
SCENARIO 1: Legacy Network (RSA + Static CBL)
==================================================
   [HACK] Factoring Alice's RSA Key... Success! Private Key Stolen.
   [ACTION] Eve creates Transaction: 'Alice -> Eve 100 BTC'
   [ACTION] Eve broadcasts chain length 4 (Honest is 2)...

   [CONSENSUS] Validating Fork under mode: LEGACY_CBL
      ❌ REJECTED: Static CBL Violation! Eve mined 3 blocks.
   [RESULT] Attack 1 FAILED. Funds Safe.

==================================================
SCENARIO 2: Improved Network (ECC + Stake-CBL)
==================================================
   [HACK] Attempting to crack Alice's ECC Key... FAILED.
   [INFO] Elliptic Curve cryptography is computationally secure.
   [ACTION] Eve cannot steal keys. Switches to Sybil Attack.
   [ACTION] Eve broadcasts Sybil chain (Length 5)...

   [CONSENSUS] Validating Fork under mode: STAKE_CBL
      ⚖️  Honest Weight: 10000
      ⚖️  Attacker Weight: 5200
      ❌ REJECTED: Insufficient Stake Weight (Sybil Detected).
   [RESULT] Attack 2 FAILED. Network Safe.
```
