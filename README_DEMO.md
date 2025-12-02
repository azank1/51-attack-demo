# Automated Demo Script Guide

## Overview

The `demo_script.py` automates all 5 blockchain attack scenarios, running them sequentially with proper timing and state management.

## Prerequisites

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Flask server:**
   ```bash
   python app.py
   ```
   The server should be running on http://localhost:5000

## Running the Demo

### Full Demo (All 5 Scenarios)

```bash
python demo_script.py
```

This will:
- Open your browser automatically
- Run all 5 scenarios sequentially
- Show progress in terminal
- Display summary at the end

### Run Specific Scenario

```bash
# Run only Scenario 1
python demo_script.py --scenario 1

# Run only Scenario 3 (Sybil Attack)
python demo_script.py --scenario 3
```

### Options

```bash
# Don't open browser automatically
python demo_script.py --no-browser

# Use faster timing (1s delays instead of 3s)
python demo_script.py --fast

# Custom server URL
python demo_script.py --url http://localhost:5000

# Combine options
python demo_script.py --fast --scenario 2 --no-browser
```

## Scenarios Covered

### Scenario 1: Bitcoin Vulnerability (LEGACY)
- **Demonstrates**: Basic 51% attack succeeds
- **Steps**: Reset → Mine honest blocks → Crack RSA → Acquire 51% → Mine 3 blocks → Broadcast → **Attack succeeds**

### Scenario 2: Static CBL Defense
- **Demonstrates**: CBL blocks consecutive mining
- **Steps**: Enable CBL → Mine honest → Crack RSA → Acquire 51% → Mine 3 consecutive → Broadcast → **Attack blocked**

### Scenario 3: Sybil Attack
- **Demonstrates**: Multiple identities bypass CBL
- **Steps**: Enable Sybil → Mine honest → Crack RSA → Acquire 51% → Mine 3 with Sybil → Broadcast → **Attack succeeds**

### Scenario 4: Stake-CBL + ECC Defense
- **Demonstrates**: Full security with economic weight
- **Steps**: Upgrade to Stake-CBL → Mine honest → Try crack ECC (fails) → Acquire 51% → Mine with Sybil → Broadcast → **Attack blocked + slashing**

### Scenario 5: Hybrid Defense
- **Demonstrates**: All security checks combined
- **Steps**: Enable Hybrid → Mine honest → Try crack ECC (fails) → Acquire 51% → Mine 3 consecutive → Broadcast → **Attack blocked**

## Timing Configuration

Default delays:
- **Action delay**: 3 seconds (between major actions)
- **Scenario delay**: 10 seconds (between scenarios)
- **Animation delay**: 2 seconds (for GUI updates)
- **Broadcast delay**: 5 seconds (after broadcasting chain)

Use `--fast` flag to reduce all delays to 1-3 seconds.

## Stateful Progression

The demo uses **stateful network upgrades**:
- Scenario 1 → Scenario 2: Uses `enable_cbl()` (no reset)
- Scenario 2 → Scenario 3: Continues with CBL enabled
- Scenario 3 → Scenario 4: Uses `upgrade_network()` (no reset)
- Scenario 4 → Scenario 5: Uses `enable_hybrid()` (no reset)

This demonstrates **chronological story flow**: Attack → Defense → Attack → Defense

## Output

The script provides:
- **Terminal logs** with timestamps and status
- **Browser visualization** (if auto-browser enabled)
- **Summary report** at the end showing which scenarios passed/failed

## Troubleshooting

### Server Not Running
```
ERROR: Cannot connect to server at http://localhost:5000
```
**Solution**: Start the Flask server first: `python app.py`

### API Errors
If you see API errors, check:
1. Server is running on correct port
2. No firewall blocking connections
3. Correct URL in `--url` parameter

### Browser Not Opening
Use `--no-browser` flag and open manually: http://localhost:5000

## Example Output

```
[14:30:15] [DEMO] STARTING AUTOMATED DEMO - All 5 Scenarios
[14:30:15] [DEMO] Opening browser...
[14:30:18] [SCENARIO] SCENARIO 1: Bitcoin Vulnerability (LEGACY Mode)
[14:30:18] [INFO] Resetting simulation...
[14:30:21] [INFO] Mining 2 honest blocks...
[14:30:24] [INFO] Cracking RSA key...
[14:30:27] [SUCCESS] ✓ RSA key cracked: Key cracked in 0.01ms
...
[14:35:00] [SUMMARY] Total: 5/5 scenarios passed
```

## Integration with GUI

The demo script works alongside the GUI:
- You can watch the browser while the script runs
- GUI updates in real-time
- You can pause/resume manually if needed
- Script and GUI use the same API endpoints

## Next Steps

After running the demo:
1. Review the terminal output for detailed logs
2. Check browser visualization for blockchain state
3. Examine code execution flow panel for detailed steps
4. Try manual interaction with GUI buttons

