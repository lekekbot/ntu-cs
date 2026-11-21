
public class Cylinder implements Shape {
    private Circle base;
    private Rectangle lateral;

    public Cylinder(double radius, double height) {
        this.base = new Circle(radius);
        this.lateral = new Rectangle(2 * Math.PI * radius, height);
    }

    public double getArea() {
        return (2 * base.getArea()) + lateral.getArea();
    }
}
