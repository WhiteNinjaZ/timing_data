from timing_calculator_comparitor import *

# Init parser
parser = argparse.ArgumentParser(
    usage="timing_calculator_comparitor.py [-h] [-v] sheet excel_file",
    add_help=True,
)
parser.add_argument("-v", "--verbose", action="store_true", default=False)
parser.add_argument("excel_file", type=str)
parser.add_argument("sheet", default="Net ALU1_n_56", type=str)
parser.add_argument("wire", type=str)


def main():
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    routing_structures = None

    # file is "/home/chem3000/Desktop/timing_basys.ods"
    # sheet is "Net ALU1_n_56"
    routing_structures = parse_file(args)
    time_wire(args.wire, routing_structures)


if __name__ == "__main__":
    main()
