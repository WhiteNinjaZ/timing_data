// This timescale statement indicates that each time tick of the simulator
// is 1 nanosecond and the simulator has a precision of 1 picosecond. This 
// is used for simulation and all of your SystemVerilog files should have 
// this statement at the top. 
`timescale 1 ns / 1 ps 


/***************************************************************************
* 
* File: regfile.sv
*
* Author: Joshua Fife
* Class: ECEN 323, Sec. 002, Winter Semester 2022
* Date: 1/26/2022
*
* Module: regfile
*
* Description:
*    This module implements the low level version of a Register file.
*    The regfile implemented in this module is 32x32 in size.
*    It has 2 read ports and one right port.
****************************************************************************/
module regfile(clk, readReg1, readReg2, writeReg, writeData, write, readData1, readData2);

	// input and output ports of the regfile. Port names are self explanitory. 
	input wire logic clk, write;
	input wire logic [4:0] readReg1, readReg2, writeReg;
	input wire logic [31:0] writeData;
	output logic [31:0] readData1, readData2;
	
	// the register file 32x32
	logic [31:0] register[31:0];
	
	// Parameter for register size used in for loop. 
	// Our current register is 32*32 
	localparam registerSize = 32;
	
	
	// initialize the register file with all zeros
	integer i;
    initial
      for (i=0; i < registerSize; i=i+1)
        register[i] = 0;

     
     // This always_ff block is the internal logic for
     // our 32x32 register. The code is based off of the
     // code in the lab write up for lab3 we must ensure that 
     // register zero is never writen too.
	 always_ff@ (posedge clk) begin
	   readData1 <= register[readReg1];
	   readData2 <= register[readReg2];

	   if (write && writeReg != 0) begin
	     register[writeReg] <= writeData;

	     if (readReg1 == writeReg)
	         readData1 <= writeData;

	     if (readReg2 == writeReg)
	         readData2 <= writeData;

	   end
	   
	 end	


endmodule