# Graph Data Mining

This project 2 is to implement the alogrithm discussed in Paper 1, Efficient Identification of Overlapping Communities.

## Environment to test the script
This project has been tested on `CSC591_ADBI_v3` VCL environment.

## Packages requirment
Please ensure the `networkx` to be installed beforehand, or run the following command to install:
```
pip3 install networkx
```
If the installtion failed from the command above, please download from website and following the instructioins on the website to install.
[https://pypi.org/project/networkx/#files](https://pypi.org/project/networkx/#files)

## How to run the script
After download the zip, first unzip the zip file and get into the folder.
```
unzip GDM_Project2.zip
cd GDM_Project2
```
Once the path is under `GDM_Project2`, please run the command in following format. 
```
python3 main.py <path/to/file/file>
```
For example, if we would like to run the `amazon.graph.small`, please run the command as following:
```
python3 main.py ./datasets/amazon/amazon.graph.small 
```
After the program complete, the final communiites will be store in `result/output.txt`, the program should run 3 mins to 10 mins depends on the graph size.

Note that if `output.txt` will be overwrited if re-run the prorgam.
The output file will be in the format as below:
```
0 1
2 3 6 7 119 119
35 366 988 23 98 112 
```
Each line present the nodes with same community and, for example, the second community contains 6 nodes.

## Project Member:
1. Wen-Han Hu (whu24)
2. Yang-Kai Chou (ychou3)
3. Yuan Xu (yxu48)

