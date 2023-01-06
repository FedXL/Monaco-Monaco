import codecs
import datetime
from collections import OrderedDict
from dataclasses import dataclass
from os import path
from fuzzywuzzy import fuzz
from brains.config import files, RACERS, limit, START, END


class RacerInfo:
    def __init__(self, place=None, name=None, team=None, start_time=None, end_time=None, lap_time=None):
        self.place = place
        self.name = name
        self.team = team
        self.start_time = start_time
        self.end_time = end_time
        self.lap_time = lap_time

    def calculate_lap_time(self):
        start = self.start_time.split(":")
        end = self.end_time.split(":")
        time_start = [float(num) for num in start]
        time_end = [float(num) for num in end]
        tm1 = datetime.timedelta(hours=time_start[0], minutes=time_start[1], seconds=time_start[2])
        tm2 = datetime.timedelta(hours=time_end[0], minutes=time_end[1], seconds=time_end[2])
        time_delta = tm2 - tm1
        self.lap_time = time_delta
        self.start_time = None
        self.end_time = None

    def get_print(self):
        print(
            self.place,
            self.name,
            self.team,
            self.lap_time,
            sep=" | "
        )


def add_time(start_time_list: list, end_time_list: list, data: {str: RacerInfo}) -> {str: RacerInfo}:
    for line in start_time_list:
        initials, time = parce_time(line)
        racer: RacerInfo = data.get(initials)
        racer.start_time = time

    for line in end_time_list:
        initials, time = parce_time(line)
        racer: RacerInfo = data.get(initials)
        racer.end_time = time

    return data


def parce_time(line):
    initials = line[:3]
    time = line.split("_")[1]
    return initials, time


def read_file(folder, file):
    with open(path.join(folder, file), "r", encoding='utf-8') as record:
        text = record.read().strip().split("\n")
    return text


def collect_data(folder):
    abbreviations = read_file(folder, RACERS)
    abbreviations = [abr.split("_") for abr in abbreviations]
    data_collection = {line[0]: RacerInfo(name=line[1], team=line[2]) for line in abbreviations}
    start_time, end_time = read_file(folder, START), read_file(folder, END)
    data_collection = add_time(start_time, end_time, data_collection)
    for racer in data_collection.values():
        racer.calculate_lap_time()
    return data_collection


def sort_data(data, pos):
    abr = list(data.keys())
    lap_time = [time.lap_time for time in data.values()]
    abr_lap_time = dict(zip(lap_time, abr))
    lap_time.sort()
    racers = OrderedDict({abr_lap_time[lap]: data[abr_lap_time[lap]] for lap in lap_time})
    return racers


def add_rating_to_data(data_collection: {str: RacerInfo}, pos=False):
    print("_" * 60)
    data = sort_data(data_collection, pos)
    cheaters = []
    counter = 1
    for abr, racer in data.items():
        if racer.lap_time.total_seconds() <= 30:
            racer.lap_time = "INVALID TIME"
            racer.place = "DNF"
            cheaters.append(abr)
        else:
            racer.place = counter
            counter += 1
    for cheater in cheaters:
        data.move_to_end(cheater)
    return data


a = collect_data("C:\\Users\\Asus\\PycharmProjects\\monaco\\storage")

a = add_rating_to_data(a)
for i in a.values():
    i.get_print()

# def reverse_score(racers_info):
#     score = racers_info.score
#     initials = list(score.keys())
#     winners = initials[0:limit]
#     winners.reverse()
#     losers = initials[limit:]
#     together = winners + losers
#     score_reversed = {initial: score[initial] for initial in together}
#     return score_reversed

