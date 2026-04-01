package oop.workshop.unit5_abstraction;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class AbstractionTest {
    @Test
    public void testMicrowave() {
        Appliance app = new Microwave();
        assertEquals("Microwave is heating", app.turnOn());
    }
}
