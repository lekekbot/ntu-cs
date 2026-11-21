
public class Cuboid implements Shape {
    private Rectangle face1;
    private Rectangle face2;
    private Rectangle face3;

    public Cuboid(double length, double breadth, double height) {
        this.face1 = new Rectangle(length, breadth);
        this.face2 = new Rectangle(breadth, height);
        this.face3 = new Rectangle(height, length);
    }

    public double getArea() {
        return 2 * (face1.getArea() + face2.getArea() + face3.getArea());
    }
}
