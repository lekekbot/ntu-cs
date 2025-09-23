`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 25.02.2020 15:48:02
// Design Name: 
// Module Name: vsevenseg
// Project Name: Lab3
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


// Experiment 3
// 7 segment display with SOP logic expressions 
//


module vsevenseg(
    input [3:0] x,         // 4 rightmost switches
   	output [6:0] seg_L,    // active low segment display
	output [3:0] anode_L   // active low digit display
	);

// declare internal active high segments
wire [6:0] seg;	            // 1:on, 0:off

// turn on only the two rightmost digits - active low
assign anode_L = 4'b1100;  

// pull cathode low to light up segment - active low
assign seg_L = ~seg;

// x format {msb, ., ., lsb}
// seg[6:0] format {g, f, e, d, c, b, a} - active high
// segment a, b, e, g expressions are given 
  // segment a= x3'x2x0 + x2x1 + x3'x1 + x3x0' + x3x2'x1' + x2'x0'
   assign seg[0] = ~x[3]&x[2]&x[0]|x[2]&x[1]|~x[3]&x[1]|x[3]&~x[0]|x[3]&~x[2]&~x[1]|~x[2]&~x[0];
  // segment b= x3'x2' + x2'x0' + x3'x1'x0' + x3'x1x0 + x3x1'x0
   assign seg[1] = ~x[3]&~x[2]|~x[2]&~x[0]|~x[3]&~x[1]&~x[0]|~x[3]&x[1]&x[0]|x[3]&~x[1]&x[0];
  // segment e= x3x2 + x3x1 + x2'x0' + x1x0'
   assign seg[4] = x[3]&x[2]|x[3]&x[1]|~x[2]&~x[0]|x[1]&~x[0];
  // segment g= x1x0' + x3x2' + x3x0 + x2'x1 + x3'x2x1'
   assign seg[6] = x[1]&~x[0]|x[3]&~x[2]|x[3]&x[0]|~x[2]&x[1]|~x[3]&x[2]&~x[1];
   
////////////////////////////////////////////
// students to fill in these 3 expressions
// remember to end each statement with a semicolon ";"
  // segment c
   assign seg[2] = 

  // segment d
   assign seg[3] = 

  // segment f
   assign seg[5] = 

 
endmodule
