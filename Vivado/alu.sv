// This timescale statement indicates that each time tick of the simulator
// is 1 nanosecond and the simulator has a precision of 1 picosecond. This 
// is used for simulation and all of your SystemVerilog files should have 
// this statement at the top. 
`timescale 1 ns / 1 ps 

// Include the RISC-V constraints
`include "riscv_alu_constants.sv"

/***************************************************************************
* 
* File: alu.sv
*
* Author: Joshua Fife
* Class: ECEN 323, Sec. 002, Winter Semester 2022
* Date: 1/18/2022
*
* Module: alu
*
* Description:
*    This module implements an ALU for the RISC-V processor. 
*	 Operations that this implementation can perform are 
* 	 add, subtract, bitwise and, bitwise or and xor, less than,
*  	 shift left logical, shift right logical, and shift right arithmatic.
*    you can find out more by going to part one of the lab write up for this
*    lab.
****************************************************************************/
module alu(op1, op2, alu_op, zero, result);

	// input and output ports of the alu. Port names are self explanitory
	// zero is high when the result of our alu is 0. 
	input wire logic [31:0] op1, op2;
	input wire logic [3:0] alu_op;
	output logic zero;
	output logic [31:0] result;
	
	
	// The combinational logic used for the ALU. 
	// performs varius operations on op1 and op2 depending on the 
	// value of alu_op
	always_comb 
	begin

	   case (alu_op)
	   	   default : result = op1 + op2;
	       ADD_OP :  result = op1 + op2;
	       SUB_OP :  result = op1 - op2;
	       AND_OP :  result = op1 & op2;
	       OR_OP : result = op1 | op2;
	       XOR_OP : result = op1 ^ op2;
	       LESS_OP : result = $signed(op1) < $signed(op2);
	       LEFT_L_OP : result = op1 << op2[4:0];
	       RIGHT_L_OP : result = op1 >> op2[4:0];
	       RIGHT_AR_OP : result = $unsigned($signed(op1) >>> op2[4:0]);
	   endcase
	   
	   // set zero high if the result is 0.
	   if(!result)
	       zero = 1;
	   else
	       zero = 0;
	       
	end

	
	
endmodule