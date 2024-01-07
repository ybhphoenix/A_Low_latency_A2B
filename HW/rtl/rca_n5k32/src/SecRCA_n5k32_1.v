//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2023-10-08
// File Name     : SecRCA_n5k32_1.v
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
module SecRCA_n5k32_1(
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         i_dvld,
    input  wire         i_rvld,
    input  wire [309:0] i_n,
    input  wire [159:0] i_x,
    input  wire [159:0] i_y,
    output wire [159:0] o_z,
    output wire         o_dvld);

wire            dvld_0;
wire    [159:0] a_0;
wire    [159:0] x_0;
wire            c_0;
wire            dvld_1;
wire    [159:0] a_1;
wire    [154:0] x_1;
wire      [4:0] c_1;
wire            dvld_2;
wire    [159:0] a_2;
wire    [149:0] x_2;
wire      [9:0] c_2;
wire            dvld_3;
wire    [159:0] a_3;
wire    [144:0] x_3;
wire     [14:0] c_3;
wire            dvld_4;
wire    [159:0] a_4;
wire    [139:0] x_4;
wire     [19:0] c_4;
wire            dvld_5;
wire    [159:0] a_5;
wire    [134:0] x_5;
wire     [24:0] c_5;
wire            dvld_6;
wire    [159:0] a_6;
wire    [129:0] x_6;
wire     [29:0] c_6;
wire            dvld_7;
wire    [159:0] a_7;
wire    [124:0] x_7;
wire     [34:0] c_7;
wire            dvld_8;
wire    [159:0] a_8;
wire    [119:0] x_8;
wire     [39:0] c_8;
wire            dvld_9;
wire    [159:0] a_9;
wire    [114:0] x_9;
wire     [44:0] c_9;
wire            dvld_10;
wire    [159:0] a_10;
wire    [109:0] x_10;
wire     [49:0] c_10;
wire            dvld_11;
wire    [159:0] a_11;
wire    [104:0] x_11;
wire     [54:0] c_11;
wire            dvld_12;
wire    [159:0] a_12;
wire     [99:0] x_12;
wire     [59:0] c_12;
wire            dvld_13;
wire    [159:0] a_13;
wire     [94:0] x_13;
wire     [64:0] c_13;
wire            dvld_14;
wire    [159:0] a_14;
wire     [89:0] x_14;
wire     [69:0] c_14;
wire            dvld_15;
wire    [159:0] a_15;
wire     [84:0] x_15;
wire     [74:0] c_15;
wire            dvld_16;
wire    [159:0] a_16;
wire     [79:0] x_16;
wire     [79:0] c_16;
wire            dvld_17;
wire    [159:0] a_17;
wire     [74:0] x_17;
wire     [84:0] c_17;
wire            dvld_18;
wire    [159:0] a_18;
wire     [69:0] x_18;
wire     [89:0] c_18;
wire            dvld_19;
wire    [159:0] a_19;
wire     [64:0] x_19;
wire     [94:0] c_19;
wire            dvld_20;
wire    [159:0] a_20;
wire     [59:0] x_20;
wire     [99:0] c_20;
wire            dvld_21;
wire    [159:0] a_21;
wire     [54:0] x_21;
wire    [104:0] c_21;
wire            dvld_22;
wire    [159:0] a_22;
wire     [49:0] x_22;
wire    [109:0] c_22;
wire            dvld_23;
wire    [159:0] a_23;
wire     [44:0] x_23;
wire    [114:0] c_23;
wire            dvld_24;
wire    [159:0] a_24;
wire     [39:0] x_24;
wire    [119:0] c_24;
wire            dvld_25;
wire    [159:0] a_25;
wire     [34:0] x_25;
wire    [124:0] c_25;
wire            dvld_26;
wire    [159:0] a_26;
wire     [29:0] x_26;
wire    [129:0] c_26;
wire            dvld_27;
wire    [159:0] a_27;
wire     [24:0] x_27;
wire    [134:0] c_27;
wire            dvld_28;
wire    [159:0] a_28;
wire     [19:0] x_28;
wire    [139:0] c_28;
wire            dvld_29;
wire    [159:0] a_29;
wire     [14:0] x_29;
wire    [144:0] c_29;
wire            dvld_30;
wire    [159:0] a_30;
wire      [9:0] x_30;
wire    [149:0] c_30;
wire            dvld_31;
wire    [159:0] a_31;
wire      [4:0] x_31;
wire    [154:0] c_31;
wire    [159:0] c_e;


// ------------------------------------------------------------------------------
// c[i]=0;
// ------------------------------------------------------------------------------
assign c_0 = 1'd0;

