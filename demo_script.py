#!/usr/bin/env python3
"""
Automated Demo Script for 51% Attack Simulation
Runs all scenarios sequentially with proper timing and state management
"""

import requests
import time
import webbrowser
from typing import Dict, Optional, List
import json

class BlockchainDemo:
    """Automated demo controller for blockchain attack simulation"""
    
    def __init__(self, base_url: str = "http://localhost:5000", 
                 auto_browser: bool = True,
                 delays: Optional[Dict[str, float]] = None):
        self.base_url = base_url
        self.auto_browser = auto_browser
        self.delays = delays or {
            'action': 3.0,      # Delay between actions (seconds)
            'scenario': 10.0,  # Delay between scenarios
            'animation': 2.0,  # Delay for GUI animations
            'broadcast': 5.0   # Delay after broadcast
        }
        self.paused = False
        self.current_scenario = None
        self.step = 0
        
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
    
    def wait(self, duration: Optional[float] = None):
        """Wait for specified duration or default animation delay"""
        if self.paused:
            self.log("Demo paused. Press Enter to continue...", "PAUSE")
            input()
        delay = duration or self.delays['animation']
        time.sleep(delay)
    
    def api_call(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict:
        """Make API call and return JSON response"""
        url = f"{self.base_url}{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, timeout=5)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=5)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.log(f"API Error: {e}", "ERROR")
            return {'success': False, 'message': str(e)}
    
    def get_state(self) -> Dict:
        """Get current simulation state"""
        return self.api_call("/api/state")
    
    def validate_state(self, expected: Dict) -> bool:
        """Validate current state matches expected values"""
        state = self.get_state()
        for key, value in expected.items():
            if state.get(key) != value:
                self.log(f"State validation failed: {key} = {state.get(key)}, expected {value}", "WARN")
                return False
        return True
    
    # ========== API Wrapper Methods ==========
    
    def reset(self) -> bool:
        """Reset simulation to initial state"""
        self.log("Resetting simulation...")
        result = self.api_call("/api/reset", "POST")
        self.wait(self.delays['action'])
        return result.get('success', False)
    
    def mine_honest_block(self, miner: str = "Miner1") -> bool:
        """Mine a block on the honest chain"""
        self.log(f"Mining honest block as {miner}...")
        result = self.api_call("/api/mine_honest_block", "POST", {"miner": miner})
        self.wait(self.delays['animation'])
        return result.get('success', False)
    
    def mine_multiple_honest(self, count: int = 2) -> bool:
        """Mine multiple honest blocks"""
        self.log(f"Mining {count} honest blocks...")
        result = self.api_call("/api/mine_multiple_honest", "POST", {"count": count})
        self.wait(self.delays['action'])
        return result.get('success', False)
    
    def crack_rsa(self) -> bool:
        """Crack Alice's RSA key"""
        self.log("Cracking RSA key...")
        result = self.api_call("/api/crack_rsa", "POST")
        self.wait(self.delays['action'])
        if result.get('success'):
            self.log(f"✓ RSA key cracked: {result.get('message')}", "SUCCESS")
        return result.get('success', False)
    
    def acquire_hash_power(self) -> bool:
        """Acquire 51% hash power"""
        self.log("Acquiring 51% hash power...")
        result = self.api_call("/api/acquire_hash_power", "POST")
        self.wait(self.delays['action'])
        if result.get('success'):
            self.log("✓ 51% hash power acquired", "SUCCESS")
        return result.get('success', False)
    
    def mine_attack_block(self) -> bool:
        """Mine a block on the attack chain"""
        self.log("Mining attack block...")
        result = self.api_call("/api/mine_attack_block", "POST")
        self.wait(self.delays['animation'])
        return result.get('success', False)
    
    def mine_multiple_attack(self, count: int = 3) -> bool:
        """Mine multiple attack blocks"""
        self.log(f"Mining {count} attack blocks...")
        result = self.api_call("/api/mine_multiple_attack", "POST", {"count": count})
        self.wait(self.delays['action'])
        return result.get('success', False)
    
    def broadcast_chain(self) -> tuple:
        """Broadcast attack chain"""
        self.log("Broadcasting attack chain...")
        result = self.api_call("/api/broadcast_chain", "POST")
        self.wait(self.delays['broadcast'])
        success = result.get('success', False)
        message = result.get('message', '')
        if success:
            self.log(f"✓ Chain accepted: {message}", "SUCCESS")
        else:
            self.log(f"✗ Chain rejected: {message}", "FAILED")
        return success, message
    
    def enable_cbl(self) -> bool:
        """Enable CBL defense"""
        self.log("Enabling CBL defense...")
        result = self.api_call("/api/enable_cbl", "POST")
        self.wait(self.delays['action'])
        return result.get('success', False)
    
    def enable_stake_cbl(self) -> bool:
        """Enable Stake-CBL + ECC defense"""
        self.log("Enabling Stake-CBL + ECC defense...")
        result = self.api_call("/api/enable_stake_cbl", "POST")
        self.wait(self.delays['action'])
        return result.get('success', False)
    
    def enable_hybrid(self) -> bool:
        """Enable Hybrid defense"""
        self.log("Enabling Hybrid defense...")
        result = self.api_call("/api/enable_hybrid", "POST")
        self.wait(self.delays['action'])
        return result.get('success', False)
    
    def enable_sybil(self) -> bool:
        """Enable Sybil attack mode"""
        self.log("Enabling Sybil attack mode...")
        result = self.api_call("/api/enable_sybil", "POST")
        self.wait(self.delays['action'])
        return result.get('success', False)
    
    def upgrade_network(self) -> bool:
        """Upgrade network statefully"""
        self.log("Upgrading network...")
        result = self.api_call("/api/upgrade_network", "POST")
        self.wait(self.delays['action'])
        if result.get('success'):
            self.log(f"✓ Network upgraded: {result.get('old_mode')} → {result.get('new_mode')}", "SUCCESS")
        return result.get('success', False)
    
    # ========== Scenario Execution Methods ==========
    
    def run_scenario_1(self) -> bool:
        """
        Scenario 1: Bitcoin Vulnerability (LEGACY mode)
        Demonstrates: Basic 51% attack succeeds
        """
        self.log("\n" + "="*60, "SCENARIO")
        self.log("SCENARIO 1: Bitcoin Vulnerability (LEGACY Mode)", "SCENARIO")
        self.log("="*60, "SCENARIO")
        
        # Reset to clean state
        if not self.reset():
            return False
        
        # Mine some honest blocks
        self.log("\n--- Step 1: Honest miners mine blocks ---")
        if not self.mine_multiple_honest(2):
            return False
        
        # Crack RSA key
        self.log("\n--- Step 2: Attacker cracks RSA key ---")
        if not self.crack_rsa():
            return False
        
        # Acquire 51% hash power
        self.log("\n--- Step 3: Attacker acquires 51% hash power ---")
        if not self.acquire_hash_power():
            return False
        
        # Mine attack blocks
        self.log("\n--- Step 4: Attacker mines secret chain (3 blocks) ---")
        if not self.mine_multiple_attack(3):
            return False
        
        # Broadcast chain
        self.log("\n--- Step 5: Attacker broadcasts chain ---")
        success, message = self.broadcast_chain()
        
        if success:
            self.log("\n✓ SCENARIO 1 COMPLETE: Attack succeeded (Bitcoin vulnerability demonstrated)", "SUCCESS")
        else:
            self.log(f"\n✗ SCENARIO 1 FAILED: {message}", "FAILED")
        
        self.wait(self.delays['scenario'])
        return success
    
    def run_scenario_2(self) -> bool:
        """
        Scenario 2: Static CBL Defense
        Demonstrates: CBL blocks consecutive mining attacks
        """
        self.log("\n" + "="*60, "SCENARIO")
        self.log("SCENARIO 2: Static CBL Defense", "SCENARIO")
        self.log("="*60, "SCENARIO")
        
        # Use stateful upgrade (no reset)
        self.log("\n--- Step 1: Network upgrades to CBL defense ---")
        if not self.enable_cbl():
            return False
        
        # Mine some honest blocks
        self.log("\n--- Step 2: Honest miners mine blocks ---")
        if not self.mine_multiple_honest(2):
            return False
        
        # Crack RSA key
        self.log("\n--- Step 3: Attacker cracks RSA key ---")
        if not self.crack_rsa():
            return False
        
        # Acquire 51% hash power
        self.log("\n--- Step 4: Attacker acquires 51% hash power ---")
        if not self.acquire_hash_power():
            return False
        
        # Mine attack blocks (3 consecutive - should be blocked)
        self.log("\n--- Step 5: Attacker mines 3 consecutive blocks ---")
        if not self.mine_multiple_attack(3):
            return False
        
        # Broadcast chain (should be rejected)
        self.log("\n--- Step 6: Attacker broadcasts chain (should be blocked) ---")
        success, message = self.broadcast_chain()
        
        if not success and "CBL violation" in message:
            self.log("\n✓ SCENARIO 2 COMPLETE: Attack blocked by CBL (defense works!)", "SUCCESS")
            return True
        else:
            self.log(f"\n✗ SCENARIO 2 FAILED: Expected CBL violation, got: {message}", "FAILED")
            return False
    
    def run_scenario_3(self) -> bool:
        """
        Scenario 3: Sybil Attack
        Demonstrates: Multiple identities bypass Static CBL
        """
        self.log("\n" + "="*60, "SCENARIO")
        self.log("SCENARIO 3: Sybil Attack (CBL Bypass)", "SCENARIO")
        self.log("="*60, "SCENARIO")
        
        # CBL should already be enabled from Scenario 2
        state = self.get_state()
        if state.get('defense_mode') != 'CBL':
            self.log("Enabling CBL defense...")
            if not self.enable_cbl():
                return False
        
        # Enable Sybil mode
        self.log("\n--- Step 1: Attacker creates Sybil identities (Eve_A, Eve_B) ---")
        if not self.enable_sybil():
            return False
        
        # Mine some honest blocks
        self.log("\n--- Step 2: Honest miners mine blocks ---")
        if not self.mine_multiple_honest(2):
            return False
        
        # Crack RSA key
        self.log("\n--- Step 3: Attacker cracks RSA key ---")
        if not self.crack_rsa():
            return False
        
        # Acquire 51% hash power
        self.log("\n--- Step 4: Attacker acquires 51% hash power ---")
        if not self.acquire_hash_power():
            return False
        
        # Mine attack blocks with Sybil (alternating miners)
        self.log("\n--- Step 5: Attacker mines 3 blocks with Sybil (alternating Eve_A/Eve_B) ---")
        if not self.mine_multiple_attack(3):
            return False
        
        # Broadcast chain (should succeed - bypasses CBL)
        self.log("\n--- Step 6: Attacker broadcasts Sybil chain ---")
        success, message = self.broadcast_chain()
        
        if success:
            self.log("\n✓ SCENARIO 3 COMPLETE: Sybil attack succeeded (CBL bypassed)", "SUCCESS")
        else:
            self.log(f"\n✗ SCENARIO 3 FAILED: {message}", "FAILED")
        
        self.wait(self.delays['scenario'])
        return success
    
    def run_scenario_4(self) -> bool:
        """
        Scenario 4: Stake-CBL + ECC Defense
        Demonstrates: Full security with economic weight and cryptography
        """
        self.log("\n" + "="*60, "SCENARIO")
        self.log("SCENARIO 4: Stake-CBL + ECC Defense", "SCENARIO")
        self.log("="*60, "SCENARIO")
        
        # Upgrade network to Stake-CBL + ECC (stateful)
        self.log("\n--- Step 1: Network upgrades to Stake-CBL + ECC ---")
        if not self.upgrade_network():
            # If upgrade doesn't work, try direct enable
            if not self.enable_stake_cbl():
                return False
        
        # Mine some honest blocks
        self.log("\n--- Step 2: Honest miners mine blocks ---")
        if not self.mine_multiple_honest(2):
            return False
        
        # Try to crack RSA key (should fail - ECC is secure)
        self.log("\n--- Step 3: Attacker attempts to crack ECC key (should fail) ---")
        result = self.api_call("/api/crack_rsa", "POST")
        if not result.get('success'):
            self.log("✓ ECC key cracking failed (as expected - ECC is secure)", "SUCCESS")
        else:
            self.log("✗ ECC key was cracked (unexpected!)", "FAILED")
        
        # Acquire 51% hash power
        self.log("\n--- Step 4: Attacker acquires 51% hash power ---")
        if not self.acquire_hash_power():
            return False
        
        # Mine attack blocks with Sybil (low stake weight)
        self.log("\n--- Step 5: Attacker mines 3 blocks with Sybil (low stake) ---")
        if not self.mine_multiple_attack(3):
            return False
        
        # Broadcast chain (should be rejected - insufficient stake weight)
        self.log("\n--- Step 6: Attacker broadcasts chain (should be blocked) ---")
        success, message = self.broadcast_chain()
        
        if not success and ("stake" in message.lower() or "slashed" in message.lower()):
            self.log("\n✓ SCENARIO 4 COMPLETE: Attack blocked by Stake-CBL (slashing occurred)", "SUCCESS")
            return True
        else:
            self.log(f"\n✗ SCENARIO 4 FAILED: Expected stake rejection, got: {message}", "FAILED")
            return False
    
    def run_scenario_5(self) -> bool:
        """
        Scenario 5: Hybrid Defense
        Demonstrates: Comprehensive security with all checks combined
        """
        self.log("\n" + "="*60, "SCENARIO")
        self.log("SCENARIO 5: Hybrid Defense (All Checks Combined)", "SCENARIO")
        self.log("="*60, "SCENARIO")
        
        # Enable Hybrid defense
        self.log("\n--- Step 1: Network upgrades to Hybrid defense ---")
        if not self.enable_hybrid():
            return False
        
        # Mine some honest blocks
        self.log("\n--- Step 2: Honest miners mine blocks ---")
        if not self.mine_multiple_honest(2):
            return False
        
        # Try to crack RSA key (should fail - ECC is secure)
        self.log("\n--- Step 3: Attacker attempts to crack ECC key (should fail) ---")
        result = self.api_call("/api/crack_rsa", "POST")
        if not result.get('success'):
            self.log("✓ ECC key cracking failed (as expected)", "SUCCESS")
        
        # Acquire 51% hash power
        self.log("\n--- Step 4: Attacker acquires 51% hash power ---")
        if not self.acquire_hash_power():
            return False
        
        # Mine attack blocks (should be blocked by CBL)
        self.log("\n--- Step 5: Attacker mines 3 consecutive blocks (should be blocked) ---")
        if not self.mine_multiple_attack(3):
            return False
        
        # Broadcast chain (should be rejected - CBL violation)
        self.log("\n--- Step 6: Attacker broadcasts chain (should be blocked) ---")
        success, message = self.broadcast_chain()
        
        if not success:
            self.log("\n✓ SCENARIO 5 COMPLETE: Attack blocked by Hybrid defense (all checks passed)", "SUCCESS")
            return True
        else:
            self.log(f"\n✗ SCENARIO 5 FAILED: Attack should have been blocked, got: {message}", "FAILED")
            return False
    
    # ========== Demo Control Methods ==========
    
    def run_full_demo(self) -> bool:
        """Run all scenarios sequentially"""
        self.log("\n" + "="*70, "DEMO")
        self.log("STARTING AUTOMATED DEMO - All 5 Scenarios", "DEMO")
        self.log("="*70, "DEMO")
        
        if self.auto_browser:
            self.log("Opening browser...")
            webbrowser.open(self.base_url)
            self.wait(3)  # Wait for browser to load
        
        scenarios = [
            ("Scenario 1", self.run_scenario_1),
            ("Scenario 2", self.run_scenario_2),
            ("Scenario 3", self.run_scenario_3),
            ("Scenario 4", self.run_scenario_4),
            ("Scenario 5", self.run_scenario_5)
        ]
        
        results = []
        for name, scenario_func in scenarios:
            try:
                self.current_scenario = name
                success = scenario_func()
                results.append((name, success))
            except KeyboardInterrupt:
                self.log("\nDemo interrupted by user", "INTERRUPT")
                break
            except Exception as e:
                self.log(f"Error in {name}: {e}", "ERROR")
                results.append((name, False))
        
        # Summary
        self.log("\n" + "="*70, "SUMMARY")
        self.log("DEMO SUMMARY", "SUMMARY")
        self.log("="*70, "SUMMARY")
        for name, success in results:
            status = "✓ PASSED" if success else "✗ FAILED"
            self.log(f"{name}: {status}", "SUMMARY")
        
        passed = sum(1 for _, success in results if success)
        total = len(results)
        self.log(f"\nTotal: {passed}/{total} scenarios passed", "SUMMARY")
        
        return passed == total
    
    def pause(self):
        """Pause demo execution"""
        self.paused = True
        self.log("Demo paused", "PAUSE")
    
    def resume(self):
        """Resume demo execution"""
        self.paused = False
        self.log("Demo resumed", "RESUME")
    
    def stop(self):
        """Stop demo execution"""
        self.paused = False
        self.current_scenario = None
        self.log("Demo stopped", "STOP")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated demo script for 51% Attack Simulation")
    parser.add_argument("--url", default="http://localhost:5000", help="Base URL of the Flask server")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    parser.add_argument("--fast", action="store_true", help="Use faster delays (1s instead of 3s)")
    parser.add_argument("--scenario", type=int, choices=[1, 2, 3, 4, 5], help="Run specific scenario only")
    
    args = parser.parse_args()
    
    delays = {
        'action': 1.0 if args.fast else 3.0,
        'scenario': 5.0 if args.fast else 10.0,
        'animation': 1.0 if args.fast else 2.0,
        'broadcast': 3.0 if args.fast else 5.0
    }
    
    demo = BlockchainDemo(
        base_url=args.url,
        auto_browser=not args.no_browser,
        delays=delays
    )
    
    # Check if server is running
    try:
        state = demo.get_state()
        if not state:
            print("ERROR: Cannot connect to server. Make sure app.py is running.")
            return
    except Exception as e:
        print(f"ERROR: Cannot connect to server at {args.url}")
        print(f"Error: {e}")
        print("\nMake sure the Flask server is running:")
        print("  python app.py")
        return
    
    # Run demo
    if args.scenario:
        scenario_funcs = {
            1: demo.run_scenario_1,
            2: demo.run_scenario_2,
            3: demo.run_scenario_3,
            4: demo.run_scenario_4,
            5: demo.run_scenario_5
        }
        scenario_funcs[args.scenario]()
    else:
        demo.run_full_demo()


if __name__ == "__main__":
    main()

