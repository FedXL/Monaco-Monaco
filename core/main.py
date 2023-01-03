import argparse


def use_parser():
    parser = argparse.ArgumentParser(description="Monaco Racing Task",
                                     epilog="I hope it will be funny")
    parser.add_argument('--files', type=str, default=None, help="Enter your folder path")
    parser.add_argument('--asc', type=int, default=0, help="direct order")
    parser.add_argument('-desc', type=int, default=1, help="reverse order")
    parser.add_argument('--driver', type=str, default=None, help="Enter racer name")
    parser.add_argument('move', choices=['--rock', '--paper', '--scissors'], default=None)

    args = parser.parse_args()
    print(args)
    return args



def main():
    args = use_parser()


if __name__ == "__main__":
    main()