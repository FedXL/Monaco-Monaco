import time


def calculate_critical_threshold(RACERS_TYPE):
    monaco_lap_distance = 3337  # meters
    if RACERS_TYPE == "AIRCRAFT_FIGHTER":
        max_fighter_speed = 3000 # km/hour
        critical_threshold = calculate_minimal_theoretical_time_of_lap(max_fighter_speed, monaco_lap_distance)
    else:
        max_bolid_speed = 350 # km/hour
        critical_threshold = calculate_minimal_theoretical_time_of_lap(max_bolid_speed, monaco_lap_distance)
    return critical_threshold


def calculate_minimal_theoretical_time_of_lap(max_speed,distance):
    speed_m_sec=(max_speed*1000)/(3600)
    min_time = distance/speed_m_sec
    return min_time


def read_some (a):
    if a == 1:
        time.sleep(3)
        return 111
    if a == 2:
        time.sleep(3)
        return 222
    if a == 3:
        time.sleep(3)
        return 333

def main():
    result = []
    for i in [1,2,3]:
        read_file = read_some(i)
        result.append(read_file)
    return result
