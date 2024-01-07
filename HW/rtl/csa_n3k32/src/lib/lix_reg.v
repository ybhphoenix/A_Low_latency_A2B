//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2023-09-01
// File Name     : lix_reg.v
// Project Name  : 
// Design Name   : 
// Description   : 
// 
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
module lix_reg #(
    parameter  W = 32
  )(
    input  wire          clk_i,
    input  wire          rst_ni,
    input  wire          i_vld,
    input  wire          i_en,
    input  wire  [W-1:0] i_x,
    output wire  [W-1:0] o_z);

`ifdef SIM

  reg [W-1:0] data;
  genvar i;
  generate
  for (i = 0 ; i < W ; i = i + 1)begin: GREG

    always@(negedge rst_ni or posedge clk_i) begin
      if (~rst_ni)begin
        data[i] <= 1'b0;
      end else if (i_vld && i_en) begin
        data[i] <= i_x[i];
      end
    end
    
    assign o_z[i] = data[i];
    
  end
  endgenerate



`elsif FPGA

reg [W-1:0] data;
always@(negedge rst_ni or posedge clk_i) begin
  if (~rst_ni)begin
    data <= {{W}{1'b0}};
  end else if (i_vld && i_en) begin
    data <= i_x;
  end
end

assign o_z = data;


`elsif TSMC_28N

  genvar i;

  wire en;
  lix_and  #(.W(1)
  ) u_and(
    .i_x (i_vld),
    .i_y (i_en),
    .o_z (en));

  generate
    for (i = 0 ; i < W ; i = i +1) begin: GREG
      EDFCNQD4BWP12T30P140LVT u_reg ( 
        .D(i_x[i]), 
        .E(en), 
        .CP(clk_i), 
        .CDN(rst_ni), 
        .Q(o_z[i]));
    end
  endgenerate

`else


`endif


endmodule
