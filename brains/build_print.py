from config import files
from build_data import build_data
from fuzzywuzzy import fuzz


def build_person_print(folder, name):
    BigData = build_data(folder, files)
    for key in list(BigData.racers_initials.keys()):
        ratio = fuzz.ratio(key.lower(), name.lower())
        if ratio >= 75:
            racer_key_name = key
            break
    INC = BigData.racers_initials[racer_key_name]
    place = BigData.score[INC]
    lap_time = BigData.time_lap[INC]
    command = BigData.racers_info[INC][1]
    print("*" * 20,
          "Awesome Monaco #Personal Report",
          "Place: " + str(place),
          "Name: " + racer_key_name,
          "Command: " + command,
          "Lap Time: " + str(lap_time),
          "*" * 20,
          sep="\n")


def build_place_print(place):
    if len(str(place)) < 2:
        return str(place) + ". "
    else:
        return str(place) + "."


def build_total_report(folder, back_order):
    BigData = build_data(folder, files)
    score = BigData.score

    if back_order:
        INClist = list(score.keys())
        reversed_list = INClist[0:15]
        reversed_list.reverse()
        other_list = INClist[15:]
        INClist = reversed_list + other_list
        new_score = {}
        for key in INClist:
            new_score[key] = score[key]
        score = new_score
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
    for string in report:
        if len(string[1] + string[2]) > max_length:
            max_length = len(string[1] + string[2])
    return max_length


def build_total_print(folder, back_order):
    report = build_total_report(folder, back_order)
    max_length_name = check_max_string_length(report)
    counter = 0
    print("*"*60)
    print("Awesome Monaco #TOTAL REPORT")
    for string in report:
        place = build_place_print(string[0])
        name_and_command = string[1] + " " + string[2] + (max_length_name - len(string[1] + string[2])) * " "
        lap_time = string[3]
        print(place, name_and_command, lap_time, sep="|")
        if counter == 14:
            print("-" * (len(place + str(lap_time)) + max_length_name + 3))
        counter += 1
    print("*"*60)

if __name__ == "__main__":
    build_person_print("Kimi Raikkenen")
    build_total_print("storage")
