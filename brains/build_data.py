import codecs
import datetime
import os
from collections import OrderedDict
from dataclasses import dataclass
from os import path
from fuzzywuzzy import fuzz
from config import files, RACERS, limit


@dataclass
class DataStorage:
    racers_info: dict  # initials: (Racer name , command)
    racers_initials: dict  # Racer name: initials
    time_start: dict  # initials: time_start
    time_end: dict  # initials: time_end
    time_lap: dict  # initials: time_lap
    score: dict  # initials: place


# ----------------------READ FILES--------------------------------------------------------------------------------------


def read_folder(folder, file):
    a = "../"
    with codecs.open(path.join("../", folder, file), "r", 'utf-8') as record:
        text = record.readlines()
        lines = [line[:-1] for line in text if len(line) > 1]
        record.close()
    return lines


def racers_parcer(text: str) -> ({str: (str, str)}, {str: str}):
    """parce racers abbreviations
    :parameter
            text unparsed text from config RACERS
    :return
            initials_name_team {initials: (racer_name,racer_team)}
            name_initials {racer_name: initial"""
    abbreviations = [string.split("_") for string in text]
    initials_name_team = {line[0]: (line[1], line[2],) for line in abbreviations}
    name_initials = {line[1]: line[0] for line in abbreviations}
    return initials_name_team, name_initials


def timer_parcer(lines: list) -> dict:
    """from DRR2018-05-24_12:11:24.067 -> {DDR: (2018-05-24,12:11:24.067)} """
    time = {line[:3]: line[3:].split("_") for line in lines}
    return time


# ------------------------------------BUILDING DATA---------------------------------------------------------------------


def calculate_time_lap(data: DataStorage) -> DataStorage:
    """calculate time lap for each initials"""
    keys = data.time_start.keys()
    time_delta = OrderedDict()

    for key in keys:
        time_start = [float(num) for num in data.time_start[key][1].replace(" ", "").split(":")]
        time_end = [float(num) for num in data.time_end[key][1].replace(" ", "").split(":")]
        tm1 = datetime.timedelta(hours=time_start[0], minutes=time_start[1], seconds=time_start[2])
        tm2 = datetime.timedelta(hours=time_end[0], minutes=time_end[1], seconds=time_end[2])
        time_delta[key] = tm2 - tm1

    data.time_lap = sort_time_lap(time_delta)
    return data


def sort_time_lap(time_lap: OrderedDict):
    """sort racer by places"""
    values = time_lap.values()
    new = {value: key for key, value in time_lap.items()}
    sorted_values = sorted(values)
    sorted_keys = [new[key] for key in sorted_values]
    result = OrderedDict({key: time_lap[key] for key in sorted_keys})
    result = handle_invalid_time_in_rating(result)
    return result


def handle_invalid_time_in_rating(positions: OrderedDict):
    """change invalid time_lap to DNF"""
    dnf_list = [racer for racer, time in positions.items() if time.total_seconds() <= 0]
    for racer in dnf_list:
        positions[racer] = False
        positions.move_to_end(racer)
    return positions


def make_score(time_lap):
    """make inc:PLACE vocabulary"""
    inc = list(time_lap.keys())
    score = {inc[place]: place + 1 for place in range(len(inc))}
    return score


def parce_files_all(file, text):
    assert file in files
    if file == RACERS:
        return racers_parcer(text)
    else:
        return timer_parcer(text)


def build_data(folder) -> DataStorage:
    """func to build DataStorage"""
    data = [parce_files_all(file, read_folder(folder, file)) for file in files]
    race_info = DataStorage(racers_info=data[0][0],
                            racers_initials=data[0][1],
                            time_start=data[1],
                            time_end=data[2],
                            time_lap=OrderedDict(),
                            score={})
    race_info = calculate_time_lap(race_info)
    race_info.score = make_score(race_info.time_lap)
    return race_info


# ----------------------------BUILDING REPORT---------------------------------------------------------------------------


def check_true_racer_name(data: DataStorage, racer_name):
    racer_key_name = None
    for key in list(data.racers_initials.keys()):
        ratio = fuzz.ratio(key.lower(), racer_name.lower())
        if ratio >= 75:
            racer_key_name = key
            break
    return racer_key_name, data.racers_info[data.racers_initials[racer_key_name]][1]


def check_place(lap_time, score):
    if lap_time:
        return score
    return False


def build_data_for_personal_report(racer_name: str, folder: str):
    racers_info = build_data(folder)
    racer_name, racer_team = check_true_racer_name(racers_info, racer_name)
    initials = racers_info.racers_initials[racer_name]
    lap_time = racers_info.time_lap[initials]
    place = check_place(lap_time, racers_info.score[initials])
    report = (place, racer_name, racer_team, lap_time)
    return report


def build_data_for_total_report(reverse: bool, folder: str):
    racers_info = build_data(folder)
    if reverse:
        score = racers_info.score
        initials = list(score.keys())
        winners = initials[0:limit]
        winners.reverse()
        losers = initials[limit:]
        together = winners + losers
        racers_info.score = {initial: score[initial] for initial in together}
    return racers_info



build_data_for_personal_report("Lewis Hamilton", "storage")
build_data_for_personal_report("Fernando Alonso", "storage")
build_data_for_total_report(True, "storage")

