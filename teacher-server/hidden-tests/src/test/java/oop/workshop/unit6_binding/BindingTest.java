package oop.workshop.unit6_binding;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BindingTest {
    @Test
    public void testDynamicBinding() {
        Employee emp = new Manager(50000.0, 10000.0);
        assertEquals(60000.0, emp.calculateSalary(), 0.001);
    }
}
