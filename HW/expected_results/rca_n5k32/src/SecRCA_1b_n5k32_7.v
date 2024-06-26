//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2024-04-26
// File Name     : SecRCA_1b_n5k32_7.v
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
module SecRCA_1b_n5k32_7(
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         i_dvld,
    input  wire         i_rvld,
    input  wire   [9:0] i_n,
    input  wire [159:0] i_a,
    input  wire [124:0] i_x,
    input  wire  [34:0] i_c,
    output wire [159:0] o_a,
    output wire [119:0] o_x,
    output wire  [39:0] o_c,
    output wire         o_dvld);

wire      [4:0] aj;
wire      [4:0] xj;
wire    [119:0] xrs;
wire      [4:0] b;
wire      [4:0] tmp;
wire      [4:0] cj;
wire      [4:0] tx;
wire    [159:0] ad;
wire    [119:0] xd;
wire     [34:0] cd;
wire      [4:0] xjd;

// ------------------------------------------------------------------------------
// Get the j=7 bit in per shares
// aj[i] = (a[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign aj[  0] = i_a[  7];
assign aj[  1] = i_a[ 39];
assign aj[  2] = i_a[ 71];
assign aj[  3] = i_a[103];
assign aj[  4] = i_a[135];


// ------------------------------------------------------------------------------
// Get the low bit in per shares
// x[i] & (uint32_t)1;
// ------------------------------------------------------------------------------
assign xj[  0] = i_x[  0];
assign xj[  1] = i_x[ 25];
assign xj[  2] = i_x[ 50];
assign xj[  3] = i_x[ 75];
assign xj[  4] = i_x[100];


// ------------------------------------------------------------------------------
// Remove the low bit in per shares
// x[i] = x[i] >> 1;
// ------------------------------------------------------------------------------
assign xrs[  0+: 24] = i_x[  1+: 24];
assign xrs[ 24+: 24] = i_x[ 26+: 24];
assign xrs[ 48+: 24] = i_x[ 51+: 24];
assign xrs[ 72+: 24] = i_x[ 76+: 24];
assign xrs[ 96+: 24] = i_x[101+: 24];


// ------------------------------------------------------------------------------
// Get the j=6 bit in per shares
// cj[i] = (c[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign cj[ 0] = i_c[ 6];
assign cj[ 1] = i_c[13];
assign cj[ 2] = i_c[20];
assign cj[ 3] = i_c[27];
assign cj[ 4] = i_c[34];


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
  #(.W (120),
    .N (2))
  u3_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (xrs[0+:120]),
    .o_z    (xd[0+:120]));



// ------------------------------------------------------------------------------
// Connect to the output
// ------------------------------------------------------------------------------
assign o_x[  0+:120] = xd[  0+:120];


// ------------------------------------------------------------------------------
// Delay i_c
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (35),
    .N (2))
  u4_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (i_c[0+:35]),
    .o_z    (cd[0+:35]));



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
assign o_c[ 0+: 8] = {tx[0],cd[ 0+: 7]};
assign o_c[ 8+: 8] = {tx[1],cd[ 7+: 7]};
assign o_c[16+: 8] = {tx[2],cd[14+: 7]};
assign o_c[24+: 8] = {tx[3],cd[21+: 7]};
assign o_c[32+: 8] = {tx[4],cd[28+: 7]};

endmodule
