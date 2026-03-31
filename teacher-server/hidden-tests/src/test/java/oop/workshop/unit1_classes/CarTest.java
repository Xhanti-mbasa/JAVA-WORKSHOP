package oop.workshop.unit1_classes;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CarTest {
    @Test
    public void testCarCreation() {
        Car car = new Car("Toyota", 2022);
        assertEquals("Toyota", car.getBrand());
        assertEquals(2022, car.getYear());
    }
}
