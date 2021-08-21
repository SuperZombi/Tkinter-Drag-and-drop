# Tkinter-Drag-and-drop

### Install

Download from this github repo or from this sourse:

```tkdnd2.8```: https://sourceforge.net/projects/tkdnd/  <br/>
```TkinterDnD2```: https://sourceforge.net/projects/tkinterdnd/  <br/>

You can also install TkinterDnD2 from pypi: ```pip install tkinterdnd2```


1) Copy the tkdnd2.8 directory to ```...\Python\tcl```
2) Copy the TkinterDnD2 directory to ```...\Python\Lib\site-packages```<br/>
If you installed it from pypi - skip this step

<br/>

### My code usage example:


#### Drag_and_drop(```"title"```, ```"comment"```, ```"icon.ico"```, ```sorting by files and folders```)
```
files = Drag_and_drop(title="TkinterDnD Canvas", comment='Drag and drop files here:', icon=None, sort=False)
```

<br/>
I also added a function to delete the selected element when pressing the Delete key, but I did not have time to make update the coordinates of the remaining elements. If you do - I will be very grateful.
