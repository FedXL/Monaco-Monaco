from brains.build_data import RacerReport
from brains.config import limit



def dub_place_print(place):
    """generate same lenght of string from 1 adn 11 numbers  """
    if not place:
        place = "DNF"
    elif len(str(place)) < 2:
        place = str(place) + ". "
    else:
        place = str(place) + "."
    return place


def check_max_string_length(reports):
    """find max length of racer name + command
    used to build the same length of strings in build_total_print"""
    max_length = 0
    for report in reports:
        length = len(report.name + report.team)
        if length > max_length:
            max_length = length
    return max_length


def clean_string_len(max_racers_info_length, name, team):
    space_len = max_racers_info_length - len(name + team)
    return space_len


def build_print(reports):
    max_racers_info_lenght = check_max_string_length(reports)
    counter = 0
    max_count = limit
    for report in reports:
        report: RacerReport
        place = dub_place_print(report.place)
        name = report.name
        team = report.team
        lap_time = (report.lap_time)
        if not lap_time :
            lap_time = "INVALID"
        lap_time = str(lap_time)
        add_spacers = clean_string_len(max_racers_info_lenght, name, team)
        if counter == limit:
            print("-"*65)
        print(place, name + " " + team + " " * add_spacers, lap_time, sep=" | ")
        counter +=1