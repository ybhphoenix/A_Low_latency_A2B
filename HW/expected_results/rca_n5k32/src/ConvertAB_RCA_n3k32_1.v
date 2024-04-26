//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2024-04-26
// File Name     : ConvertAB_RCA_n3k32_1.v
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
module ConvertAB_RCA_n3k32_1(
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         i_dvld,
    input  wire         i_rvld,
    input  wire [123:0] i_n,
    input  wire  [95:0] i_a,
    output wire  [95:0] o_z,
    output wire         o_dvld);

wire     [31:0] x;
wire     [31:0] xd;
wire     [95:0] xp;
wire     [63:0] y;
wire     [63:0] yd;
wire     [95:0] yp;
wire            vrl;
wire            vy;
wire            vll;

// ------------------------------------------------------------------------------
// Connect i_dvld to left leaf valid
// ------------------------------------------------------------------------------
assign vll = i_dvld;


// ------------------------------------------------------------------------------
// Connect input port to left leaf data
// ------------------------------------------------------------------------------
assign x[ 0+:32] = i_a[ 0+:32];


// ------------------------------------------------------------------------------
// Delay left leaf
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (32),
    .N (62))
  u0_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (vll),
    .i_en   (i_rvld),
    .i_x    (x[0+:32]),
    .o_z    (xd[0+:32]));



// ------------------------------------------------------------------------------
// Do a Expand(left leaf) instance
// ------------------------------------------------------------------------------
Expand1_n1o3k32
  u1_Expand1_n1o3k32
   (.i_x  (xd[0+:32]),
    .o_xp (xp[0+:96]));



// ------------------------------------------------------------------------------
// Do ConvertAB(right leaf) instance
// ------------------------------------------------------------------------------
ConvertAB_RCA_n2k32_1
  u2_ConvertAB_RCA_n2k32_1
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (i_dvld),
    .i_rvld (i_rvld),
    .i_n    (i_n[0+:31]),
    .i_a    (i_a[32+:64]),
    .o_z    (y[0+:64]),
    .o_dvld (vrl));



// ------------------------------------------------------------------------------
// Connect right leaf valid to right leaf output
// ------------------------------------------------------------------------------
assign vy = vrl;


// ------------------------------------------------------------------------------
// Connect right leaf data to Expand'input
// ------------------------------------------------------------------------------
assign yd[ 0+:64] = y[ 0+:64];


// ------------------------------------------------------------------------------
// Do a Expand(right leaf) instance
// ------------------------------------------------------------------------------
Expand2_n2o3k32
  u3_Expand2_n2o3k32
   (.i_x  (yd[0+:64]),
    .o_xp (yp[0+:96]));



// ------------------------------------------------------------------------------
// Do a RCA instance
// ------------------------------------------------------------------------------
SecRCA_n3k32_1
  u4_SecRCA_n3k32_1
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (vy),
    .i_rvld (i_rvld),
    .i_n    (i_n[31+:93]),
    .i_x    (xp[0+:96]),
    .i_y    (yp[0+:96]),
    .o_z    (o_z[0+:96]),
    .o_dvld (o_dvld));


endmodule