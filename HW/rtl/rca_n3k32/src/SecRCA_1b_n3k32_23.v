//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2023-10-08
// File Name     : SecRCA_1b_n3k32_23.v
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
module SecRCA_1b_n3k32_23(
    input  wire        clk_i,
    input  wire        rst_ni,
    input  wire        i_dvld,
    input  wire        i_rvld,
    input  wire  [2:0] i_n,
    input  wire [95:0] i_a,
    input  wire [26:0] i_x,
    input  wire [68:0] i_c,
    output wire [95:0] o_a,
    output wire [23:0] o_x,
    output wire [71:0] o_c,
    output wire        o_dvld);

wire      [2:0] aj;
wire      [2:0] xj;
wire     [23:0] xrs;
wire      [2:0] b;
wire      [2:0] tmp;
wire      [2:0] cj;
wire      [2:0] tx;
wire     [95:0] ad;
wire     [23:0] xd;
wire     [68:0] cd;
wire      [2:0] xjd;

// ------------------------------------------------------------------------------
// Get the j=23 bit in per shares
// aj[i] = (a[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign aj[ 0] = i_a[23];
assign aj[ 1] = i_a[55];
assign aj[ 2] = i_a[87];


// ------------------------------------------------------------------------------
// Get the low bit in per shares
// x[i] & (uint32_t)1;
// ------------------------------------------------------------------------------
assign xj[ 0] = i_x[ 0];
assign xj[ 1] = i_x[ 9];
assign xj[ 2] = i_x[18];


// ------------------------------------------------------------------------------
// Remove the low bit in per shares
// x[i] = x[i] >> 1;
// ------------------------------------------------------------------------------
assign xrs[ 0+: 8] = i_x[ 1+: 8];
assign xrs[ 8+: 8] = i_x[10+: 8];
assign xrs[16+: 8] = i_x[19+: 8];


// ------------------------------------------------------------------------------
// Get the j=22 bit in per shares
// cj[i] = (c[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign cj[ 0] = i_c[22];
assign cj[ 1] = i_c[45];
assign cj[ 2] = i_c[68];


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
  #(.W (24),
    .N (2))
  u3_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (xrs[0+:24]),
    .o_z    (xd[0+:24]));



// ------------------------------------------------------------------------------
// Connect to the output
// ------------------------------------------------------------------------------
assign o_x[ 0+:24] = xd[ 0+:24];


// ------------------------------------------------------------------------------
// Delay i_c
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (69),
    .N (2))
  u4_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (i_c[0+:69]),
    .o_z    (cd[0+:69]));



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
assign o_c[ 0+:24] = {tx[0],cd[ 0+:23]};
assign o_c[24+:24] = {tx[1],cd[23+:23]};
assign o_c[48+:24] = {tx[2],cd[46+:23]};

endmodule
