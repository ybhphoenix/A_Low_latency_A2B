//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2023-10-08
// File Name     : SecRCA_1b_n3k32_26.v
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
module SecRCA_1b_n3k32_26(
    input  wire        clk_i,
    input  wire        rst_ni,
    input  wire        i_dvld,
    input  wire        i_rvld,
    input  wire  [2:0] i_n,
    input  wire [95:0] i_a,
    input  wire [17:0] i_x,
    input  wire [77:0] i_c,
    output wire [95:0] o_a,
    output wire [14:0] o_x,
    output wire [80:0] o_c,
    output wire        o_dvld);

wire      [2:0] aj;
wire      [2:0] xj;
wire     [14:0] xrs;
wire      [2:0] b;
wire      [2:0] tmp;
wire      [2:0] cj;
wire      [2:0] tx;
wire     [95:0] ad;
wire     [14:0] xd;
wire     [77:0] cd;
wire      [2:0] xjd;

// ------------------------------------------------------------------------------
// Get the j=26 bit in per shares
// aj[i] = (a[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign aj[ 0] = i_a[26];
assign aj[ 1] = i_a[58];
assign aj[ 2] = i_a[90];


// ------------------------------------------------------------------------------
// Get the low bit in per shares
// x[i] & (uint32_t)1;
// ------------------------------------------------------------------------------
assign xj[ 0] = i_x[ 0];
assign xj[ 1] = i_x[ 6];
assign xj[ 2] = i_x[12];


// ------------------------------------------------------------------------------
// Remove the low bit in per shares
// x[i] = x[i] >> 1;
// ------------------------------------------------------------------------------
assign xrs[ 0+: 5] = i_x[ 1+: 5];
assign xrs[ 5+: 5] = i_x[ 7+: 5];
assign xrs[10+: 5] = i_x[13+: 5];


// ------------------------------------------------------------------------------
// Get the j=25 bit in per shares
// cj[i] = (c[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign cj[ 0] = i_c[25];
assign cj[ 1] = i_c[51];
assign cj[ 2] = i_c[77];


// ------------------------------------------------------------------------------
// b[i] = xj[i] ^ cj[i];
// ------------------------------------------------------------------------------
lix_xor
  #(.W (3))
  u0_lix_xor
   (.i_x (xj),
    .i_y (cj),
    .o_z (b));



// ------------------------------------------------------------------------------
// Do a SecAnd instance
// ------------------------------------------------------------------------------
SecAnd_PINI1_n3k1_1
  u1_SecAnd_PINI1_n3k1_1
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
  #(.W (96),
    .N (2))
  u2_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (i_a[0+:96]),
    .o_z    (ad[0+:96]));



// ------------------------------------------------------------------------------
// Connect to the output
// ------------------------------------------------------------------------------
assign o_a[ 0+:96] = ad[ 0+:96];


// ------------------------------------------------------------------------------
// Delay xrs
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (15),
    .N (2))
  u3_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (xrs[0+:15]),
    .o_z    (xd[0+:15]));



// ------------------------------------------------------------------------------
// Connect to the output
// ------------------------------------------------------------------------------
assign o_x[ 0+:15] = xd[ 0+:15];


// ------------------------------------------------------------------------------
// Delay i_c
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (78),
    .N (2))
  u4_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (i_c[0+:78]),
    .o_z    (cd[0+:78]));



// ------------------------------------------------------------------------------
// Delay xj
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (3),
    .N (2))
  u5_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (xj[0+:3]),
    .o_z    (xjd[0+:3]));



// ------------------------------------------------------------------------------
// tx[i] = tmp[i] ^ xj[i];
// ------------------------------------------------------------------------------
lix_xor
  #(.W (3))
  u6_lix_xor
   (.i_x (tmp),
    .i_y (xjd),
    .o_z (tx));



// ------------------------------------------------------------------------------
// c[i] |= (tx[i] << (j+1));
// ------------------------------------------------------------------------------
assign o_c[ 0+:27] = {tx[0],cd[ 0+:26]};
assign o_c[27+:27] = {tx[1],cd[26+:26]};
assign o_c[54+:27] = {tx[2],cd[52+:26]};

endmodule
