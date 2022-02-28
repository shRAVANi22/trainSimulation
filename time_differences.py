from test_basics import get_WL_TL_TR_WR, save_sorted_times_with_tag
import numpy as np

number_of_coaches=2
output = r'C:\#DATA\WPMS\embedded\30kmph_two_coaches_train_time_delays.txt'
wheel_sensor_times = get_WL_TL_TR_WR(number_of_coaches)
print(len(wheel_sensor_times))
time_delays = []
prev_time = 0
for time_entry in wheel_sensor_times:
    print(time_entry)
    delay = time_entry[0] - prev_time
    time_delays.append(np.asarray([delay, time_entry[1]]))
    prev_time = time_entry[0]

# print(time_delays)
save_sorted_times_with_tag(time_delays, output)