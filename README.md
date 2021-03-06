# gear-shaper-simulator
A visualization of gear profile from shaping with a straight flank cutter

# Requirements

You need this to run the simulation https://github.com/CadQuery/CQ-editor

# Notes
Start by editing the module, pressure angle, and tooth count variables.
You may need to play with the "clearance" variable to get a good profile.  
To compare to a generated profile you can export the blank to an STL file.  You must click the blank in the viewer to get the export option enabled.
My A axis is driven in mm not degrees, there is a "factor" variable that ensures the correct rotation factor.

# Sample output
![image](https://user-images.githubusercontent.com/20271/149571736-50374cd9-5b53-46e5-81c3-09f860f9f0de.png)

Video explaination: https://www.youtube.com/watch?v=mzRelz0BbCg  

Andy's Machines math for gears and gear hobber plans: https://www.youtube.com/watch?v=L1r36zN_tOI&t=295s

# install cq_gears

The "with_cq_gears.py" generates a "perfect gear" right in the cq-editor so you can compare the flanks and relief.  The rotation is a bit fiddly but it is easier than import/export to fusion 360 to compare the result.

first install conda/python

create env,took ~ 1 hour
`conda create -n py38_2 python=3.8 anaconda cadquery=master cq-editor=master ocp -c cadquery -c conda-forge`

activated it

`conda activate py38_2`

update OCP ( this may not be nessisary as the main cadquery is updated )

` conda update -n py38_2 ocp -c cadquery`

finally, install the cq_gears module.

`pip install git+https://github.com/meadiode/cq_gears.git@main`

to launch the editor in this env just run 

`cq-editor`



