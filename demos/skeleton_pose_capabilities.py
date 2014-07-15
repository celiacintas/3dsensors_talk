
# In[1]:

import openni as opi
import numpy as np
import Image
import matplotlib.pyplot as plt
import pygame
from pygame.locals import KEYDOWN, K_ESCAPE

POSE2USE = 'Psi'
name_joints = ['SKEL_HEAD', 'SKEL_LEFT_FOOT', 'SKEL_RIGHT_SHOULDER',
                       'SKEL_LEFT_HAND', 'SKEL_NECK',
                       'SKEL_RIGHT_FOOT', 'SKEL_LEFT_HIP', 'SKEL_RIGHT_HAND',
                       'SKEL_TORSO', 'SKEL_LEFT_ELBOW', 'SKEL_LEFT_KNEE',
                       'SKEL_RIGHT_HIP', 'SKEL_LEFT_SHOULDER',
                       'SKEL_RIGHT_ELBOW', 'SKEL_RIGHT_KNEE']


##### Create de Context and Generators

# In[2]:

ctx = opi.Context()
ctx.init()


# In[3]:

depth_generator = opi.DepthGenerator()
depth_generator.create(ctx)
depth_generator.set_resolution_preset(opi.RES_VGA)
depth_generator.fps = 30

image_generator = opi.ImageGenerator()
image_generator.create(ctx)

user = opi.UserGenerator()
user.create(ctx)


##### Get the skeleton and pose capabilites from the user generator

# In[4]:

skel_cap = user.skeleton_cap
pose_cap = user.pose_detection_cap


##### Create and register some callbacks

# In[5]:

def new_user(src, id):
    print "Hi User %s. Make the secret pose ..." %(id)
    pose_cap.start_detection(POSE2USE, id)

def pose_detected(src, pose, id):
    print "The User %s is doing the secret pose %s, now do the calibration" %(id, pose)
    pose_cap.stop_detection(id)
    skel_cap.request_calibration(id, True)

def calibration_complete(src, id, status):
    if status == opi.CALIBRATION_STATUS_OK:
        print "Congrats User %s! You're Calibrated" %(id)
        skel_cap.start_tracking(id)
    else:
        print "Something went wrong User %s :(" %(id)
        new_user(user, id)

def lost_user(src, id):
    print "Bye Bye User %s" %(id)


# In[6]:

user.register_user_cb(new_user, lost_user)
pose_cap.register_pose_detected_cb(pose_detected)
skel_cap.register_c_complete_cb(calibration_complete)
skel_cap.set_profile(opi.SKEL_PROFILE_ALL)


##### Now, lets get the x,y position of our joints ...

# In[7]:

def get_joints():
    for id in user.users:
        if skel_cap.is_tracking(id) and skel_cap.is_calibrated(id):
            joints = [skel_cap.get_joint_position(id, j)
                  for j in map(lambda a: getattr(opi, a), name_joints)]

            return depth_generator.to_projective([j.point for j in joints])


##### And a camera to see the output

# In[8]:

def capture_rgb():
    rgb_frame = np.fromstring(image_generator.get_raw_image_map_bgr(),
                              dtype=np.uint8).reshape(480, 640, 3)
    
    im = Image.fromarray(rgb_frame)
    b, g, r = im.split()
    im = Image.merge("RGB", (r, g, b))
    return pygame.image.frombuffer(im.tostring(), im.size, 'RGB')


##### Run sensor run

# In[9]:

ctx.start_generating_all()


# In[10]:

pygame.init()
running = True
screen = pygame.display.set_mode((640, 480), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('My First Joint View')

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE: running = False
    ctx.wait_any_update_all()
    screen.blit(capture_rgb(), (0, 0))
    newpos_skeleton = get_joints()
    if newpos_skeleton:
        map(lambda pos: pygame.draw.circle(screen, (255, 50, 0),
           (int(pos[0]), int(pos[1])), 10, 10), newpos_skeleton)
    pygame.display.update()
    pygame.display.flip()
    
pygame.display.quit()
pygame.quit()


# Out[10]:

#     Hi User 1. Make the secret pose ...
#     Bye Bye User 1
#     Hi User 1. Make the secret pose ...
#     Bye Bye User 1
#     Hi User 1. Make the secret pose ...
#     Bye Bye User 1
#     Hi User 1. Make the secret pose ...
#     Bye Bye User 1
#     Hi User 1. Make the secret pose ...
#     Hi User 2. Make the secret pose ...
#     Bye Bye User 1
#     Bye Bye User 2
#     Hi User 2. Make the secret pose ...
#     The User 2 is doing the secret pose Psi, now do the calibration
#     Congrats User 2! You're Calibrated
# 

# In[11]:

ctx.stop_generating_all()
ctx.shutdown()

