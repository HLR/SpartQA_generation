import random
import numpy as np


def scene_obj_relation(story, scene, obj):
    
    
    y_loc = story['structured_rep'][scene][obj]['y_loc']
    x_loc = story['structured_rep'][scene][obj]['x_loc']
    size = story['structured_rep'][scene][obj]['size']
    
    rels = []
    
    T_B = random.choice([0,1])#Use top and bottom
    Touching = random.choice([1,1,1])# TPP??
    
    repeat = 1        
    if Touching: #TPP
        if y_loc == 0:
            rels.append('touching the top edge of') 
            #repeat = 0
        elif y_loc+size == 100:
            rels.append('touching the bottom edge of')
            #repeat = 0
        
        if x_loc == 0:
            rels.append('touching the left edge of')
        elif x_loc+size == 100:
            rels.append('touching the right edge of ')
            
    #adding top and bottom relation between object and scene      
    #if T_B and repeat:
    #    if 100 - y_loc > 70:
    #        rels.append('at the top of')
    #    elif 100 - y_loc < 30:
    #        rels.append('at the bottom of')
            
            
    return rels
        

def obj_obj_relation(scene, fst, sec, limitation):
    
    objs_rels = []
    obj1 = scene[fst][1]
    obj2 = scene[sec][1]
    
    x_1st = obj1['x_loc']
    y_1st = obj1['y_loc']
    size_1st = obj1['size']
    x_2nd = obj2['x_loc']
    y_2nd = obj2['y_loc']
    size_2nd = obj2['size']
    
    #set limitation
    forbid_rel= []
    for x in limitation:
        if x[0][0] == sec and x[0][1] == fst:
            for r in x[1]:
                forbid_rel.append(forbid(r))

    
    x = 2#random.choice([0,1,2])
    if x == 0: dir_choose, dis_choose = 1, 0 # if choose direction in relations or not
    elif x == 1: dir_choose, dis_choose = 0, 1 # if choose distant in relations or not
    else: dir_choose, dis_choose = 1, 1 # both of them
        
    if dir_choose:
        
        dir_type = 2 #random.choice([0,0,1,1,2])
        
        if dir_type == 0: #just left or right
            
            if x_1st - x_2nd < 0 and (x_1st+size_1st) - (x_2nd+size_2nd) < -10 and 'left' not in forbid_rel:
                objs_rels.append('left')
                
            elif x_1st - x_2nd > 0 and (x_1st+size_1st) - (x_2nd+size_2nd) > 10 and 'right' not in forbid_rel:
                objs_rels.append('right')
                
        elif dir_type == 1: #just below or above
            
            if y_1st - y_2nd < 0 and (y_1st+size_1st) - (y_2nd+size_2nd) < -10 and 'above' not in forbid_rel:
                objs_rels.append('above')
                
            elif y_1st - y_2nd > 0 and (y_1st+size_1st) - (y_2nd+size_2nd) > 10 and 'below' not in forbid_rel:
                objs_rels.append('below')
                
        elif dir_type == 2: #both of them
            
            if x_1st - x_2nd < 0 and (x_1st+size_1st) - (x_2nd+size_2nd) < -10 and 'left' not in forbid_rel:
                objs_rels.append('left')
                
            elif x_1st - x_2nd > 0 and (x_1st+size_1st) - (x_2nd+size_2nd) > 10 and 'right' not in forbid_rel:
                objs_rels.append('right')
                
            if y_1st - y_2nd < 0 and (y_1st+size_1st) - (y_2nd+size_2nd) < -10 and 'above' not in forbid_rel:
                objs_rels.append('above')
                
            elif y_1st - y_2nd > 0 and (y_1st+size_1st) - (y_2nd+size_2nd) > 10 and 'below' not in forbid_rel:
                objs_rels.append('below')
        
    if dis_choose:

        if (y_1st+size_1st == y_2nd) or (y_2nd+size_2nd == y_1st) or (x_1st+size_1st == x_2nd) or (x_2nd+size_2nd == x_1st):
            if 'touching' not in forbid_rel:
                objs_rels.append('touching')


        up_treshhold, down_treshhold = 70, 20
        if 'near to' not in forbid_rel :
                
            if  ((np.absolute((y_1st+size_1st) - y_2nd) < down_treshhold) or (np.absolute(y_1st - (y_2nd++size_2nd)) < down_treshhold)) and ((np.absolute((x_1st+size_1st) - x_2nd) < down_treshhold) or (np.absolute(x_1st - (x_2nd++size_2nd)) < down_treshhold)):
                objs_rels.append('near to')

                
        if 'far from' not in forbid_rel:

            if ((np.absolute((y_1st+size_1st) - y_2nd) > up_treshhold) or (np.absolute(y_1st - (y_2nd++size_2nd)) > up_treshhold)) and ((np.absolute((x_1st+size_1st) - x_2nd) > up_treshhold) or (np.absolute(x_1st - (x_2nd++size_2nd)) > up_treshhold)):
                objs_rels.append('far from')

    return objs_rels
            
    
    
def forbid(word):
    
    words={'left':'right', 'right':'left', 'above':'below', 'below':'above', 'touching':'touching', 'far from':'far from','near to':'near to'}
    
    return words[word]