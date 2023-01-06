from brains.build_data import RacerInfo
from brains.config import limit


def build_print(report: {str:RacerInfo}):
    spaces_max = check_max_string_length(report)
    counter = 0
    for racer in report.values():
        if counter == limit:
            print("_"*60)
        spacer_length = clean_string_len(spaces_max,racer.name,racer.team)
        racer.get_print(spacer_length)
        counter +=1

def clean_string_len(max_racers_info_length, name, team):
    space_len = max_racers_info_length - len(name + team)
    return space_len


def check_max_string_length(reports):
    """find max length of racer name + command
    used to build the same length of strings in build_total_print"""
    max_length = 0
    for report in reports.values():
        length = len(report.name + report.team)
        if length > max_length:
            max_length = length
    return max_length


def clean_string_len(max_racers_info_length, name, team):
    space_len = max_racers_info_length - len(name + team)
    return space_len

