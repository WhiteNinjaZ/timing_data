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
    print("**************WIRE TIMING*********************")
    if time.time is None:
        print("No timing data found for given wire")
    else:
        print(f"RES WIRE: {time.time.res}")
        print(f"CAP WIRE: {time.time.cap}")
        print(f"TIME WIRE: {time.time.time} ps\n\n")

    print("**************CB_I*********************")
    if time.cb_i is None:
        print("No timing data found for given wire")
    else:
        print(f"RES CB_I: {time.cb_i.res}")
        print(f"CAP CB_I: {time.cb_i.cap}")
        print(f"TIME CB_I: {time.cb_i.time} ps\n\n")

    print("**************CB_O*********************")
    if time.cb_o is None:
        print("No timing data found for given wire")
    else:
        print(f"RES CB_O: {time.cb_o.res}")
        print(f"CAP CB_O: {time.cb_o.cap}")
        print(f"TIME CB_O: {time.cb_o.time} ps\n\n")

    print("**************SB*********************")
    if time.sb_time is None:
        print("No timing data found for given wire")
    else:
        print(f"RES SB: {time.sb_time.res}")
        print(f"CAP SB: {args.wire} is {time.sb_time.cap}")
        print(f"TIME SB: {time.sb_time.time} ps\n\n")


if __name__ == "__main__":
    main()
