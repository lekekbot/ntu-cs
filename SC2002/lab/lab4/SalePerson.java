// *************************************************************
// SalePerson.java
//
// Represents a salesperson and supports ranking by weekly sales.
// *************************************************************
public class SalePerson implements Comparable<SalePerson>
{
	private String firstName;
	private String lastName;
	private int totalSales;

	public SalePerson(String first, String last, int sales)
	{
		firstName = first;
		lastName = last;
		totalSales = sales;
	}

	public int compareTo(SalePerson other)
	{
		int salesCmp = Integer.compare(this.totalSales, other.totalSales);
		if (salesCmp != 0)
			return salesCmp;

		int lastCmp = other.lastName.compareTo(this.lastName);
		if (lastCmp != 0)
			return lastCmp;

		return other.firstName.compareTo(this.firstName);
	}

	public boolean equals(Object obj)
	{
		if (this == obj)
			return true;
		if (!(obj instanceof SalePerson))
			return false;

		SalePerson other = (SalePerson) obj;
		return this.firstName.equals(other.firstName)
			&& this.lastName.equals(other.lastName);
	}

	public String getFirstName()
	{
		return firstName;
	}

	public String getLastName()
	{
		return lastName;
	}

	public int getTotalSales()
	{
		return totalSales;
	}

	public String toString()
	{
		return lastName + ", " + firstName + ": " + totalSales;
	}
}
