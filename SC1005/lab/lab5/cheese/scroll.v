// Produces a 16-bit display value by scrolling through the
// sequence using a 4-bit counter and four convert instances.

module scroll (
    input  clk,
    input  rst,
    output [15:0] display
);

    reg  [3:0] count;
    wire [3:0] a, b, c, d;
    wire [3:0] ao, bo, co, do;

    // 4-bit up counter with synchronous reset, wraps 0..15
    always @(posedge clk) begin
        if (rst)
            count <= 4'd0;
        else
            count <= count + 4'd1;
    end

    // Generate four sequential indices
    assign a = count;
    assign b = count + 4'd1;
    assign c = count + 4'd2;
    assign d = count + 4'd3;

    // Map indices to 7-seg nibble values
    convert u_conv_a(.in(a), .out(ao));
    convert u_conv_b(.in(b), .out(bo));
    convert u_conv_c(.in(c), .out(co));
    convert u_conv_d(.in(d), .out(do));

    // Concatenate into display output (MSB = a, LSB = d)
    assign display = {ao, bo, co, do};

endmodule