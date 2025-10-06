//=============================================================
// SC1005 Lab 4: Behavioural Seven-Segment Display Decoder
// Module: vsevenseg
// Description: Converts 4-bit binary input to active-low 7-segment display output
//=============================================================

module vsevenseg(
    input  [3:0] x,          // 4-bit binary input
    output reg [6:0] seg_L   // 7-bit active-low segment output (gfedcba)
);

    // Combinational logic for seven-segment display
    always @* begin
        case (x)
            4'd0: seg_L = 7'b100_0000; // 0
            4'd1: seg_L = 7'b111_1001; // 1
            4'd2: seg_L = 7'b010_0100; // 2
            4'd3: seg_L = 7'b011_0000; // 3
            4'd4: seg_L = 7'b001_1001; // 4
            4'd5: seg_L = 7'b001_0010; // 5
            4'd6: seg_L = 7'b000_0010; // 6
            4'd7: seg_L = 7'b111_1000; // 7
            4'd8: seg_L = 7'b000_0000; // 8
            4'd9: seg_L = 7'b001_0000; // 9
            4'd10: seg_L = 7'b000_1000; // A
            4'd11: seg_L = 7'b000_0011; // b
            4'd12: seg_L = 7'b100_0110; // C
            4'd13: seg_L = 7'b010_0001; // d
            4'd14: seg_L = 7'b000_0110; // E
            4'd15: seg_L = 7'b000_1110; // F
            default: seg_L = 7'b111_1111; // all segments off
        endcase
    end

endmodule
