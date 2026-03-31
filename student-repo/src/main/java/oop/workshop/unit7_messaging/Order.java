package oop.workshop.unit7_messaging;

public class Order {
    private String status = "Pending";
    
    public void process() {
        this.status = "Processed";
    }
    
    public String getStatus() {
        return status;
    }
}
