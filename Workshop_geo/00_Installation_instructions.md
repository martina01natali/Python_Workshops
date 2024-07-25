# Installation instructions

These are installation instructions for installing the package manager miniconda on your pc and create an environment to run the jupyter notebooks for the workshop. 

## Windows users

1. Install miniconda on your pc (please rembember to choose the option to add it to the environment path variables):
	https://docs.conda.io/projects/miniconda/en/latest/

2. Open miniconda terminal (search miniconda on the windows app bar)

3. Create new environment:
```
	conda create –n geoenv
```
	Command explanation: call conda (conda) and create (create) an environment named (-n) geoenv
	
4. Activate new environment:
```
conda activate geoenv
```

5. Install following packages:
```
conda install –c conda-forge python numpy pandas matplotlib scipy pip jupyter jupyterlab ipykernel openpyxl netCDF4 xarray rasterio cartopy h5py gdal bottleneck dask cython
```

6. Now run jupyter lab:
```
jupyter lab
```
Now you can open your notebooks.


## Linux users
Everything will be installed automatically by running `setup_conda_geoenv.sh`.
1. Open the file `setup_conda_geoenv.sh` and modify the working directory `fp_cwd` to your working directory. Save it and close it.

2. Open a terminal in the working directory, ensure that `setup_conda_geoenv.sh` is executable (chmod +x setup_conda_geoenv.sh) and run it:
```
./setup_conda_geoenv.sh
```

3. At the end of the process, on the terminal, activate your environment:
```
conda activate geoenv
```
Now (geoenv) should appear at the beginning of the line.

4. Now run jupyter lab:
```
jupyter lab
```
Now you can open your notebooks.
