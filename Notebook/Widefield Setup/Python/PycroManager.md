`pip install pycromanager`

[github](https://github.com/micro-manager/pycro-manager?tab=readme-ov-file)

[Acquisition Hooks](https://pycro-manager.readthedocs.io/en/latest/acq_hooks.html#acq-hooks)

How to use [[PycroManager]] to acquire 10 frames through [[MicroManager]]:
1. Initialize devices from config file: 
```python
	from pycromanager import Acquisition, multi_d_acquisition_events, Core

	# Initialize the micromanager Core for access to the API core functions
    core = Core()
    # Load the micromanager .cfg config file
    core.load_system_configuration('path/to/.cfg') 
    
    with Acquisition(directory='path/to/save/dir') as acq:
        events = multi_d_acquisition_events(num_time_points=10)
        acq.acquire(events)
   
```