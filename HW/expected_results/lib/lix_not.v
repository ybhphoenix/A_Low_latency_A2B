//////////////////////////////////////////////////////////////////////////////////
// Company       : TSU
// Engineer      : 
// 
// Create Date   : 2023-09-01
// File Name     : lix_not.v
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
module lix_not #(
    parameter  W = 32
  )(
    input  wire  [W-1:0] i_x,
    output wire  [W-1:0] o_z);

`ifdef SIM

  genvar i;
  generate
  for (i = 0 ; i < W ; i = i + 1)begin: GNOT

    assign o_z[i] = ~ i_x[i];
    
  end
  endgenerate


`elsif FPGA

  genvar i;
  generate    
    for (i = 0 ; i < W ; i = i +1) begin: GNOT

      LUT6 #(.INIT(64'h0000000000000001))      
       lut6_not_inst(
        .O (o_z[i]),
        .I0(i_x[i]),
        .I1(1'd0),
        .I2(1'd0),
        .I3(1'd0),
        .I4(1'd0),
        .I5(1'd0)
        );

    end
  endgenerate


`elsif TSMC_28N

  genvar i;
  generate
    for (i = 0 ; i < W ; i = i +1) begin: GNOT
      INVD16BWP12T30P140LVT u_not
      (.I(i_x[i]),.ZN(o_z[i]));
    end
  endgenerate

`elsif LIB_45NM

  genvar i;
  generate    
    for (i = 0 ; i < W ; i = i +1) begin: GNOT
      INV_X4 u_not
      (.A(i_x[i]), .ZN(o_z[i]));
    end
  endgenerate



`else


`endif


endmodule
