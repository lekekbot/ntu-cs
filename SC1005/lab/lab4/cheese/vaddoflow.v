//=============================================================
// SC1005 Lab 4: Behavioural Adder with Overflow Display
// Module: vaddoflow
// Description: Adds two 4-bit inputs, shows sum on 7-segment,
//              lights overflow LED when sum > 15 (0xF)
//=============================================================

module vaddoflow(
    input  [3:0] a,        // 4-bit input A
    input  [3:0] b,        // 4-bit input B
    output [6:0] seg_L,    // 7-segment display output (active-low)
    output oflow            // overflow indicator LED
);

    // Internal 5-bit wire to hold sum (4-bit + 4-bit = max 8'h1E)
    wire [4:0] x;

    // Add a and b
    assign x = a + b;

    // Instantiate the seven-segment decoder
    vsevenseg U1 (
        .x(x[3:0]),     // connect lower 4 bits of sum to decoder
        .seg_L(seg_L)   // connect 7-segment output
    );

    // Overflow flag: high when sum exceeds 4-bit range (i.e. x[4] == 1)
    assign oflow = x[4];

endmodule
