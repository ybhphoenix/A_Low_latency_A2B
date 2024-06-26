//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2024-04-26
// File Name     : Expand1_n1o2k32.v
// Project Name  : 
// Design Name   : 
// Description   : 
//                
// 
// Dependencies  : 
// 
// Revision      : 
//                 - V1.0 File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////
// 
// WARNING: THIS FILE IS AUTOGENERATED
// ANY MANUAL CHANGES WILL BE LOST

`timescale 1ns/1ps
module Expand1_n1o2k32(
    input  wire [31:0] i_x,
    output wire [63:0] o_xp);


// ------------------------------------------------------------------------------
// for(i=0;i<1;i++)
// {
//   xp[i]=x[i];
// }
// ------------------------------------------------------------------------------
assign o_xp[ 0+:32] = i_x[ 0+:32];


// ------------------------------------------------------------------------------
// for(i=1;i<2;i++)
// {
//   xp[i]=0;
// }
// ------------------------------------------------------------------------------
assign o_xp[32+:32] = 32'd0;


endmodule
