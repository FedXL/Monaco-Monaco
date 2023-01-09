



def calculate_critical_threshold(RACERS_TYPE):
    monaco_lap_distance = 3337  # meters
    if RACERS_TYPE == "AIRCRAFT FITER":
        max_fighter_speed = 3000 # km/hour
        critical_threshold = calculate_minimal_theoretical_time_of_lap(max_fighter_speed, 3337)
    else:
        max_bolid_speed = 350 # km/hour
        critical_threshold = calculate_minimal_theoretical_time_of_lap(max_bolid_speed, 3337)
    return critical_threshold


def calculate_minimal_theoretical_time_of_lap(max_speed,distance):
    speed_m_sec=(max_speed*1000)/(3600)
    min_time = distance/speed_m_sec
    return min_time
