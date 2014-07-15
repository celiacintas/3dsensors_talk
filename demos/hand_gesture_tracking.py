
# In[ ]:

import openni as opi
import numpy as np
import pygame
from pygame.locals import KEYDOWN, K_ESCAPE
from pygame.color import THECOLORS
import Image
from random import randrange


##### Create context and generators

# In[66]:

ctx = opi.Context()
ctx.init()


# In[67]:

depth_generator = opi.DepthGenerator()
depth_generator.create(ctx)
depth_generator.set_resolution_preset(opi.RES_VGA)
depth_generator.fps = 30

image_generator = opi.ImageGenerator()
image_generator.create(ctx)

gesture_generator = opi.GestureGenerator()
gesture_generator.create(ctx)
gesture_generator.add_gesture('Wave')

hands_generator = opi.HandsGenerator()
hands_generator.create(ctx)


##### Write some callbalks ...

# In[68]:

def gesture_detected(src, gesture, id, end_point):
    hands_generator.start_tracking(end_point)

def gesture_progress(src, gesture, point, progress): 
    print "Dave is waving !!", src

def destroy(src, id, time):
    sprites.remove(hands[id])
    del hands[id]

def create(src, id, pos, time):
    try:
        hands[id] = Hand(file_names[randrange(len(file_names))])
        sprites.add(hands[id])
    except KeyError:
        print 
    
        
def update(src, id, pos, time):
    if pos:
        tmp_pos = depth_generator.to_projective([pos])[0]
        hands[id].rect.centerx, hands[id].rect.centery = tmp_pos[0], tmp_pos[1] 


##### And register them ...

# In[69]:

gesture_generator.register_gesture_cb(gesture_detected, gesture_progress)
hands_generator.register_hand_cb(create, update, destroy)


# Out[69]:

#     <void* at 0x7f7c4168df90>

##### Some things for this particular demo ...

# In[70]:

hands = {}
file_names = ['Images/mano_1.png', 'Images/mano_2.png', 'Images/mano_3.png']


# In[71]:

class Hand(pygame.sprite.Sprite):
    """Hand Class for set image, speed and angle """
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.img_load(image)
        
    def img_load(self, filename):
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (60,60))  
        self.rect = self.image.get_rect()


##### To display the camera ...

# In[72]:

def capture_rgb():
    rgb_frame = np.fromstring(image_generator.get_raw_image_map_bgr(),
                              dtype=np.uint8).reshape(480, 640, 3)
    
    im = Image.fromarray(rgb_frame)
    b, g, r = im.split()
    im = Image.merge("RGB", (r, g, b))
    #im.save("/tmp/image.png")
    #return np.array(im)
    return pygame.image.frombuffer(im.tostring(), im.size, 'RGB')


#### The main loop ...

# In[73]:

pygame.init()
running = True
screen = pygame.display.set_mode((640, 480), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('My First Hand Tracking')
sprites = pygame.sprite.RenderUpdates()
ctx.start_generating_all()

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE: running = False
    ctx.wait_any_update_all()
    
    screen.blit(capture_rgb(), (0, 0))
    map(lambda i: i.update(), hands.values())
    dirty = sprites.draw(screen)
    pygame.display.update(dirty)
    pygame.display.flip()
    
pygame.display.quit()
pygame.quit()


# Out[73]:

#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
#     Dave is waving !! <openni.GestureGenerator object at 0x3a91488>
# 

##### Then we stop and close the context

# In[74]:

ctx.stop_generating_all()
ctx.shutdown()

