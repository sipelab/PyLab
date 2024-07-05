---
Operation: "[[=GlassNest]]"
LOG: 2024-06-11
tags:
  - widefield
author: jgronemeyer
canvas: "[[+alpha.canvas|+alpha]]"
---
*GlassNest.alpha (PyLab)*
~~Integrate Matlab and Python into a transparent workspace~~
**Build PyLab SCADA package for controlling wfield instruments**

# Tasks
- [ ] Install PyControl [[NapariComp]]

# Archive

## [[2024-06-18]]
- [x] https://www.mathworks.com/matlabcentral/answers/322709-matlab-python-how-to-push-user-input-from-matlab-gui-into-python-graphical-interface  [completion:: 2024-06-20]
*started keeping log notes within the daily note files themselves*
## [[2024-06-17]] Monday
- Matlab Code Reviewer changes to WidefieldImager.m
	- Line 49: eventdata -> ~
	- Line 86: length -> isscalar()
- Installed the MATLAB Engine API for Python in the wfield and Base conda environments succesfully
	- `python -m pip install matlabengine`
- Successfully called WidefieldImager.m script from Python Pylab but the GUI crashed instantly. Likely need to setup the engine: 
	- [x] https://www.mathworks.com/help/matlab/matlab_external/start-the-matlab-engine-for-python.html  [due:: 2024-06-18]  [completion:: 2024-06-20]
- Simulated the tandem lense with online software
## [[2024-06-14]] Friday
- Matlab2024 launches Widefield GUI but [[NI USB-6001]] not detected:
```Matlab
>> WidefieldImager
Unable to detect 'ni' hardware:
National Instruments NI-DAQmx driver is either not installed or the installed version is not supported.
Use the Windows Control Panel to uninstall any existing NI-DAQmx driver listed under 'National Instruments Software'.
Then, open the Add-On Explorer to install the Data Acquisition Toolbox Support Package for 
National Instruments NI-DAQmx Devices.

No NI devices found or data acquisition toolbox missing.
Use software triggers instead.
PCO camera not available. Searching for other cameras.
Using tucamimaq2016a64 as current video adapter
```
- Upgrading NI-DAQmx Firmware 
	- Confirmed that [[NI USB-6001]] supported in new update from [this link](https://www.ni.com/en/support/documentation/compatibility/17/devices-and-modules-no-longer-supported-in-ni-daqmx-17-6-and-lat.html)
	- Previous driver: [[NI USB-6001_deprecatedDriver.png]] for archival purposes
	- Updating a Restarting according to Matlab Plugin Suggestion after installation completed
- After restart error: [[Bug]]
```Matlab
>> WidefieldImager
Error using tabular/length (line 286)
Undefined function 'LENGTH' for input arguments of type 'table'. Use the height, width, or size functions instead.

Error in WidefieldImager>RecordMode_Callback (line 1319)
    for x = 1 : length(daqs)

Error in WidefieldImager>WidefieldImager_OpeningFcn (line 69)
handles = RecordMode_Callback(handles.RecordMode, [], handles); %check recording mode to create correct ni object

Error in gui_mainfcn (line 220)
    feval(gui_State.gui_OpeningFcn, gui_hFigure, [], guidata(gui_hFigure), varargin{:});

Error in WidefieldImager (line 43)
    gui_mainfcn(gui_State, varargin{:});
```
- Solved from line 1303
```Matlab
%daqs = daqlist;
daqs = daq.getDevices;
```
## [[2024-06-12]]
- Installed Matlab 2024 with my jgronemeyer PSU account
	- Sucessful
- Added the TuCamImaq2016a64.dll to imaqregister function according to Image Acquisition Toolbox documentation for the `imaqregister` function under the "Register Third-Part Adaptor"
	- ran into error: [[-alpha_troubleshooting]]
## [[2024-06-11]]
- Established a /dev folder for development in C:/ drive
	- /Notebook contains these Obsidian files for managing logbook
	- `PyLab` is the python dev environment for operation [[=GlassNest]]
		- [[+alpha]] and [[+tango]] represent the first two components of the project 
- Updated Anaconda to `2.6.1`

1. Cloned template dev repository into PyLab
2. Installed `Click` into virtual environment with Python 3.11 to help develop a client interface
3. Constructing MATLAB engine's Python API
	1. Required downgrading from `python=3.11` to `python=3.8` (>3.9 not supported)
		- `python conda install python=3.6`
	- [x] Upgrade Matlab version  [created:: 2024-06-11]  [scheduled:: 2024-06-12]  [completion:: 2024-06-12]
		- [ `raise InvalidVersion(f"Invalid version: '{version}'") setuptools.extern.packaging.version.InvalidVersion: Invalid version: 'R2022a`
		- Matlab root for Python API: 
			- *C:\Program Files\MATLAB\R2022a\extern\engines\python*
			- 





# Goals:

-  ~~All Matlab functions should be accessible from Python Environment~~
	-  ~~https://mscipio.github.io/post/matlab-from-python/~~
- ~~Python scripts should run Matlab functions and provide input~~
- ~~Use python to visualize output from Matlab functions~~

# Resources
https://www.mathworks.com/help/matlab/matlab_external/call-user-script-and-function-from-python.html

