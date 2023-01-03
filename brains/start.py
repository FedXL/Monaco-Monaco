import argparse

from build_print import build_person_print, build_total_print


def use_parser():
    parser = argparse.ArgumentParser(description="Monaco Racing Task",
                                     epilog="I hope it will be funny")
    parser.add_argument('--files', type=str, required=True, help="Enter your folder path")
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('--asc', help="direct order", action="store_true")
    group.add_argument('--dasc', help="undirect order", action="store_true")
    group.add_argument('--driver', help="driver name", type=str, default=None)
    args = parser.parse_args()
    print(args)
    return args


def run():
    args = use_parser()
    folder=args.files
    if args.driver:
         build_person_print(folder,args.driver)
    elif args.asc:
         build_total_print(folder, back_order=False)
    elif args.dasc:
         build_total_print(folder, back_order=True)

if __name__ == "__main__":
    run()

