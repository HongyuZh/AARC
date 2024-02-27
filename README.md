# AARC

AARC presents a serverless computing resource allocation framework founded on the fundamental principle of ***resource decoupling***. In this project, we'll use data and experiments to showcase the rationale behind decoupling computing and storage resources. 

## Project Overview

* **benchmark**: contains six Docker functions and the deployment script `run.sh`. 
* **utils**: contains essential Python tools employed in this project, such as Docker APK, a priority queue class, and code for generating plots.
* **profiling**: contains a discarded projection that highlights the insignificance of assigned memories in comparison to CPU cores concerning serverless function performance. Our findings indicate a strong correlation between the assigned CPU cores and the execution time of serverless functions, depicted by a well-fitting reverse proportional function.
* **scheduler**: contains the project's scheduler, featuring a DAG method for comprehensive graph operations and the capability to generate visualized graph images. This folder encompasses two distinct scheduling methods: fixed proportional scheduling and our priority scheduling.
* **placement**: contains the placement algorithm, which includes comparison groups employing both the first-fit and best-fit strategies.

## Usage

### Profiling

In the main directory, run the following command to start profiling.

```bash
python3 -m profiling -i $image_name$
```

### Scheduling

In the main directory, run the following command to start scheduling.

```python
python3 -m scheduler
```

See the data in the data sub-dir and process the data to get images. 

### Placement

In the main directory, run the following command to start placing.

```python-repl
python3 -m placement
```
