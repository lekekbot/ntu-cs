package lab3;

public class PlaneSeat {
    private int seatId, customerId;
    private boolean assigned;

    public PlaneSeat(int seatId) {
        this.seatId = seatId;
        this.assigned = false;
    }

    public int getSeatId() {
        return seatId;
    }

    public int getCustomerId() {
        return customerId;
    }

    public boolean isOccupied() {
        return assigned;
    }

    public void assign(int cust_id) {
        if (assigned) {
            System.out.println("Seat already assigned to a customer.");
        } else {
            this.customerId = cust_id;
            this.assigned = true;
            System.out.println("Seat " + seatId + " assigned to customer " + customerId);
        }
    }

    public void unAssign() {
        if (assigned) {
            System.out.println("Seat Unassigbed!");
            this.customerId = 0;
            this.assigned = false;
        } else {
            System.out.println("Seat " + seatId + " is already unassigned.");
        }
    }

}