#
#
# """
# def racers_parcer(text: str) -> ({str: (str, str)}, {str: str}):
#     abbreviations = [string.split("_") for string in text]
#     initials_name_team = {line[0]: (line[1], line[2],) for line in abbreviations}
#     name_initials = {line[1]: line[0] for line in abbreviations}
#     return initials_name_team, name_initials
#
#
# def timer_parcer(lines: list) -> dict:
#     time = {line[:3]: line[3:].split("_") for line in lines}
#     return time
#
#
# # ------------------------------------BUILDING DATA---------------------------------------------------------------------
#
#
# def calculate_time_lap(data: DataStorage) -> DataStorage:
#
#     keys = data.time_start.keys()
#     time_delta = OrderedDict()
#
#     for key in keys:
#         time_start = [float(num) for num in data.time_start[key][1].replace(" ", "").split(":")]
#         time_end = [float(num) for num in data.time_end[key][1].replace(" ", "").split(":")]
#
#         tm1 = datetime.timedelta(hours=time_start[0], minutes=time_start[1], seconds=time_start[2])
#         tm2 = datetime.timedelta(hours=time_end[0], minutes=time_end[1], seconds=time_end[2])
#         time_delta[key] = tm2 - tm1
#
#     data.time_lap = sort_time_lap(time_delta)
#     return data
#
#
# def sort_time_lap(time_lap: OrderedDict):
#
#     values = time_lap.values()
#     new = {value: key for key, value in time_lap.items()}
#     sorted_values = sorted(values)
#     sorted_keys = [new[key] for key in sorted_values]
#     result = OrderedDict({key: time_lap[key] for key in sorted_keys})
#     result = handle_invalid_time_in_rating(result)
#     return result
#
#
# def handle_invalid_time_in_rating(positions: OrderedDict):
#
#
#     for racer in dnf_list:
#         positions[racer] = False
#         positions.move_to_end(racer)
#     return positions
#
#
# def make_score(time_lap):
#
#
#
#
# def parce_files_all(file, text):
#     assert file in files
#     if file == RACERS:
#         return racers_parcer(text)
#     else:
#         return timer_parcer(text)
#
#
# def collect_data(folder) -> DataStorage:
#
#     data = [parce_files_all(file, read_folder(folder, file)) for file in files]
#     race_info = DataStorage(racers_info=data[0][0],
#                             racers_initials=data[0][1],
#                             time_start=data[1],
#                             time_end=data[2],
#                             time_lap=OrderedDict(),
#                             score={})
#     race_info = calculate_time_lap(race_info)
#     race_info.score = make_score(race_info.time_lap)
#     return race_info
#
#
# # ----------------------------BUILDING REPORT---------------------------------------------------------------------------
#
#
# def check_true_racer_name(data: DataStorage, racer_name):
#     racer_key_name = None
#     for key in list(data.racers_initials.keys()):
#         ratio = fuzz.ratio(key.lower(), racer_name.lower())
#         if ratio >= 75:
#             racer_key_name = key
#             break
#     return racer_key_name
#
#
# def check_place(lap_time, score):
#     if lap_time:
#         return score
#     return False
#
#
# def get_initial_from_racer_name(racer_name: str, data: DataStorage):
#     true_racer_name = check_true_racer_name(data, racer_name)
#     initials = data.racers_initials[true_racer_name]
#     return initials
#
#
# def get_report(initial, data: DataStorage):
#     racer_name = data.racers_info[initial][0]
#     racer_team = data.racers_info[initial][1]
#     lap_time = data.time_lap[initial]
#     place = data.score[initial]
#     place = check_place(lap_time, place)
#     result = RacerReport(
#         place=place,
#         name=racer_name,
#         team=racer_team,
#         lap_time=lap_time
#     )
#     return result
#
#
#
#
#
# def build_data(reverse: bool, folder: str):
#     racers_info = collect_data(folder)
#     if reverse:
#         racers_info.score = reverse_score(racers_info)
#     return racers_info
#
#
# def build_report(args):
#     folder = args.files
#     if args.driver:
#         racers_info = build_data(False, folder)
#         initials = get_initial_from_racer_name(args.driver, racers_info)
#         report = [get_report(initials, racers_info)]
#     else:
#         racers_info = build_data(args.desc, folder)
#         report = [get_report(initial, racers_info) for initial in racers_info.score.keys()]
#     return report
#
# """
