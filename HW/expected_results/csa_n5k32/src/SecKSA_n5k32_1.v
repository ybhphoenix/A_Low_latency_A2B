//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2024-04-26
// File Name     : SecKSA_n5k32_1.v
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
module SecKSA_n5k32_1(
    input  wire          clk_i,
    input  wire          rst_ni,
    input  wire          i_dvld,
    input  wire          i_rvld,
    input  wire [3199:0] i_n,
    input  wire  [159:0] i_x,
    input  wire  [159:0] i_y,
    output wire  [159:0] o_z,
    output wire          o_dvld);

wire    [159:0] p;
wire    [159:0] g;
wire    [159:0] tmp;
wire    [159:0] a;
wire            vld0;
wire      [4:0] vld;
wire    [799:0] pl;
wire    [799:0] gl;
wire    [159:0] ga;
wire    [159:0] xd;
wire    [159:0] yd;
wire    [159:0] gd;
wire    [159:0] glw;
wire    [159:0] glh;
wire    [159:0] gals;
wire    [159:0] pd;
wire    [159:0] plh;
wire            vld5;
wire    [159:0] xxy;

// ------------------------------------------------------------------------------
// p[i]=x[i]^y[i];
// ------------------------------------------------------------------------------
lix_xor
  #(.W (160))
  u0_lix_xor
   (.i_x (i_x),
    .i_y (i_y),
    .o_z (p));



// ------------------------------------------------------------------------------
// Delay p
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (160),
    .N (2))
  u1_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (p),
    .o_z    (pd));



// ------------------------------------------------------------------------------
// Do a SecAnd instance
// ------------------------------------------------------------------------------
SecAnd_PINI1_n5k32_1
  u2_SecAnd_PINI1_n5k32_1
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (i_dvld),
    .i_rvld (i_rvld),
    .i_n    (i_n[0+:320]),
    .i_x    (i_x),
    .i_y    (i_y),
    .o_c    (g),
    .o_dvld (vld0));



// ------------------------------------------------------------------------------
// Connect SecAnd'output to KSA_w1l'input
// ------------------------------------------------------------------------------
assign vld[0] = vld0;


// ------------------------------------------------------------------------------
// Connect delayed p to KSA_w1l'input
// ------------------------------------------------------------------------------
assign pl[  0+:160] = pd[  0+:160];


// ------------------------------------------------------------------------------
// Connect SecAnd'output to KSA_w1l'input
// ------------------------------------------------------------------------------
assign gl[  0+:160] = g[  0+:160];


// ------------------------------------------------------------------------------
// Do a SecKSA_1l instance with SHIFT=0
// ------------------------------------------------------------------------------
SecKSA_1l_n5k32
  #(.SHIFT (0))
  u3_SecKSA_1l_n5k32
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (vld[0]),
    .i_rvld (i_rvld),
    .i_n    (i_n[320+:640]),
    .i_p    (pl[0+:160]),
    .i_g    (gl[0+:160]),
    .o_p    (pl[160+:160]),
    .o_g    (gl[160+:160]),
    .o_dvld (vld[1]));



// ------------------------------------------------------------------------------
// Do a SecKSA_1l instance with SHIFT=1
// ------------------------------------------------------------------------------
SecKSA_1l_n5k32
  #(.SHIFT (1))
  u4_SecKSA_1l_n5k32
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (vld[1]),
    .i_rvld (i_rvld),
    .i_n    (i_n[960+:640]),
    .i_p    (pl[160+:160]),
    .i_g    (gl[160+:160]),
    .o_p    (pl[320+:160]),
    .o_g    (gl[320+:160]),
    .o_dvld (vld[2]));



// ------------------------------------------------------------------------------
// Do a SecKSA_1l instance with SHIFT=2
// ------------------------------------------------------------------------------
SecKSA_1l_n5k32
  #(.SHIFT (2))
  u5_SecKSA_1l_n5k32
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (vld[2]),
    .i_rvld (i_rvld),
    .i_n    (i_n[1600+:640]),
    .i_p    (pl[320+:160]),
    .i_g    (gl[320+:160]),
    .o_p    (pl[480+:160]),
    .o_g    (gl[480+:160]),
    .o_dvld (vld[3]));



