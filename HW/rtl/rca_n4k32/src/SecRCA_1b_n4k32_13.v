//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2023-10-08
// File Name     : SecRCA_1b_n4k32_13.v
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
module SecRCA_1b_n4k32_13(
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         i_dvld,
    input  wire         i_rvld,
    input  wire   [5:0] i_n,
    input  wire [127:0] i_a,
    input  wire  [75:0] i_x,
    input  wire  [51:0] i_c,
    output wire [127:0] o_a,
    output wire  [71:0] o_x,
    output wire  [55:0] o_c,
    output wire         o_dvld);

wire      [3:0] aj;
wire      [3:0] xj;
wire     [71:0] xrs;
wire      [3:0] b;
wire      [3:0] tmp;
wire      [3:0] cj;
wire      [3:0] tx;
wire    [127:0] ad;
wire     [71:0] xd;
wire     [51:0] cd;
wire      [3:0] xjd;

// ------------------------------------------------------------------------------
// Get the j=13 bit in per shares
// aj[i] = (a[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign aj[  0] = i_a[ 13];
assign aj[  1] = i_a[ 45];
assign aj[  2] = i_a[ 77];
assign aj[  3] = i_a[109];


// ------------------------------------------------------------------------------
// Get the low bit in per shares
// x[i] & (uint32_t)1;
// ------------------------------------------------------------------------------
assign xj[ 0] = i_x[ 0];
assign xj[ 1] = i_x[19];
assign xj[ 2] = i_x[38];
assign xj[ 3] = i_x[57];


// ------------------------------------------------------------------------------
// Remove the low bit in per shares
// x[i] = x[i] >> 1;
// ------------------------------------------------------------------------------
assign xrs[ 0+:18] = i_x[ 1+:18];
assign xrs[18+:18] = i_x[20+:18];
assign xrs[36+:18] = i_x[39+:18];
assign xrs[54+:18] = i_x[58+:18];


// ------------------------------------------------------------------------------
// Get the j=12 bit in per shares
// cj[i] = (c[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign cj[ 0] = i_c[12];
assign cj[ 1] = i_c[25];
assign cj[ 2] = i_c[38];
assign cj[ 3] = i_c[51];


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
  #(.W (72),
    .N (2))
  u3_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (xrs[0+:72]),
    .o_z    (xd[0+:72]));



// ------------------------------------------------------------------------------
// Connect to the output
// ------------------------------------------------------------------------------
assign o_x[ 0+:72] = xd[ 0+:72];


// ------------------------------------------------------------------------------
// Delay i_c
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (52),
    .N (2))
  u4_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (i_c[0+:52]),
    .o_z    (cd[0+:52]));



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
assign o_c[ 0+:14] = {tx[0],cd[ 0+:13]};
assign o_c[14+:14] = {tx[1],cd[13+:13]};
assign o_c[28+:14] = {tx[2],cd[26+:13]};
assign o_c[42+:14] = {tx[3],cd[39+:13]};

endmodule
