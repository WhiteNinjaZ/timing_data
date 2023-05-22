import json 
import re
import argparse
import statistics as stat

# for wires go thorough every json file and look in the wires list for matches to a specif name part. 

# parse wires in a single sheet.
# def parse_wires():
class timing:
    def __init__(self, res, cap, time):
        self.res = res
        self.cap = cap
        self.time = time

def parse_sb(data, name):
    pips = data["pips"]

    wire_to_wire_time = []
    res = []
    cap = []

    for key in pips:
        if re.match(f"(.*)((WW\d+|NN\d+|SS\d+|EE\d+|SW\d+|SE\d+|NW\d+|NE\d+)|(S|N|W|E)(L1|R1))(END\d+)(->|->>)({name})(BEG\d+)", key):
            for i in range(len(pips[key]["src_to_dst"]["delay"])):
                wire_to_wire_time.append(float(pips[key]["src_to_dst"]["delay"][i])) 
            res.append(float(pips[key]["src_to_dst"]["res"]))
            cap.append(float(pips[key]["src_to_dst"]["in_cap"]))
    
    return timing(res, cap, wire_to_wire_time)

def parse_cbo(data, name):
    pips = data["pips"]

    wire_to_wire_time = []
    res = []
    cap = []

    for key in pips:
        if re.match(f"(.*)(LOGIC)(.*)(->|->>)({name})(BEG\d+)", key):
            for i in range(len(pips[key]["src_to_dst"]["delay"])):
                wire_to_wire_time.append(float(pips[key]["src_to_dst"]["delay"][i])) 
            res.append(float(pips[key]["src_to_dst"]["res"]))
            cap.append(float(pips[key]["src_to_dst"]["in_cap"]))
    
    return timing(res, cap, wire_to_wire_time)


def parse_wire(data, name):
    wires = data["wires"]

    cap = []
    res = []

    for key in wires:
        if re.match(f"(.*)({name})(.*)", key) and wires[key] != None:
            x = float(wires[key]["res"])
            y = float(wires[key]["cap"])
            if x != None:
                res.append(x)
            if y != None:
                cap.append(y)

    return timing(res, cap, 0.0)
    
class internal_timing_info:
    def __init__(self, time_pin, res_pin, buf_cap, res_buf, time_buf):
        self.time_pin = time_pin
        self.res_pin = res_pin
        self.buf_cap = buf_cap
        self.res_buf = res_buf
        self.time_buf = time_buf 


def parse_cb_internal(data):
    pips = data["pips"]
    sites = data["sites"][0]["site_pins"]
    outpin_list = ["D", "DMUX", "C", "CMUX", "B", "BMUX", "A", "AMUX"]
    # wires = ? what are the regex to find the parts of the wires we want? Do we even need these 
    # since the wires don't have timing?

    outpin_info = [sites[site] for site in sites if site in outpin_list]
    time_pin = []
    res_pin = []
    # ! There is no capacitance for the opins. 
    for info in outpin_info:
        # Wonder why capacitance is not included here in the json for site pins?
        for dellay in info["delay"]:
            time_pin.append(float(dellay))
        
        res_pin.append(float(info["res"]))

    cap_buf = []
    res_buf = []
    timing_buf = []
    for buffer in pips: # get the pips for the cross bar section. 
        if re.match(f"(.*)(_D|_DMUX|_C|_CMUX|_B|_BMUX|_A|_AMUX)(->|->>)(.*)(LOGIC)(.*)", buffer):
            single_res = pips[buffer]["src_to_dst"]["res"]
            single_cap = pips[buffer]["src_to_dst"]["in_cap"]
            single_delay = pips[buffer]["src_to_dst"]["delay"]
            if single_res != None:
                res_buf.append(float(single_res))
            if single_cap != None:
                cap_buf.append(float(single_cap))
            if single_delay != None:
                for i in range(len(single_delay)):
                    timing_buf.append(float(single_delay[i])) 

        # wires = data["wires"]

        # ! MAY NEED TO ACOUNT FOR THE AMUX->A PIPS

        # for wire in wires:
        #     if 

    #! As far as I can tell, internal wires have no timing in the json folder (assuming that the wires we are looking 
    #! for are LOGIC (between crossbar and CB) and wires ending in _A/_AMUX for wire between outpin and crossbar)

    #! Interesting enough it looks like the opins A1-6 etc. do have timing. 


    #  We need pip info for connections
    #  We need site info to get the timing for the outpins
    # We need wire info in order to get the small internal wire.

    return internal_timing_info(time_pin, res_pin, cap_buf, res_buf, timing_buf)
    

