def first_occurrence(arr, target):
    #insert your codes
    low = 0
    high = len(arr) - 1
    result = -1  # Default if target is not found
    
    while low <= high:
        mid = (low + high) // 2
        
        if arr[mid] == target:
            result = mid      # Record the index
            high = mid - 1    # Keep searching the left side for an earlier occurrence
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
            
    return result
n, target = map(int, input().split())
arr = list(map(int, input().split()))
result = first_occurrence(arr, target)
print(result)