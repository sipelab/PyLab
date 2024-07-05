## [[2024-06-12]]
- [x] Matlab error  [completion:: 2024-06-20]

Downloading https://www.ni.com/en/support/downloads/drivers/download/packaged.ni-daq-mx.532710.html because of 
	- - [ ] ![[Pasted image 20240612190851.png]]
#### code
```
Invalid or deleted object.
Please press the TAKE SNAPSHOT button. Recording will only start when at least one snapshot is taken.
Warning: An error occurred when running a class's saveobj method. The object that was saved in the
MAT-file was a copy of the object before the saveobj method was run. The rest of the variables were
also saved in the MAT-file.
The encountered error was:
Dot indexing is not supported for variables of this type.
 
> In WidefieldImager>AcquireData (line 620)
In WidefieldImager>TakeSnapshot_Callback (line 378)
In gui_mainfcn (line 95)
In WidefieldImager (line 43)
In matlab.graphics.internal.figfile.FigFile/read>@(hObject,eventdata)WidefieldImager('TakeSnapshot_Callback',hObject,eventdata,guidata(hObject)) 
Error using matlab.ui.control.WebComponent/set
Error setting property 'Enable' of class 'Panel':
Invalid enum value. Use one of these values: 'on' | 'off'.

Error in WidefieldImager>AcquireData (line 643)
    set(findall(handles.ControlPanel, '-property', 'enable'), 'enable', 'inactive')

Error in WidefieldImager>TakeSnapshot_Callback (line 378)
        AcquireData(handles.WidefieldImager); %set to acquisition mode

Error in gui_mainfcn (line 95)
        feval(varargin{:});

Error in WidefieldImager (line 43)
    gui_mainfcn(gui_State, varargin{:});

Error in matlab.graphics.internal.figfile.FigFile/read>@(hObject,eventdata)WidefieldImager('TakeSnapshot_Callback',hObject,eventdata,guidata(hObject))
 
Error while evaluating UIControl Callback.

```

