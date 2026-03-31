package oop.workshop.unit3_polymorphism;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PolymorphismTest {
    @Test
    public void testCircleArea() {
        Shape shape = new Circle(5.0);
        assertEquals(Math.PI * 25, shape.getArea(), 0.001);
    }
}
