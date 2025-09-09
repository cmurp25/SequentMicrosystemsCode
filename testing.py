import time
import sm_4rel4in

# Initialize the relay card (stack level 0)
rel = sm_4rel4in.SM4rel4in(0)

# Channels to monitor
channel_1 = 1
channel_2 = 2

# Tracking variables
sum_value = 0
signal_1_detected = False
signal_2_detected = False

# Optional: Debounce timing
last_trigger_time_ch1 = 0
last_trigger_time_ch2 = 0
debounce_delay = 0.001  # 1ms debounce

try:
    while True:
        signal_1 = rel.get_in(channel_1)
        signal_2 = rel.get_in(channel_2)

        # Rising edge detection for channel 1 → increment sum
        if signal_1 == 1 and not signal_1_detected and time.time() - last_trigger_time_ch1 > debounce_delay:
            sum_value += 1
            signal_1_detected = True
            last_trigger_time_ch1 = time.time()
        elif signal_1 != 1 and signal_1_detected:
            signal_1_detected = False

        # Rising edge detection for channel 2 → decrement sum
        if signal_2 == 1 and not signal_2_detected and time.time() - last_trigger_time_ch2 > debounce_delay:
            sum_value -= 1
            signal_2_detected = True
            last_trigger_time_ch2 = time.time()
        elif signal_2 != 1 and signal_2_detected:
            signal_2_detected = False

        # Print status
        print(f"Sum: {sum_value}")

        # Sleep for CPU efficiency
        time.sleep(0.001)

except KeyboardInterrupt:
    print("\nStopped by user.")
