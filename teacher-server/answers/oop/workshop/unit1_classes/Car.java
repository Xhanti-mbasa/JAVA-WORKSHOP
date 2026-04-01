package oop.workshop.unit1_classes;

public class Car {
    private String brand;
    private int year;
    
    public Car(String brand, int year) {
        this.brand = brand;
        this.year = year;
    }
    
    public String getBrand() {
        return brand;
    }
    
    public int getYear() {
        return year;
    }
}
