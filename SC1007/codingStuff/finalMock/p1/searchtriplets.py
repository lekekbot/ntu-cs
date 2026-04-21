def solve(N, A):
#add you codes
    count = 0
    # instead of y - x = z - y, change it to
    # 2y = x + z, using this knowledge, we can determine that y is the middle and must follow suit 
    # with 0 < X < Y < Z < N

    for x in range(1, N-1): #take the middle middle only
        target = A[x] * 2
        left = 0
        right = N - 1
        
        while left < x and right > x:
            sum = A[left] + A[right]

            if(sum == target):
                count += 1
                left +=1
                right -=1
            elif sum < target:
                left +=1
            elif sum > target:
                right -= 1
    return count 


import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
A = list(map(int, data[1:]))
print(solve(N,A))