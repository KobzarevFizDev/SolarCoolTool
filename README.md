<h1 align="center">TimeDistancePlotBuilder ☀️ </h1>

# Table of Contents

- [Introduction](#introduction)
- [Installation Process](#installation-process)
- [Program Usage Example](#program-usage-example)
- [Examples of Obtained Results](#examples-of-obtained-results)

## Introduction

Currently, one of the observation objects that scientists in the field of solar physics are focused on is coronal loops. Coronal loops are one of the dominant types of magnetic structures in the solar corona, characterized by increased temperature and density relative to the surrounding plasma.

Observing the evolution of coronal loops allows us to extract information about the processes occurring within them, which is useful for solving the "Coronal Heating Problem." This problem is that the outer atmosphere of the Sun is much hotter than its surface, although temperature is expected to decrease with distance from the core. To this day, this issue remains unresolved. It turns out that observed MHD oscillations and waves in the solar atmosphere can help shed light on this question and deepen our understanding of the processes occurring in the Sun's corona.

The space-time intensity diagram (STID) helps in studying coronal loop processes. This is a type of two-dimensional graph that shows the distribution of radiation intensity along the loop over a period of time.

![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Interface.png)

This program is designed to simplify the construction of STID from FITS files available on your computer. To construct an STID, follow this algorithm:

## Installation Process

- Create a directory where the program will be installed. Place install.ps1 there. This script will download an archive with the latest program build and test images. This may take some time!

![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/change/Kobzarev/NewImagesForReadme/images/InstallDirectory.png)

- Run the script via PowerShell. This script will download the latest program build and test solar images. It will create a desktop shortcut to launch the program.

![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/change/Kobzarev/NewImagesForReadme/images/ExecuteScript.png)

- If you've done everything correctly, you'll see something like this. Don't be alarmed — the script is downloading archives with solar images and the program itself.

![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/change/Kobzarev/NewImagesForReadme/images/Downloading.png)

- When everything is downloaded, you can close the console.

![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/change/Kobzarev/NewImagesForReadme/images/Installed.png)

- The program should be launched via the shortcut or the console.

![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/change/Kobzarev/NewImagesForReadme/images/StartProgramCMD.png)

## Program Usage Example

Program loading

![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Loading.png)

Initial state of the program after loading for images in channel 131
![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Interface.png)

Initial state of the program after loading for images in channel 171
![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Interface2.png)

Selected region in the solar corona
![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Interface3.png)

Constructed STID for the selected loop
![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Interface4.png)

Constructed and formatted graph
![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Interface5.png)

Graph export window
![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Interface7.png)

Data export window (image and numpy array for further processing)
![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/Interface6.png)

Image export window
![Interface](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/ExportPopup.png)

## Examples of Obtained Results

![A94](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/A94.png)
![A131](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/A131.png)
![A171](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/A171.png)
![A193](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/A193.png)
![A211](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/A211.png)
![A304](https://github.com/KobzarevFizDev/SolarCoolTool/raw/main/images/A304.png)

## From the Author

This program was written as a thesis project and has its shortcomings. If my program was useful to you in any way, please give it a ⭐. If you find errors, please create an issue, and I will try to help you.
