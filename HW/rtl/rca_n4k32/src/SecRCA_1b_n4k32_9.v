//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2023-10-08
// File Name     : SecRCA_1b_n4k32_9.v
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
module SecRCA_1b_n4k32_9(
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         i_dvld,
    input  wire         i_rvld,
    input  wire   [5:0] i_n,
    input  wire [127:0] i_a,
    input  wire  [91:0] i_x,
    input  wire  [35:0] i_c,
    output wire [127:0] o_a,
    output wire  [87:0] o_x,
    output wire  [39:0] o_c,
    output wire         o_dvld);

wire      [3:0] aj;
wire      [3:0] xj;
wire     [87:0] xrs;
wire      [3:0] b;
wire      [3:0] tmp;
wire      [3:0] cj;
wire      [3:0] tx;
wire    [127:0] ad;
wire     [87:0] xd;
wire     [35:0] cd;
wire      [3:0] xjd;

// ------------------------------------------------------------------------------
// Get the j=9 bit in per shares
// aj[i] = (a[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign aj[  0] = i_a[  9];
assign aj[  1] = i_a[ 41];
assign aj[  2] = i_a[ 73];
assign aj[  3] = i_a[105];


// ------------------------------------------------------------------------------
// Get the low bit in per shares
// x[i] & (uint32_t)1;
// ------------------------------------------------------------------------------
assign xj[ 0] = i_x[ 0];
assign xj[ 1] = i_x[23];
assign xj[ 2] = i_x[46];
assign xj[ 3] = i_x[69];


// ------------------------------------------------------------------------------
// Remove the low bit in per shares
// x[i] = x[i] >> 1;
// ------------------------------------------------------------------------------
assign xrs[ 0+:22] = i_x[ 1+:22];
assign xrs[22+:22] = i_x[24+:22];
assign xrs[44+:22] = i_x[47+:22];
assign xrs[66+:22] = i_x[70+:22];


// ------------------------------------------------------------------------------
// Get the j=8 bit in per shares
// cj[i] = (c[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign cj[ 0] = i_c[ 8];
assign cj[ 1] = i_c[17];
assign cj[ 2] = i_c[26];
assign cj[ 3] = i_c[35];


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
  #(.W (88),
    .N (2))
  u3_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (xrs[0+:88]),
    .o_z    (xd[0+:88]));



// ------------------------------------------------------------------------------
// Connect to the output
// ------------------------------------------------------------------------------
assign o_x[ 0+:88] = xd[ 0+:88];


// ------------------------------------------------------------------------------
// Delay i_c
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (36),
    .N (2))
  u4_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (i_c[0+:36]),
    .o_z    (cd[0+:36]));



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
assign o_c[ 0+:10] = {tx[0],cd[ 0+: 9]};
assign o_c[10+:10] = {tx[1],cd[ 9+: 9]};
assign o_c[20+:10] = {tx[2],cd[18+: 9]};
assign o_c[30+:10] = {tx[3],cd[27+: 9]};

endmodule
