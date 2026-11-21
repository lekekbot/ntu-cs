import java.util.Scanner;

public class Lab2p1 {
    public static void main(String[] args) {
        int choice;
        Scanner sc = new Scanner(System.in);
        do {
            System.out.println("Perform the following methods:");
            System.out.println("1: miltiplication test");
            System.out.println("2: quotient using division by subtraction");
            System.out.println("3: remainder using division by subtraction");
            System.out.println("4: count the number of digits");
            System.out.println("5: position of a digit");
            System.out.println("6: extract all odd digits");
            System.out.println("7: quit");
            choice = sc.nextInt();
            switch (choice) {
                case 1: /* add mulTest() call */
                    mulTest();
                    break;
                case 2: /* add divide() call */
                    int num, div;
                    System.out.println("type a num");
                    num = sc.nextInt();
                    System.out.println("dividend");

                    div = sc.nextInt();
                    divide(num, div);
                    break;
                case 3: /* add modulus() call */
                    int num2, div2;
                    System.out.println("type a num");
                    num2 = sc.nextInt();
                    System.out.println("dividend");

                    div2 = sc.nextInt();
                    modulus(num2, div2);
                    System.out.println(num2 + " % " + div2 + " = " + modulus(num2, div2));
                    break;
                case 4: /* add countDigits() call */
                    int num3;
                    System.out.println("Enter a number:");
                    num3 = sc.nextInt();
                    countDigits(num3);
                    break;
                case 5: /* add position() call */
                    int num5, digit5;
                    System.out.println("Enter a number:");
                    num5 = sc.nextInt();
                    System.out.println("Enter a digit:");
                    digit5 = sc.nextInt();
                    System.out.println("position = " + position(num5, digit5));
                    break;
                case 6: /* add extractOddDigits() call */
                    long num6;
                    System.out.println("Enter a number:");
                    num6 = sc.nextLong();
                    long result = extractOddDigits(num6);
                    if (result != -1) {
                        System.out.println("oddDigits = " + result);
                    }
                    break;
                case 7:
                    System.out.println("Program terminating ….");
            }
        } while (choice < 7);
    }

    public static void mulTest() {
        int answers = 0;
        for (int i = 0; i < 5; i++) {
            int num1, num2, answer, userAnswer;
            num1 = (int) (Math.random() * 9) + 1;
            num2 = (int) (Math.random() * 9) + 1;

            answer = num1 * num2;
            Scanner sc = new Scanner(System.in);
            System.out.println("How much is " + num1 + " times " + num2 + "?");
            userAnswer = sc.nextInt();
            if (userAnswer == answer) {
                System.out.println("Correct!");
                answers++;
            } else {
                System.out.println("Incorrect. The correct answer is " + answer);
            }
        }
        System.out.println(answers + " out of 5 answers are correct");

    }

    public static void divide(int num, int div) {
        int increment = 0;
        int i = num;
        do {
            i = i - div;
            if (i >= 0) {
                increment++;
            }

        } while (i > 0);

        System.out.println(num + "/" + div + "=" + increment);
    }

    public static int modulus(int m, int n) {
        int increment = 0;
        int i = m;
        do {
            i = i - n;
            if (i >= 0) {
                increment++;
            }
        } while (i > 0);
        return m - (increment * n);
    }

    public static int countDigits(int n) {
        if (n < 0) {
            System.out.println("Error Input");
            return -1;
        }
        int count = 0;
        while (n != 0) {
            n = n / 10;
            count++;
        }
        System.out.println(n + " - Count = " + count);
        return count;
    }

    public static int position(int n, int digit) {
        int pos = 1;
        while (n > 0) {
            if (n % 10 == digit) {
                return pos;
            }
            n = n / 10;
            pos++;
        }
        return -1;
    }

    public static long extractOddDigits(long n) {
        if (n < 0) {
            System.out.println("Error input!!");
            return -1;
        }

        String result = "";
        String numStr = String.valueOf(n);

        for (char c : numStr.toCharArray()) {
            int digit = Character.getNumericValue(c);
            if (digit % 2 == 1) { // odd digit
                result += c;
            }
        }

        if (result.isEmpty()) {
            System.out.println("-1");
            return -1;
        }

        return Long.parseLong(result);
    }
}
