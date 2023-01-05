from parser import get_args
from build_print import build_person_print, build_total_print




def main():
    args = get_args()
    folder = args.files
    if args.driver:
        build_person_print(folder, args.driver)
    elif args.asc:
        build_total_print(folder, back_order=False)
    elif args.dasc:
        build_total_print(folder, back_order=True)


if __name__ == "__main__":
    main()
