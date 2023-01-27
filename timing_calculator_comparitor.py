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
# LB<------------------------CB<------------SB<------------>
#     from_rout_pip_to_LB
#
#
#


#! set python enterpreter by ctrl+shift+p (open command pallete) type python enterpreter and select

# constant definitions
MEAN_OF_FOUR = 4
MEAN_OF_TWO = 2


class routing_structures:
    def __init__(self, wires, from_log_to_rout_pip):
        self.wires = wires
        self.from_log_to_rout_pip = from_log_to_rout_pip


# parse file does the shabang
# time wire parses a single data frame and gives us the routing structures timing
#


def parse_routing_structures(data):
    nameArray = data["Name"]

    from_log_to_rout_pip = pd.DataFrame()
    wire_wire_connections = pd.DataFrame()
    wires = pd.DataFrame()
    # wires.columns(data.head)
    # cb_list = []
    # for name in nameArray:
    #     # print(name)
    #     if not pd.isna(name):
    #         if re.match(
    #             "(.*)((WW\d+|NN\d+|SS\d+|EE\d+|SW\d+|SE\d+|NW\d+|NE\d+)|(S|N|W|E)(L1|R1))(END\d+)(->|->>)(IMUX)(.*)",
    #             name,
    #         ) or re.match(
    #             "(.*)(LOGIC)(.*)(->|->>)((WW\d+|NN\d+|SS\d+|EE\d+|SW\d+|SE\d+|NW\d+|NE\d+)|(S|N|W|E)(L1|R1))(BEG\d+)",
    #             name,
    #         ):
    # from_log_to_rout_pip = from_log_to_rout_pip.append(
    #     data[data["Name"] == name], ignore_index=True
    # )
    # from_log_to_rout_pip.loc[len(from_log_to_rout_pip)] = data[
    #     data["Name"] == name
    # ]

    # from_log_to_rout_pip = pd.concat(
    #     [from_log_to_rout_pip, data[data["Name"] == name]],
    #     axis=0,
    #     ignore_index=True,
    # )
    # from_log_to_rout_pip = pd.concat(
    #     [from_log_to_rout_pip, cb_list], ignore_index=True, axis=0
    # )
    # print("****************LOGIC to ROUTING****************")
    # print(cb_list)

    wire_list = []
    cb_list = []
    # wire_list.append(data.head())
    for row in data.index:
        if data["Type"].iloc[row] == "Part of wire":  # this is our wires
            wire_list.append(data.iloc[row])
        wire_name = data["Name"].iloc[row]
        if re.match(
            "(.*)((WW\d+|NN\d+|SS\d+|EE\d+|SW\d+|SE\d+|NW\d+|NE\d+)|(S|N|W|E)(L1|R1))(END\d+)(->|->>)(IMUX)(.*)",
            str(wire_name),
        ) or re.match(
            "(.*)(LOGIC)(.*)(->|->>)((WW\d+|NN\d+|SS\d+|EE\d+|SW\d+|SE\d+|NW\d+|NE\d+)|(S|N|W|E)(L1|R1))(BEG\d+)",
            str(wire_name),
        ):
            cb_list.append(data.iloc[row])

    wires = pd.concat(
        [wires, pd.DataFrame(wire_list)],
        ignore_index=True,
        axis=0,
    )

    from_log_to_rout_pip = pd.concat(
        [from_log_to_rout_pip, pd.DataFrame(cb_list)],
        ignore_index=True,
        axis=0,
    )

    logger.debug("************WIRES****************")
    logger.debug(wires)

    logger.debug("****************LOGIC to ROUTING****************")
    logger.debug(from_log_to_rout_pip)

    return routing_structures(wires, from_log_to_rout_pip)


class timing:
    def __init__(self, res, cap, time):
        self.res = res
        self.cap = cap
        self.time = time

    def __eq__(self, other):
        return (
            self.res == other.res and self.time == other.time and self.cap == other.cap
        )


def time_cb(name, routing_structures):
    logic_to_routing = routing_structures.from_log_to_rout_pip


