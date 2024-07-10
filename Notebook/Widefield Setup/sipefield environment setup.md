- [ ] Add a high_framerate.cfg simulation camera for development

1. Install [[MicroManager]] from [[MicroManager#^963752|here]]
	- Note the installation path somewhere C:/Program Files/Micro-Manager-2.0
2. Install the [[Dhyana 400BSI V2]]  driver for MicroManager from [[Dhyana 400BSI V2#^65d0c1|here]]
	- Follow the Tuscan camera [[Dhyana 400BSI V2#^5c9057|user guide]] for importing the driver files into the MicroManager program file folder noted above


Installation of [[Napari]]

Initialize `conda` environment named `sipefield` with `Python 3.10`
`conda create -y -n sipefield -c conda-forge python=3.10`
`conda activate napari-env`

install napari
`conda install -c conda-forge napari pyqt`

update napari
`conda update napari`

launch napari
`napari` 

Install [[Napari#^293649|micromanager plugin]]
- On [[sipefield environment setup]] `pip install napari-micromanager`
- `mmcore install` for [[MicroManager]] adaptors