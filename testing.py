import sm_4rel4in
import time

# Initialize relay/input card at stack level 0
rel = sm_4rel4in.SM4rel4in(0)

# Channels to monitor
channels = [1, 2, 3, 4]

# Counts for trays
sum_1_value = 0   # Overhead buffer trays
sum_2_value = 0   # Wet section trays

# Previous states to detect rising/falling edges
prev_states = {ch: 0 for ch in channels}

# Track previous totals for conditional printing
prev_sum1 = 0
prev_sum2 = 0

print("Wet Section Counter Test Started")
print("Monitoring inputs 1-4... Press Ctrl+C to exit.\n")

while True:
    try:
        # Loop through inputs and read their state
        current_states = {ch: rel.get_in(ch) for ch in channels}

        # Channel 1: Overhead buffer addition
        if current_states[1] == 1 and prev_states[1] == 0:
            sum_1_value += 1

        # Channel 2: Overhead buffer subtraction
        if current_states[2] == 1 and prev_states[2] == 0:
            if sum_1_value > 0:
                sum_1_value -= 1

        # Channel 3: Wet section addition
        if current_states[3] == 1 and prev_states[3] == 0:
            sum_2_value += 1

        # Channel 4: Wet section subtraction
        if current_states[4] == 1 and prev_states[4] == 0:
            if sum_2_value > 0:
                sum_2_value -= 1

        # Print when totals change
        if sum_1_value != prev_sum1 or sum_2_value != prev_sum2:
            print("===========================================")
            print("OHB and WS Trays Count")
            print(f"Overhead Buffer Trays: {sum_1_value}")
            print(f"Wet Section Trays:     {sum_2_value}")
            prev_sum1 = sum_1_value
            prev_sum2 = sum_2_value

        # Save current state for next loop
        prev_states = current_states

        # Small delay to avoid bouncing issues
        time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nExiting...")
        break
