# Student Team Allocation Algorithm

## Overview

This Python program implements an intelligent student team allocation algorithm that creates balanced teams within tutorial groups. The algorithm aims to maximize diversity across multiple dimensions including CGPA (academic performance), school affiliation, and gender while maintaining team size constraints.

## Problem Statement

The challenge is to automatically assign students to teams such that:
- Teams are balanced in terms of academic performance (CGPA)
- No single school or gender dominates any team (diversity constraint)
- Team sizes are as uniform as possible
- Students are grouped within their tutorial groups

## Data Structure

The input data consists of student records with the following attributes:
- **Tutorial Group**: The tutorial class the student belongs to
- **Student ID**: Unique identifier for each student
- **Name**: Student's full name
- **School**: Academic school/faculty (e.g., EEE, CCDS, CoB, etc.)
- **Gender**: Male/Female
- **CGPA**: Cumulative Grade Point Average (academic performance metric)

## Algorithm Components

### 1. Data Loading and Preprocessing

```python
def load_records(path):
    # Loads student data from CSV file
    # Converts CGPA to float and strips whitespace from text fields
```

```python
def group_by_tutorial(students):
    # Groups students by tutorial group
    # Sorts students within each group by CGPA (descending) then by name
```

### 2. CGPA-Based Student Categorization

The algorithm categorizes students into three performance tiers using tertile thresholds:

```python
def tertile_thresholds(vals):
    # Calculates 33rd and 67th percentile CGPA values
    # Returns (low_threshold, high_threshold)
```

```python
def cgpa_bucket(cg, t1, t2):
    # Categorizes CGPA into three buckets:
    # "L" (Low): Below 33rd percentile
    # "M" (Medium): Between 33rd and 67th percentile  
    # "H" (High): Above 67th percentile
```

**Computational Thinking Principle**: *Decomposition* - Breaking down the complex problem of balancing academic performance by creating discrete performance categories.

### 3. Team Size Optimization

```python
def target_team_sizes(n, size):
    # Calculates optimal team sizes given n students and target size
    # Uses division to create teams as close to target size as possible
    # Example: 23 students, target size 5 → [6, 6, 6, 5] (3 teams of 6, 1 team of 5)
```

**Computational Thinking Principle**: *Algorithmic Thinking* - Using mathematical division and modulo operations to distribute students optimally.

### 4. Diversity Constraint Management

```python
def max_same_limit(n):
    # Calculates maximum allowed students from same school/gender
    # Uses n//2 to ensure no single attribute dominates (majority rule)
```

```python
def can_add(team, cand, lim, key):
    # Checks if adding a candidate would violate diversity constraints
    # Uses Counter to track attribute frequency in current team
```

**Computational Thinking Principle**: *Pattern Recognition* - Identifying when teams become unbalanced and applying consistent rules to maintain diversity.

### 5. Core Team Building Algorithm

The `build_team` function implements a sophisticated allocation strategy:

```python
def build_team(cands, target, limit):
    # Main team building logic with constraint relaxation
```

**Algorithm Strategy**:
1. **Priority-based selection**: Prioritizes CGPA buckets with more candidates
2. **Constraint enforcement**: Checks school and gender diversity limits
3. **Progressive relaxation**: Gradually relaxes constraints if strict allocation fails
   - Initially: Enforce both school and gender diversity
   - Step 1: Relax school constraint (try 2 iterations)
   - Step 2: Relax gender constraint (try 3 iterations)  
   - Step 3: Force allocation from any available bucket

**Computational Thinking Principle**: *Abstraction* - Creating a flexible framework that can handle various constraint scenarios through systematic relaxation.

### 6. Tutorial Group Processing

```python
def assign_teams_for_group(students, size=5):
    # Processes one tutorial group:
    # 1. Calculate CGPA tertiles for the group
    # 2. Categorize students into L/M/H buckets
    # 3. Determine target team sizes
    # 4. Build teams sequentially using core algorithm
```

```python
def allocate_all(students, size=5):
    # Processes all tutorial groups and formats output
    # Creates standardized output with team identifiers
```

## Algorithm Evaluation

### Metrics Calculated

The evaluation system measures algorithm effectiveness across multiple dimensions:

```python
def evaluate(rows):
    # Calculates key performance metrics:
    # - school_viol: Number of teams violating school diversity
    # - gender_viol: Number of teams violating gender diversity  
    # - avg_std: Average CGPA standard deviation across teams
```

**Key Metrics**:
- **Diversity Violations**: Teams where one school/gender represents more than 50% of members
- **CGPA Distribution**: Mean and standard deviation of CGPA within each team
- **Team Count**: Total number of teams created

### Visualization

```python
def plot_results(metrics, summaries):
    # Creates three visualizations:
    # 1. Bar chart of diversity violations
    # 2. Histogram of team CGPA means
    # 3. Histogram of team CGPA standard deviations
```

## Computational Thinking Reflection

### 1. Decomposition
The complex team allocation problem is broken down into manageable components:
- Data loading and preprocessing
- Student categorization by performance
- Team size calculation
- Constraint checking
- Progressive constraint relaxation

### 2. Pattern Recognition
The algorithm identifies patterns in team imbalance:
- Recognizes when teams become dominated by single schools/genders
- Detects when strict constraints prevent viable team formation
- Applies consistent rules across all tutorial groups

### 3. Abstraction
Key abstractions simplify the problem:
- CGPA buckets abstract continuous performance into discrete categories
- Diversity limits abstract complex balance requirements into simple majority rules
- Constraint relaxation abstracts the trade-off between ideality and feasibility

### 4. Algorithmic Thinking
The solution employs systematic algorithmic approaches:
- Greedy selection with backtracking (constraint relaxation)
- Priority-based processing (larger buckets first)
- Mathematical optimization for team sizes

## Implementation Highlights

### Data Structures Used
- **Lists**: For storing students and team members
- **Dictionaries**: For grouping by tutorial and storing student attributes
- **Counters**: For tracking attribute frequencies and detecting violations
- **Sets**: For managing constraint relaxation state

### Algorithm Complexity
- **Time Complexity**: O(n log n) due to sorting operations
- **Space Complexity**: O(n) for storing student data and intermediate results

### Robustness Features
- Handles edge cases (empty groups, insufficient students)
- Progressive constraint relaxation prevents infinite loops
- Maintains data integrity through careful list manipulation

## Usage Example

```python
# Load student data
students = load_records('records.csv')

# Allocate teams with target size of 5
allocated = allocate_all(students, size=5)

# Save results
with open('output.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=allocated[0].keys())
    writer.writeheader()
    writer.writerows(allocated)

# Evaluate and visualize results
metrics, summaries = evaluate(allocated)
print(metrics)
plot_results(metrics, summaries)
```

## Conclusion

This algorithm successfully balances multiple competing objectives in team formation:
- **Academic Balance**: Ensures teams have diverse CGPA representation
- **Social Diversity**: Promotes school and gender mixing
- **Practical Constraints**: Maintains reasonable team sizes
- **Scalability**: Handles large datasets efficiently

The progressive constraint relaxation mechanism ensures that teams can always be formed, even when ideal balance is not possible, making the algorithm robust for real-world applications.