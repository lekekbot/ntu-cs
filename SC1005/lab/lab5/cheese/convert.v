// Maps a 4-bit index (0..15) to the sequence
// "AACOFFEEA15A900D" using hexadecimal nibble outputs
// to be consumed by seg7_driver (0..F).

module convert (
    input  [3:0] in,
    output reg [3:0] out
);

    always @* begin
        case (in)
            4'd0  : out = 4'd10; // A (blank via seg7 default)
            4'd1  : out = 4'd10; // A (blank)
            4'd2  : out = 4'd12; // C
            4'd3  : out = 4'd0;  // O
            4'd4  : out = 4'd15; // F
            4'd5  : out = 4'd15; // F
            4'd6  : out = 4'd14; // E
            4'd7  : out = 4'd14; // E
            4'd8  : out = 4'd10; // A (blank)
            4'd9  : out = 4'd1;  // 1
            4'd10 : out = 4'd5;  // 5
            4'd11 : out = 4'd10; // A (blank)
            4'd12 : out = 4'd9;  // 9
            4'd13 : out = 4'd0;  // 0
            4'd14 : out = 4'd0;  // 0
            4'd15 : out = 4'd13; // D
            default: out = 4'd10; // default to A (blank)
        endcase
    end

endmodule