#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import openni
import zmq
import json

class Kinect:
    """Manage context and generator of the kinect"""
    def __init__(self, dir_pub):

        self.ctx_zmq = zmq.Context()
        self.socket = self.ctx_zmq.socket(zmq.PUB)
        self.socket.bind(dir_pub)

        self.context = openni.Context()
        self.context.init()
        self.depth_generator = openni.DepthGenerator()
        self.depth_generator.create(self.context)
        self.depth_generator.set_resolution_preset(openni.RES_VGA)
        self.depth_generator.fps = 30

        self.gesture_generator = openni.GestureGenerator()
        self.gesture_generator.create(self.context)
        self.gesture_generator.add_gesture('Wave')
        
        self.hands_generator = openni.HandsGenerator()
        self.hands_generator.create(self.context)

        self.gesture_generator.register_gesture_cb(self.gesture_detected, self.gesture_progress)
        self.hands_generator.register_hand_cb(self.create, self.update, self.destroy)
        self.context.start_generating_all()

 	def update_frame(self):
 		self.context.wait_any_update_all()

    def gesture_progress(self, src, gesture, point, progress): 
        print "Dave is waving !!", src

    def destroy(self, src, id, time):
        data = {'type':'remove_hand', 'id': id}
        message = json.dumps(data)
        self.socket.send(message)

    def create(self, src, id, pos, time):
        try:
            #tmp_pos = self.depth_generator.to_projective([pos])[0]
            data = {'type':'create_hand', 'id': id, 'hand_x': pos[0], 
                    'hand_y': pos[1], 'hand_z': pos[2]}
        except NoneType:
            print "There is no pos yet"
        else:
            message = json.dumps(data)
            self.socket.send(message)

    def update(self, src, id, pos, time):
        try:
            #tmp_pos = self.depth_generator.to_projective([pos])[0]
            data = {'type':'update_pos', 'id': id, 'hand_x': pos[0], 
                    'hand_y': pos[1], 'hand_z': pos[2]}
        except NoneType:
            print "There is no pos yet"
        else:
            message = json.dumps(data)
            self.socket.send(message)

    def gesture_detected(self, src, gesture, id, end_point):
        print "Detected gesture:", gesture
        self.hands_generator.start_tracking(end_point)

    def kinect_loop(self):
        while 1:
            self.context.wait_any_update_all()

