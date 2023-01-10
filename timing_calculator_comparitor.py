import zipfile
import xml.parsers.expat
import pandas as pd
import logging
import re
import argparse

# from typing import Lists, string

# init logger
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

# Xilinx has a net X composed of z L1, y L2 wires
# with averaging data we create we artificialy build a net with those same wires and counts and see what the timing info is.


# Please dont over think things.


# Wires in VTR
# what is Rmetal -> resistance of wire per unit block. i.e. if L1 and L2 have same rmetal then L2 will have
# double timing to L1. Same for Cmetal.

# Wires in Xilinx:
# Since prjxary gives us data for wires that pass through tiles I wonder if we could use that to calculate
# Rmetal Cmetal? I think this would tottaly be valid! since by definition they are the same things.


# Switches in xilinx:
# these are "buffers in prjxary" this INT_L_X4Y53/INT_L.LOGIC_OUTS_L23->>WW2BEG1 is a switch from a logic out to a L2 Wire in an
# SB eq to a CB switch in VTR.


# Problems to solve:

# 1) Need to know what componenet a net is made up of. (get this from symbiflow script)
# # Break up of this
# # # 1) How many buffers (switches) and what types
# # # # 1) How many CB switches to specific wires IPIN and OPIN
# # # # 2) How many SB switches and between what wires
# # # 2) How many wires and what types
# # # 3) How many internal componenets and what types


# Calculate the names and types of ipins, takes in an array of the raw data
# def calc_IPIN(connections):
# here we are looking for buffers
# could be a little tricky since VTR uses the same switch for all wire types. Might not be so bad though
# we can build the delay into the internal connections

# INT_L_X4Y53/INT_L.LOGIC_OUTS_L23->>WW2BEG1 + opin stuff


# remember the first half will be output second will be input


# Picture of our delay model and names:
#                                                    WIRE
# LB------------------------->CB------------>SB<------------>
#     from_log_to_rout_pip       CB_SB_DELAY
#
#
#
#
#
#


# Init parser
parser = argparse.ArgumentParser(
    usage="timing_calculator_comparitor.py [-h] [-v] sheet excel_file",
    add_help=True,
)
parser.add_argument("-v", "--verbose", action="store_true", default=False)
parser.add_argument("excel_file", type=str)
parser.add_argument("sheet", default="Net ALU1_n_56", type=str)
parser.add_argument("wire", type=str)


class routing_structures:
    def __init__(self, wires, from_log_to_rout_pip):
        self.wires = wires
        self.from_log_to_rout_pip = from_log_to_rout_pip


def parse_file(args):
    # ziparchive = zipfile.ZipFile("/home/chem3000/Desktop/timing_basys.ods", "r")
    # xmldata = ziparchive.read("content.xml")
    # ziparchive.close()
    data = pd.read_excel(
        args.excel_file,
        sheet_name=args.sheet
        # usecols="A:A",
    )
    logger.debug(data)

    nameArray = data["Name"]

    from_log_to_rout_pip = pd.DataFrame()
    wires = pd.DataFrame()
    for name in nameArray:
        # print(name)
        if not pd.isna(name):
            if re.match(
                "(.*)((WW\d+|NN\d+|SS\d+|EE\d+|SW\d+|SE\d+|NW\d+|NE\d+)|(S|N|W|E)(L1|R1))(.*)(->|->>)(.*)",
                name,
            ) or re.match(
                "(.*)(->|->>)((WW\d+|NN\d+|SS\d+|EE\d+|SW\d+|SE\d+|NW\d+|NE\d+)|(S|N|W|E)(L1|R1))(.*)",
                name,
            ):
                from_log_to_rout_pip = from_log_to_rout_pip.append(
                    data[data["Name"] == name], ignore_index=True
                )
            elif re.match(
                "(.*)(/)((WW\d+|NN\d+|SS\d+|EE\d+|SW\d+|SE\d+|NW\d+|NE\d+)|(S|N|W|E)(L1|R1))(.{2,4})",
                name,
            ):  # this is our wires
                wires = wires.append(data[data["Name"] == name], ignore_index=True)
    logger.debug("************WIRES****************")
    logger.debug(wires)

    return routing_structures(wires, from_log_to_rout_pip)


class timing:
    def __init__(self, res, cap, time):
        self.res = res
        self.cap = cap
        self.time = time


def time_wire(name, wires):
    res = 0
    cap = 0
    time = 0
    cnt = 0
    logger.debug("****************TEST****************")
    # for wire in wires:
    print((wires["Name"].iloc[0]).find(name))
    for row in wires.index:
        if (wires["Name"].iloc[0]).find(name) == -1:
            wires = wires.drop(row)
    logger.debug(f"Only the timing data for the given wires {wires}")

    print(f"Resistance for {name} is {wires.RES.mean()}")
    print(f"Capacitance for {name} is {wires.CAP.mean()}")
    mean_list = ["FAST_MAX", "FAST_MIN", "SLOW_MAX", "SLOW_MIN"]
    # Sum all columns together
    df_mean = wires[mean_list].sum(axis=1)
    logger.debug(f"data structure before division\n{df_mean}")
    df_mean = df_mean.div(4)

    print(f"Time average for four corners of {name} is {df_mean.mean()}")
    # if (wire["Name"].iloc[0]).find(name) != -1:

    #     cnt += 1
    #     res += wire["RES"]
    #     cap += wire["CAP"]
    #     time += (wire["FAST_MAX"] + wire["FAST_MIN"]) / 2


def main():
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    routing_structures = None

    # file is "/home/chem3000/Desktop/timing_basys.ods"
    # sheet is "Net ALU1_n_56"
    routing_structures = parse_file(args)
    time_wire(args.wire, routing_structures.wires)


if __name__ == "__main__":
    main()
