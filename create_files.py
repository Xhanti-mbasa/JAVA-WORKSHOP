import os

files = {
    "student-repo/src/main/java/oop/workshop/unit1_classes/Car.java": """package oop.workshop.unit1_classes;

public class Car {
    // TODO 1: Create a private String variable named 'brand'
    // TODO 2: Create a private int variable named 'year'
    
    // TODO 3: Create a constructor that takes 'brand' and 'year' parameters
    
    // TODO 4: Create a public method named 'getBrand' that returns the brand
    
    // TODO 5: Create a public method named 'getYear' that returns the year
}
""",
    "student-repo/src/main/java/oop/workshop/unit2_inheritance/Animal.java": """package oop.workshop.unit2_inheritance;

public class Animal {
    protected String name;
    
    public Animal(String name) {
        this.name = name;
    }
    
    public String makeSound() {
        return "Some generic sound";
    }
}
""",
    "student-repo/src/main/java/oop/workshop/unit2_inheritance/Dog.java": """package oop.workshop.unit2_inheritance;

// TODO 1: Make the Dog class inherit from the Animal class
public class Dog {
    
    // TODO 2: Create a constructor that takes a 'name' parameter and calls the parent constructor using 'super(name)'
    
    // TODO 3: Override the 'makeSound' method to return "Woof"
}
""",
    "student-repo/src/main/java/oop/workshop/unit3_polymorphism/Shape.java": """package oop.workshop.unit3_polymorphism;

public class Shape {
    public double getArea() {
        return 0.0;
    }
}
""",
    "student-repo/src/main/java/oop/workshop/unit3_polymorphism/Circle.java": """package oop.workshop.unit3_polymorphism;

// TODO 1: Inherit from Shape
public class Circle {
    private double radius;
    
    public Circle(double radius) {
        this.radius = radius;
    }
    
    // TODO 2: Override getArea() to return Math.PI * radius * radius
}
""",
    "student-repo/src/main/java/oop/workshop/unit4_encapsulation/BankAccount.java": """package oop.workshop.unit4_encapsulation;

public class BankAccount {
    // TODO 1: Declare a private double variable named 'balance'
    
    // TODO 2: Create a constructor that initializes the balance
    
    // TODO 3: Create a public getter method for balance named 'getBalance'
    
    // TODO 4: Create a public setter method named 'deposit' that adds a given amount.
    // If the amount is less than or equal to 0, do not change the balance.
}
""",
    "student-repo/src/main/java/oop/workshop/unit5_abstraction/Appliance.java": """package oop.workshop.unit5_abstraction;

// TODO 1: Make this class abstract
public class Appliance {
    // TODO 2: Create a public abstract method named 'turnOn' that returns a String
}
""",
    "student-repo/src/main/java/oop/workshop/unit5_abstraction/Microwave.java": """package oop.workshop.unit5_abstraction;

// TODO 1: Inherit from Appliance
public class Microwave {
    
    // TODO 2: Implement the required turnOn method. It should return "Microwave is heating"
}
""",
    "student-repo/src/main/java/oop/workshop/unit6_binding/Employee.java": """package oop.workshop.unit6_binding;

public class Employee {
    protected double baseSalary;
    
    public Employee(double baseSalary) {
        this.baseSalary = baseSalary;
    }
    
    public double calculateSalary() {
        return baseSalary;
    }
}
""",
    "student-repo/src/main/java/oop/workshop/unit6_binding/Manager.java": """package oop.workshop.unit6_binding;

// TODO 1: Make Manager inherit from Employee
public class Manager {
    private double bonus;
    
    // TODO 2: Create constructor that takes baseSalary and bonus, and calls super(baseSalary)
    
    // TODO 3: Override calculateSalary to return baseSalary + bonus
}
""",
    "student-repo/src/main/java/oop/workshop/unit7_messaging/Order.java": """package oop.workshop.unit7_messaging;

public class Order {
    private String status = "Pending";
    
    public void process() {
        this.status = "Processed";
    }
    
    public String getStatus() {
        return status;
    }
}
""",
    "student-repo/src/main/java/oop/workshop/unit7_messaging/Customer.java": """package oop.workshop.unit7_messaging;

public class Customer {
    // TODO 1: Create a method named 'placeOrder' that accepts an Order object as a parameter.
    // Inside the method, call the 'process()' method on the order object.
}
"""
}

# The hidden tests that the teacher will run
tests = {
    "teacher-server/hidden-tests/src/test/java/oop/workshop/unit1_classes/CarTest.java": """package oop.workshop.unit1_classes;

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
""",
    "teacher-server/hidden-tests/src/test/java/oop/workshop/unit2_inheritance/InheritanceTest.java": """package oop.workshop.unit2_inheritance;

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
""",
    "teacher-server/hidden-tests/src/test/java/oop/workshop/unit3_polymorphism/PolymorphismTest.java": """package oop.workshop.unit3_polymorphism;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PolymorphismTest {
    @Test
    public void testCircleArea() {
        Shape shape = new Circle(5.0);
        assertEquals(Math.PI * 25, shape.getArea(), 0.001);
    }
}
""",
    "teacher-server/hidden-tests/src/test/java/oop/workshop/unit4_encapsulation/EncapsulationTest.java": """package oop.workshop.unit4_encapsulation;

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
""",
    "teacher-server/hidden-tests/src/test/java/oop/workshop/unit5_abstraction/AbstractionTest.java": """package oop.workshop.unit5_abstraction;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class AbstractionTest {
    @Test
    public void testMicrowave() {
        Appliance app = new Microwave();
        assertEquals("Microwave is heating", app.turnOn());
    }
}
""",
    "teacher-server/hidden-tests/src/test/java/oop/workshop/unit6_binding/BindingTest.java": """package oop.workshop.unit6_binding;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BindingTest {
    @Test
    public void testDynamicBinding() {
        Employee emp = new Manager(50000.0, 10000.0);
        assertEquals(60000.0, emp.calculateSalary(), 0.001);
    }
}
""",
    "teacher-server/hidden-tests/src/test/java/oop/workshop/unit7_messaging/MessagingTest.java": """package oop.workshop.unit7_messaging;

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
"""
}

base_dir = "/home/shatter/WTC/JAVA-WORKSHOP"

for path, content in {**files, **tests}.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(content)

print("Files created successfully.")
