######################################################################################################################
#  See Readme for instructions on installing a working cq-editor and cq_gears
#
#
#
#
#####################################################################################################################

import cadquery as cq
import math
from cq_gears import SpurGear


##################################################################
#stuff you should edit
gear_module = 1
tooth_count = 20
pressure_angle = 29.0
# more steps == finer but slower
steps =14
# render cuts 1 == true 0 == false
render = 1
# generate gcode boolean
gcode = 0

# How far you want to mill in x (the width of your tooth or blank)
x_feed = 7

# number of teeth holes to cut.  2 for full tooth
render_tooth_count = 4

# for gcode generation to drive a axis

s_mm = 31.7
# factor is steps per mm / 360 to get steps per degree factor
factor = s_mm/360

# additional depth for cut
clearance = 1.

feedrate = 300

filename = "out.nc"

gcode_preamble = """
G90 G94

G17

G21

M3 S16000

G01 F{feedrate}

"""

gcode_postamble = """

m5
"""

##################################################################
# stuff you shouldn't edit

# perfect gear comparison
rotate_compare = (360/tooth_count)/1.5  
spur_gear = SpurGear(pressure_angle=pressure_angle, module=gear_module, teeth_number=tooth_count, width=1.0, bore_d=0.1)

#wp = cq.Workplane('XY').gear(spur_gear).rotateAboutCenter((0,0,1),rotate_compare)
wp = (
      cq.Workplane('XY')
        .transformed(offset=(0,0, 1.0), rotate=(0, 0, rotate_compare))
        .gear(spur_gear))

gcodes = [gcode_preamble]

tooth_height = 2.4 * gear_module

if gear_module > 1.25:
    tooth_height = 2.25 * gear_module

pitch_diameter = tooth_count * gear_module
#blank_diameter = 12.995
blank_diameter = (tooth_count + 2)* gear_module
print(f'blank_diameter {blank_diameter}')
#this determines how fine the tooth is, keep small to keep fast



#travel_distance_y = (pitch_diameter*.55)
# TODO: fix this with math
travel_distance_y = 15
old_y_pos = -(travel_distance_y/2)

y_pos = old_y_pos
step_linear = travel_distance_y / steps

print(f'pitch_diameter = {pitch_diameter} ')

step_degree = 360 / ((pitch_diameter * math.pi )/step_linear)
print(f'Step Linear X {step_linear} Step Degree {step_degree}')




circular_pitch = math.pi * gear_module
tooth_pitch_spacing = circular_pitch/2

addendum = gear_module
dedendum = tooth_height - addendum
print(f'dedendum {dedendum} tooth_height {tooth_height} ')

depth = tooth_height * clearance 

hyp = math.tan(pressure_angle * math.pi /180) 
#tool_tip_width=.15
opp = hyp * dedendum

tool_tip_width = tooth_pitch_spacing - (2*opp)
print(f'hyp {hyp} opp {opp}  tooth_pitch_spacing {tooth_pitch_spacing} ')

print(f'tool width {tool_tip_width}')

x_gear_tool_start_pos = (blank_diameter/2)- depth

#indicates angle
gear_blank = (
    cq.Workplane("front")
    .circle(blank_diameter/2)
    .extrude(1)
    .box(10,.1,2)
    )
    
    

 
y_tool_start= -(travel_distance_y/2)

gear_tool = (
            cq.Workplane("front")
            #.transformed(offset=(x_gear_tool_start_pos,old_y_pos, 0.0), rotate=(0, 0, 0))
            #-(travel_distance_x/2)
            .transformed(offset=(x_gear_tool_start_pos,y_tool_start, 0.0), rotate=(0, 0, 0))
            .vLine(tool_tip_width/2)
            #.polarLineTo(tooth_height * 2,(90 - pressure_angle))
            #.polarLineTo((tooth_height * 2), pressure_angle)
            .polarLine((tooth_height * 2),pressure_angle)
            .hLineTo(tooth_height * 2)
            .vLineTo(0.0)
            .mirrorX()
            .extrude(3)
        )






if(gcode):
    for x in range(10):
        print("\n")
        
def cut_tooth():
    global y_pos
    global gear_blank
    global old_y_pos
    global gear_tool
    global render
    global gcode
    global x_feed
    global factor
    tmp_x_feed = x_feed
    flopper = -1
    for x in range(steps):        
        
        y_pos = y_pos + step_linear;
        if(render):
            gear_tool = gear_tool.translate((0,step_linear,0))        
            gear_blank = gear_blank.rotate((0,0,0),(0,0,-1),-step_degree ).cut(gear_tool)
            print(f'rendering step {x} sl{step_linear} step_degree: {-step_degree}')
        if(gcode):
            gcodes.append(f';step {x}')
            gcodes.append(f'G91 Y{step_linear}')
            gcodes.append(f'G91 A{-step_degree * factor}')
            #TODO: use an actual helix angle, learn the math
            distance = (360/tooth_count) * factor * flopper
            gcodes.append(f'G91 X{tmp_x_feed} A{distance}')
            flopper = flopper * -1
            distance = (360/tooth_count) * factor * flopper
            gcodes.append(f'G91 X{tmp_x_feed} A{distance}')
            flopper = flopper * -1
            tmp_x_feed = tmp_x_feed * -1
        
    #rotate back to beginning
    if(render):
        gear_blank = gear_blank.rotate((0,0,0),(0,0,-1),step_degree*steps )
    if(gcode):
        
        gcodes.append(f'G91 Z10')
        gcodes.append(f'G90 Y0X0')
        gcodes.append(f'G91 Z-10')
    y_pos = old_y_pos


for tooth in range(render_tooth_count):
    cut_tooth()
    if(render):
        gear_blank = gear_blank.rotate((0,0,0),(0,0,-1),(360/tooth_count))
        #move tool back to beginning
        gear_tool = gear_tool.translate((0,-(step_linear * steps),0))
        
    if(gcode):
        #  move a axis back to initial position
        gcodes.append(f';tooth {tooth}')
        # go to beginning
        gcodes.append(f'G91 A{step_degree * steps*factor}')
        # advance on tooth
        gcodes.append(f'g91 A{(360/tooth_count) * factor}')
        #print(f'')

if(gcode):
    print('writing file')
    text_file = open(filename, "w")
    out = '\n'.join(gcodes)
    out += gcode_postamble
    n = text_file.write(out)
    text_file.close()
    #print('\n'.join(gcodes))
    for x in range(3):
        print("\n")
# Displays the result of this script

print('done')
#show_object(gear_blank)
