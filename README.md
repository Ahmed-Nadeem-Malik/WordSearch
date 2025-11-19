# Word Search 

This document summarizes four versions of a word search implementation and their performance differences, focusing on the impact of multiprocessing. Tested on python 3.14

---

## Version Summaries

### **V1 — Basic Search**
At each index, we search **left** and **down** if we have a first character match.  
First version made before a better solution was realized.

---

### **V2 — Precomputed Words**
When we instantiate the class, we compute **all possible words**, which means that looking up of a word is really fast.  
- Lookup time for a specific word: **O(1)**  
- Compute time for the word set: **High**  
- Space complexity: **High**, since all possible words are stored.

---

### **V3 — Multiprocessing Implementation**
Same methodology as V2, but introduces the **`multiprocessing`** library.  
A separate worker is assigned for each row, allowing multiple rows to be processed in parallel.  
This was implemented to explore how **Python’s multiprocessing** compares to **C++**.

---

### **V4 — Multithreading Implementation**
Same methodology as V3, but introduces the **`multithreading`** .  
Wanted to see the perfomance of GIL being removed in python 14.

---

## Hypothesis
Multiprocessing should be faster.
Multithreading should be faster that multiprocessing. 


---

## Test Cases
Two test cases were run:  
- Small grid  
- Large grid  

---

## Results

### Original Grid
| Version | Time (seconds) |
|----------|----------------|
| V2 | 0.0003752919983526226 |
| V3 | 0.0737524169999233 |
| V4 | 0.014568999991752207 |


### Large Grid
| Version | Time (seconds) |
|----------|----------------|
| V2 | 47.72359229200083 |
| V3 | 4.3694680410008 |
| V4 | 5.93039658400812 | 

---

## Conclusion
The **multiprocessing library** introduces overhead that causes slower performance on smaller grids.  
However, as the grid size increases, multiprocessing becomes significantly more efficient, achieving about a **10× speedup** in this case.


---

## Conclusion edit after adding multithreading

Thought that this would be faster than V3 for large grids as there is not context switch but results show otherwise.
This may be due to GIL limitations as its still in the process of beign removed. However something interesting is that 
its faster than V3 in smaller grids so maybe the context switch overhead is much more significant in smaller grids but
as the grid is larger its much less significant and a full process may be much more performant than a thread.

---

## References
- [Multiprocessing in Python](https://superfastpython.com/multiprocessing-pool-python/)
