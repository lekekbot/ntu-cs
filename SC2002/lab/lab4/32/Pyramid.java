
public class Pyramid implements Shape {
    private Square base;
    private Triangle face;

    public Pyramid(double baseSide, double slantHeight) {
        this.base = new Square(baseSide);
        this.face = new Triangle(baseSide, slantHeight);
    }

    public double getArea() {
        return base.getArea() + (4 * face.getArea());
    }
}
