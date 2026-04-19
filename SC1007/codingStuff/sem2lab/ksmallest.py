def kth_smallest(matrix, k):
    """
    Finds the k-th smallest element in a row-wise and column-wise sorted matrix.
    """
    n = len(matrix)
    
    def count_less_or_equal(target):
        """
        Counts the number of elements in the matrix that are <= target.
        Starts from the bottom-left corner of the matrix.
        """
        count = 0
        row = n - 1
        col = 0
        
        while row >= 0 and col < n:
            if matrix[row][col] <= target:
                # If the current element is <= target, all elements above it 
                # in the same column are also <= target because columns are sorted.
                count += (row + 1)
                # Move right to check the next column
                col += 1
            else:
                # If the current element is > target, move up to find smaller elements
                row -= 1
                
        return count

    # The smallest element is at the top-left, the largest at the bottom-right
    left = matrix[0][0]
    right = matrix[n-1][n-1]
    
    # Binary search over the VALUE range, not the indices
    while left < right:
        mid = left + (right - left) // 2
        
        # If the number of elements <= mid is strictly less than k,
        # the k-th smallest element must be strictly greater than mid.
        if count_less_or_equal(mid) < k:
            left = mid + 1
        else:
            # Otherwise, the k-th smallest element is <= mid.
            right = mid
            
    return left

#read the input
n, k = map(int, input().split())
matrix = []
for _ in range(n):
    matrix.append(list(map(int, input().split())))
#output
print(kth_smallest(matrix, k))