def time_wire(name, routing_structures):
    # TODO: our current wire list does not include wire parts of the form CLBLL_L_X4Y54/CLBLL_WL1END3
    # TODO: this must be rectified. I think the wires we are getting are actually the incorrect type because
    # all of their values are zero

    res = 0
    cap = 0
    time = 0

    wires = routing_structures.wires
    logger.debug("****************TEST****************")
    # for wire in wires:
    # print((wires["Name"].iloc[0]).find(name))
    true_wires = []
    # print("Wires:\n\n", wires)
    for row in wires.index:
        if (wires["Name"].iloc[row]).find(name) != -1:
            true_wires.append(wires.iloc[row])
    wires = pd.DataFrame(true_wires)
    # for row in logic_to_routing.index:
    #     if logic_to_routing["Name"].iloc[0].find(name) == -1:
    #         logic_to_routing = logic_to_routing.drop(row)

    # logger.debug(
    #     f"Only the timing data for the given wires\n{wires}\n\n{logic_to_routing}\n\n{logic_to_routing}"
    # )
    mean_list = ["FAST_MAX", "FAST_MIN", "SLOW_MAX", "SLOW_MIN"]
    if len(wires) != 0:
        res = wires.RES.mean()
        cap = wires.CAP.mean()
        wire_mean = wires[mean_list].sum(axis=1)
        logger.debug(f"Wire data structure before division\n{wire_mean}")
        wire_mean = wire_mean.div(MEAN_OF_FOUR)
        time = wire_mean.mean()

    #     if len(logic_to_routing) != 0:
    #         res += logic_to_routing.RES.mean()
    #         res /= MEAN_OF_TWO
    #         cap += logic_to_routing.CAP.mean()
    #         cap /= MEAN_OF_TWO

    #         rout_mean = logic_to_routing[mean_list].sum(axis=1)
    #         rout_mean = rout_mean.div(MEAN_OF_FOUR)
    #         time += rout_mean.mean()
    #         time /= MEAN_OF_TWO

    # elif len(logic_to_routing) != 0:
    #     res = wires.RES.mean()
    #     cap = wires.CAP.mean()

    #     rout_mean = logic_to_routing[mean_list].sum(axis=1)
    #     rout_mean = rout_mean.div(MEAN_OF_FOUR)
    #     time = rout_mean.mean()
    else:
        return None  # TODO whatever calls this needs to skip a mean addition if this function returns none

    logger.debug(f"Resistance for {name} is {res}")
    logger.debug(f"Capacitance for {name} is {cap}")
    logger.debug(f"Time average for four corners of {name} is {time}")
    # res = (wires.RES.mean() + logic_to_routing.RES.mean()) / MEAN_OF_TWO

    # print(f"Resistance for {name} is {res}")
    # cap = (wires.CAP.mean() + logic_to_routing.CAP.mean()) / MEAN_OF_TWO

    # print(f"Capacitance for {name} is {cap}")

    # Sum all columns together

    # time = (wire_mean.mean() + rout_mean.mean()) / MEAN_OF_TWO
    # print(f"Time average for four corners of {name} is {time}")
    # if (wire["Name"].iloc[0]).find(name) != -1:

    #     cnt += 1
    #     res += wire["RES"]
    #     cap += wire["CAP"]
    #     time += (wire["FAST_MAX"] + wire["FAST_MIN"]) / 2
    return timing(res, cap, time)


def parse_file(args):
    # ziparchive = zipfile.ZipFile("/home/chem3000/Desktop/timing_basys.ods", "r")
    # xmldata = ziparchive.read("content.xml")
    # ziparchive.close()
    if args.sheet is None:
        all_sheets = pd.read_excel(args.excel_file, sheet_name=None)
        rout_struct = None
        time = timing(0, 0, 0)
        sheet_time = None
        rout_struct = None
        for sheet_key in all_sheets:
            # try:
            if sheet_key == "Summary":
                continue
            rout_struct = parse_routing_structures(all_sheets[sheet_key])
            sheet_time = time_wire(args.wire, rout_struct)
            if sheet_time is None or sheet_time == timing(0, 0, 0):
                continue
            time = timing(
                (time.res + sheet_time.res) / MEAN_OF_TWO,
                (time.cap + sheet_time.cap) / MEAN_OF_TWO,
                (time.time + sheet_time.time) / MEAN_OF_TWO,
            )
            # except Exception as e:
            #     print(f"error caught on sheet {sheet_key}\n\n")
            #     print("Error raised:", e)
            #     print(all_sheets[sheet_key])
            #     return None
        return timing(time.res, time.cap, time.time)

    else:
        data = pd.read_excel(
            args.excel_file,
            sheet_name=args.sheet
            # usecols="A:A",
        )
        rout_struct = parse_routing_structures(data)
        return time_wire(args.wire, rout_struct)
    # logger.debug(data)
