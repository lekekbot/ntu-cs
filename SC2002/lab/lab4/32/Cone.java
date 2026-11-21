
public class Cone implements Shape {
    private Circle base;
    private double slantHeight;

    public Cone(double radius, double slantHeight) {
        this.base = new Circle(radius);
        this.slantHeight = slantHeight;
    }

    public double getArea() {
        return base.getArea() + (Math.PI * base.getRadius() * slantHeight);
    }
}
