# 51% Attack Demo: Blockchain Security Simulation

A Python simulation demonstrating blockchain vulnerabilities and defenses against 51% attacks, Sybil attacks, and cryptographic exploits.

## Overview

This educational simulation demonstrates how blockchain networks can be attacked and defended through two scenarios:

1. **Legacy Network (RSA + Static CBL)**: Shows vulnerability to RSA key cracking and 51% attacks
2. **Modern Network (ECC + Stake-CBL)**: Demonstrates enhanced security with ECC cryptography and stake-weighted consensus

## Components

### 1. Identity & Cryptography (`Wallet`)
- Simulates wallet owners with balances and cryptographic keys
- **RSA Keys**: Vulnerable to quantum/computational attacks (simulated)
- **ECC Keys**: Computationally secure against cracking attempts

### 2. Blockchain Database (`Block`, `Blockchain`)
- Simple blockchain implementation with SHA-256 hashing
- Tracks blocks with index, miner, transactions, and previous hash

### 3. Consensus Engine
Two consensus modes:

#### LEGACY_CBL (Consecutive Block Limit)
- Static limit: No miner can create more than 2 consecutive blocks
- Vulnerable to Sybil attacks (creating fake identities to bypass limits)
- Length-based chain selection

#### STAKE_CBL (Stake-Weighted CBL)
- Same consecutive block limit enforcement
- **Additional protection**: Validates total stake weight
- Rejects chains from low-stake attackers even if CBL rules are bypassed

## Attack Scenarios

### Scenario 1: RSA Vulnerability + 51% Attack
**Attack Vector:**
1. Eve cracks Alice's RSA private key
2. Creates fraudulent transaction stealing Alice's funds
3. Attempts to mine 3 consecutive blocks to override honest chain

**Defense:**
- Static CBL detects and rejects 3 consecutive blocks from Eve
- Attack fails despite stolen keys

### Scenario 2: Sybil Attack on Static CBL
**Attack Vector:**
1. Eve attempts to crack Alice's ECC key (fails)
2. Creates multiple fake identities (Eve_A, Eve_B)
3. Alternates mining between identities to bypass CBL
4. Broadcasts longer chain to override honest network

**Defense:**
- Stake-weighted validation checks total economic weight
- Eve's combined stake (200) < Alice's stake (5000)
- Attack rejected despite bypassing con
secutive block limits

## Running the Simulation

```bash
python3 sim.py
```

## Key Takeaways

✅ **ECC > RSA**: Elliptic curve cryptography provides better security
✅ **Stake-weighting matters**: Economic stake prevents Sybil attacks
✅ **Multi-layer defense**: Combining cryptography, CBL, and stake validation creates robust security
⚠️ **Static limits alone are insufficient**: Identity-based limits can be bypassed

## Technical Details

- **Language**: Python 3
- **Dependencies**: Standard library only (`hashlib`, `time`, `copy`)
- **Educational Purpose**: Demonstrates blockchain security concepts, not production code

## License

Educational demonstration code.