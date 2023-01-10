from brains.build_data import RacerInfo
from brains.config import limit


def build_print(report: {str: RacerInfo}):
    spacer = check_max_string_length(report)
    racers = list(report.values())
    
    befor_limit = racers[:limit]
    after_limit = racers[limit:]

    for racer in befor_limit:
        racer.print(spacer)
    print("_" * 60)
    for racer in after_limit:
        racer.print(spacer)



def check_max_string_length(reports):
    """find max length of racer name + command
    used to build the same length of strings in build_total_print"""

    max_length = max(reports.values(), key= lambda i : len(i.name) + len(i.team))
    max_length = len( max_length.team) + len(max_length.name)


    max_length = max([len(report.name) + len(report.team) for report in reports.values()])
    return max_length + 1
