Operating System Page Replacement Algorithms
This repository contains implementations of various page replacement algorithms, including:

- FCFS (First-Come, First-Served)
- LFU (Least Frequently Used)
- LRU (Least Recently Used)
 MFU (Most Frequently Used)
- MRU (Most Used- Optimal

These algorithms are implemented in Python, and the repository also includes a paging simulation.

 to Use

Clone the Repository
To use this repository, it to your local machine using the following command:

```
git clone https:///kirankirthan/os-el.git
```

Running the Page Replacement Algorithms
After cloning the repository, navigate the project folder:

```
cd os-el
```

To run any of the six-page replacement algorithms, execute the `main.py` file:

```
python main.py
```

The program will prompt you to enter inputs, such as the number of pages and the page reference string. Once entered, it will the page replacement algorithm and provide results for the chosen.

Running the Paging Simulation
To run a different paging simulation simply execute the `paging.py file:

```
python paging.py
```

This will run another paging simulation where you can provide different inputs simulate the paging.

Requirements
Ensure you have Python installed on your machine. The code uses the following libraries (if required):

- pygame (used for simulations)

You can install the required libraries using:

```
pip install pygame
```

Example Inputs formain.py`
When running the `main.py` file, you will be asked to enter:
- The page replacement algorithm you want to use.
- A page reference stringa sequence of page numbers to simulate).
- The number of pages in the system.
- time delay in seconds.

After entering this information, the program will simulate the algorithm and output the results.
