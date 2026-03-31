package oop.workshop.unit7_messaging;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class MessagingTest {
    @Test
    public void testMessagePassing() {
        Customer c = new Customer();
        Order o = new Order();
        c.placeOrder(o);
        assertEquals("Processed", o.getStatus());
    }
}
