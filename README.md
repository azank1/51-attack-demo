# 51% Attack Simulation - Blockchain Security Demo

Interactive web-based demonstration of blockchain attacks and defenses from the attacker's perspective.

## Quick Start

### Install Dependencies
```bash
pip install flask flask-cors
```

### Run Web Server
```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

## Understanding the Attack

### The Problem: 51% Attack
An attacker (Eve) with majority hash power can:
1. **Crack weak RSA keys** - Factor small primes to steal private keys
2. **Mine a longer secret chain** - Create blocks faster than honest miners
3. **Double spend** - Broadcast the longer chain to reverse transactions

### Attack Sequence
**Note**: You can perform attacks in any order! Key cracking is optional.
- **Option A (Realistic 51% Attack)**: Acquire 51% hash power → Mine blocks with your own coins → Broadcast
- **Option B (Combined Attack)**: Crack RSA Key → Acquire 51% hash power → Mine blocks with stolen coins → Broadcast

## Understanding the Defense

### Defense 1: Consecutive Block Limit (CBL) - Basic
- **Rule**: No miner can mine more than 2 consecutive blocks
- **Effect**: Blocks Eve's 51% attack (she mines 3 blocks)
- **Limitation**: Can be bypassed with Sybil attack (alternating miners)

### Defense 2: ECC + Stake-Weighted CBL
- **ECC Cryptography**: Prevents key theft (computationally secure)
- **Stake-Weighted CBL**: Validates chain by economic weight, not just length
- **Slashing**: Attackers lose stake when caught
- **Effect**: Blocks both key theft and Sybil attacks

## How to Use the Web Interface

### Left Panel (Attacker - Eve)
- **Crack RSA Key**: Factor victim's public key
- **51% Attack**: Mine longer chain with double spend
- **Double Spend (Bob)**: Attack different victim
- **Sybil Attack**: Use multiple identities to bypass CBL

### Right Panel (Network Defense)
- **Enable CBL (Basic)**: Activate Consecutive Block Limit defense
- **Enable ECC + Stake**: Upgrade to full security with slashing

### Center Panel
- **Blockchain Visualization**: Interactive graph showing honest (blue) and attack (red) chains
- **Genesis Block**: Highlighted with special border

## Demo Scenarios

### Scenario 1: Bitcoin Vulnerability (LEGACY Mode)
**Goal**: Demonstrate how a basic 51% attack succeeds on unprotected Bitcoin

**Steps**:
1. **Acquire 51% Hash Power** → Click "Acquire 51% Hash" (rents from cloud mining)
2. **Mine Attack Blocks** → Click "Mine 3 Blocks" (uses Eve's own coins - no key cracking needed!)
3. **Broadcast Chain** → Click "Broadcast Chain"

**Result**: ✅ Attack succeeds (demonstrates vulnerability)

**Explain**: "This shows how 51% attacks work on unprotected Bitcoin. Eve doesn't need to crack keys - she can double-spend her own coins using majority hash power."

**Optional**: You can also crack Alice's key first to demonstrate theft attack, but it's not required.

---

### Scenario 2: CBL Defense Blocks Attack
**Goal**: Show how Consecutive Block Limit (CBL) prevents 51% attacks

**Steps**:
1. **Enable CBL Defense** → Click "Enable CBL"
2. **Acquire 51% Hash Power** → Click "Acquire 51% Hash"
3. **Mine 3 Blocks** → Click "Mine 3 Blocks" (all consecutive blocks by Eve)
4. **Broadcast Chain** → Click "Broadcast Chain"

**Result**: ❌ Attack blocked (CBL prevents consecutive mining)

**Explain**: "CBL catches the attack by limiting consecutive blocks. Eve mined 3 consecutive blocks, which violates the limit of 2."

---

### Scenario 3: Sybil Attack Bypasses CBL
**Goal**: Show how attackers bypass CBL using multiple identities

**Steps**:
1. **Ensure CBL is Enabled** (from Scenario 2)
2. **Enable Sybil Attack** → Click "Enable Sybil" (creates Eve_A and Eve_B)
3. **Acquire 51% Hash Power** → Click "Acquire 51% Hash"
4. **Mine 3 Blocks** → Click "Mine 3 Blocks" (blocks appear in purple - alternating miners)
5. **Broadcast Chain** → Click "Broadcast Chain"

**Result**: ✅ Attack succeeds (Sybil bypasses CBL)

**Explain**: "Multiple identities bypass CBL by alternating miners. Notice the purple blocks - Eve_A, Eve_B, Eve_A. Since they're different miners, CBL doesn't catch it."

---

### Scenario 4: ZK Stake-CBL Defense
**Goal**: Show how Zero Knowledge stake validation prevents Sybil attacks

**Steps**:
1. **Enable ZK Stake-CBL** → Click "Enable ZK Stake-CBL"
2. **Acquire 51% Hash Power** → Click "Acquire 51% Hash"
3. **Mine 3 Blocks** → Click "Mine 3 Blocks" (with Sybil still active)
4. **Broadcast Chain** → Click "Broadcast Chain"

**Result**: ❌ Attack blocked (ZK stake prevents Sybil)

**Explain**: "ZK stake validates without revealing amounts or identities. Even with Sybil, Eve's total stake is low compared to honest miners + whale backing. The attack is rejected and Eve's stake is slashed."

---

### Scenario 5: ECC Upgrade
**Goal**: Show how ECC prevents key cracking

**Steps**:
1. **Enable ECC** → Click "Enable ECC"
2. **Try to Crack Key** → Click "Crack RSA Key"

**Result**: ❌ Key cracking fails (ECC is secure)

**Explain**: "ECC prevents key theft unlike weak RSA. There's no known efficient algorithm to break ECC cryptography."

---

### Scenario 6: Complete Defense
**Goal**: Show comprehensive defense combining all mechanisms

**Steps**:
1. **Enable Complete Defense** → Click "Enable ZK Stake-CBL" (combines ZK stake + ECC + CBL)
2. **Try All Attacks** → Try each attack button - all should fail:
   - Crack RSA Key → Fails (ECC)
   - Mine 3 Blocks → Fails (CBL)
   - Broadcast Chain → Fails (ZK Stake)

**Result**: ❌ All attacks blocked

**Explain**: "Comprehensive defense combining ECC (prevents key cracking), CBL (prevents consecutive mining), and ZK Stake (prevents Sybil attacks while protecting privacy)."

---

## Demo Flow Summary

1. **Start**: Network is vulnerable (no defenses)
2. **Scenario 1**: Basic 51% attack succeeds (no key cracking needed!)
3. **Scenario 2**: Enable CBL → Attack blocked
4. **Scenario 3**: Enable Sybil → Attack succeeds (bypasses CBL)
5. **Scenario 4**: Enable ZK Stake-CBL → Attack blocked
6. **Scenario 5**: Enable ECC → Key cracking fails
7. **Scenario 6**: Complete defense → All attacks blocked

## Key Concepts

- **RSA Vulnerability**: Small primes (p=61, q=53) can be factored quickly
- **51% Attack**: Mining longer chain allows double spending
- **CBL Defense**: Limits consecutive blocks per miner (catches 51% but not Sybil)
- **Sybil Attack**: Multiple identities bypass basic CBL
- **Stake-Weighted CBL**: Economic weight prevents Sybil attacks
- **Stake Slashing**: Attackers lose stake when caught
- **ECC Security**: Elliptic curve cryptography prevents key theft

## Files

- `app.py` - Flask web server backend
- `templates/index.html` - Web interface
- `static/css/style.css` - Styling
- `static/js/app.js` - Frontend logic and visualization
- `51%ATTACK.md` - Complete software specification and architecture
- `requirements.txt` - Python dependencies
- `start_server.bat` / `start_server.sh` - Server startup scripts

## Requirements

- Python 3.7+
- Flask, flask-cors
- Modern web browser (Chrome, Firefox, Edge)

## Architecture

- **Backend**: Flask REST API with OOP blockchain simulation
- **Frontend**: Modern HTML/CSS/JavaScript with vis.js for graph visualization
- **Real-time Updates**: Polling-based state synchronization
- **Interactive**: Click buttons to trigger attacks and defenses
