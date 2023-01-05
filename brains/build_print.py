from config import files
from build_data import collect_data, RacerReport
from fuzzywuzzy import fuzz


def find(folder, report):

    """build person report"""

    print("*" * 20,
          "Awesome Monaco #Personal Report",
          "Place: " + str(report.place),
          "Name: " + report.racer_name,
          "Command: " + report.team,
          "Lap Time: " + report.lap_time,
          "*" * 20,
          sep="\n")


def build_place_print(place):
    """generate same lenght of string from 1 adn 11 numbers  """
    if len(str(place)) < 2:
        return str(place) + ". "
    else:
        return str(place) + "."


def check_max_string_length(reports):
    """find max length of racer name + command
    used to build the same length of strings in build_total_print"""
    max_length = 0
    for report in reports:
        length = len(report.name + report.team)
        if  length > max_length:
            max_length = length
    return max_length



def build_print(reports):
    max_racers_info_lenght = check_max_string_length(reports)
    for report in reports:
        print(report)





