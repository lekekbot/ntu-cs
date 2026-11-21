// #include <stdio.h>

// int main()
// {
//     int num = 0;
//     int student_id = 0;
//     printf("Enter Student ID: ");
//     scanf("%d", &student_id);
//     if (student_id == -1)
//     {
//         return 0;
//     }

//     printf("Enter Mark: ");
//     scanf("%d", &num);
//     char grade;

//     if (num >= 75 && num <= 100)
//         grade = 'A';
//     else if (num >= 65 && num < 75)
//         grade = 'B';
//     else if (num >= 55 && num < 65)
//         grade = 'C';
//     else if (num >= 45 && num < 55)
//         grade = 'D';
//     else if (num >= 0 && num < 45)
//         grade = 'F';

//     printf("Grade = %c\n", grade);

//     return 0;
// }

#include <stdio.h>

int main()
{
    int num_lines = 0;
        printf("Enter number of lines:\n");
        scanf("%d", &num_lines);
    
    for (int i = 0; i < num_lines; i++)
    {
        printf("Enter line %d (end with -1):\n", i + 1);
        
        int num = 0;
        int sum = 0;
        int count = 0;
        
        while (scanf("%d", &num) == 1 && num != -1)
        {
            sum += num;
            count++;
        }
        
        double average = (count > 0) ? (double)sum / count : 0.0;
        printf("Average = %.2f\n", average);
    }
    
    return 0;
}
