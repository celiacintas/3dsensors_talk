
# In[1]:

import openni as opi
import numpy as np
import Image
import matplotlib.pyplot as plt
import pygame
from pygame.locals import KEYDOWN, K_ESCAPE
from pygame.color import THECOLORS


##### RGB Camera

# In[2]:

ctx = opi.Context()
ctx.init()


# In[3]:

image_generator = opi.ImageGenerator()
image_generator.create(ctx)


# In[4]:

ctx.start_generating_all()


# In[7]:

def capture_rgb():
    rgb_frame = np.fromstring(image_generator.get_raw_image_map_bgr(),
                              dtype=np.uint8).reshape(480, 640, 3)
    
    im = Image.fromarray(rgb_frame)
    b, g, r = im.split()
    im = Image.merge("RGB", (r, g, b))
    #im.save("/tmp/image.png")
    #return np.array(im)
    return pygame.image.frombuffer(im.tostring(), im.size, 'RGB')


# In[6]:

plt.imshow(capture_rgb())


# Out[6]:

#     <matplotlib.image.AxesImage at 0x40e4d10>

# image file:

###### Now a live cam ..

# In[8]:

pygame.init()
running = True
screen = pygame.display.set_mode((640, 480), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('My First Camera')

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE: running = False
    ctx.wait_any_update_all()
    screen.blit(capture_rgb(), (0, 0))
    pygame.display.update()
    pygame.display.flip()
    
pygame.display.quit()
pygame.quit()


# In[9]:

ctx.stop_generating_all()
ctx.shutdown()


##### Depth Camera

# In[10]:

ctx = opi.Context()
ctx.init()


# In[11]:

depth_generator = opi.DepthGenerator()
depth_generator.create(ctx)
depth_generator.set_resolution_preset(opi.RES_VGA)
depth_generator.fps = 30


# In[12]:

ctx.start_generating_all()


# In[13]:

def capture_depth():
    depth_map = np.asarray(depth_generator.get_tuple_depth_map())
    depth_map = depth_map.reshape((480, 640))
    
    return depth_map


# In[14]:

plt.imshow(capture_depth())


# Out[14]:

#     <matplotlib.image.AxesImage at 0x3f30a50>

# image file:

# In[15]:

ctx.stop_generating_all()
ctx.shutdown()


##### IR Camera

# In[16]:

ctx = opi.Context()
ctx.init()


# In[17]:

ir_generator = opi.IRGenerator()
ir_generator.create(ctx)
ir_generator.set_resolution_preset(opi.RES_VGA)
ir_generator.fps = 30
print len(ir_generator.get_tuple_ir_map())


# Out[17]:

#     307200
# 

# In[18]:

ctx.start_generating_all()


# In[19]:

def capture_IR():
    ir_map = np.asarray(ir_generator.get_tuple_ir_map())
    ir_map = ir_map.reshape((480, 640))
    
    return ir_map


# In[20]:

plt.imshow(capture_IR())


# Out[20]:

#     <matplotlib.image.AxesImage at 0x549e650>

# image file:

# In[21]:

ctx.stop_generating_all()
ctx.shutdown()


# In[ ]:



