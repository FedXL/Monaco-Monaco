from brains.build_data import build_report
from brains.build_print import build_print
from brains.parser import get_args


def main():
    args = get_args()
    print(args)
    report = build_report(args)
    build_print(report)

if __name__ == "__main__":
    main()
