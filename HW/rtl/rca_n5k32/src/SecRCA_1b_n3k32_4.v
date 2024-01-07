//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2023-10-08
// File Name     : SecRCA_1b_n3k32_4.v
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
module SecRCA_1b_n3k32_4(
    input  wire        clk_i,
    input  wire        rst_ni,
    input  wire        i_dvld,
    input  wire        i_rvld,
    input  wire  [2:0] i_n,
    input  wire [95:0] i_a,
    input  wire [83:0] i_x,
    input  wire [11:0] i_c,
    output wire [95:0] o_a,
    output wire [80:0] o_x,
    output wire [14:0] o_c,
    output wire        o_dvld);

wire      [2:0] aj;
wire      [2:0] xj;
wire     [80:0] xrs;
wire      [2:0] b;
wire      [2:0] tmp;
wire      [2:0] cj;
wire      [2:0] tx;
wire     [95:0] ad;
wire     [80:0] xd;
wire     [11:0] cd;
wire      [2:0] xjd;

// ------------------------------------------------------------------------------
// Get the j=4 bit in per shares
// aj[i] = (a[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign aj[ 0] = i_a[ 4];
assign aj[ 1] = i_a[36];
assign aj[ 2] = i_a[68];


// ------------------------------------------------------------------------------
// Get the low bit in per shares
// x[i] & (uint32_t)1;
// ------------------------------------------------------------------------------
assign xj[ 0] = i_x[ 0];
assign xj[ 1] = i_x[28];
assign xj[ 2] = i_x[56];


// ------------------------------------------------------------------------------
// Remove the low bit in per shares
// x[i] = x[i] >> 1;
// ------------------------------------------------------------------------------
assign xrs[ 0+:27] = i_x[ 1+:27];
assign xrs[27+:27] = i_x[29+:27];
assign xrs[54+:27] = i_x[57+:27];


// ------------------------------------------------------------------------------
// Get the j=3 bit in per shares
// cj[i] = (c[i]>>j) & (uint32_t)1;
// ------------------------------------------------------------------------------
assign cj[ 0] = i_c[ 3];
assign cj[ 1] = i_c[ 7];
assign cj[ 2] = i_c[11];


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
  #(.W (81),
    .N (2))
  u3_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (xrs[0+:81]),
    .o_z    (xd[0+:81]));



// ------------------------------------------------------------------------------
// Connect to the output
// ------------------------------------------------------------------------------
assign o_x[ 0+:81] = xd[ 0+:81];


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
assign o_c[ 0+: 5] = {tx[0],cd[ 0+: 4]};
assign o_c[ 5+: 5] = {tx[1],cd[ 4+: 4]};
assign o_c[10+: 5] = {tx[2],cd[ 8+: 4]};

endmodule
