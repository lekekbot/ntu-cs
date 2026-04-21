def longest_subarray(arr, K):
#add you codes
    longy = 0

    for i in range(len(arr)):
        c = 0 #count internally for 0s
     
        for x in range(i, len(arr)):

            if(arr[x] == 0):
                c += 1

            if (c > K):
                break
            consecutive = x - i + 1
            if consecutive > longy:
                longy = consecutive
    return longy

arr = list(map(int, input().split()))
K = int(input())

print(longest_subarray(arr, K))