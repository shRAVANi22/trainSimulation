import numpy as np
import plotly.graph_objects as go
fig = go.Figure()

# within same bogie axle to axle distance i.e axle 1 to axle2 = 2.7 mts = 2700mm
# within same coach boggie to boggoe min distance i.e axle 2 to axle3 = 12mts = 12000mm
# bogie to bogie min in between coaches i.e axle4 of coach 1 to axle1 of coach2 = 6.13 m = 6130mm
output = r'C:\#DATA\WPMS\embedded\160kmph_four_coaches_train.txt'
number_of_coaches = 4


train_speed_kmph = 160
train_speed_mmpms = train_speed_kmph / 3.6

# m/s = mm/ms
same_bogie_dist_mm = 2700
same_coach_bogie_dist_mm = 12000
next_coach_bogie_dist_mm = 6130

print('same_bogie_time_ms: ', round((same_bogie_dist_mm/train_speed_mmpms), 2))
print('same_coach_bogie_time_ms: ', round((same_coach_bogie_dist_mm/train_speed_mmpms), 2))
print('next_coach_bogie_time_ms: ', round((next_coach_bogie_dist_mm/train_speed_mmpms), 2))

WL_TL_dist = 50000
WR_TR_dist = 50000
TL_TR_dist = 138

print('least_count: ', round((same_bogie_dist_mm/train_speed_mmpms), 2))


delta_WL = 0
delta_TL = delta_WL + round((WL_TL_dist/train_speed_mmpms), 2)
delta_TR = delta_WL + round(((WL_TL_dist+TL_TR_dist)/train_speed_mmpms), 2)
delta_WR = delta_WL + round(((WL_TL_dist+TL_TR_dist+WR_TR_dist)/train_speed_mmpms), 2)

print('delta_WL: ', delta_WL)
print('delta_WR: ', delta_WR)
print('delta_TL: ', delta_TL)
print('delta_TR: ', delta_TR)


def add_nth_coach_times_ms(n, previous_coach_last_time):
    if n == 1:
        t1 = 0
    else:
        t1 = (previous_coach_last_time + (next_coach_bogie_dist_mm/train_speed_mmpms))
    t2 = t1 + (same_bogie_dist_mm/train_speed_mmpms)
    t3 = t2 + (same_coach_bogie_dist_mm/train_speed_mmpms)
    t4 = t3 + (same_bogie_dist_mm/train_speed_mmpms)
    return round(t1, 2), round(t2, 2), round(t3, 2), round(t4, 2)


def simulate_train(number_of_coaches):
    times = []
    previous_coach_last_time = 0
    for i in range(0, number_of_coaches):
        n = i + 1
        t1, t2, t3, t4 = add_nth_coach_times_ms(n, previous_coach_last_time)
        previous_coach_last_time = t4
        times.append(t1)
        times.append(t2)
        times.append(t3)
        times.append(t4)
    return np.asarray(times)


def add_impulse_times(coach_times):
    x = coach_times[:, 0]
    y = coach_times[:, 1]
    fig.add_trace(
        go.Scatter(x=x, y=y, mode='markers+lines', marker=dict(size=10), name='impulses')
    )


def get_WL_TL_TR_WR(number_of_coaches):
    coach_times = simulate_train(number_of_coaches)
    times = []
    for time in coach_times:
        times.append(np.asarray([(time + delta_WL), 1.0]))
        times.append(np.asarray([(time + delta_TL), 2.0]))
        times.append(np.asarray([(time + delta_TR), 3.0]))
        times.append(np.asarray([(time + delta_WR), 4.0]))
    sorted_times = sorted(times, key=lambda a_entry: a_entry[0])
    return sorted_times


def save_sorted_times_with_tag(sorted_times, file):
    log = open(file, 'w')
    for time in sorted_times:
        if time[1] == 1: # 'WL
            log.write('WL ')
        elif time[1] == 2:
            log.write('TL ')
        elif time[1] == 3:
            log.write('TR ')
        elif time[1] == 4:
            log.write('WR ')
        log.write(str(time[0]) + '\n')
    log.close()


wheel_sensor_times = get_WL_TL_TR_WR(number_of_coaches)
save_sorted_times_with_tag(wheel_sensor_times, output)
add_impulse_times(np.asarray(wheel_sensor_times))
fig.show()
