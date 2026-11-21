#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int isprime(int num)
{
    int count = 0;
    for (int i = 1; i < num + 1; i++)
    {
        if (num % i == 0)
        {
            count += 1;
        }
    }
    if (count > 2)
        return 0;
    return 1;
}

int pfactorisation(int num, int div)
{
    if (num == 1)
    {
        printf(" %d\n", num);
    }
    else
    {
        while (num != 1)
        {
            if (isprime(div) == 1)
            {
                while (num % div == 0)
                {
                    num = num / div;
                    if (num == 1)
                    {
                        printf(" %d\n", div);
                    }
                    else
                    {
                        printf(" %d%2c", div, 'X');
                    }
                }
                div = div + 1;
            }
            else
            {
                div += 1;
            }
        }
    }
}

int product(int num1, int num2, int num3)
{
}

int correct_num3(int num1, int num2)
{
    int product = num1 * num2;
    int num3 = 1;
    int i, count;

    for (i = 2; i <= product; i++)
    {
        count = 0;

        while (product % i == 0)
        {
            count++;
            product = product / i;
        }
        if (count % 2 == 1)
            num3 = num3 * i;
    }
    if (product > 1)
    {
        num3 = num3 * product;
        return num3;
    }
}

int main(void)
{
    int num1 = 0, num2 = 0, num3 = 0, div = 2;
    int correct_product;
    char user_choice = 'N';

    srand((unsigned)time(NULL));
    /* Wrap the main game loop in a do-while so the user can play again. */
    do
    {
        num1 = rand() % 20 + 1;
        num2 = rand() % 20 + 1;

        printf("===Make Perfect Square===\n\n");
        printf("Two non-prime integers between 1 and 20 are: \n");
        printf("num1%27d%2c", num1, '=');
        pfactorisation(num1, div);
        printf("num2%27d%2c", num2, '=');
        pfactorisation(num2, div);

        /* Prompt for num3 and flush so prompt is visible before scanf */
        while (num3 <= 0)
        {
            printf("Enter num3: ");
            fflush(stdout);
            if (scanf("%d", &num3) != 1)
            {
                int ch;
                while ((ch = getchar()) != '\n' && ch != EOF)
                    ;
                num3 = 0;
            }
        }

        printf("num3%27d%2c", num3, '=');
        pfactorisation(num3, div);
        printf("num1 X num2 X num3 %12d%2c", num1 * num2 * num3, '=');
        pfactorisation(num3 * num1 * num2, div);

        if (num3 == correct_num3(num1, num2))
        {
            printf("\nCorrect!\n");
            printf("%d is the smallest number that makes num1 X num2 X num3 a perfect square.\n", num3);
        }
        else
        {
            int correct = correct_num3(num1, num2);
            printf("\nWrong! The correct num3 is %d = ", correct);
            pfactorisation(correct, div);
            correct_product = num1 * num2 * correct;
            printf("\nnum1 X num2 X num3 %12d%2c", correct_product, '=');
            pfactorisation(correct_product, div);
            printf("\n%d is the smallest num3 that makes num1 X num2 X num3 a perfect square.\n", correct);
        }

        /* Play again prompt */
        printf("\nEnter Y to play again or any other key to quit: ");
        fflush(stdout);
        /* Read a single non-whitespace character */
        if (scanf(" %c", &user_choice) != 1)
            user_choice = 'N';

        /* consume rest of line to avoid leftover input affecting next loop */
        int ch;
        while ((ch = getchar()) != '\n' && ch != EOF)
            ;

        printf("\n");
    } while (user_choice == 'Y' || user_choice == 'y');

    printf("Goodbye!\n");
    return 0;
}