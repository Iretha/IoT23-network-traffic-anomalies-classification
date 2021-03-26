# Detection and Classification of Network Traffic Anomalies

Experiments are based on the light version of
[IoT-23](https://www.stratosphereips.org/datasets-iot23) [[1]](#footnote-1) dataset.

## 1. Prerequisites

### 1.1. Install Project Dependencies 

No  | <div style="width:100px">Name</div>| Version          | Description
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

### 1.2. Download & Extract Dataset

1. Download the lighter version of [IoT-23](https://www.stratosphereips.org/datasets-iot23) (archive size - 8.8 GB)
> The lighter version contains only labeled flows without the pcaps files 
2. Extract Archive (size - approx. 44 GB)
> 

## 2. Setup Project
1. Clone this repo
2. Install missing libraries
3. Open **config.py** and configure required directories
> * **iot23_scenarios_dir** should point to the home folder, where iot23 scenarios are located
> * **iot23_attacks_dir** will be used to store files for each attack type from the scenarios files
> * **iot23_data_dir** will be used to store files with data, extracted from attack files
> * **iot23_experiments_dir** will be used to store experiment files, including trained models and results (Excel files & Charts)
4. Check configuration by running **run_step00_configuration_check.py**
> Make sure the output message says that you may continue to the next step. If not, then check
> your configuration and fix the errors.

## 3. Prepare Data for ML
### 3.1. Extract Data From Scenarios
Run data extraction by running **run_step01_extract_data_from_scenarios.py**
> Even though, there are multiple scenarios, files still contain mixed attack and benign traffic.
> For this reason we are going to extract the entries of a similar type into separate files.
> The output files will be stored to **iot23_attacks_dir**.
>
> ⚠️ This step takes about 2h to complete.

### 3.2. Shuffle File Content
Run content shuffling by running **run_step01_shuffle_file_content.py**
> This step will provide more reliable data samples.
> Larger files are split into partitions of 1 GB. Then the content of all partitions (of the same file) gets shuffled. 
> When shuffling is ready, the partitions are merged back into a single file, that replaces the original one.
> 
> ⚠️ This step takes about 2.5 - 3h to complete.

----

# Option 1: Run Demo

#### 1.1. Prerequisites
>
> 1. [Download & Extract Dataset](#12-download--extract-dataset)
>
> 2. [Setup Project](#2-setup-project)
>
> 3. [Prepare Data for ML](#3-prepare-data-for-ml)

#### 1.2. Run demo by running **run_demo.py**

> TODO


# Option 2: Run Designed Experiments

#### 2.1. Prerequisites
>
> 1. [Download & Extract Dataset](#12-download--extract-dataset)
>
> 2. [Setup Project](#2-setup-project)
>
> 3. [Prepare Data for ML](#3-prepare-data-for-ml)

#### 2.2. Run designed experiments by running **run_experiments.py**
> ⚠️⚠️⚠️ **This step takes about 24h to complete!**
>  
> Data samples for training and testing consist of more than **20M** records.

>TODO

# Option 3: Run Custom Experiments
#### 3.1. Prerequisites
>
> 1. [Download & Extract Dataset](#12-download--extract-dataset)
>
> 2. [Setup Project](#2-setup-project)
>
> 3. [Prepare Data for ML](#3-prepare-data-for-ml)

#### 3.2. Run designed experiments by running **run_experiments.py**

>TODO


---
<a name="footnote-1">[1]</a>: “Stratosphere Laboratory. A labeled dataset with malicious and benign IoT network traffic. January 22th. Agustin
Parmisano, Sebastian Garcia, Maria Jose Erquiaga. Online: https://www.stratosphereips.org/datasets-iot23
