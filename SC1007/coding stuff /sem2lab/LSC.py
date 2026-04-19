def find_lcs(n, A, B):
    """
    Parameters:
    n (int): The number of elements in sequences A and B.
    A (list): A permutation of integers from 1 to n.
    B (list): A permutation of integers from 1 to n.
    
    Returns:
    tuple: (max_length, total_count)
    """
    
    # Step 1: Create a position map for elements in B
    # pos[x] will store the 1-based index of element x in array B
    pos = {val: i + 1 for i, val in enumerate(B)}
    
    # Step 2: Map elements of A to their corresponding indices in B
    # This transforms the LCS problem into an LIS problem
    A_mapped = [pos[val] for val in A]
    
    # Step 3: Initialize a Binary Indexed Tree (Fenwick Tree)
    # bit[i] will store a tuple: [max_length, count_of_max_length]
    # We use size n + 1 because the Fenwick Tree is 1-indexed
    bit = [[0, 0] for _ in range(n + 1)]
    
    def query(idx):
        """
        Finds the maximum LIS length and its count for all elements strictly smaller 
        than the current element (which correspond to earlier positions in B).
        """
        res_len = 0
        res_count = 1  # Base case: A single element forms an LIS of length 1
        
        while idx > 0:
            cur_len, cur_count = bit[idx]
            if cur_len > res_len:
                # Found a strictly longer subsequence
                res_len = cur_len
                res_count = cur_count
            elif cur_len == res_len and cur_len > 0:
                # Found another subsequence of the same maximum length
                res_count += cur_count
            
            # Move to the next interval in the Fenwick Tree
            idx -= idx & (-idx)
            
        return res_len, res_count

    def update(idx, length, count):
        """
        Updates the Fenwick tree with the new sequence length and count
        at the given index.
        """
        while idx <= n:
            if length > bit[idx][0]:
                # New absolute maximum length for this interval
                bit[idx] = [length, count]
            elif length == bit[idx][0]:
                # Additional combinations for the existing maximum length
                bit[idx][1] += count
                
            # Move to the parent interval in the Fenwick Tree
            idx += idx & (-idx)

    # Step 4: Iterate through the mapped array to compute LIS lengths and counts
    for val in A_mapped:
        # Query the maximum sequence formed by elements smaller than 'val'
        q_len, q_count = query(val - 1)
        
        # The new length includes the current element
        new_len = q_len + 1
        
        # Update the tree with the sequence ending at 'val'
        update(val, new_len, q_count)

    # Step 5: The final answer is the max length and count across all elements
    return query(n)

# --- The boilerplate provided in your snippet remains exactly the same below ---
line1 = input().split()
if line1:
    n = int(line1[0])
    
    # Read array A
    A = list(map(int, input().split()))
    
    # Read array B
    B = list(map(int, input().split()))
    
    max_length, total_count = find_lcs(n, A, B)
        
    # Output in the required format
    print(f"Max Length: {max_length}")
    print(f"Total Count: {total_count}")