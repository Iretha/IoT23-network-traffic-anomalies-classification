# IoT-23-anomaly-detection

ML experiments with IoT23 dataset [1]

## 1. Prerequisites (Part 1): Install missing libraries

No  | Name          | Version          | Description
--- |------------   |------------   |-------------
1   | [Python](https://www.python.org/downloads/release/python-380/)|3.8.8|Programming Language
2   | [scikit-learn](https://scikit-learn.org/stable/)|0.24.1|Tools for Machine Learning in Python
3   | [NymPy](https://numpy.org/)|1.19.5|Tools for Scientific Computing in Python
4   | [pandas](https://pandas.pydata.org/)|1.2.2|Tools for Data Analysis & Data Manipulation in Python
5   | [matplotlib](https://matplotlib.org/stable/tutorials/introductory/pyplot.html)|3.3.4|Visualization with Python
6   | [seaborn](https://seaborn.pydata.org/)|0.11.1|Statistical data visualization
7   | [psutil](https://github.com/giampaolo/psutil)|5.8.0|Cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in Python
8   | [scikit-plot](https://github.com/reiinakano/scikit-plot)|0.3.7|Library for visualizations
9   | [pickle](https://docs.python.org/3/library/pickle.html)|-|Python object serialization for model serialization

## 2. Prerequisites (Part 2): Configure project

1. Download & Extract [IoT23](https://www.stratosphereips.org/datasets-iot23)
2. Clone this repo
3. Install missing libraries
4. Open **config.py** and configure required directories

> * **iot23_scenarios_dir** should point to the home folder, where iot23 scenarios are located
> * **iot23_attacks_dir** will be used to store files for each attack type from the scenarios files
> * **iot23_data_dir** will be used to store datasets, extracted from attack files
> * **iot23_experiments_dir** will be used to store experiment files, including trained models and results

5. Run configuration check by running **run_step00_configuration_check.py**

> Make sure the output message says that you may continue to the next step. If not, then check
> your configuration and fix the errors.

## 3. (Step 1) Extract Traffic Types from Scenarios

1. Run data extraction by running **run_step01_extract_data_from_scenarios.py**

> Even though, there are multiple scenarios, files still contain mixed attack and benign traffic.
> For this reason we are going to extract the entries of a similar type into separate files.
> The output files will be stored in **iot23_attacks_dir**.

2. Run content shuffling by running **run_step01_shuffle_file_content.py**

> This step will provide more reliable data samples.

## 4. (Step 2) Run Demo

1. Run demo by running **run_demo.py**


---
[1] “Stratosphere Laboratory. A labeled dataset with malicious and benign IoT network traffic. January 22th. Agustin
Parmisano, Sebastian Garcia, Maria Jose Erquiaga. Online: https://www.stratosphereips.org/datasets-iot23