# def parse_crosbar_pips(data):



# timing info from logic out to routing. 
# def parse_clbo():

parser = argparse.ArgumentParser(
    usage="timing_calculator_comparitor.py [-h] [-v] json_file wire_name",
    add_help=True,
)
parser.add_argument("-v", "--verbose", action="store_true", default=False)
parser.add_argument("json_file", type=str)
# parser.add_argument("-s", "--sheet", dest="sheet", default=None, type=str)
parser.add_argument("wire_name", type=str)

def main():
    args = parser.parse_args()
    # your json object will be stored as a dictionary where the objects are keys (i.e. pips) and the values are lists. 
    # you will probably have to iterate through the keys and then through the lists.  

    with open(args.json_file, 'r') as INT_L:
        data = json.load(INT_L)
        time_data = parse_sb(data, args.wire_name)
        # print(time_data.res)
        if time_data.res != []:
            print(f"Resistance to wire SB: {stat.mean(time_data.res)}, std: {stat.stdev(time_data.res)}")
        if time_data.cap != []:
            print(f"Capacitance to wire SB: {stat.mean(time_data.cap)}, std: {stat.stdev(time_data.cap)}")
        if time_data.time != []:
            print(f"Delay to wire SB: {stat.mean(time_data.time)}, std: {stat.stdev(time_data.time)}\n")

        # /////////////////////////////////////////// CB output ///////////////////////////////////
        list_of_cb_files = ["/home/chem3000/Programs/prjxray/database/artix7/tile_type_CLBLL_L.json"]

        time_cb = parse_cbo(data, args.wire_name) # The outer timming is only found in the connection blocks. 

        for file in list_of_cb_files:
            with open(file, 'r') as FILE:
                cb_data = json.load(FILE)
                time_internal = parse_cb_internal(cb_data)


        print(f"Resistance for the internal out pin: {stat.mean([x + y for x, y in zip(time_internal.res_pin, time_internal.res_buf)])}, std: {stat.mean([x + y for x, y in zip(time_internal.res_pin, time_internal.res_buf)])}\n")
        #  in the first test we did all other values for this where zero

        if time_data.res != []:
            print(f"Resistance to wire CBO: {stat.mean(time_cb.res)}, std: {stat.stdev(time_cb.res)}")
        if time_data.cap != []:
            print(f"Capacitance to wire CBO: {stat.mean(time_cb.cap)}, std: {stat.stdev(time_cb.cap)}")
        if time_data.time != []:
            print(f"Delay to wire CBO: {stat.mean(time_cb.time)}, std: {stat.stdev(time_cb.time)}")

        # /////////////////////////////////////////// Wire ///////////////////////////////////
        time_wire = parse_wire(data, args.wire_name)

        if time_wire.res != []:
            print(f"Resistance for wire: {stat.mean(time_wire.res)}, std: {stat.stdev(time_wire.res)}")
        if time_wire.cap != []:
            print(f"Capacitance for wire: {stat.mean(time_wire.cap)}, std: {stat.stdev(time_wire.cap)}")

        # !next step is to see what kind of deviation is between the components that make up the 
        # !wires that come into the CB connection. 

        # delay is delay. If you can use the stuff in vtr go for it. 

    # alright here we go this is how things are set up:
    # the entire json file is an object. 
    # pips are a list of json objects.

if __name__ == "__main__":
    main()
