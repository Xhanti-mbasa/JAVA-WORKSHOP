package oop.workshop.unit2_inheritance;

public class Dog extends Animal {
    public Dog(String name) {
        super(name);
    }
    
    @Override
    public String makeSound() {
        return "Woof";
    }
}
