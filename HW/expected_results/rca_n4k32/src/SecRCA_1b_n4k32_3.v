//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2024-04-26
// File Name     : SecRCA_1b_n4k32_3.v
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
module SecRCA_1b_n4k32_3(
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         i_dvld,
    input  wire         i_rvld,
    input  wire   [5:0] i_n,
    input  wire [127:0] i_a,
    input  wire [115:0] i_x,
    input  wire  [11:0] i_c,
    output wire [127:0] o_a,
    output wire [111:0] o_x,
    output wire  [15:0] o_c,
    output wire         o_dvld);

wire      [3:0] aj;
wire      [3:0] xj;
wire    [111:0] xrs;
wire      [3:0] b;
wire      [3:0] tmp;
wire      [3:0] cj;
wire      [3:0] tx;
wire    [127:0] ad;
wire    [111:0] xd;
wire     [11:0] cd;
wire      [3:0] xjd;

// ------------------------------------------------------------------------------
// Get the j=3 bit in per shares
// aj[i] = (a[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign aj[  0] = i_a[  3];
assign aj[  1] = i_a[ 35];
assign aj[  2] = i_a[ 67];
assign aj[  3] = i_a[ 99];


// ------------------------------------------------------------------------------
// Get the low bit in per shares
// x[i] & (uint32_t)1;
// ------------------------------------------------------------------------------
assign xj[  0] = i_x[  0];
assign xj[  1] = i_x[ 29];
assign xj[  2] = i_x[ 58];
assign xj[  3] = i_x[ 87];


// ------------------------------------------------------------------------------
// Remove the low bit in per shares
// x[i] = x[i] >> 1;
// ------------------------------------------------------------------------------
assign xrs[  0+: 28] = i_x[  1+: 28];
assign xrs[ 28+: 28] = i_x[ 30+: 28];
assign xrs[ 56+: 28] = i_x[ 59+: 28];
assign xrs[ 84+: 28] = i_x[ 88+: 28];


// ------------------------------------------------------------------------------
// Get the j=2 bit in per shares
// cj[i] = (c[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign cj[ 0] = i_c[ 2];
assign cj[ 1] = i_c[ 5];
assign cj[ 2] = i_c[ 8];
assign cj[ 3] = i_c[11];


// ------------------------------------------------------------------------------
// b[i] = xj[i] ^ cj[i];
// ------------------------------------------------------------------------------
lix_xor
  #(.W (4))
  u0_lix_xor
   (.i_x (xj),
    .i_y (cj),
    .o_z (b));



// ------------------------------------------------------------------------------
// Do a SecAnd instance
// ------------------------------------------------------------------------------
SecAnd_PINI1_n4k1_1
  u1_SecAnd_PINI1_n4k1_1
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
  #(.W (128),
    .N (2))
  u2_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (i_a[0+:128]),
    .o_z    (ad[0+:128]));



// ------------------------------------------------------------------------------
// Connect to the output
// ------------------------------------------------------------------------------
assign o_a[  0+:128] = ad[  0+:128];


// ------------------------------------------------------------------------------
// Delay xrs
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (112),
    .N (2))
  u3_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (xrs[0+:112]),
    .o_z    (xd[0+:112]));



// ------------------------------------------------------------------------------
// Connect to the output
// ------------------------------------------------------------------------------
assign o_x[  0+:112] = xd[  0+:112];


// ------------------------------------------------------------------------------
// Delay i_c
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (12),
    .N (2))
  u4_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (i_c[0+:12]),
    .o_z    (cd[0+:12]));



// ------------------------------------------------------------------------------
// Delay xj
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (4),
    .N (2))
  u5_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (xj[0+:4]),
    .o_z    (xjd[0+:4]));



// ------------------------------------------------------------------------------
// tx[i] = tmp[i] ^ xj[i];
// ------------------------------------------------------------------------------
lix_xor
  #(.W (4))
  u6_lix_xor
   (.i_x (tmp),
    .i_y (xjd),
    .o_z (tx));



// ------------------------------------------------------------------------------
// c[i] |= (tx[i] << (j+1));
// ------------------------------------------------------------------------------
assign o_c[ 0+: 4] = {tx[0],cd[ 0+: 3]};
assign o_c[ 4+: 4] = {tx[1],cd[ 3+: 3]};
assign o_c[ 8+: 4] = {tx[2],cd[ 6+: 3]};
assign o_c[12+: 4] = {tx[3],cd[ 9+: 3]};

endmodule
