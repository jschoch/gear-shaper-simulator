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
gear_module = 1.0
tooth_count = 40
pressure_angle = 18.0
# more steps == finer but slower
steps =50
# render cuts 1 == true 0 == false
render = 1
# generate gcode boolean
gcode = 1

# number of teeth holes to cut.  2 for full tooth
render_tooth_count = 2

# for gcode generation to drive a axis
s_mm = 252.0
factor = s_mm/360

# additional depth for cut
clearance = 1.

##################################################################
# stuff you shouldn't edit

# perfect gear comparison
rotate_compare = (360/tooth_count)/1.5  
spur_gear = SpurGear(module=gear_module, teeth_number=tooth_count, width=1.0, bore_d=0.1)

#wp = cq.Workplane('XY').gear(spur_gear).rotateAboutCenter((0,0,1),rotate_compare)
wp = (
      cq.Workplane('XY')
        .transformed(offset=(0,0, 1.0), rotate=(0, 0, rotate_compare))
        .gear(spur_gear))

tooth_height = 2.4 * gear_module

if gear_module < 1.25:
    tooth_height = 2.25 * gear_module

pitch_diameter = tooth_count * gear_module
#blank_diameter = 12.995
blank_diameter = (tooth_count + 2)* gear_module
print(f'blank_diameter {blank_diameter}')
#this determines how fine the tooth is, keep small to keep fast



travel_distance_x = (pitch_diameter*.9)
old_y_pos = -(travel_distance_x/2)

y_pos = old_y_pos
step_linear = travel_distance_x / steps

step_degree = (360)/ ((pitch_diameter * math.pi )/step_linear)
print(f'Step Linear X {step_linear} Step Degree {step_degree}')




circular_pitch = math.pi * gear_module
tooth_pitch_spacing = circular_pitch/2

addendum = gear_module
dedendum = tooth_height - addendum
print(f'dedendum {dedendum} ')

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
    
    

 
y_tool_start= -(travel_distance_x/2)

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


y_feed = 5



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
    global y_feed
    global factor
    for x in range(0,steps,1):        
        
        y_pos = y_pos + step_linear;
        if(render):
            gear_tool = gear_tool.translate((0,step_linear,0))        
            gear_blank = gear_blank.rotate((0,0,0),(0,0,-1),-step_degree ).cut(gear_tool)
        if(gcode):
            print(f'G91 Y{step_linear}')
            print(f'G91 A{-step_degree * factor}')
            print(f'G91 X{y_feed}')
            y_feed = y_feed * -1
        
    #rotate back to beginning
    if(render):
        gear_blank = gear_blank.rotate((0,0,0),(0,0,-1),step_degree*steps )
    if(gcode):
        print(f'G91 Z10')
        print(f'G90 Y0X0')
        print(f'G91 Z-10')
    y_pos = old_y_pos


for tooth in range(render_tooth_count):
    cut_tooth()
    #rotate one tooth 
    if(render):
        gear_blank = gear_blank.rotate((0,0,0),(0,0,-1),(360/tooth_count))
        #move tool back to beginning
        gear_tool = gear_tool.translate((0,-(step_linear * steps),0))
        #show_object(gear_tool)
        #show_object(gear_blank)
    if(gcode):
        print(f'G91 A{(360/tooth_count)*factor}')
        #print(f'')

if(gcode):
    for x in range(10):
        print("\n")
# Displays the result of this script

#show_object(gear_blank)
