//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2023-10-08
// File Name     : SecRCA_1b_n5k32_11.v
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
module SecRCA_1b_n5k32_11(
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         i_dvld,
    input  wire         i_rvld,
    input  wire   [9:0] i_n,
    input  wire [159:0] i_a,
    input  wire [104:0] i_x,
    input  wire  [54:0] i_c,
    output wire [159:0] o_a,
    output wire  [99:0] o_x,
    output wire  [59:0] o_c,
    output wire         o_dvld);

wire      [4:0] aj;
wire      [4:0] xj;
wire     [99:0] xrs;
wire      [4:0] b;
wire      [4:0] tmp;
wire      [4:0] cj;
wire      [4:0] tx;
wire    [159:0] ad;
wire     [99:0] xd;
wire     [54:0] cd;
wire      [4:0] xjd;

// ------------------------------------------------------------------------------
// Get the j=11 bit in per shares
// aj[i] = (a[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign aj[  0] = i_a[ 11];
assign aj[  1] = i_a[ 43];
assign aj[  2] = i_a[ 75];
assign aj[  3] = i_a[107];
assign aj[  4] = i_a[139];


// ------------------------------------------------------------------------------
// Get the low bit in per shares
// x[i] & (uint32_t)1;
// ------------------------------------------------------------------------------
assign xj[  0] = i_x[  0];
assign xj[  1] = i_x[ 21];
assign xj[  2] = i_x[ 42];
assign xj[  3] = i_x[ 63];
assign xj[  4] = i_x[ 84];


// ------------------------------------------------------------------------------
// Remove the low bit in per shares
// x[i] = x[i] >> 1;
// ------------------------------------------------------------------------------
assign xrs[  0+: 20] = i_x[  1+: 20];
assign xrs[ 20+: 20] = i_x[ 22+: 20];
assign xrs[ 40+: 20] = i_x[ 43+: 20];
assign xrs[ 60+: 20] = i_x[ 64+: 20];
assign xrs[ 80+: 20] = i_x[ 85+: 20];


// ------------------------------------------------------------------------------
// Get the j=10 bit in per shares
// cj[i] = (c[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign cj[ 0] = i_c[10];
assign cj[ 1] = i_c[21];
assign cj[ 2] = i_c[32];
assign cj[ 3] = i_c[43];
assign cj[ 4] = i_c[54];


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
  #(.W (100),
    .N (2))
  u3_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (xrs[0+:100]),
    .o_z    (xd[0+:100]));



// ------------------------------------------------------------------------------
// Connect to the output
// ------------------------------------------------------------------------------
assign o_x[ 0+:100] = xd[ 0+:100];


// ------------------------------------------------------------------------------
// Delay i_c
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (55),
    .N (2))
  u4_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (i_c[0+:55]),
    .o_z    (cd[0+:55]));



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
assign o_c[ 0+:12] = {tx[0],cd[ 0+:11]};
assign o_c[12+:12] = {tx[1],cd[11+:11]};
assign o_c[24+:12] = {tx[2],cd[22+:11]};
assign o_c[36+:12] = {tx[3],cd[33+:11]};
assign o_c[48+:12] = {tx[4],cd[44+:11]};

endmodule
