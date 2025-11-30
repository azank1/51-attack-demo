import hashlib
import time
import copy

# ==========================================
# COMPONENT 1: IDENTITY & CRYPTO
# ==========================================

class Wallet:
    def __init__(self, name, balance, stake, key_type="RSA"):
        self.name = name
        self.balance = balance
        self.stake = stake
        self.key_type = key_type # "RSA" or "ECC"
        self.is_cracked = False

    def try_crack(self):
        if self.key_type == "RSA":
            print(f"   [HACK] Factoring {self.name}'s RSA Key... Success! Private Key Stolen.")
            self.is_cracked = True
            return True
        else:
            print(f"   [HACK] Attempting to crack {self.name}'s ECC Key... FAILED.")
            print("   [INFO] Elliptic Curve cryptography is computationally secure.")
            return False

# ==========================================
# COMPONENT 2: BLOCKCHAIN DATABASE
# ==========================================

class Block:
    def __init__(self, index, miner, transactions, prev_hash):
        self.index = index
        self.miner = miner
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.hash = hashlib.sha256(f"{index}{miner}{transactions}".encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [Block(0, "System", "Genesis", "0")]

    def add_block(self, miner_name, txs):
        prev = self.chain[-1]
        new_block = Block(prev.index + 1, miner_name, txs, prev.hash)
        self.chain.append(new_block)

# ==========================================
# COMPONENT 3: CONSENSUS ENGINE (The Brain)
# ==========================================

class ConsensusEngine:
    def __init__(self, security_mode):
        self.mode = security_mode # "LEGACY_CBL" or "STAKE_CBL"

    def validate_fork(self, current_chain, new_chain, stake_registry):
        print(f"\n   [CONSENSUS] Validating Fork under mode: {self.mode}")
        
        # 1. CALCULATE WEIGHT
        honest_weight = 0
        attacker_weight = 0
        
        # Calculate Honest Weight (Current Chain)
        # Simplified: Assume honest chain is backed by Alice's High Stake
        honest_weight = stake_registry['Alice'] * len(current_chain.chain)
        
        # Calculate Attacker Weight
        for block in new_chain.chain:
            # In Legacy, weight is just 1 per block. In Stake, it's the stake amount.
            if self.mode == "STAKE_CBL":
                attacker_weight += stake_registry.get(block.miner, 0)
            else:
                attacker_weight += 10000 # In Legacy, we ignore stake, so length wins (simulated high weight)

        # 2. CHECK CBL (Consecutive Block Limits)
        # Scan the new chain for violations
        consecutive = 0
        last_miner = ""
        
        for block in new_chain.chain:
            if block.miner == last_miner:
                consecutive += 1
            else:
                consecutive = 1
                last_miner = block.miner
            
            # THE RULE: Static limit of 2
            if consecutive > 2:
                print(f"      ❌ REJECTED: Static CBL Violation! {block.miner} mined {consecutive} blocks.")
                return False

        # 3. FINAL DECISION
        if self.mode == "STAKE_CBL":
            print(f"      ⚖️  Honest Weight: {honest_weight}")
            print(f"      ⚖️  Attacker Weight: {attacker_weight}")
            if attacker_weight < honest_weight:
                print("      ❌ REJECTED: Insufficient Stake Weight (Sybil Detected).")
                return False
        
        return True

# ==========================================
# SCENARIO ORCHESTRATOR
# ==========================================

def run_simulation():
    # --- CONFIG ---
    # Alice is Rich (Honest), Eve is Poor (Attacker)
    stakes = {'Alice': 5000, 'Eve': 100, 'Eve_A': 50, 'Eve_B': 50}
    
    # ==========================================
    # ATTACK 1: LEGACY + RSA + STATIC CBL
    # ==========================================
    print("\n" + "="*50)
    print("SCENARIO 1: Legacy Network (RSA + Static CBL)")
    print("="*50)
    
    # 1. Init Actors
    alice = Wallet("Alice", 100, 5000, "RSA")
    eve = Wallet("Eve", 0, 100, "RSA")
    
    # 2. The Hack
    success = alice.try_crack()
    if success:
        print(f"   [ACTION] Eve creates Transaction: 'Alice -> Eve 100 BTC'")
        
        # 3. The 51% Attack (Mining 3 blocks)
        engine = ConsensusEngine("LEGACY_CBL")
        honest_chain = Blockchain()
        honest_chain.add_block("Alice", "Tx: Honest") # Block 1
        
        eve_chain = copy.deepcopy(honest_chain)
        # Eve mines 3 in a row
        eve_chain.add_block("Eve", "Tx: Theft")
        eve_chain.add_block("Eve", "Tx: Empty")
        eve_chain.add_block("Eve", "Tx: Empty")
        
        # 4. Consensus Check
        print("   [ACTION] Eve broadcasts chain length 4 (Honest is 2)...")
        result = engine.validate_fork(honest_chain, eve_chain, stakes)
        
        if not result:
            print("   [RESULT] Attack 1 FAILED. Funds Safe.")

    # ==========================================
    # ATTACK 2: MODERN + ECC + STAKE-CBL
    # ==========================================
    print("\n" + "="*50)
    print("SCENARIO 2: Improved Network (ECC + Stake-CBL)")
    print("="*50)

    # 1. Init Actors (Upgrade Keys)
    alice = Wallet("Alice", 100, 5000, "ECC")
    
    # 2. The Hack Attempt
    success = alice.try_crack()
    if not success:
        print("   [ACTION] Eve cannot steal keys. Switches to Sybil Attack.")
        
        # 3. The Sybil Attack (Bypassing Static CBL)
        engine = ConsensusEngine("STAKE_CBL")
        
        eve_sybil_chain = copy.deepcopy(honest_chain)
        # Eve alternates to bypass the "Consecutive > 2" rule
        eve_sybil_chain.add_block("Eve_A", "Tx: Spam") 
        eve_sybil_chain.add_block("Eve_B", "Tx: Spam")
        eve_sybil_chain.add_block("Eve_A", "Tx: Spam")
        eve_sybil_chain.add_block("Eve_B", "Tx: Spam")
        
        # 4. Consensus Check
        print("   [ACTION] Eve broadcasts Sybil chain (Length 5)...")
        # Note: Static CBL check will PASS because she alternated names!
        # But Stake Check will FAIL.
        result = engine.validate_fork(honest_chain, eve_sybil_chain, stakes)

        if not result:
            print("   [RESULT] Attack 2 FAILED. Network Safe.")

if __name__ == "__main__":
    run_simulation()