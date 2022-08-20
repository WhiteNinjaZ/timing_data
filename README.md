## Overview

This repo includes some of the work I have done on the timing info for the artix parts. Recently I have been using python scripts to figure out how the json timing data in prjxray works. interpret_wire_timing.py is an example of that. Right now the code loops through every wire inside of the INT L and R tiles and makes sure that the timing info of a buffer that goes to a specific wire length is the same (i.e. makes sure that all pips that ending in ->>WW2BEG0 are the same). It might be worth looking through the json files I point to in that script as well as the script itself to get an idea of what is going on.

## Useful info 
There are two things that I see as very useful to us in prjxray. One is the tile_type.json files located in database/artix7. These not only include general interconnect for the tiles but also include prjxrays timing models for every internal switch and every wire crossing through the tile. 

The second thing I see as useful are the pre-made timing report scripts found in prjxray/utils. It is possible to run a design through prjxray and get detailed timing info for every wire, buffer, and OPIN/IPIN along each net in a design. Here are the steps to do that for a the provided design meant for a basys board: 

Here is how I got the Excell spreadsheet of timing info for the design in the Vivado folder:
1) build a project using the provided .sv and constraint files.
2) run implementation and open implemented design
3) source <path to prjxray dir>/utils/write_timing_info.tcl
4) run write_timing_info <path to your desired output json file> in the tcl consol
5) copy your output json file into another file in the same directory with the .json5 extension. (eg. cp output_basys.json output_basys.json5)
6) run prjxray/utils/clean_json5.py <path to your json5 file from step 5> <path to original json file from step 4>
7) finally run prjxray/utils/create_timing_worksheet_db.py --timing_json <path to json file from step 4> --db-root <path to prjxray>/database/artix7 --part "xc7a35tcpg236-2" --output_xlsx <path to output Excel spreadsheet>

Once the Excel spread sheet is created open it and take a look. Along the bottom will be diffrent spreadsheets for every individual net in your design. Each sheet has the following useful properties:
1) The path the net takes is given in order from top to bottom (i.e. in the sheet "Net ALU1_n_33" CLBLM_L_X10Y54/CLBLM_M_AMUX
is the start of the net. The interconnect then continues through a wire of the same name and then passes through a passTransistor and onto a LOGIC_OUT wire. Eventually the interconnect makes its way to an IPIN). Note if a net branches from an outpin into more than one input pin (and most of them do) then every path along the net will be specified.

2) After each path along the net is given a timing summery is given for the net that compares symbiflows timing model to vivado (for example on sheet "Net ALU1_n_33" row 24-26 give the overall calculated timing for the first branch of the net).


## Some useful info about the naming of Xilinx Interconnect

1) A net is a routed collection of wires and contains timing info we can parse from Vivado. A node is essentially a wire in Vivado.
2) With the exception of length 1,12, and 18 wires each wires name contains the name of the tile in which it originated followed by a `/` followed by the wires direction (i.e. NN, NW, SS, SW) followed by the wires length followed by what I think is the pip name from which the wire originated (usually END for end or BEG for beginning. Wires without these suffixes are probably internal wires to logic blocs). An example of this is a NW L4 wire originating in the INT_L_X10Y54 tile (INT_L_X10Y54/NW4BEG0). 
3) Length one wires only have only one character specifying their cardinal direction. This is followed by either an L or an R.
4) length 18 and 12 wires have their own naming conventions. Pg. 17 of netcracker and specificly figure 9 might be helpful in understanding these wires naming.  
