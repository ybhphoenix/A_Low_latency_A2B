//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2023-10-08
// File Name     : Expand2_n3o5k32.v
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
module Expand2_n3o5k32(
    input  wire  [95:0] i_x,
    output wire [159:0] o_xp);


// ------------------------------------------------------------------------------
// for(i=0;i<2;i++)
// {
//   xp[i]=0;
// }
// ------------------------------------------------------------------------------
assign o_xp[ 0+:32] = 32'd0;
assign o_xp[32+:32] = 32'd0;

// ------------------------------------------------------------------------------
// for(i=0;i<3;i++)
// {
//   xp[5-3+i]=x[i];
// }
// ------------------------------------------------------------------------------
assign o_xp[ 64+: 32] = i_x[  0+: 32];
assign o_xp[ 96+: 32] = i_x[ 32+: 32];
assign o_xp[128+: 32] = i_x[ 64+: 32];



endmodule