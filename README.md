# Robotarm


## Setup
- Install [Blender 2.8](https://www.blender.org/download/)
- Go to `<BLENDER_FOLDER>/2.80/python/bin`, copy the `requirements.txt` file there and execute the following:
```
./python.exe -m ensurepip
./python.exe -m pip install --upgrade pip setuptools wheel
./python.exe -m pip install --user -r requirements.txt
```
When you open this project in your IDE, make sure you set the python executable in the blender bin folder as your interpeter.
## Executing
- Open the `RobotArm model.blend` in Blender, make sure the `src` folder containing the scripts is in the same folder as the blend file!
- Go to the scripting tab at the top
- `Window` > `Toggle System Console`
- Click on `Run script` in the text editor, a menu will be shown in the System console. Blender will freeze while showing the menu, press 0 to quit.  
 If you didn't open the System console before running the script, Blender will freeze and you must force-stop it.
- You can define `option` in the script inside Blender, this will skip the input menu in the Window console and execute that option.


To run `app.py` outside Blender, comment out `import bpy` in the `blenderhelper.py` file.
