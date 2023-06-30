# ASUSC
## Folders
* **benchmark**: six docker functions and the deployment script `run.sh`.
* **utils**: python tools used in this project. 
* **profiling**: code used for profiling.
    * **image**: the output graph of the profiling. 
    * **data**: the output data of the profiling. 
    * **config**: the configuration file of the base memory. 
## Usage
### Profiling
In the main directory, run the following command to start profiling.
```bash
python3 -m profiling -c $image_name$
```
