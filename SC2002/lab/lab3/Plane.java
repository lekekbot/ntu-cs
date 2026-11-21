package lab3;

public class Plane {
    private PlaneSeat[] seat;
    private int numEmptySeats = 0;

    public Plane() {
        seat = new PlaneSeat[12];
        for (int i = 0; i < 12; i++) {
            seat[i] = new PlaneSeat(i + 1);
            numEmptySeats++;
        }
    }

    private PlaneSeat[] sortSeats() {
        PlaneSeat[] tempSeats = new PlaneSeat[seat.length];
        for (int i = 0; i < seat.length; i++) {
            tempSeats[i] = seat[i];
        }
        for (int i = 0; i < tempSeats.length - 1; i++) {
            for (int j = 0; j < tempSeats.length - i - 1; j++) {
                if (tempSeats[j].getCustomerId() > tempSeats[j + 1].getCustomerId()) {
                    PlaneSeat temp = tempSeats[j];
                    tempSeats[j] = tempSeats[j + 1];
                    tempSeats[j + 1] = temp;
                }
            }
        }
        return tempSeats;
    }

    public void showNumEmptySeats() {
        System.out.println("There are " + numEmptySeats + " empty seats");
    }

    public void showEmptySeats() {
        System.out.println("The following seats are empty:");
        for (int i = 0; i < seat.length; i++) {
            if (!seat[i].isOccupied()) {
                System.out.print("SeatID " +  seat[i].getSeatId() + "\n");
            }
        }
    }

    public void showAssignedSeats(boolean bySeatId) {
        System.out.println("The seat assignments are as follow:");
        PlaneSeat[] seatsToShow = bySeatId ? seat : sortSeats();
        for (int i = 0; i < seatsToShow.length; i++) {
            if (seatsToShow[i].isOccupied()) {
                System.out.println("SeatID " + seatsToShow[i].getSeatId() + " assigned to CustomerID " + seatsToShow[i].getCustomerId() + ".");
            }
        }
    }

    public void assignSeat(int seatId, int custId) {
        if (seatId < 1 || seatId > seat.length) {
            System.out.println("Invalid seat ID: " + seatId);
            return;
        }
        if (custId <= 0) {
            System.out.println("Invalid customer ID: " + custId);
            return;
        }
        if (seat[seatId - 1].isOccupied()) {
            System.out.println("Seat " + seatId + " is already assigned to customer " + seat[seatId - 1].getCustomerId());
        } else {
            seat[seatId - 1].assign(custId);
            numEmptySeats--;
        }
    }

    public void unAssignSeat(int seatId) {
        if (seatId < 1 || seatId > seat.length) {
            System.out.println("Invalid seat ID: " + seatId);
            return;
        }
        if (!seat[seatId - 1].isOccupied()) {
            System.out.println("Seat " + seatId + " is already unassigned.");
        } else {
            seat[seatId - 1].unAssign();
            numEmptySeats++;
        }
    }

}
