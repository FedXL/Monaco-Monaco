from brains.build_data import RacerInfo


def build_print(report: {str:RacerInfo}):
    spaces_max = check_max_string_length(report)
    for racer in report.values():
        name = racer.name
        team = racer.team
        place = dub_place_print(racer.place)

        lap_time = racer.lap_time
        spaces_len = clean_string_len(spaces_max,name,team)
        print(place, name + spaces_len*" " + team, lap_time, sep=" | ")


def dub_place_print(place):
    """generate same lenght of string from 1 adn 11 numbers  """
    if place == "DNF":
        return place
    elif len(str(place)) < 2:
        place = str(place) + ". "
    else:
        place = str(place) + "."
    return place


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

