# __polys_trimmer__
This tool removes poly A and poly T tails from 3' and 5' and nucleotide sequences.
The input data can be in FASTQ format.
Also removes mistakes C/G insertion in the poly A and poly T tail and creat a stats file.


# How to use:
When you open the script(PolysTrimmer.py), you will have the choice of _custom_ parameters or _default_ parameters available to you.
___Default parameters___: prefix = "file", the statistics file directory is the directory of results files, the name of the statistics file is stats_file.

___
![img 1](images/run%20in%20cmd.png)
# Example
## Example of work this script:
_Poly T_ was deleted and  was deleted corresponding _accuracy of reading symbols_
___
![img 2](images/example.png)
## Example of the stat file:
__Data in the stats file:__
- Total: 3122 // deleted
- Poly A: 1130 // deleted Poly A 
- Poly T: 1355 // deleted Poly T
- Poly A with errors: 318 // Poly A mistkes
- Poly T with errors: 319 // Poly T mistkes
- Poly A errors(%): 21.96
- Poly T errors(%): 19.06
- Middle read length: 233.18175
- Total read(lines): 4000
___
![img 2](images/stat%20example.png)
