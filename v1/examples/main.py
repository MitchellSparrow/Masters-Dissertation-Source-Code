#!/usr/bin/env python
# Copyright (c) 2016, Universal Robots A/S,
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Universal Robots A/S nor the names of its
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL UNIVERSAL ROBOTS A/S BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from sequence_1_imports import *


# logging.basicConfig(level=logging.INFO)

#ROBOT_HOST = '192.168.86.128'
ROBOT_HOST = '10.0.1.1'
ROBOT_PORT = 30004
config_filename = 'control_loop_configuration.xml'

keep_running = True

logging.getLogger().setLevel(logging.INFO)

conf = rtde_config.ConfigFile(config_filename)
state_names, state_types = conf.get_recipe('state')
setp_names, setp_types = conf.get_recipe('setp')
setg_names, setg_types = conf.get_recipe('setg')
watchdog_names, watchdog_types = conf.get_recipe('watchdog')

con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
# con.send_pause()

# con.disconnect()
con.connect()

# get controller version
con.get_controller_version()

print(con.get_controller_version())
# setup recipes
con.send_output_setup(state_names, state_types)
setp = con.send_input_setup(setp_names, setp_types)
setg = con.send_input_setup(setg_names, setg_types)
watchdog = con.send_input_setup(watchdog_names, watchdog_types)

# Setpoints to move the robot to
# setp1 = [-0.12, -0.43, 0.14, 0, 3.11, 0.04]
# setp2 = [-0.12, -0.51, 0.21, 0, 3.11, 0.04]

#setp1 = [-0.107, -0.290, -0.48, 2.284, -0.055, -2.145]
#setp2 = [-0.280, -0.289, -0.449, 2.284, -0.055, -2.145]

setp1 = [-0.129, -0.322, -0.05, -0.022, -1.603, -0.034]
setp2 = [-0.25, -0.322, -0.05, -0.022, -1.603, -0.034]

grip_pos = [-0.25, -0.322, -0.155, -0.022, -1.603, -0.034]
above_grip_pos = [-0.25, -0.322, -0.1, -0.022, -1.603, -0.034]
home_pos = [-0.129, -0.322, -0.1, -0.022, -1.603, -0.034]
shake_1_pos = [-0.2426, -0.2607, -0.102, -0.1513, -1.6037, -0.1677]
shake_2_pos = [-0.2466, -0.3875, -0.0976, 0.1153, -1.5933, 0.1079]

setp.input_double_register_0 = 0
setp.input_double_register_1 = 0
setp.input_double_register_2 = 0
setp.input_double_register_3 = 0
setp.input_double_register_4 = 0
setp.input_double_register_5 = 0

# The function "rtde_set_watchdog" in the "rtde_control_loop.urp" creates a 1 Hz watchdog
watchdog.input_int_register_0 = 0

setg.input_int_register_1 = 0


def setp_to_list(setp):
    list = []
    for i in range(0, 6):
        list.append(setp.__dict__["input_double_register_%i" % i])
    return list


def list_to_setp(setp, list):
    for i in range(0, 6):
        setp.__dict__["input_double_register_%i" % i] = list[i]
    return setp


# start data synchronization
if not con.send_start():
    sys.exit()

print(setp_to_list(setp))


# Wait and run
def new_move(target):

    target_pose = [round(p, 4) for p in target]
    list_to_setp(setp, target_pose)
    con.send(setp)

    while True:
        # receive the current state
        state = con.receive()
        actual_pose = [round(p, 4) for p in state.target_TCP_pose]

        if state is None or actual_pose == target_pose:
            break

        con.send(watchdog)


def new_grip(target_grip):

    setg.__dict__["input_int_register_1"] = target_grip
    con.send(setg)

    while True:
        # receive the current state
        state = con.receive()
        actual_grip = state.output_int_register_1

        if state is None or actual_grip == target_grip:
            break

        con.send(watchdog)


def go_home():
    print("\tMoving to home position")
    new_move(home_pos)


def squeeze():
    print("\tMoving to above grip position")
    new_move(above_grip_pos)
    print("\tMoving to grip position")
    new_move(grip_pos)
    print("\tOpen grip")
    new_grip(1)
    print("\tClose grip")
    new_grip(0)
    print("\tOpen grip")
    new_grip(1)
    print("\tClose grip")
    new_grip(0)
    print("\tOpen grip")
    new_grip(1)
    print("\tMoving to above grip position")
    new_move(above_grip_pos)


def shake():
    print("\tMoving to above grip position")
    new_move(above_grip_pos)
    print("\tMoving to grip position")
    new_move(grip_pos)
    print("\tClose grip")
    new_grip(0)
    print("\tMoving to above grip position")
    new_move(above_grip_pos)
    print("\tMoving to shake 1 position")
    new_move(shake_1_pos)
    print("\tMoving to shake 2 position")
    new_move(shake_2_pos)
    print("\tMoving to shake 1 position")
    new_move(shake_1_pos)
    print("\tMoving to shake 2 position")
    new_move(shake_2_pos)
    print("\tMoving to above grip position")
    new_move(above_grip_pos)
    print("\tMoving to grip position")
    new_move(grip_pos)
    print("\tOpen grip")
    new_grip(1)
    print("\tMoving to above grip position")
    new_move(above_grip_pos)


try:
    while keep_running:
        # state = con.receive()
        # actual_pose = [round(p, 4) for p in state.target_TCP_pose]
        # print(actual_pose)

        print("STARTING PROGRAM")
        go_home()
        squeeze()
        shake()
        go_home()
        print("PROGRAM FINISHED")

        # print("\tMoving to home position")
        # new_move(home_pos)
        # print("\tMoving to above grip position")
        # new_move(above_grip_pos)
        # print("\tMoving to grip position")
        # new_move(grip_pos)
        # print("\tOpen grip")
        # new_grip(1)
        # print("\tClose grip")
        # new_grip(0)
        # print("\tOpen grip")
        # new_grip(1)
        # print("\tClose grip")
        # new_grip(0)
        # print("\tOpen grip")
        # new_grip(1)
        # print("\tClose grip")
        # new_grip(0)
        # print("\tMoving to above grip position")
        # new_move(above_grip_pos)
        # print("\tMoving to shake 1 position")
        # new_move(shake_1_pos)
        # print("\tMoving to shake 2 position")
        # new_move(shake_2_pos)
        # print("\tMoving to shake 1 position")
        # new_move(shake_1_pos)
        # print("\tMoving to shake 2 position")
        # new_move(shake_2_pos)
        # print("\tMoving to above grip position")
        # new_move(above_grip_pos)
        # print("\tMoving to grip position")
        # new_move(grip_pos)
        # print("\tOpen grip")
        # new_grip(1)
        # print("\tMoving to above grip position")
        # new_move(above_grip_pos)


except KeyboardInterrupt:
    pass

con.send_pause()

con.disconnect()
