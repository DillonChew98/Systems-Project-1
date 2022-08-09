# Code description
## Lane detection
1. cmd.py: testing cmd_vel 
2. path.py: original code with angles (testing)
3. path_safe.py: original code with angles, finalised speed values
4. path_with_P.py: new code with 0.5 speed
5. path_with_PD.py: new code with 0.8 speed
6. path_with_PID.py: new code with 0.2 speed
***
## Limo navigator
1. T1_to_T2_straight_path.py: Revised edition. Goes straight from T1 to T3 and back. Pretty good to use.
2. T1_to_T2_multiple_points.py: Quite alright. Only from T1 to T2 there is slight problem. Otherwise smooth. Might
                                Might have problems from weston to foodcourt. 


# Final_testing for competition
## Lane detection safe values
1. linear speed = 0.1
2. angular speed = 0.05
3. Kp = 0.003
4. Kd = 0.01
5. interested_region = [
    (0,435),
    (0,420),
    (580,420),
    (580,440)
]
