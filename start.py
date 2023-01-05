from brains.build_data import  build_data
from brains.build_print import build_print


def main():
    report = build_data()
    build_print(report)

if __name__ == "__main__":
    main()
