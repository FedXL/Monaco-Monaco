from brains.build_data import build_report
from brains.build_print import build_print
from brains.parser import get_args


def main():
    args = get_args()
    report = build_report(folder = args.files, driver=args.driver, reverse=args.desc)
    build_print(report)

if __name__ == "__main__":
    main()
