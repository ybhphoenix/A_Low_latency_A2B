//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2023-10-08
// File Name     : SecRCA_1b_n5k32_17.v
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
module SecRCA_1b_n5k32_17(
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         i_dvld,
    input  wire         i_rvld,
    input  wire   [9:0] i_n,
    input  wire [159:0] i_a,
    input  wire  [74:0] i_x,
    input  wire  [84:0] i_c,
    output wire [159:0] o_a,
    output wire  [69:0] o_x,
    output wire  [89:0] o_c,
    output wire         o_dvld);

wire      [4:0] aj;
wire      [4:0] xj;
wire     [69:0] xrs;
wire      [4:0] b;
wire      [4:0] tmp;
wire      [4:0] cj;
wire      [4:0] tx;
wire    [159:0] ad;
wire     [69:0] xd;
wire     [84:0] cd;
wire      [4:0] xjd;

// ------------------------------------------------------------------------------
// Get the j=17 bit in per shares
// aj[i] = (a[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign aj[  0] = i_a[ 17];
assign aj[  1] = i_a[ 49];
assign aj[  2] = i_a[ 81];
assign aj[  3] = i_a[113];
assign aj[  4] = i_a[145];


// ------------------------------------------------------------------------------
// Get the low bit in per shares
// x[i] & (uint32_t)1;
// ------------------------------------------------------------------------------
assign xj[ 0] = i_x[ 0];
assign xj[ 1] = i_x[15];
assign xj[ 2] = i_x[30];
assign xj[ 3] = i_x[45];
assign xj[ 4] = i_x[60];


// ------------------------------------------------------------------------------
// Remove the low bit in per shares
// x[i] = x[i] >> 1;
// ------------------------------------------------------------------------------
assign xrs[ 0+:14] = i_x[ 1+:14];
assign xrs[14+:14] = i_x[16+:14];
assign xrs[28+:14] = i_x[31+:14];
assign xrs[42+:14] = i_x[46+:14];
assign xrs[56+:14] = i_x[61+:14];


// ------------------------------------------------------------------------------
// Get the j=16 bit in per shares
// cj[i] = (c[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign cj[ 0] = i_c[16];
assign cj[ 1] = i_c[33];
assign cj[ 2] = i_c[50];
assign cj[ 3] = i_c[67];
assign cj[ 4] = i_c[84];


// ------------------------------------------------------------------------------
// b[i] = xj[i] ^ cj[i];
// ------------------------------------------------------------------------------
lix_xor
  #(.W (5))
  u0_lix_xor
   (.i_x (xj),
    .i_y (cj),
    .o_z (b));



// ------------------------------------------------------------------------------
// Do a SecAnd instance
// ------------------------------------------------------------------------------
SecAnd_PINI1_n5k1_1
  u1_SecAnd_PINI1_n5k1_1
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (i_dvld),
    .i_rvld (i_rvld),
    .i_n    (i_n),
    .i_x    (b),
    .i_y    (aj),
    .o_c    (tmp),
    .o_dvld (o_dvld));



// ------------------------------------------------------------------------------
// Delay i_a
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (160),
    .N (2))
  u2_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (i_a[0+:160]),
    .o_z    (ad[0+:160]));



// ------------------------------------------------------------------------------
// Connect to the output
// ------------------------------------------------------------------------------
assign o_a[  0+:160] = ad[  0+:160];


// ------------------------------------------------------------------------------
// Delay xrs
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (70),
    .N (2))
  u3_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (xrs[0+:70]),
    .o_z    (xd[0+:70]));



// ------------------------------------------------------------------------------
// Connect to the output
// ------------------------------------------------------------------------------
assign o_x[ 0+:70] = xd[ 0+:70];


// ------------------------------------------------------------------------------
// Delay i_c
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (85),
    .N (2))
  u4_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (i_c[0+:85]),
    .o_z    (cd[0+:85]));



// ------------------------------------------------------------------------------
// Delay xj
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (5),
    .N (2))
  u5_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (xj[0+:5]),
    .o_z    (xjd[0+:5]));



// ------------------------------------------------------------------------------
// tx[i] = tmp[i] ^ xj[i];
// ------------------------------------------------------------------------------
lix_xor
  #(.W (5))
  u6_lix_xor
   (.i_x (tmp),
    .i_y (xjd),
    .o_z (tx));



// ------------------------------------------------------------------------------
// c[i] |= (tx[i] << (j+1));
// ------------------------------------------------------------------------------
assign o_c[ 0+:18] = {tx[0],cd[ 0+:17]};
assign o_c[18+:18] = {tx[1],cd[17+:17]};
assign o_c[36+:18] = {tx[2],cd[34+:17]};
assign o_c[54+:18] = {tx[3],cd[51+:17]};
assign o_c[72+:18] = {tx[4],cd[68+:17]};

endmodule
