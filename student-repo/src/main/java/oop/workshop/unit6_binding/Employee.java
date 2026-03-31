package oop.workshop.unit6_binding;

public class Employee {
    protected double baseSalary;
    
    public Employee(double baseSalary) {
        this.baseSalary = baseSalary;
    }
    
    public double calculateSalary() {
        return baseSalary;
    }
}
