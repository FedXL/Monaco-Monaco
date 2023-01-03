from core.config import files
from core.build_data import DATA, build_data
from fuzzywuzzy import fuzz


def build_person_print(name):
    BigData = build_data("storage", files)

    for key in list(BigData.racers_initials.keys()):
        ratio = fuzz.ratio(key.lower(), name.lower())
        if ratio >= 75:
            racer_key_name = key
            break
    INC = BigData.racers_initials[racer_key_name]
    place = BigData.score[INC]
    lap_time = BigData.time_lap[INC]
    command = BigData.racers_info[INC][1]
    print(str(place) + ". ", racer_key_name + " " + command, lap_time,sep="|")

def build_place_print(place):
    if len(str(place)) < 2:
        return str(place) + ". "
    else:
        return str(place) +"."




def build_total_report():
    BigData = build_data("storage", files)
    score = BigData.score
    fifteen = 0
    report = []
    for INC, value in score.items():
        place = value
        racer_name = BigData.racers_info[INC][0]
        command = BigData.racers_info[INC][1]
        lap_time = BigData.time_lap[INC]
        string = (place, racer_name, command, lap_time)
        report.append(string)
    return report

def check_max_string_length(report):
    max_length = 0
    for string in report :
        if len(string[1]+string[2]) > max_length:
            max_length = len(string[1]+string[2])
    return max_length

def build_total_print():
    report=build_total_report()
    max_length_name = check_max_string_length(report)
    counter = 0
    for string in report:
        place = build_place_print(string[0])
        spaces = max_length_name - len(string[1] + string[2])
        name_and_command = string[1] +" "+ string[2] +(max_length_name-len(string[1]+string[2]))*" "
        lap_time = string[3]
        print(place, name_and_command, lap_time, sep="|")
        if counter == 14:
            print("-"*(len(place+str(lap_time))+max_length_name+3))
        counter +=1





build_person_print("Kimi Raikkenen")
build_total_print()







