package oop.workshop.unit6_binding;

public class Manager extends Employee {
    private double bonus;
    
    public Manager(double baseSalary, double bonus) {
        super(baseSalary);
        this.bonus = bonus;
    }
    
    @Override
    public double calculateSalary() {
        return baseSalary + bonus;
    }
}
