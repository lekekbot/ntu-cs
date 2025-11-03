`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 17.04.2020 17:08:32
// Design Name: 
// Module Name: Lab5_top
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
//	Inputs:  100MHz system clock (clk); active high reset (rst)
//	Outputs: Active low 7 segment value (seg_L); Active low anode driver (anode_L)
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////

// The top level module. It implements the Verilog system shown in Figure 1.

module Lab5_top(input clk, rst, sel, output [6:0] seg_L, output [3:0] anode_L);

    // Wires
    wire        clk_slow;
    wire [15:0] display;

    // Instantiate slow clock for scrolling
    slow_clkgen u_slow (.clk(clk), .rst(rst), .clk_out(clk_slow));

    // Instantiate scroll logic that produces 4 nibbles
    scroll u_scroll (.clk(clk_slow), .rst(rst), .display(display));

    // 7-seg driver: uses system clk for anode refresh, displays `display`
    seg7_driver u_seg7 (
        .clk(clk), .rst(rst), .sel(sel),
        .value(display), .anode_d(4'b0000),
        .seg_L(seg_L), .anode_L(anode_L)
    );

endmodule