// ------------------------------------------------------------------------------
// a[i]=x[i] ^ y[i];
// ------------------------------------------------------------------------------
lix_xor
  #(.W (160))
  u0_lix_xor
   (.i_x (i_x),
    .i_y (i_y),
    .o_z (a_0));



// ------------------------------------------------------------------------------
// connect x to SecRCA_1b inst0'x
// ------------------------------------------------------------------------------
assign x_0[  0+:160] = i_x[  0+:160];


// ------------------------------------------------------------------------------
// connect i_dvld to SecRCA_1b inst0'i_dvld
// ------------------------------------------------------------------------------
assign dvld_0 = i_dvld;


// ------------------------------------------------------------------------------
// Do SecRCA_1b 0 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_0
  u1_SecRCA_1b_n5k32_0
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_0),
    .i_rvld (i_rvld),
    .i_n    (i_n[0+:10]),
    .i_a    (a_0),
    .i_x    (x_0),
    .i_c    (c_0),
    .o_a    (a_1),
    .o_x    (x_1),
    .o_c    (c_1),
    .o_dvld (dvld_1));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 1 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_1
  u2_SecRCA_1b_n5k32_1
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_1),
    .i_rvld (i_rvld),
    .i_n    (i_n[10+:10]),
    .i_a    (a_1),
    .i_x    (x_1),
    .i_c    (c_1),
    .o_a    (a_2),
    .o_x    (x_2),
    .o_c    (c_2),
    .o_dvld (dvld_2));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 2 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_2
  u3_SecRCA_1b_n5k32_2
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_2),
    .i_rvld (i_rvld),
    .i_n    (i_n[20+:10]),
    .i_a    (a_2),
    .i_x    (x_2),
    .i_c    (c_2),
    .o_a    (a_3),
    .o_x    (x_3),
    .o_c    (c_3),
    .o_dvld (dvld_3));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 3 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_3
  u4_SecRCA_1b_n5k32_3
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_3),
    .i_rvld (i_rvld),
    .i_n    (i_n[30+:10]),
    .i_a    (a_3),
    .i_x    (x_3),
    .i_c    (c_3),
    .o_a    (a_4),
    .o_x    (x_4),
    .o_c    (c_4),
    .o_dvld (dvld_4));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 4 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_4
  u5_SecRCA_1b_n5k32_4
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_4),
    .i_rvld (i_rvld),
    .i_n    (i_n[40+:10]),
    .i_a    (a_4),
    .i_x    (x_4),
    .i_c    (c_4),
    .o_a    (a_5),
    .o_x    (x_5),
    .o_c    (c_5),
    .o_dvld (dvld_5));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 5 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_5
  u6_SecRCA_1b_n5k32_5
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_5),
    .i_rvld (i_rvld),
    .i_n    (i_n[50+:10]),
    .i_a    (a_5),
    .i_x    (x_5),
    .i_c    (c_5),
    .o_a    (a_6),
    .o_x    (x_6),
    .o_c    (c_6),
    .o_dvld (dvld_6));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 6 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_6
  u7_SecRCA_1b_n5k32_6
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_6),
    .i_rvld (i_rvld),
    .i_n    (i_n[60+:10]),
    .i_a    (a_6),
    .i_x    (x_6),
    .i_c    (c_6),
    .o_a    (a_7),
    .o_x    (x_7),
    .o_c    (c_7),
    .o_dvld (dvld_7));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 7 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_7
  u8_SecRCA_1b_n5k32_7
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_7),
    .i_rvld (i_rvld),
    .i_n    (i_n[70+:10]),
    .i_a    (a_7),
    .i_x    (x_7),
    .i_c    (c_7),
    .o_a    (a_8),
    .o_x    (x_8),
    .o_c    (c_8),
    .o_dvld (dvld_8));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 8 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_8
  u9_SecRCA_1b_n5k32_8
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_8),
    .i_rvld (i_rvld),
    .i_n    (i_n[80+:10]),
    .i_a    (a_8),
    .i_x    (x_8),
    .i_c    (c_8),
    .o_a    (a_9),
    .o_x    (x_9),
    .o_c    (c_9),
    .o_dvld (dvld_9));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 9 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_9
  u10_SecRCA_1b_n5k32_9
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_9),
    .i_rvld (i_rvld),
    .i_n    (i_n[90+:10]),
    .i_a    (a_9),
    .i_x    (x_9),
    .i_c    (c_9),
    .o_a    (a_10),
    .o_x    (x_10),
    .o_c    (c_10),
    .o_dvld (dvld_10));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 10 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_10
  u11_SecRCA_1b_n5k32_10
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_10),
    .i_rvld (i_rvld),
    .i_n    (i_n[100+:10]),
    .i_a    (a_10),
    .i_x    (x_10),
    .i_c    (c_10),
    .o_a    (a_11),
    .o_x    (x_11),
    .o_c    (c_11),
    .o_dvld (dvld_11));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 11 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_11
  u12_SecRCA_1b_n5k32_11
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_11),
    .i_rvld (i_rvld),
    .i_n    (i_n[110+:10]),
    .i_a    (a_11),
    .i_x    (x_11),
    .i_c    (c_11),
    .o_a    (a_12),
    .o_x    (x_12),
    .o_c    (c_12),
    .o_dvld (dvld_12));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 12 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_12
  u13_SecRCA_1b_n5k32_12
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_12),
    .i_rvld (i_rvld),
    .i_n    (i_n[120+:10]),
    .i_a    (a_12),
    .i_x    (x_12),
    .i_c    (c_12),
    .o_a    (a_13),
    .o_x    (x_13),
    .o_c    (c_13),
    .o_dvld (dvld_13));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 13 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_13
  u14_SecRCA_1b_n5k32_13
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_13),
    .i_rvld (i_rvld),
    .i_n    (i_n[130+:10]),
    .i_a    (a_13),
    .i_x    (x_13),
    .i_c    (c_13),
    .o_a    (a_14),
    .o_x    (x_14),
    .o_c    (c_14),
    .o_dvld (dvld_14));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 14 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_14
  u15_SecRCA_1b_n5k32_14
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_14),
    .i_rvld (i_rvld),
    .i_n    (i_n[140+:10]),
    .i_a    (a_14),
    .i_x    (x_14),
    .i_c    (c_14),
    .o_a    (a_15),
    .o_x    (x_15),
    .o_c    (c_15),
    .o_dvld (dvld_15));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 15 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_15
  u16_SecRCA_1b_n5k32_15
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_15),
    .i_rvld (i_rvld),
    .i_n    (i_n[150+:10]),
    .i_a    (a_15),
    .i_x    (x_15),
    .i_c    (c_15),
    .o_a    (a_16),
    .o_x    (x_16),
    .o_c    (c_16),
    .o_dvld (dvld_16));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 16 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_16
  u17_SecRCA_1b_n5k32_16
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_16),
    .i_rvld (i_rvld),
    .i_n    (i_n[160+:10]),
    .i_a    (a_16),
    .i_x    (x_16),
    .i_c    (c_16),
    .o_a    (a_17),
    .o_x    (x_17),
    .o_c    (c_17),
    .o_dvld (dvld_17));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 17 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_17
  u18_SecRCA_1b_n5k32_17
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_17),
    .i_rvld (i_rvld),
    .i_n    (i_n[170+:10]),
    .i_a    (a_17),
    .i_x    (x_17),
    .i_c    (c_17),
    .o_a    (a_18),
    .o_x    (x_18),
    .o_c    (c_18),
    .o_dvld (dvld_18));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 18 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_18
  u19_SecRCA_1b_n5k32_18
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_18),
    .i_rvld (i_rvld),
    .i_n    (i_n[180+:10]),
    .i_a    (a_18),
    .i_x    (x_18),
    .i_c    (c_18),
    .o_a    (a_19),
    .o_x    (x_19),
    .o_c    (c_19),
    .o_dvld (dvld_19));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 19 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_19
  u20_SecRCA_1b_n5k32_19
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_19),
    .i_rvld (i_rvld),
    .i_n    (i_n[190+:10]),
    .i_a    (a_19),
    .i_x    (x_19),
    .i_c    (c_19),
    .o_a    (a_20),
    .o_x    (x_20),
    .o_c    (c_20),
    .o_dvld (dvld_20));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 20 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_20
  u21_SecRCA_1b_n5k32_20
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_20),
    .i_rvld (i_rvld),
    .i_n    (i_n[200+:10]),
    .i_a    (a_20),
    .i_x    (x_20),
    .i_c    (c_20),
    .o_a    (a_21),
    .o_x    (x_21),
    .o_c    (c_21),
    .o_dvld (dvld_21));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 21 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_21
  u22_SecRCA_1b_n5k32_21
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_21),
    .i_rvld (i_rvld),
    .i_n    (i_n[210+:10]),
    .i_a    (a_21),
    .i_x    (x_21),
    .i_c    (c_21),
    .o_a    (a_22),
    .o_x    (x_22),
    .o_c    (c_22),
    .o_dvld (dvld_22));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 22 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_22
  u23_SecRCA_1b_n5k32_22
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_22),
    .i_rvld (i_rvld),
    .i_n    (i_n[220+:10]),
    .i_a    (a_22),
    .i_x    (x_22),
    .i_c    (c_22),
    .o_a    (a_23),
    .o_x    (x_23),
    .o_c    (c_23),
    .o_dvld (dvld_23));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 23 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_23
  u24_SecRCA_1b_n5k32_23
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_23),
    .i_rvld (i_rvld),
    .i_n    (i_n[230+:10]),
    .i_a    (a_23),
    .i_x    (x_23),
    .i_c    (c_23),
    .o_a    (a_24),
    .o_x    (x_24),
    .o_c    (c_24),
    .o_dvld (dvld_24));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 24 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_24
  u25_SecRCA_1b_n5k32_24
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_24),
    .i_rvld (i_rvld),
    .i_n    (i_n[240+:10]),
    .i_a    (a_24),
    .i_x    (x_24),
    .i_c    (c_24),
    .o_a    (a_25),
    .o_x    (x_25),
    .o_c    (c_25),
    .o_dvld (dvld_25));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 25 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_25
  u26_SecRCA_1b_n5k32_25
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_25),
    .i_rvld (i_rvld),
    .i_n    (i_n[250+:10]),
    .i_a    (a_25),
    .i_x    (x_25),
    .i_c    (c_25),
    .o_a    (a_26),
    .o_x    (x_26),
    .o_c    (c_26),
    .o_dvld (dvld_26));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 26 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_26
  u27_SecRCA_1b_n5k32_26
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_26),
    .i_rvld (i_rvld),
    .i_n    (i_n[260+:10]),
    .i_a    (a_26),
    .i_x    (x_26),
    .i_c    (c_26),
    .o_a    (a_27),
    .o_x    (x_27),
    .o_c    (c_27),
    .o_dvld (dvld_27));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 27 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_27
  u28_SecRCA_1b_n5k32_27
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_27),
    .i_rvld (i_rvld),
    .i_n    (i_n[270+:10]),
    .i_a    (a_27),
    .i_x    (x_27),
    .i_c    (c_27),
    .o_a    (a_28),
    .o_x    (x_28),
    .o_c    (c_28),
    .o_dvld (dvld_28));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 28 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_28
  u29_SecRCA_1b_n5k32_28
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_28),
    .i_rvld (i_rvld),
    .i_n    (i_n[280+:10]),
    .i_a    (a_28),
    .i_x    (x_28),
    .i_c    (c_28),
    .o_a    (a_29),
    .o_x    (x_29),
    .o_c    (c_29),
    .o_dvld (dvld_29));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 29 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_29
  u30_SecRCA_1b_n5k32_29
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_29),
    .i_rvld (i_rvld),
    .i_n    (i_n[290+:10]),
    .i_a    (a_29),
    .i_x    (x_29),
    .i_c    (c_29),
    .o_a    (a_30),
    .o_x    (x_30),
    .o_c    (c_30),
    .o_dvld (dvld_30));



