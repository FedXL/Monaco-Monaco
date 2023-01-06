import datetime
from collections import OrderedDict

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


def find_driver(driver):
    print(driver)
    pass


def build_report(folder, driver: str = None, reverse: bool = False):
    data = collect_data(folder)
    data = add_rating_to_data(data)
    if reverse:
        data = reverse_data(data)
    if driver:
        data = find_driver(driver)
    return data


def collect_data(folder):
    abbreviations = read_file(folder, RACERS)
    abbreviations = [abr.split("_") for abr in abbreviations]
    data_collection = {line[0]: RacerInfo(name=line[1], team=line[2]) for line in abbreviations}
    start_time, end_time = read_file(folder, START), read_file(folder, END)
    data_collection = add_time(start_time, end_time, data_collection)
    for racer in data_collection.values():
        racer.calculate_lap_time()
    return data_collection


def reverse_data(data):
    initials = list(data.keys())
    winners = initials[0:limit]
    winners.reverse()
    losers = initials[limit:]
    together = winners + losers
    new_data = {abr: data[abr] for abr in together}
    return new_data


def add_rating_to_data(data_collection: {str: RacerInfo}):
    data = sort_data(data_collection)
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


def read_file(folder, file):
    with open(path.join(folder, file), "r", encoding='utf-8') as record:
        text = record.read().strip().split("\n")
    return text


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


def sort_data(data):
    abr = list(data.keys())
    lap_time = [time.lap_time for time in data.values()]
    abr_lap_time = dict(zip(lap_time, abr))
    lap_time.sort()
    racers = OrderedDict({abr_lap_time[lap]: data[abr_lap_time[lap]] for lap in lap_time})
    return racers

if __name__=="__main__":
    folder = "C:\\Users\\Asus\\PycharmProjects\\monaco\\storage"
    build_report(folder, True)
    report = build_report(folder, False)
    for i in report.values():
        i.get_print()

