// ensure that the following constants are included only once
`ifndef RISCV_ALU_CONSTANTS
`define RISCV_ALU_CONSTANTS

/***************************************************************************
* 
* File: riscv_alu_constants.sv
*
* Author: Joshua Fife
* Class: ECEN 323, Sec. 002, Winter Semester 2022
* Date: 1/18/2022
*
*
* Description:
*    This file contains the varius constant values used by the alu_op to 
*    perform operations. The details of these constants can be found in the 
*    lab write up for lab 2 and the parameter names are self explanitory.
****************************************************************************/
localparam[3:0] AND_OP = 4'b0000;
localparam[3:0] OR_OP = 4'b0001;
localparam[3:0] ADD_OP = 4'b0010;
localparam[3:0] SUB_OP = 4'b0110;
localparam[3:0] LESS_OP = 4'b0111;
localparam[3:0] RIGHT_L_OP = 4'b1000;
localparam[3:0] LEFT_L_OP = 4'b1001;
localparam[3:0] RIGHT_AR_OP = 4'b1010;
localparam[3:0] XOR_OP = 4'b1101;

`endif // RISCV_ALU_CONSTANTS

// end of file