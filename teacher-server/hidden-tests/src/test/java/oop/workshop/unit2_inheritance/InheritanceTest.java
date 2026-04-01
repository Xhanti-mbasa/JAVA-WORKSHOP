package oop.workshop.unit2_inheritance;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class InheritanceTest {
    @Test
    public void testDogInheritsAnimal() {
        Dog dog = new Dog("Buddy");
        assertTrue(dog instanceof Animal);
        assertEquals("Woof", dog.makeSound());
    }
}
