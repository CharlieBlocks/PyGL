# PyGL
A render engine similar to OpenGL that runs natively on python. Mainly targeted towards simply 3D games and visualisation of information.

To do:
    Add in texturing
    Make plain textures more userfriendly.
    Add in a CPU only renderer.

PyGL currently requires a cuda install to work. Aslong as you have a cuda enabled GPU with the cuda drivers install it should work
A requirements.txt file is present for all necessary libarys. 

Current Setup:
The module does not currently have a pip install so it is only currently usefull for demostrations.
- Download the current version of PyGL
- Place PyGL into you working directory
- Download the test file from my other repo
- Place the test file in the same diretory that PyGL is placed.
- The diretorys should look like this
-   /your_dir/PyGL
-   /your_dir/test.py
- Run the test file

When running the test file a spinning cube should appear.
Changing the line that has cube.obj on it to IcoSphere.obj will change the shape from a cube to an Ico Sphere, All shapes are included in the package.

Should you have any dificulty running the package or come across some bugs please do raise an issue.

