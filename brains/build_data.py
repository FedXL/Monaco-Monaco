import codecs
import datetime
import os
from collections import OrderedDict
from dataclasses import dataclass
from os import path
from fuzzywuzzy import fuzz
from brains.config import files, RACERS, limit
import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Monaco Racing Task",
                                     epilog="I hope it will be funny")
    parser.add_argument('--files', type=str, required=True, help="Enter your folder path")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--asc', help="direct order", action="store_true")
    group.add_argument('--desc', help="undirected order", action="store_true")
    group.add_argument('--driver', help="driver name", type=str, default=None)
    args = parser.parse_args()
    return args


@dataclass
class DataStorage:
    racers_info: dict  # initials: (Racer name , command)
    racers_initials: dict  # Racer name: initials
    time_start: dict  # initials: time_start
    time_end: dict  # initials: time_end
    time_lap: dict  # initials: time_lap
    score: dict  # initials: place


@dataclass()
class RacerReport:
    place: ""
    name: ""
    team: ""
    lap_time: ""


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


def collect_data(folder) -> DataStorage:
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
    return racer_key_name


def check_place(lap_time, score):
    if lap_time:
        return score
    return False


def get_initial_from_racer_name(racer_name: str, data: DataStorage):
    true_racer_name = check_true_racer_name(data, racer_name)
    initials = data.racers_initials[true_racer_name]
    return initials


def get_report(initial, data: DataStorage):
    racer_name = data.racers_info[initial][0]
    racer_team = data.racers_info[initial][1]
    lap_time = data.time_lap[initial]
    place = data.score[initial]
    place = check_place(lap_time, place)
    result = RacerReport(
        place=place,
        name=racer_name,
        team=racer_team,
        lap_time=lap_time
    )
    return result


def reverse_score(racers_info):
    score = racers_info.score
    initials = list(score.keys())
    winners = initials[0:limit]
    winners.reverse()
    losers = initials[limit:]
    together = winners + losers
    score_reversed = {initial: score[initial] for initial in together}
    return score_reversed


def build_data(reverse: bool, folder: str):
    racers_info = collect_data(folder)
    if reverse:
        racers_info.score = reverse_score(racers_info)
    return racers_info


def build_report():
    args = get_args()
    folder = args.files
    if args.driver:
        racers_info = build_data(False, folder)
        initials = get_initial_from_racer_name(args.driver, racers_info)
        report = get_report(initials, racers_info)
    else:
        racers_info = build_data(True, folder)
        report = [get_report(initial, racers_info) for initial in racers_info.score.keys()]
    for i in report:
        print(i)
    return report

if __name__ == "__main__":
    build_report()