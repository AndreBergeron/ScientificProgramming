# Sea Surface Temperature & NDWI Analysis
## Credit to Clark Universituy Geography Department
## Andre Bergeron 
## October 30, 2025

## Introduction
This repository contains the updated scripts and files of work done for Clark University's Advanced Geospatial Analytics with Python course. The script files contain reproducible code that can be run and manipulated using the environment file accompanied with the repository. These script help understand how to build an efficient pipeline to calculate time series of NDWI values from Sentinel-2 data. 

## Installation (Container)
To run the scripts within a running container, the user should follow the instructions below:
- Ensure docker is correctly configured on your local machine 
- Change working directory within the terminal to be within the assignment-5 repository. 
- Run the following command to build an image: 
```
git built -t assignment-5 .
```
- After building the image, run the following command to run the container: 
```
docker run -it -p 8888:8888 -v $(pwd):/home/assign5user assignment-5
```
- Once the code has finished executing in the container, open VS-code and open the extension icon within the extensions tab. There should be a container names assignment5 in green. Select it by right clicking and choosing "attach to vs-code" when the drop down menu appears. This will bring you to the correct files where you can now manipulate and reproduce the deliverables for this repository (make sure the to choose the correct kernel). 