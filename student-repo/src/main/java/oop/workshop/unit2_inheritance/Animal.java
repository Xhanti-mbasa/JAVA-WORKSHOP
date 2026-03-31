package oop.workshop.unit2_inheritance;

public class Animal {
    protected String name;
    
    public Animal(String name) {
        this.name = name;
    }
    
    public String makeSound() {
        return "Some generic sound";
    }
}
