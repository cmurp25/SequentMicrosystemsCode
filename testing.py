import sm_4rel4in
import time

# Initialize relay/input card at stack level 0
rel = sm_4rel4in.SM4rel4in(0)

# Enable counting on all 4 input channels at startup
print("Enabling counting on all channels and resetting counts...")
for i in range(4):
    rel.set_count_cfg(i + 1, 1)   # Enable counting
    rel.reset_count(i + 1)        # Reset count to zero

# Trays mapping
# Channel 1: Overhead buffer addition
# Channel 2: Overhead buffer subtraction
# Channel 3: Wet section addition
# Channel 4: Wet section subtraction

print("Wet Section Counter Test Started")
print("Monitoring inputs 1-4 with hardware counters... Press Ctrl+C to exit.\n")

# Previous values to detect change
prev_counts = {i: 0 for i in range(1, 5)}
sum_1_value = 0   # Overhead buffer trays
sum_2_value = 0   # Wet section trays

try:
    while True:
        # Read hardware counts
        counts = {i: rel.get_count(i) for i in range(1, 5)}

        # Process deltas
        for ch in range(1, 5):
            delta = counts[ch] - prev_counts[ch]
            if delta > 0:
                if ch == 1:  # Overhead buffer addition
                    sum_1_value += delta
                elif ch == 2:  # Overhead buffer subtraction
                    sum_1_value = max(0, sum_1_value - delta)
                elif ch == 3:  # Wet section addition
                    sum_2_value += delta
                elif ch == 4:  # Wet section subtraction
                    sum_2_value = max(0, sum_2_value - delta)

        # Print only when totals change
        if counts != prev_counts:
            print("===========================================")
            print("OHB and WS Trays Count")
            print(f"Overhead Buffer Trays: {sum_1_value}")
            print(f"Wet Section Trays:     {sum_2_value}")

        prev_counts = counts
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nCleaning up...")
    for i in range(4):
        rel.reset_count(i + 1)       # Reset count
        rel.set_count_cfg(i + 1, 0)  # Disable counting
    print("Counts cleared and counting disabled. Exiting...")
