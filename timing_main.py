from timing_calculator_comparitor import *

# Init parser
parser = argparse.ArgumentParser(
    usage="timing_calculator_comparitor.py [-h] [-v] sheet excel_file",
    add_help=True,
)
parser.add_argument("-v", "--verbose", action="store_true", default=False)
parser.add_argument("excel_file", type=str)
parser.add_argument("-s", "--sheet", dest="sheet", default=None, type=str)
parser.add_argument("wire", type=str)


def main():
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # file is "/home/chem3000/Desktop/timing_basys.ods"
    # sheet is "Net ALU1_n_56"
    parse_file(args)
    time = parse_file(args)
    if time is None:
        print("No timing data found for given wire")
        return
    print(f"Resistance for wire {args.wire} is {time.time.res}")
    print(f"Capacitance for wire {args.wire} is {time.time.cap}")
    print(f"Intrinsic time for wire {args.wire} is {time.time.time}")

    if time.cb_i is None:
        print("No timing data found for given wire")
        return
    print(f"Resistance for cb_i {args.wire} is {time.cb_i.res}")
    print(f"Capacitance for cb_i {args.wire} is {time.cb_i.cap}")
    print(f"Intrinsic time for cb_i {args.wire} is {time.cb_i.time}")


if __name__ == "__main__":
    main()
