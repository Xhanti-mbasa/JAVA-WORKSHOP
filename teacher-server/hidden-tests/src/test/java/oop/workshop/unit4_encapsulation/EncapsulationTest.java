package oop.workshop.unit4_encapsulation;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class EncapsulationTest {
    @Test
    public void testBankAccount() {
        BankAccount acc = new BankAccount(100.0);
        assertEquals(100.0, acc.getBalance(), 0.001);
        acc.deposit(50.0);
        assertEquals(150.0, acc.getBalance(), 0.001);
        acc.deposit(-20.0);
        assertEquals(150.0, acc.getBalance(), 0.001);
    }
}
