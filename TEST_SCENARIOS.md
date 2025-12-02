# Test Scenarios - Verification Guide

## Overview
This document describes how to test all scenarios and verify the terminal shows real execution logic.

## Terminal Panel Features
The terminal panel at the bottom shows:
- **Real execution steps** with timestamps
- **Function call stack** showing which functions are executing
- **Code snippets** showing actual code logic being executed
- **Security context** explaining what's happening
- **Blockchain state** proving the graph is real (not mocked)

## Test Scenarios

### Scenario 1: Basic 51% Attack (LEGACY Mode)
**Goal**: Demonstrate Bitcoin vulnerability - attack succeeds

**Steps**:
1. Click "Crack RSA Key" → Terminal shows RSA factorization steps
2. Click "Acquire 51% Hash" → Terminal shows cloud mining rental steps
3. Click "Mine 3 Blocks" → Terminal shows block mining logic
4. Click "Broadcast Chain" → Terminal shows chain validation logic

**Expected Terminal Output**:
- RSA cracking: Factorization algorithm, phi(n) calculation, private key derivation
- 51% acquisition: Cloud mining rental method explanation
- Block mining: Block creation with transactions
- Chain validation: PoW check, chain length comparison
- Result: "Attack chain accepted" (attack succeeds)

**Verify**: Terminal shows real code execution, not mocked responses

---

### Scenario 2: CBL Defense Blocks Attack
**Goal**: CBL prevents consecutive mining attacks

**Steps**:
1. Click "Enable CBL" → Terminal shows CBL activation
2. Click "Crack RSA Key"
3. Click "Acquire 51% Hash"
4. Click "Mine 3 Blocks" → Terminal shows CBL check
5. Click "Broadcast Chain" → Terminal shows CBL violation

**Expected Terminal Output**:
- CBL activation: Defense mode set to CBL
- Block mining: Shows consecutive block check
- Chain validation: "CBL violation: Eve mined 3 consecutive blocks (limit: 2)"
- Result: "Chain rejected" (attack blocked)

**Verify**: Terminal shows CBL validation logic with actual block miner checks

---

### Scenario 3: Sybil Attack Bypasses CBL
**Goal**: Multiple identities bypass Static CBL

**Steps**:
1. Ensure CBL is enabled (from Scenario 2)
2. Click "Enable Sybil" → Terminal shows Sybil identity creation
3. Click "Crack RSA Key"
4. Click "Acquire 51% Hash"
5. Click "Mine 3 Blocks" → Terminal shows alternating miners (Eve_A, Eve_B)
6. Click "Broadcast Chain" → Terminal shows CBL check passes

**Expected Terminal Output**:
- Sybil activation: Eve_A and Eve_B identities created
- Block mining: Shows alternating miners (Eve_A → Eve_B → Eve_A)
- CBL check: "No consecutive block violation" (different miners)
- Result: "Attack chain accepted" (Sybil bypasses CBL)

**Verify**: Terminal shows real Sybil miner alternation logic

---

### Scenario 4: ZK Stake-CBL Defense
**Goal**: Zero Knowledge stake validation prevents Sybil attacks

**Steps**:
1. Click "Enable ZK Stake-CBL" → Terminal shows ZK proof initialization
2. Click "Crack RSA Key" (should fail if ECC enabled)
3. Click "Acquire 51% Hash"
4. Click "Mine 3 Blocks" (with Sybil)
5. Click "Broadcast Chain" → Terminal shows ZK stake weight check

**Expected Terminal Output**:
- ZK activation: ZK proofs created (stake amounts hidden)
- ZK stake check: "Attack ZK weight: X, Honest ZK weight: Y (whale backing hidden)"
- Result: "Insufficient ZK stake weight" (attack blocked)

**Verify**: Terminal shows ZK proof validation without revealing stake amounts

---

### Scenario 5: ECC Upgrade
**Goal**: ECC prevents RSA key cracking

**Steps**:
1. Click "Enable ECC" → Terminal shows wallet upgrade to ECC
2. Click "Crack RSA Key" → Terminal shows ECC cracking attempt fails

**Expected Terminal Output**:
- ECC upgrade: All wallets upgraded to ECC (secp256k1)
- RSA crack attempt: "ECC key cracking failed" (as expected)
- Result: Key remains secure

**Verify**: Terminal shows ECC upgrade logic and failed cracking attempt

---

### Scenario 6: Complete ZK Stake-CBL Network
**Goal**: Final comprehensive defense

**Steps**:
1. Click "Enable ZK Stake-CBL" → Combines ZK stake + ECC + CBL
2. Try all attack steps → All should be blocked

**Expected Terminal Output**:
- All defense mechanisms active
- Multiple validation checks shown in terminal
- All attacks blocked

**Verify**: Terminal shows comprehensive validation logic

---

## Verification Checklist

- [ ] Terminal shows real execution steps (not mocked)
- [ ] Code snippets match actual backend code
- [ ] Function call stack shows real function names
- [ ] Blockchain state matches graph visualization
- [ ] Timestamps are real (not hardcoded)
- [ ] Security context explains what's happening
- [ ] All scenarios produce expected terminal output
- [ ] Terminal auto-scrolls to show latest steps
- [ ] Clear button works

## Real vs Mocked - How to Tell

**Real Execution Indicators**:
- Function names match backend code (`ConsensusEngine.validate_fork`, `CryptoEngine.crack_rsa`, etc.)
- Code snippets show actual Python code from `app.py`
- Timestamps increment with each action
- Call stack changes as functions are called
- Blockchain state updates match graph changes

**If Mocked (should not happen)**:
- Generic messages without function names
- No code snippets
- Hardcoded timestamps
- No call stack
- Blockchain state doesn't match graph

## Testing Commands

Run the Flask server:
```bash
python app.py
```

Open browser: http://localhost:5000

Watch the terminal panel as you click buttons - it should show real execution logic!

