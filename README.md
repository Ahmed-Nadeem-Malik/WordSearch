## Version Summaries

---

### V1
At each index we search left and down if we have a first character match. First version made before i realised a better solution

---

### V2
When we instantiate the class we compute all possible words. This means lookup of a word is O(1), however the compute time for the words is quite large. Also, the space complexity is quite large as it’s all possible words.

---

### V3
Same methodology as V2 but we introduce the multiprocessing library, which we use when computing the word set. We assign a worker for each row that processes that row while other rows are processed at the same time. This was just implemented because I wanted to see how Python differs from C++ in the context of multiprocessing.

---

## Hypothesis
Multiprocessing should be faster.

---

## Test Cases
Small and large grid.

---

## Results

For the original grid used for testing:  
**V2:** 0.0003752919983526226 seconds  
**V3:** 0.0737524169999233 seconds  

For the larger grid:  
**V2:** 47.72359229200083 seconds  
**V3:** 4.3694680410008 seconds  

---

## Conclusion
The multiprocessing library must have some overhead that can make the results take longer for smaller grids, but as we increase the size of the grid it can be a lot faster, such as a 10x speedup in this case.


## References
Multiprocessing: https://superfastpython.com/multiprocessing-pool-python/