// ------------------------------------------------------------------------------
// Do SecRCA_1b 30 instance
// ------------------------------------------------------------------------------
SecRCA_1b_n5k32_30
  u31_SecRCA_1b_n5k32_30
   (.clk_i  (clk_i),
    .rst_ni (rst_ni),
    .i_dvld (dvld_30),
    .i_rvld (i_rvld),
    .i_n    (i_n[300+:10]),
    .i_a    (a_30),
    .i_x    (x_30),
    .i_c    (c_30),
    .o_a    (a_31),
    .o_x    (x_31),
    .o_c    (c_31),
    .o_dvld (dvld_31));



// ------------------------------------------------------------------------------
// c[i] |= (tx[i] << (j+1))
// when j=0, bit0=0
// ------------------------------------------------------------------------------
assign c_e[  0+: 32] = {c_31[  0+: 31],1'd0};
assign c_e[ 32+: 32] = {c_31[ 31+: 31],1'd0};
assign c_e[ 64+: 32] = {c_31[ 62+: 31],1'd0};
assign c_e[ 96+: 32] = {c_31[ 93+: 31],1'd0};
assign c_e[128+: 32] = {c_31[124+: 31],1'd0};


// ------------------------------------------------------------------------------
// z[i]=a[i] ^ c[i]
// ------------------------------------------------------------------------------
lix_xor
  #(.W (160))
  u32_lix_xor
   (.i_x (a_31),
    .i_y (c_e),
    .o_z (o_z));



// ------------------------------------------------------------------------------
// connect last inst'o_dvld to port o_dvld
// ------------------------------------------------------------------------------
assign o_dvld = dvld_31;

endmodule