// ------------------------------------------------------------------------------
// Do a SecKSA_1l instance with SHIFT=3
// ------------------------------------------------------------------------------
SecKSA_1l_n5k32
  #(.SHIFT (3))
  u6_SecKSA_1l_n5k32
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (vld[3]),
    .i_rvld (i_rvld),
    .i_n    (i_n[2240+:640]),
    .i_p    (pl[480+:160]),
    .i_g    (gl[480+:160]),
    .o_p    (pl[640+:160]),
    .o_g    (gl[640+:160]),
    .o_dvld (vld[4]));



// ------------------------------------------------------------------------------
// Connect SecKSA_1l to delay module
// ------------------------------------------------------------------------------
assign glh[  0+:160] = gl[640+:160];


// ------------------------------------------------------------------------------
// Connect SecKSA_1l to SecAnd
// ------------------------------------------------------------------------------
assign plh[  0+:160] = pl[640+:160];


// ------------------------------------------------------------------------------
// Connect SecKSA_1l to delay module
// ------------------------------------------------------------------------------
assign vld5 = vld[4];


// ------------------------------------------------------------------------------
// Connect SecKSA_1l to SecAnd with left shift
// tmp[i]=(g[i]<<(1<<W))&MASK;
// ------------------------------------------------------------------------------
assign tmp[  0+: 32] = glh[  0+: 32]  <<  16;
assign tmp[ 32+: 32] = glh[ 32+: 32]  <<  16;
assign tmp[ 64+: 32] = glh[ 64+: 32]  <<  16;
assign tmp[ 96+: 32] = glh[ 96+: 32]  <<  16;
assign tmp[128+: 32] = glh[128+: 32]  <<  16;


// ------------------------------------------------------------------------------
// Delay SecKSA_1l'output
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (160),
    .N (2))
  u7_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (vld5),
    .i_en   (i_rvld),
    .i_x    (glh),
    .o_z    (gd));



// ------------------------------------------------------------------------------
// Do a SecAnd instance
// ------------------------------------------------------------------------------
SecAnd_PINI1_n5k32_1
  u8_SecAnd_PINI1_n5k32_1
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (vld[4]),
    .i_rvld (i_rvld),
    .i_n    (i_n[2880+:320]),
    .i_x    (plh[0+:160]),
    .i_y    (tmp[0+:160]),
    .o_c    (a[0+:160]),
    .o_dvld (o_dvld));



// ------------------------------------------------------------------------------
// g[i]=g[i]^a[i];
// ------------------------------------------------------------------------------
lix_xor
  #(.W (160))
  u9_lix_xor
   (.i_x (gd),
    .i_y (a),
    .o_z (ga));



// ------------------------------------------------------------------------------
// Delay i_x;
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (160),
    .N (12))
  u10_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (i_x),
    .o_z    (xd));



// ------------------------------------------------------------------------------
// Delay i_y;
// ------------------------------------------------------------------------------
lix_shr0
  #(.W (160),
    .N (12))
  u11_lix_shr0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_vld  (i_dvld),
    .i_en   (i_rvld),
    .i_x    (i_y),
    .o_z    (yd));



// ------------------------------------------------------------------------------
// (g[i]<<1))
// ------------------------------------------------------------------------------
assign gals[  0+: 32] = ga[  0+: 32]  <<  1;
assign gals[ 32+: 32] = ga[ 32+: 32]  <<  1;
assign gals[ 64+: 32] = ga[ 64+: 32]  <<  1;
assign gals[ 96+: 32] = ga[ 96+: 32]  <<  1;
assign gals[128+: 32] = ga[128+: 32]  <<  1;


// ------------------------------------------------------------------------------
// x[i]^y[i]
// ------------------------------------------------------------------------------
lix_xor
  #(.W (160))
  u12_lix_xor
   (.i_x (xd),
    .i_y (yd),
    .o_z (xxy));



// ------------------------------------------------------------------------------
// z[i]=(x[i]^y[i]^(g[i]<<1))&MASK;
// ------------------------------------------------------------------------------
lix_xor
  #(.W (160))
  u13_lix_xor
   (.i_x (gals),
    .i_y (xxy),
    .o_z (o_z));


endmodule
