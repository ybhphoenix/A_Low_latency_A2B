//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2023-09-01
// File Name     : lix_shr0.v
// Project Name  : 
// Design Name   : 
// Description   : 
//                 pipeline registers without output valid
// Dependencies  : 
// 
// Revision      : 
//                 - V1.0 File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////
// 


`default_nettype none
`timescale 1ns/1ps
module lix_shr0 #(
    parameter  W = 32   ,
    parameter  N = 2    
  )(
    input  wire          clk_i,
    input  wire          rst_ni,
    input  wire          i_vld,
    input  wire          i_en,
    input  wire  [W-1:0] i_x,
    output wire  [W-1:0] o_z);

  genvar i;

  wire [N-1:0] valid;
  wire [W-1:0] data [N:0];
  assign valid[0] = i_vld;
  generate
    for (i = 0 ; i < N -1; i = i +1)begin: GVLD
      lix_reg #(.W(1))
      u_reg_vld(
        .clk_i   (clk_i),
        .rst_ni  (rst_ni),
        .i_vld   (i_en),
        .i_en    (i_en),
        .i_x     (valid[i]),
        .o_z     (valid[i+1]));
    end
  endgenerate

  assign data[0] = i_x;
  generate
    for (i = 0 ; i < N ; i = i +1) begin: GDAT
      lix_reg #(.W(W))
      u_reg_dat(
        .clk_i   (clk_i),
        .rst_ni  (rst_ni),
        .i_vld   (valid[i]),
        .i_en    (i_en),
        .i_x     (data[i]),
        .o_z     (data[i+1]));
    end
  endgenerate
  assign o_z = data[N];


endmodule
