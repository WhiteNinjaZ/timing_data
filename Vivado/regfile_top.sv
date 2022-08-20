// This timescale statement indicates that each time tick of the simulator
// is 1 nanosecond and the simulator has a precision of 1 picosecond. This 
// is used for simulation and all of your SystemVerilog files should have 
// this statement at the top. 
`timescale 1 ns / 1 ps 

/***************************************************************************
* 
* File: regfile_top.sv
*
* Author: Joshua Fife
* Class: ECEN 323, Sec. 002, Winter Semester 2022
* Date: 1/26/2022
*
* Module: regfile_top
*
* Description:
*    This module implements the top level design for lab3. It contains
*    a register file, an alu, a address register, and varius internal logic.
*    the diagram for this circuit as well as info on the expected circuit 
*    operation can be found in the lab3 write up.
****************************************************************************/
module regfile_top(clk, btnc, btnl, btnu, btnd, sw, led);

	// input and output ports of the top level design.
    // Port names are self explanitory. 
	input wire logic clk, btnc, btnl, btnu, btnd;
	input wire logic [15:0] sw;
	output logic [15:0] led;
	
    // the internal wires/registers for 
    // our address register and btnc one 
    // shot output. btnc_d is btnc sync.
    // and btnc_one is the output of the
    // one shot
	logic [14:0] Address_register;
	logic btnc_d, btnc_one;
	
    // wires for the ports of the regfile. Names match 
    // diagram in lab write up and are self explanitory
	logic [31:0] regReadDataA, regReadDataB, writeData_in;
	
    // Alu wires zero_throw is the output of the alu's zero 
    // check and is not used in this lab. result is the alu output.
	logic zero_throw;
	logic [31:0] result;
	

	//This always ff block implements our address register file
    always_ff@ (posedge clk) begin
        btnc_d <= btnc;
        if(btnu) 
            Address_register <= 0;
        else if(btnl)
            Address_register <= sw[14:0];
        else
            Address_register <= Address_register;       
    end
    
    
    //one shot module for our btnc. Reset by btnu
    OneShot osc (.clk(clk), .rst(btnu), .in(btnc_d), .os(btnc_one));
    
    // Always Comb Logic for mux going to writeData on Register
    // sw[15] = 0, writeData signal gets the output of the alu
    // sw[15] = 1, writeData = sign extended version of first 15
    // switches
    always_comb begin
        if(sw[15])
            writeData_in = {{17{sw[14]}}, sw[14:0]};
        else
            writeData_in = result;
    end
    


    // Implementation of our regfile. Follow diagram in lab write up 
    // to learn about port conection.
    regfile masterReg (.clk(clk), .readReg1(Address_register[4:0]), 
    .readReg2(Address_register[9:5]), .writeReg(Address_register[14:10]), 
    .writeData(writeData_in), .write(btnc_one), .readData1(regReadDataA), 
    .readData2(regReadDataB));


    
    // Implementation of our alu. Ports match immage in lab write up.
    alu ALU1 (.op1(regReadDataA), .op2(regReadDataB), .alu_op(sw[3:0]), 
    .zero(zero_throw), .result(result));
    
    
    // logic for multiplexor selecting values to give to the LEDs
    always_comb begin
        if(!btnd)
            led = regReadDataA[15:0];
        else
            led = regReadDataA[31:16];
    end
	

endmodule