import json
import random
import re
from Random_choice import random_choice


_final_story = ''
annotation = {"story": '', "annotations": []}
temp_annot_sent, traj, land, sp_ind, block_temp, sen_temp = '', [], [], [], [], ''
land_obj_id, traj_obj_id = [], []
scn_rels, scn_objs, objs_rels = [],[],[]
temp_checked_obj_sc, checked_obj_sc, checked_obj_obj, finished_objs = [], [], [], []
objs_attrs_f, objs_objs_f = [],[]
object_shared_prop, shared_prop = [], []
recent_objs = []
treshhold = 0
cannot_has_which = 0
no_with = 0
clr, sz, sh, sc_rl = '','','',''
End_of_block = 0
factor = 0.5
max_treshhold_for_rels = 4
_num_scenes = 0  #number of scenes
scene_num = None # the scene number 
entity_phrases = {}


def creating_story(story, f):
    
    global scn_rels, scn_objs, objs_rels, _num_scenes, _final_story, objs_attrs_f, objs_objs_f,checked_obj_sc, checked_obj_obj, finished_objs,object_shared_prop, shared_prop, recent_objs, treshhold,cannot_has_which, clr, sz, sh, sc_rl,End_of_block, annotation
    
    _final_story, objs_attrs_f, objs_objs_f = '', [], []
    annotation = {"story": '', "annotations": []}
    temp_annot_sent, traj, land, sp_ind, block_temp, sen_temp = '', [], [], [], [], ''
    
    checked_obj_sc, checked_obj_obj, finished_objs = [], [], []
    objs_attrs_f, objs_objs_f = [],[]
    object_shared_prop, shared_prop = [], []
    recent_objs = []
    treshhold = 0
    cannot_has_which = 0
    clr, sz, sh, sc_rl = '','','',''
    End_of_block = 0
    _num_scenes = 0 
    
    x = 1
    while x:
        try : 
            _temp = random_choice(story)
            if _temp == -1: return -1
            elif _temp == []: continue 
            else: scn_rels, scn_objs, objs_rels = _temp
            
            if scn_objs != []:
                x=0
        except: 
            raise
            return -1
        
    _num_scenes = len(scn_rels)+1 #number of scenes


    _final_story = B(_num_scenes)
    
    
    # reshape the text
    _final_story = edit_text_form(_final_story)

    SOT(_final_story)
    
#     print('##', objs_attrs_f, objs_objs_f)
#     print('final story\n', _final_story)
    return [_final_story, scn_rels, objs_attrs_f, objs_objs_f, annotation, _num_scenes]



#**********************************************************
#*************Start describing functions*******************
#**********************************************************


def B(N_S):
    sentence, annotation = '', ''
    
    global scene_num, land, block_temp, sen_temp, land_obj_id
    scene_num = 0
    if N_S == 1:
        x =  random.choice([0,1]) # 0 for not having starter sentences (we call it B) which describe blocks and 1 for B != NULL    
        if x:
            y = random.choice([0,1]) 
            temp = s_num()+' block'
            block_temp = [[temp]]
            sen_temp = 'There is '+temp if y else 'We have '+temp
            sentence = 'There is '+temp+ B0(0) if y else 'We have '+temp+ B0(0)
            
        else:
            y = random.choice([0,1])
            sentence = 'There '+ obj_rel_scene(scn_objs[0],0,'a block',True) if y else start_word(obj_rel_scene(scn_objs[0],1, 'a block'))
            land = [['a block']]
            land_obj_id = [[100]]
            create_annotation(sentence)
        sentence += P(scn_objs[0])    
    else:
        
        x =  1#random.choice([0,1]) # 0 for not having starter sentences (we call it B) which describe blocks and 1 for B != NULL
        
        if x:
            y = random.choice([0,1])
            sentence = 'There are '+num_to_word(str(N_S))+' blocks'+name_block_all(N_S)+ D(N_S) if y else 'We have '+num_to_word(str(N_S))+' blocks'+name_block_all(N_S)+ D(N_S)
        else: # B == Null so D is also == Null -> So we should describe relation between blocks at the start sentence of paragraph of block description
            sentence = B0D0(N_S)
    
    return sentence


def B0(num):

    global cannot_has_which, no_with, traj, sp_ind, land, land_obj_id, traj_obj_id, block_temp, sen_temp
    _sen = ''
    sen,x  = '', None
    x = 0 if cannot_has_which or no_with else random.choice([0,1,2]) 
    if x == 0: # it has|contains
        if sen_temp and land and traj and sp_ind: create_annotation(sen_temp)
        y = random.choice([0,1])
        sen += 'It has '+obj_rel_scene(scn_objs[num],2,'it') if y else 'It contains '+obj_rel_scene(scn_objs[num],2,'it')
        traj += [['it']]
        traj_obj_id += [[100+num]]
        sp_ind += [['has']] if y else [['contains']]
        _sen = sen
        sen = '. '+sen
    elif x == 1:  # with
        
        sen += ' with '+obj_rel_scene(scn_objs[num],0,'it')
        land += [['it']]
        land_obj_id +=[[100+num]]
        _sen = sen_temp + sen
        sen_temp = ''
        
    else: # which
        
        y = random.choice([0,1])
        sen += ' which has '+obj_rel_scene(scn_objs[num],2,'it') if y else ' which contains '+obj_rel_scene(scn_objs[num],2,'it') 
        sp_ind += [['has']] if y else [['contains']]
        traj += block_temp
        traj_obj_id += [[100+num]]
        block_temp = []
        _sen = sen_temp + sen
        
    sen_temp = ''
        
    cannot_has_which =0
    no_with = 0
    
    create_annotation(_sen)
    return sen

def B0D0(num):

    sen = ''
    sen += '\n'+B0D01()+P(scn_objs[scene_num]) + '\n'+B0D02(1)+B0(1)+P(scn_objs[scene_num]) if num == 2 else '\n'+B0D01()+P(scn_objs[scene_num]) + '\n'+B0D02(0)+B0(1)+P(scn_objs[scene_num]) + '\n'+B0D03()+B0(2)+P(scn_objs[scene_num])
    return sen
        
def B0D01():
    sen, _sen, sen1 ='', '', ''
    global scene_num, recent_objs, no_with, land, land_obj_id
    scene_num = 0
    x =  random.choice([0,1])

    if x: 
        sen1 = 'There is '+s_num()+' block '+name_call()+' A.' if random.choice([0,1])  else 'We have '+s_num()+' block '+name_call()+' A.'
        sen += ' There '+ obj_rel_scene(scn_objs[0],0,'this block',True)
        _sen = sen
        sen = sen1 + sen
        land, land_obj_id = [['this block']], [[100]]
        
    else:
        y = random.choice([0,1])
        sen = 'There '+ obj_rel_scene(scn_objs[0],0,'a block',True) if y else start_word(obj_rel_scene(scn_objs[0],1,'a block'))
        land, land_obj_id = [['a block']], [[100]]
        recent_objs = []
        _sen = sen
        sen += '. '+start_word(name_block_single('A'))
        no_with = 1
    
    create_annotation(_sen)
    return sen

def B0D02(s_num): # 0 -> 2 scenes, 1 -> 3 scenes
    sen = ''
    global scene_num, no_with, sen_temp, block_temp
    scene_num = 1
    if s_num: # 2 scenes
        sen += B0D021(scn_rels[0])
    else:
        if 0 in scn_rels[0][0] and 1 in scn_rels[0][0]:
            sen += B0D021(scn_rels[0])
        elif 0 in scn_rels[1][0] and 1 in scn_rels[1][0]:
            sen += B0D021(scn_rels[1])
        else:
            sen += 'There is another block '
            _sen1 = start_word(name_block_single('B',True))
            _sen2 = name_call()+' B '
            if random.choice([0,1]): sen += _sen2; sen_temp = sen; block_temp = [['another block '+_sen2]]   
            else: sen += '. '+_sen1; no_with = 1; sen_temp = _sen1; block_temp = [['B']]
    return sen
        
def B0D021(x):

    global cannot_has_which, no_with
    global traj, land, sp_ind, block_temp, sen_temp, land_obj_id, traj_obj_id
    _sen, _sen1, sen = '', '', ''
    if x[0][0] == 1: # the relation is about position of scene two to one
        _block = 'another block '+ name_call() +' B'
        sen += 'There is ' + _block+' '
        sen += R(x[1])+ ' block A '
        traj, land, sp_ind, block_temp = [[_block]], [['block A']], [[x[1]]], [[_block]]
        traj_obj_id, land_obj_id = [[101]], [[100]]
        #_sen = sen
        sen_temp = sen
        cannot_has_which = 1
        
    elif x[0][1] == 1: # the relation is about the position of scene one to two
        sen += start_word(R(reverse(x[1])))+ ' block A' # did not consider just say A instead of block A
        y = random.choice([0,1])
        _block = 'another '+one_blk()
        if y == 0:
            sen += ' there is '+_block+' '
        elif y == 1:
            sen += ' we have '+_block+' ' 
#         else:
#             sen += ' another block exists '
        _sen = sen
        _sen1 = start_word(name_block_single('B' , True))
        sen += '. '+ _sen1
        no_with = 1
        traj, land, sp_ind, block_temp= [[_block]], [['block A']], [[reverse(x[1])]], [['B']]
        traj_obj_id, land_obj_id = [[101]], [[100]]
        create_annotation(_sen)
        sen_temp = _sen1
        
    return sen

def B0D03():
    
    sen,sen1,sen2,sen3, _sen = '','','', '', ''
    global scene_num, cannot_has_which, no_with
    global traj, land, sp_ind, block_temp, sen_temp, traj_obj_id, land_obj_id
    
    scene_num = 2
    if 2 in scn_rels[0][0] and 2 in scn_rels[1][0]:
        sen1 += '' if random.choice([0,1]) else ' also'
        if scn_rels[0][0][0] == 2 and scn_rels[1][0][0] == 2:

            sen3 += 'There is'+sen1
            _block = 'another block '+name_call()+ ' C'
            sen3 += ' '+ _block
            y = random.choice([0,1,2])
            if y == 0: sen+= 'It is'; traj = [['it'],['it']]
            elif y==1: sen+= ' which is'; traj = [[_block],[_block]]
            else: traj = [[_block],[_block]]
            traj_obj_id = [[102],[102]]
            sen+= ' '+R(scn_rels[0][1])+' '
            sen2 += ' both ' if random.choice([0,1]) else ' '
            if scn_rels[0][1] == scn_rels[1][1]: 
                sen += sen2+'blocks ' +name_block(scn_rels[0][0][1])+' and '+name_block(scn_rels[1][0][1])
                sp_ind = [[scn_rels[0][1]],[scn_rels[0][1]]]
                land = [[name_block(scn_rels[0][0][1])],[name_block(scn_rels[1][0][1])]]
                
            else : 

                sen+= ' block '+name_block(scn_rels[0][0][1])+' and '+R(scn_rels[1][1])+' block '+name_block(scn_rels[1][0][1])
                sp_ind =[[scn_rels[0][1]],[scn_rels[1][1]]]
                land = [['block '+name_block(scn_rels[0][0][1])],['block '+name_block(scn_rels[1][0][1])]]
                
            land_obj_id = [[100+scn_rels[0][0][1]],[100+scn_rels[1][0][1]]]
            
            if y == 0 : _sen = sen; sen = sen3+'. ' + sen
            else: sen = sen3 + sen; _sen = sen 
            #create_annotation(_sen)
            sen_temp = _sen
            cannot_has_which = 1
        
        elif scn_rels[0][0][0] == 2 and scn_rels[1][0][1] == 2:

            sen3 += 'There is'+sen1
            _block = 'another block '+name_call()+ ' C'
            sen3 += ' '+ _block
            y = random.choice([0,1,2])
            if y == 0: sen+= 'It is '; traj = [['it']]
            elif y==1: sen+= ' which is '; traj = [[_block]]
            else: traj = [[_block]]
            traj_obj_id = [[102]]
            sen+= ' '+R(scn_rels[0][1])+' block '+name_block(scn_rels[0][0][1])
            sp_ind, land, land_obj_id = [[scn_rels[0][1]]], [['block '+name_block(scn_rels[0][0][1])]], [[100+scn_rels[0][0][1]]]
         
            z = random.choice([0,1])
            sen2= name_block(scn_rels[1][0][0])+' is '+R(scn_rels[1][1])+' it'
            if z : # one sentence finished and another starts
                if y == 0: _sen = sen; sen = sen3+'. ' + sen
                else: sen = sen3 + sen; _sen = sen
                create_annotation(_sen)
                _sen = 'Block '+ sen2
                sen += '. Block '+ sen2
                
            else:
                if y == 0: _sen = sen; sen = sen3+'. ' + sen
                else: sen = sen3 + sen; _sen = sen
                _sen += ' and block '+ sen2
                sen += ' and block '+ sen2
            
            land += [['it']]
            land_obj_id += [[102]]
            sp_ind += [[scn_rels[1][1]]]
            traj += [['block '+ name_block(scn_rels[1][0][0])]]
            traj_obj_id += [[100+scn_rels[1][0][0]]]
            #create_annotation(_sen)
            sen_temp = _sen
            cannot_has_which = 1
        
        elif scn_rels[0][0][1] ==2 and scn_rels[1][0][0] == 2:
            
            sen3 += start_word(R(reverse(scn_rels[0][1])))+' block '+name_block(scn_rels[0][0][0])+' there is'+sen1
            sp_ind, traj, land = [[reverse(scn_rels[0][1])]], [['another block']], [['block '+name_block(scn_rels[0][0][0])]]
            traj_obj_id, land_obj_id = [[102]], [[100+scn_rels[0][0][0]]]
            sen3 += ' another block '
            y = random.choice([0,1])
            if y == 0: create_annotation(sen3)
            sen+= ' which is ' if y else 'It is '
            traj += [['block']] if y else [['it']]
            traj_obj_id += [[102]]
            sen+= R(scn_rels[1][1])+' block '+name_block(scn_rels[1][0][1])+'. '
            sp_ind += [[scn_rels[1][1]]]
            land += [['block '+name_block(scn_rels[1][0][1])]]
            land_obj_id += [[100+scn_rels[1][0][1]]]
            if y: sen = sen3+ sen; _sen = sen
            else: _sen = sen; sen = sen3+'. '+ sen
            create_annotation(_sen)
            sen += start_word(name_block_single('C '))
            no_with = 1
            cannot_has_which = 1
            
        elif scn_rels[0][0][1] ==2 and scn_rels[1][0][1] ==2:

            sen2 += 'both ' if random.choice([0,1]) else ' '
            if scn_rels[0][1] == scn_rels[1][1]: 

                sen += start_word(R(reverse(scn_rels[0][1])))+' '+sen2+' blocks '+name_block(scn_rels[0][0][0])+' and '+name_block(scn_rels[1][0][0])
                sp_ind = [[reverse(scn_rels[0][1])],[reverse(scn_rels[0][1])]]
                land = [[name_block(scn_rels[0][0][0])],[name_block(scn_rels[1][0][0])]]
                
            else: 

                sen+= start_word(R(reverse(scn_rels[0][1])))+' block '+name_block(scn_rels[0][0][0])+' and '+R(reverse(scn_rels[1][1]))+' block ' + name_block(scn_rels[1][0][0])
                sp_ind = [[reverse(scn_rels[0][1])],[reverse(scn_rels[1][1])]]
                land = [['block '+name_block(scn_rels[0][0][0])], ['block ' + name_block(scn_rels[1][0][0])]]
            
            land_obj_id = [[100+scn_rels[0][0][0]],[100+scn_rels[1][0][0]]]
            
            sen+= ' there is'+sen1
            _sen1 = start_word(name_block_single('C '))
            _sen = sen + ' another block '+'. '
            sen += ' another block '+'. '+ _sen1
            traj, block_temp = [['another block'],['another block']], [['C']]
            traj_obj_id = [[102],[102]]
            sen_temp = _sen1
            create_annotation(_sen)
            no_with = 1
            
    else:
        if 2 in scn_rels[0][0]:
            sen1 += '' if random.choice([0,1]) else ' also'
            if scn_rels[0][0][0] == 2:
                sen3 += 'There is'+sen1
                _block='another block ' +name_call()+ ' C'
                sen3 += ' '+_block
                y = random.choice([0,1,2])
                if y == 0: sen+= 'It is'; traj = [['it']]
                elif y==1: sen+= ' which is'; traj = [[_block]]
                else: traj = [[_block]]
                traj_obj_id = [[102]]
                sen+= ' '+R(scn_rels[0][1])+' block '+name_block(scn_rels[0][0][1])
                land, sp_ind = [['block '+name_block(scn_rels[0][0][1])]], [[scn_rels[0][1]]]
                land_obj_id = [[100+scn_rels[0][0][1]]]
                if y == 0: _sen = sen; sen = sen3+'. ' + sen
                else: sen = sen3 + sen; _sen = sen
                #create_annotation(_sen)
                sen_temp = _sen
                cannot_has_which = 1
            else:
                sen += start_word(R(reverse(scn_rels[0][1])))+' block '+name_block(scn_rels[0][0][0])+' there is'+sen1
                _block = 'another block ' +name_call()+ ' C'
                sen += ' '+ _block
                traj, land, sp_ind= [[_block]], [['block '+name_block(scn_rels[0][0][0])]], [[reverse(scn_rels[0][1])]]
                traj_obj_id, land_obj_id = [[102]], [[100+scn_rels[0][0][0]]]
                block_temp, sen_temp = [[_block]], sen
                #create_annotation(sen)
                sen_temp = sen
                
        elif 2 in scn_rels[1][0]:
            sen1 += '' if random.choice([0,1]) else ' also'
            if scn_rels[1][0][0] == 2:
                sen3 += 'There is'+sen1
                _block = 'another block '+name_call()+ ' C'
                sen3 += ' '+ _block
                y = random.choice([0,1,2])
                if y == 0: sen+= 'It is'; traj = [['it']]
                elif y==1: sen+= ' which is'; traj = [[_block]]
                else: traj = [[_block]]
                traj_obj_id = [[102]]
                sen+= ' '+R(scn_rels[1][1])+' block '+name_block(scn_rels[1][0][1])
                land, sp_ind = [['block '+name_block(scn_rels[1][0][1])]], [[scn_rels[1][1]]]
                land_obj_id = [[100+scn_rels[1][0][1]]]
                if y == 0: _sen = sen; sen = sen3+'. '+ sen
                else: sen = sen3+ sen; _sen = sen
                #create_annotation(_sen)
                sen_temp = _sen
                cannot_has_which = 1
                
            else:
                sen += start_word(R(reverse(scn_rels[1][1])))+' block '+name_block(scn_rels[1][0][0])+' there is'+sen1+' another block '+'. '
                _sen = sen
                sen3 = start_word(name_block_single('C ',True))
                sen += sen3
                
                traj, land, sp_ind= [['another block']], [['block '+name_block(scn_rels[1][0][0])]], [[reverse(scn_rels[1][1])]]
                traj_obj_id, land_obj_id = [[102]], [[100+scn_rels[1][0][0]]]
                block_temp, sen_temp = [['C']], sen3
                #create_annotation(_sen)
                sen_temp = _sen
                no_with = 1
    
    return sen

def D(num): # D is a description about positions of block to each other

    global traj, sp_ind, land, land_obj_id, traj_obj_id
    sen, sen3 ='', ''
    x = random.choice([0,1]) # D == NUll if x =0 so the relation between blocks should described at the first paragraph 
    if x: # D != Null and B!=Null
        if num == 2: # check the index of scn_rels

            sen += " Block A is "
            sen += R(scn_rels[0][1]) if scn_rels[0][0][0] == 0 else R(reverse(scn_rels[0][1]))
            sen += " B."
            traj, land = [['block A']], [['B']]
            traj_obj_id, land_obj_id = [[100]], [[101]]
            sp_ind = [[scn_rels[0][1]]] if scn_rels[0][0][0] == 0 else [[reverse(scn_rels[0][1])]]
            create_annotation(sen)
            # Adding description about objects
            sen+= '\n'+BD(1)+P(scn_objs[scene_num])+'\n'+BD(2)+P(scn_objs[scene_num])
            
        else: #having three blocks
            
            if scn_rels[0][0][0] == scn_rels[1][0][0]: # [[0,1], 'left'][[0,2], 'something']

                if scn_rels[0][1] == scn_rels[1][1]:

                    sen += ' Block '+name_block(scn_rels[0][0][0])+' is '+R(scn_rels[0][1])+' blocks '+name_block(scn_rels[0][0][1]) +' and '+name_block(scn_rels[1][0][1]) +'.'
                    traj, land, sp_ind = [['block '+name_block(scn_rels[0][0][0])]], [[name_block(scn_rels[0][0][1]), name_block(scn_rels[1][0][1])]], [[scn_rels[0][1]]]
                    traj_obj_id, land_obj_id = [[100+scn_rels[0][0][0]]], [[100+scn_rels[0][0][1],100+scn_rels[1][0][1]]]
                    create_annotation(sen)
                    
                else:

                    y= random.choice([0,1,1,1])
                    if y: 
                        sen += ' Block '+name_block(scn_rels[0][0][0]) + ' is '+R(scn_rels[0][1])+' block '+name_block(scn_rels[0][0][1]) +' and '+R(scn_rels[1][1])+' block '+name_block(scn_rels[1][0][1]) +'.'
                        traj = [['block '+name_block(scn_rels[0][0][0])], ['block '+name_block(scn_rels[0][0][0])]]
                        
    
                    else: 
                        sen += ' Block '+name_block(scn_rels[0][0][0]) + ' is '+R(scn_rels[0][1])+' block '+name_block(scn_rels[0][0][1]) +' and it is '+R(scn_rels[1][1])+' block '+name_block(scn_rels[1][0][1]) +'.'
                        traj = [['block '+name_block(scn_rels[0][0][0])], ['it']]
                    
                    traj_obj_id = [[100+scn_rels[0][0][0]],[100+scn_rels[0][0][0]]]
                    land = [['block '+name_block(scn_rels[0][0][1])], ['block '+name_block(scn_rels[1][0][1])]]
                    land_obj_id = [[100+scn_rels[0][0][1]],[100+scn_rels[1][0][1]]]
                    sp_ind = [[scn_rels[0][1]], [scn_rels[1][1]]] 
                    create_annotation(sen)
                    
            elif scn_rels[0][0][1] == scn_rels[1][0][1]: # [[0,1], 'left'][[2,1], 'something']

                if scn_rels[0][1] == scn_rels[1][1]:

                    sen += ' Blocks '+name_block(scn_rels[0][0][0])+' and '+name_block(scn_rels[1][0][0])+' are '+R(scn_rels[0][1])+' '+name_block(scn_rels[0][0][1])+'.'
                    #!!!!
                    traj = [[name_block(scn_rels[0][0][0])], [name_block(scn_rels[1][0][0])]]
                    traj_obj_id = [[100+scn_rels[0][0][0]],[100+scn_rels[1][0][0]]]
                    land = [[name_block(scn_rels[0][0][1])], [name_block(scn_rels[0][0][1])]]
                    land_obj_id = [[100+scn_rels[0][0][1]],[100+scn_rels[0][0][1]]]
                    sp_ind = [[scn_rels[0][1]], [scn_rels[0][1]]] 
                    create_annotation(sen)
                    
                else:
                    
#                     y= random.choice([0,1,1,1])
                    sen+= ' Block '+name_block(scn_rels[0][0][0])+' is '+R(scn_rels[0][1])+' and '+name_block(scn_rels[1][0][0])+' is '+R(scn_rels[1][1])+' '+name_block(scn_rels[0][0][1])+'.'
    
                    traj = [['block '+name_block(scn_rels[0][0][0])], [name_block(scn_rels[1][0][0])]]
                    traj_obj_id = [[100+scn_rels[0][0][0]],[100+scn_rels[1][0][0]]]
                    land = [[name_block(scn_rels[0][0][1])], [name_block(scn_rels[0][0][1])]]
                    land_obj_id = [[100+scn_rels[0][0][1]],[100+scn_rels[0][0][1]]]
                    sp_ind = [[scn_rels[0][1]], [scn_rels[1][1]]] 
                    create_annotation(sen)
#                    
            else: # different [0,1] and [1,2]
                y = random.choice([0,1])
                if y: 
                    sen+= ' Block '+name_block(scn_rels[0][0][0])+' is '+R(scn_rels[0][1])+' '+name_block(scn_rels[0][0][1]) +' and block '+name_block(scn_rels[1][0][0])+' is '+R(scn_rels[1][1])+' '+name_block(scn_rels[1][0][1])+'.'
                    
                    traj = [['block '+name_block(scn_rels[0][0][0])], ['block '+name_block(scn_rels[1][0][0])]]
                    traj_obj_id = [[100+scn_rels[0][0][0]],[100+scn_rels[1][0][0]]]
                    land = [[name_block(scn_rels[0][0][1])], [name_block(scn_rels[1][0][1])]]
                    land_obj_id = [[100+scn_rels[0][0][1]],[100+scn_rels[1][0][1]]]
                    sp_ind = [[scn_rels[0][1]], [scn_rels[1][1]]] 
                    create_annotation(sen)
                    
                else: 
                    sen+= ' Block '+name_block(scn_rels[0][0][0])+' is '+R(scn_rels[0][1])+' '+name_block(scn_rels[0][0][1]) +'. '
                    
                    traj = [['block '+name_block(scn_rels[0][0][0])]]
                    traj_obj_id = [[100+scn_rels[0][0][0]]]
                    land = [[name_block(scn_rels[0][0][1])]]
                    land_obj_id = [[100+scn_rels[0][0][1]]]
                    sp_ind = [[scn_rels[0][1]]] 
                    create_annotation(sen)
                    
                    sen3 += 'Block '+name_block(scn_rels[1][0][0])+' is '+R(scn_rels[1][1])+' '+name_block(scn_rels[1][0][1])+'.'
                    
                    traj = [['block '+name_block(scn_rels[1][0][0])]]
                    traj_obj_id = [[100+scn_rels[1][0][0]]]
                    land = [[name_block(scn_rels[1][0][1])]]
                    land_obj_id = [[100+scn_rels[1][0][1]]]
                    sp_ind = [[scn_rels[1][1]]] 
                    create_annotation(sen3)
                    
                    sen += sen3
            
            # Adding description about objects
            sen +=  '\n'+BD(1)+P(scn_objs[scene_num])+'\n'+BD(2)+P(scn_objs[scene_num]) if num == 2 else '\n'+BD(1)+P(scn_objs[scene_num])+'\n'+BD(2)+P(scn_objs[scene_num])+'\n'+BD(3)+P(scn_objs[scene_num])
        
    
    else: # B != Null and D == Null
        
        sen += '\n'+BD01()+P(scn_objs[scene_num])+'\n'+BD02(1)+B0(1)+P(scn_objs[scene_num]) if num == 2 else '\n'+BD01()+P(scn_objs[scene_num])+'\n'+BD02(0)+B0(1)+P(scn_objs[scene_num])+'\n'+BD03()+B0(2)+P(scn_objs[scene_num])
    
    return sen

def BD(num): #The number of block -> first block, second block, third block

    sen = ''
    global scene_num, traj, sp_ind, traj_obj_id
    if num == 1: sen+= 'Block A '; scene_num = 0; traj = [['block A']]; traj_obj_id =[[100]]
    elif num == 2: sen+= 'Block B '; scene_num = 1; traj = [['block B']]; traj_obj_id = [[101]]
    elif num == 3: 
        scene_num = 2
        sen+= 'Block C ' if random.choice([0,1]) else 'And block C '
        traj, traj_obj_id = [['block C']], [[102]]
        
    y = random.choice([0,1])
    sen += 'has '+obj_rel_scene(scn_objs[num-1],2,'it') if y else 'contains '+obj_rel_scene(scn_objs[num-1],2,'it')
    sp_ind = [['has']] if y else [['contains']]
    create_annotation(sen)
    return sen

def BD01():

    sen =''

    global scene_num, land, sp_ind, traj, land_obj_id, traj_obj_id
    scene_num = 0
    x = random.choice([0,1])
    if x:
        sen += 'There '+ obj_rel_scene(scn_objs[0],0,'block A',True)  if random.choice([0,1]) else start_word(obj_rel_scene(scn_objs[0],1,'block A'))
        land, land_obj_id = [['block A']], [[100]]
    else:
        sen+= 'Block A '
        y = random.choice([0,1])
        sen += 'has ' if y else 'contains '
        sp_ind = [['has']] if y else [['contains']]
        sen+= obj_rel_scene(scn_objs[0],2,'block A')
        traj, traj_obj_id = [['block A']], [[100]]
    create_annotation(sen)
    return sen 

def BD02(s_num): # s_num show if the story contains two(s_num==1) or three blocks
    
    sen =''
    global scene_num, block_temp, sen_temp
    scene_num = 1
    if s_num: # 2 scenes
        sen += BD021(scn_rels[0])
    else:
        if 0 in scn_rels[0][0] and 1 in scn_rels[0][0]:
            sen += BD021(scn_rels[0])
        elif 0 in scn_rels[1][0] and 1 in scn_rels[1][0]:
            sen += BD021(scn_rels[1])
        else:
            sen += 'Then, we have block B ' if random.choice([0,1]) else 'Then, there is block B '
            block_temp, sen_temp = [['block B']] ,sen
    sen = start_word(sen)
    return sen

def BD021(x):

    global cannot_has_which, traj, land, sp_ind, block_temp, sen_temp, traj_obj_id, land_obj_id
    sen =''
    if x[0][0] == 1: # the relation is about position of scene two to one

        sen += 'Block B is '
        sen += R(x[1])+ ' block A '
        cannot_has_which = 1
        
        traj, land, sp_ind = [['block B']],[['block A']], [[x[1]]] 
        traj_obj_id, land_obj_id = [[101]], [[100]]
        #create_annotation(sen)
        sen_temp = sen
        
    elif x[0][1] == 1: # the relation is about the position of scene one to two

        sen += start_word(R(reverse(x[1])))+ ' block A'
        y = random.choice([0,1,2])
        if y == 0:
            sen += ' there is block B' 
        elif y == 1:
            sen += ' we have block B' 
        else:
            sen += ' is block B'
            
        traj, land, sp_ind = [['block B']],[['block A']], [[reverse(x[1])]] 
        traj_obj_id, land_obj_id = [[101]], [[100]]
        block_temp, sen_temp = [['block B']], sen
        #create_annotation(sen)    
        
    sen = start_word(sen)
    return sen

def BD03():
    sen, sen2, _sen, sen3 = '','', '', ''
    global scene_num, cannot_has_which
    global traj, land, sp_ind, block_temp, sen_temp, traj_obj_id, land_obj_id
    scene_num = 2
    if 2 in scn_rels[0][0] and 2 in scn_rels[1][0]:
        if scn_rels[0][0][0] == 2 and scn_rels[1][0][0] == 2:
            z, y = random.choice([0,0,1]), 3
            if z:
                sen3+= 'Finally,' #if random.choice([0,1]) else 'At last,' 
                sen3+= ' we have block C'                                                                                                
                y = random.choice([0,1,2])
                if y == 0: sen+= 'It is'; traj = [['it'],['it']]
                elif y==1: sen+= ' which is'; traj = [['block C'],['block C']]
                else: traj = [['block C'],['block C']]
            else: sen += 'Block C is'; traj = [['block C'],['block C']]
                
            traj_obj_id =[[102],[102]]     
            sen+= ' '+R(scn_rels[0][1])+' '
            sen2 += ' both ' if random.choice([0,1]) else ' '
            if scn_rels[0][1] == scn_rels[1][1]:

                sen += sen2+' blocks '+name_block(scn_rels[0][0][1])+' and '+name_block(scn_rels[1][0][1])
                sp_ind = [[scn_rels[0][1]],[scn_rels[0][1]]]
                land = [[name_block(scn_rels[0][0][1])],[name_block(scn_rels[1][0][1])]]
                #!!!!
            else : 

                sen+= 'block '+name_block(scn_rels[0][0][1])+' and '+R(scn_rels[1][1])+' block '+name_block(scn_rels[1][0][1])
                sp_ind = [[scn_rels[0][1]],[scn_rels[1][1]]]
                land = [['block '+name_block(scn_rels[0][0][1])],['block '+name_block(scn_rels[1][0][1])]]
            
            land_obj_id = [[100+scn_rels[0][0][1]],[100+scn_rels[1][0][1]]]
            if y == 0: _sen = sen; sen = sen3+'. ' + sen
            else: sen = sen3 + sen; _sen = sen    
            #create_annotation(_sen)
            sen_temp = _sen
            cannot_has_which = 1
            
        elif scn_rels[0][0][0] == 2 and scn_rels[1][0][1] == 2:
            z, y= random.choice([0,1,1,1]), 0
            if z:
                sen3+= 'Finally,'# if random.choice([0,1]) else 'At last,' 
                sen3+= ' we have block C'                                                                                                
                y = random.choice([0,1,2])
                if y == 0: sen+= 'It is'; traj = [['it']]
                elif y==1: sen+= ' which is'; traj = [['block C']]
                else: traj = [['block C']]
            else: sen += 'Block C is'; traj = [['block C']]
            traj_obj_id = [[102]]
            sen+= ' '+R(scn_rels[0][1])+' block '+name_block(scn_rels[0][0][1])
            land, sp_ind = [['block '+name_block(scn_rels[0][0][1])]], [[scn_rels[0][1]]]
            land_obj_id = [[100+scn_rels[0][0][1]]]
            h = random.choice([0,1])
            
            if h == 0:
                if y != 0: sen = sen3 + sen
                create_annotation(sen)
                sen+= '. Block '
                _sen = 'Block '
            else: 
                if y != 0: sen = sen3 + sen
                sen+= ' and block '; _sen =sen 
            
            sen += name_block(scn_rels[1][0][0])+' is '+R(scn_rels[1][1])+' it'
            _sen += name_block(scn_rels[1][0][0])+' is '+R(scn_rels[1][1])+' it'
            traj += [['block '+name_block(scn_rels[1][0][0])]]
            land += [['it']]
            traj_obj_id += [[100+scn_rels[1][0][0]]]
            land_obj_id += [[102]]
            sp_ind += [[scn_rels[1][1]]]
            #create_annotation(_sen)
            sen_temp = _sen
            if y == 0: sen = sen3 + '. '+sen
                
            cannot_has_which = 1
            
        elif scn_rels[0][0][1] ==2 and scn_rels[1][0][0] == 2:

            sen3 += 'Finally, ' #if random.choice([0,1]) else 'At last, '                                                                                                      
            sen3 += R(reverse(scn_rels[0][1]))+' block '+name_block(scn_rels[0][0][0])+' we have block C'
            traj, land, sp_ind = [['block C']], [['block '+name_block(scn_rels[0][0][0])]], [[reverse(scn_rels[0][1])]]
            traj_obj_id, land_obj_id = [[102]], [[100+scn_rels[0][0][0]]]
            
            y= random.choice([0,1])
            if y == 0:
                create_annotation(sen3)
            if y: sen+= ' which is '; traj += [['block C']] 
            else: sen += 'It is '; traj += [['it']]
            traj_obj_id += [[102]]
            sen+= R(scn_rels[1][1])+' block '+name_block(scn_rels[1][0][1])
            sp_ind += [[scn_rels[1][1]]]
            land += [['block '+name_block(scn_rels[1][0][1])]]
            land_obj_id += [[100+scn_rels[1][0][1]]]
            
            if y: sen = sen3 + sen ; sen_temp = sen#create_annotation(sen)
            else: sen_temp = sen; sen = sen3 + '. '+sen
            cannot_has_which = 1
            
        elif scn_rels[0][0][1] ==2 and scn_rels[1][0][1] ==2:
            
            sen2 += 'both ' if random.choice([0,1]) else ' '
            if scn_rels[0][1] == scn_rels[1][1]: 
                sen += start_word(R(reverse(scn_rels[0][1])))+' '+sen2+' blocks '+name_block(scn_rels[0][0][0])+' and '+name_block(scn_rels[1][0][0])
                sp_ind=[[reverse(scn_rels[0][1])], [reverse(scn_rels[0][1])]]
                land = [[name_block(scn_rels[0][0][0])], [name_block(scn_rels[1][0][0])]]
            else: 
                sen+= start_word(R(reverse(scn_rels[0][1])))+' block '+name_block(scn_rels[0][0][0])+' and '+R(reverse(scn_rels[1][1]))+' block '+name_block(scn_rels[1][0][0])
                sp_ind=[[reverse(scn_rels[0][1])], [reverse(scn_rels[1][1])]]
                land = [['block '+name_block(scn_rels[0][0][0])], ['block '+name_block(scn_rels[1][0][0])]]
            
            land_obj_id = [[100+scn_rels[0][0][0]],[100+scn_rels[1][0][0]]]
            sen+= ' there is block C'
            traj = [['block C'], ['block C']]
            traj_obj_id = [[102],[102]]
            #create_annotation(sen)
            block_temp, sen_temp = [['block C']], sen
            
    else:
        if 2 in scn_rels[0][0]:
            if scn_rels[0][0][0] == 2:

                sen3 += 'Finally, ' 
                sen3 += ' we have block C' if random.choice([0,1]) else ' there is block C'
                
                y = random.choice([0,1,2])
                if y == 0: sen+= 'It is'; traj = [['it']]
                elif y==1: sen+= ' which is'; traj = [['block C']]
                else: traj = [['block C']]
                sen+= ' '+R(scn_rels[0][1])+' block '+name_block(scn_rels[0][0][1])
                sp_ind, land = [[scn_rels[0][1]]], [['block '+name_block(scn_rels[0][0][1])]]
                traj_obj_id, land_obj_id = [[102]], [[100+scn_rels[0][0][1]]]
                if y == 0: _sen = sen ; sen = sen3+'. ' + sen
                else: sen = sen3 + sen; _sen = sen
                #create_annotation(_sen)
                sen_temp = _sen
                cannot_has_which = 1
                
            else:

                sen += start_word(R(reverse(scn_rels[0][1])))+' block '+name_block(scn_rels[0][0][0])+' there is block C' 
                traj, land, sp_ind = [['block C']], [['block '+name_block(scn_rels[0][0][0])]], [[reverse(scn_rels[0][1])]]
                traj_obj_id, land_obj_id = [[102]], [[100+scn_rels[0][0][0]]]
                block_temp, sen_temp= [['block C']], sen
                #create_annotation(sen)
                
        elif 2 in scn_rels[1][0]:
            if scn_rels[1][0][0] == 2:

                sen3 += 'Finally, '
                sen3 += ' we have block C' if random.choice([0,1]) else ' there is block C'
                
                y = random.choice([0,1,2])
                if y == 0: sen+= 'It is'; traj = [['it']]
                elif y==1: sen+= ' which is'; traj = [['block C']]
                else: traj = [['block C']]
                traj_obj_id = [[102]]
                sen+= ' '+R(scn_rels[1][1])+' block '+name_block(scn_rels[1][0][1])
                sp_ind, land = [[scn_rels[1][1]]], [['block '+name_block(scn_rels[1][0][1])]]
                land_obj_id = [[100+scn_rels[1][0][1]]]
                
                if y == 0: _sen = sen ; sen = sen3+ '. ' + sen
                else: sen = sen3 + sen; _sen = sen
                #create_annotation(_sen)
                sen_temp = _sen
                cannot_has_which = 1
                
            else:

                sen += start_word(R(reverse(scn_rels[1][1])))+' block '+name_block(scn_rels[1][0][0])+' there is block C'
                traj, land, sp_ind = [['block C']], [['block '+name_block(scn_rels[1][0][0])]], [[reverse(scn_rels[1][1])]]
                traj_obj_id, land_obj_id = [[102]], [[100+scn_rels[1][0][0]]]
                block_temp, sen_temp= [['block C']], sen
                #create_annotation(sen)
                sen_temp = sen
                
    sen = start_word(sen)
    return sen

def P(O_R):

    global End_of_block, finished_objs, checked_obj_obj, checked_obj_sc, shared_prop, object_shared_prop, treshhold, scene_num, objs_rels, recent_objs, objs_attrs_f,objs_objs_f, temp_annot_sent, traj, land, sp_ind
    sen = '. '
    

    while End_of_block != 1: # Describes all objects and their relations untill all were described

        if len(checked_obj_sc) == 0:
            sen1 = U(O_R)
            if sen1: sen += sen1
        else:
            y= random.choice([0,1])
            if y and len(checked_obj_sc) != len(O_R): 
                sen1 =  U(O_R)
                if sen1: sen += sen1
            else:  
                
                sen1 = Q(O_R)
                if sen1: sen += sen1
        treshhold = 0
    End_of_block = 0
    check_number_for_obj()
    objs_attrs_f.append(checked_obj_sc)
    objs_objs_f.append(checked_obj_obj)
    finished_objs, checked_obj_obj, checked_obj_sc,recent_objs = [], [], [], []

    return sen
    
def Q(O_R, obj_ref= None):

    global recent_objs, checked_obj_sc, checked_obj_obj
    global sz, clr, sh, sc_rl, End_of_block
    sen,sen1, sen_w ='','',''
    pre_defined = recent_objs if recent_objs else '' # nowing objects that are referenced in the previous sentence.

    recent_objs = []
    if pre_defined: # having objects with shared properties
        if len(pre_defined) >1: #like: two big circle and three yellow shapes. should mentioned by properties
            for ind1,s_o in enumerate(pre_defined):
                
                num_of_s_o = len(s_o)
                
                if len(s_o)>1: # [[0,1,2],[3,4]]
                    for ind, obj in enumerate(s_o): #obj is the id of object
                        sen1 = ''
                        shape_name = 1
                        sen1 += obj_ide(obj)
                        if 'number' not in sen1: sen1 = 'the '+sen1
                        sen_w = W(O_R,obj,defined_obj=sen1)
                        if sen_w != None: sen += sen_w+'. '

                        
                        
                
                else: # [[0],[2],[4]] # must not have first and second ...
                    sen1 = ''
#                     if ind1 == 0: 
#                         sen1 += 'a '+obj_ide(s_o[0])
#                         sen += W(O_R, s_o[0], defined_obj=sen1)
#                         if sen: sen += '. '
#                     else:
#                         sen1 += ' the '
#                         sen1 += obj_ide(s_o[0])+' '
#                         sen += W(O_R, s_o[0], defined_obj=sen1)
#                         if sen: sen += '. '        

        else: # [[0,1,2]] or [[1]]
            sen1 = ''
            num_of_s_o = len(pre_defined[0])
            if num_of_s_o>1: # [[0,1,2]]
                for ind, obj in enumerate(pre_defined[0]):
                    sen1 = ''
                    if ind == 0:
                        sen1 = obj_ide(obj)    
                    else:
                        sen1 =  obj_ide(obj)+' '
                    if 'number' not in sen1: sen1 = 'the '+sen1
                    sen_w = W(O_R, obj, defined_obj=sen1)
                    if sen_w != None: sen += sen_w+'. '

            else: #[[0]]

                for ch in checked_obj_sc:
                    if ch[0] == pre_defined[0][0]:
                        sen1 = 'this '+ sh_ob_single() 
                        sen_w = W(O_R,pre_defined[0][0],defined_obj='it') if random.choice([0,1,1]) else W(O_R,pre_defined[0][0],sen1)
                        if sen_w != None: sen += sen_w+'. ' 
                        break
                    

    else: # describing individual object for the first time or pre-defined object which is not in recent.
        sen1 = ''
        objects = [x for x in range(len(O_R))]
        for obj in objects: # consider all objects
            x = random.choice([0,1,1])
            obj_rel = [] # relation between obj and other objects
            if x: # describe that object
                sen_w = W(O_R, obj, 'UN')
                if sen_w != None: sen += sen_w+'. '
    if len(O_R) == len(checked_obj_sc) and len(checked_obj_obj) >= len(objs_rels[scene_num]): End_of_block = 1
        
    return sen

def W(O_R, obj, defined_obj=''):
    global treshhold, recent_objs, scene_num, objs_rels, temp_checked_obj_sc, traj, land, sp_ind, temp_annot_sent, land_obj_id, traj_obj_id
    
    sen,sen_ref = '',''
    traj1, land1, sp_ind1 = [], [], []
    traj_id, land_id = [], []
    object2, rel,num_objs_obj2, scn_rels = '','', -1, ''
    rels = objs_rels[scene_num]
    defined_obj1 = defined_obj
    ch_os = []
    obj_rel = []
    new_object_created = False
    for ch in checked_obj_sc: 
        ch_os.append(ch[0])
    
    if rels == []: return None
    
    y = random.choice([0,1]) if check_has_touching(O_R, obj) else 1
    
    if y:
        object2, rel, num_objs_obj2 =W1(O_R, obj, [])
        
#     else: _O_R, _obj = O_R, obj

    if defined_obj1 == 'UN': # describe an object without shared attribute.
        if obj not in ch_os: # obj is a new object
            sen_ref = 'a '+new_obj(O_R, obj, temp = True)
            #for annotation
            traj1 += [sen_ref]
            new_object_created = True
            
        else: # obj is a predefined object
            sen_ref = obj_ide(obj)
            if 'number' not in sen_ref: sen_ref = 'the '+sen_ref
            #for annotation
            traj1 += [sen_ref]  
            
        defined_obj1 = sen_ref
    
    else: traj1 += [defined_obj1]
    traj_id += [obj]
    
    
    if object2 and rel:
        z = random.choice([0,1])
        if z or defined_obj1 == 'it' or defined_obj1 == 'this object' or defined_obj1 == 'this shape': # obj1 is to the relation of the obj2
            sen += start_word(defined_obj1)+' is '
            sen += rel+' '+ object2
            
        else: # to the relation of the obj2 there is obj1
            sen += start_word(rel)+' '+object2
            sen += ' is '+defined_obj1+' ' if random.choice([0,1]) else ' there is '+defined_obj1
        recent_objs = [[obj]]
        
        
    else:#if num_objs_obj2 == 0:
        
        if y == 0:
            scn_rels = W3(O_R, obj, new_object_created)
        
        if scn_rels:

            sen += start_word(defined_obj1)+' is '+ scn_rels +' this block'
            land1 = ['this block']
            land_id = [100+scene_num]
            recent_objs = [[obj]]
            
        elif defined_obj1[0] == 'a': 
            sen += 'This block also has '+defined_obj1
            sp_ind1 = ['has']
            land1 = traj1
            land_id = traj_id
            traj_id = [100+scene_num]
            traj1 = ['this block']
            recent_objs = [[obj]]
    
    
    if sen and temp_checked_obj_sc: 
        
        update_checked_obj_sc(temp_checked_obj_sc[-1][0],temp_checked_obj_sc[-1][1],temp_checked_obj_sc[-1][2],temp_checked_obj_sc[-1][3],temp_checked_obj_sc[-1][4],temp_checked_obj_sc[-1][5])
#         temp_checked_obj_sc.pop(-1)
        
    elif temp_checked_obj_sc and new_object_created: 
        
        temp_checked_obj_sc.pop(-1)
    
        
   
    if sen:
        if traj1: traj += [traj1]; traj_obj_id += [traj_id]     
        if land1: land += [land1]; land_obj_id += [land_id]
        if sp_ind1: sp_ind += [sp_ind1]
        
        #temp_annot_sent = sen+'.'
        create_annotation(sen)

    return sen

def W1(O_R, obj, forbiden = None): # obj -> id of an elemenet

    global checked_obj_obj, temp_checked_obj_sc, treshhold, recent_objs, land, sp_ind, traj, traj_obj_id, land_obj_id
    cannot_refer = 0
    if forbiden == None: forbiden = []

    object2, relations = '',''
    land1, sp_ind1, traj1 = [], [], []
    land_id, traj_id = [], []

    new_object_created = False
    rels = objs_rels[scene_num]
    more_obj = 0
    ch_os = []
    obj_rel = []
    for ch in checked_obj_sc: 
        ch_os.append(ch[0])

    if rels == []:
        num_of_obj2 = -1

        return object2, relations, num_of_obj2          
    
    for obj_obj in rels:
        if obj_obj[0][0] == obj and obj_obj[0][1] not in forbiden: # if there is any relation between object obj and other objects.
            check =0
            for i in checked_obj_obj:
                if obj_obj[0] in i: check = 1; break
            if check == 0:
                obj_rel.append(obj_obj)
                
    z = random.choice([0,1,1,1]) 
    r_Q = {}
    if z==1: # if there is any shared relation between objects choose them
        #check if there is shared relation between some objects or an object has some relations
        
        
        for o_r in obj_rel:
            for i in o_r[1]:
                if i not in r_Q: r_Q.update({i: [o_r[0][1]]})
                else: r_Q[i].append(o_r[0][1])
        r_Q_copy = r_Q.copy()
        for i in r_Q_copy: 
            if len(r_Q[i]) <2: del r_Q[i]
        if len(r_Q) == 0: z =0
        else: # start describing shared
            f_list = [x for x in r_Q.keys()]
            f = random.choice(f_list)
            i = r_Q[f]
            relations = R(f)
            sp_ind1 += [f]
            rec_o = []
            for ob in i: 
                rec_o.append(ob)
                objj = '' 
                if ob not in ch_os: objj = 'a '+new_obj(O_R, ob, temp = True); new_object_created=True; land1 += [objj]; land_id += [ob]
                else: 
                    objj = obj_ide(ob)
                    if 'number' not in objj: objj = 'the '+objj
                    land1 += [objj]; land_id += [ob]
                    
                #land += [land1]
                if object2:
                    object2 += ', '+ objj
                    more_obj = 1 
                else:
                    object2 += objj
                for o in obj_rel:
                    if o[0] == [obj,ob] and f in o[1]: checked_obj_obj.append([o[0],[f]])
            object2 = add_and(object2)
            recent_objs= [rec_o]
                
                
    if z == 0: #
        more_obj = 0
        def_ch = 1
        obj2, relll ='',''
        attr_desc = 0
        if obj_rel:
            
            f_list = [x for x in range(len(obj_rel))]
            f = random.choice(f_list)
            ob = obj_rel[f]
            if len(ob[1])>1: # has more than one relation between two object
                for rell in ob[1]:
                    sp_ind1 += [rell]
                    relations += ', '+R(rell) if relations else R(rell)
                #sp_ind += [sp_ind1]
                relations = add_and(relations)
                
                objj = '' 
                if ob[0][1] not in ch_os: objj = 'a '+new_obj(O_R, ob[0][1], temp = True); new_object_created=True; land1 += [objj]; land_id += [ob[0][1]]
                else: 
                    objj = obj_ide(ob[0][1])
                    if 'number' not in objj: objj = 'the '+objj
                    land1 += [objj]; land_id += [ob[0][1]]
                    
                if random.choice([0,1,1]): 
                    checked_obj_obj.append(ob)
                    if treshhold<1: 
                        treshhold+=1
                        forbiden += [ob[0][0]]
                        obj2, relll, _ = W1(O_R, ob[0][1], forbiden)
                        if obj2 and relll:
                            traj += [[land1[-1]]]; traj_obj_id += [[land_id[-1]]]
                else:
                    if treshhold<1 and attr_desc == 0:
                        forbiden += [ob[0][0]]
                        obj2, relll, obj2_id = W2(ob[0][1], forbiden)
                        if obj2 and relll: 
                            treshhold+=1 
                            objj = unique_with_rel(ob[0][1], relll, obj2_id)
                            if objj != -1:
                                objj = 'the '+objj
                                land1[-1] = objj
                                land_id[-1] = ob[0][1]
                                traj += [[land1[-1]]]
                                traj_obj_id += [[land_id[-1]]]
                                land += [[obj2]]
                                land_obj_id += [[obj2_id]]
                                sp_ind += [[relll]]
                            else: 
                                objj = 'the '+obj_ide(ob[0][1])
                                obj2, relll = '',''
                    checked_obj_obj.append(ob)

                object2 += objj+' ' if objj else ''
                if obj2 and relll: 
                    object2 += ' and is ' if attr_desc else 'which is '
                    object2 += R(relll)+' '+obj2
            
            else:    
                relations = R(ob[1][0])
                sp_ind1 += [ob[1][0]]
                objj = ''
                if ob[0][1] not in ch_os: objj = 'a '+new_obj(O_R, ob[0][1], temp=True); new_object_created=True; land1 += [objj[2:]]; land_id += [ob[0][1]]
                else:
                    objj = obj_ide(ob[0][1]) 
                    if 'number' not in objj: objj = 'the '+objj
                    land1 += [objj]
                    land_id += [ob[0][1]]
                if random.choice([0,1]):
                    checked_obj_obj.append(ob)
                    if treshhold<1: 
                        treshhold+=1
                        forbiden += [ob[0][0]]
                        obj2, relll, _ = W1(O_R, ob[0][1], forbiden)
                        if obj2 and relll:
                            traj += [[land1[-1]]]
                            traj_obj_id += [[land_id[-1]]]
                else:
                    if treshhold<1 and attr_desc == 0:
                        forbiden += [ob[0][0]]
                        obj2, relll, obj2_id = W2(ob[0][1], forbiden)
                        if obj2 and relll:
                            treshhold+=1
                            objj = unique_with_rel(ob[0][1], relll, obj2_id)
                            if objj != -1:
                                objj = 'the '+objj
                                land1[-1] = objj
                                land_id[-1] = ob[0][1]
                                traj += [[land1[-1]]]
                                traj_obj_id += [[land_id[-1]]]
                                land += [[obj2]]
                                land_obj_id += [[obj2_id]]
                                
                                sp_ind += [[relll]]
                                
                            else: 
                                objj = 'the '+obj_ide(ob[0][1])
                                obj2, relll = '',''
                    checked_obj_obj.append(ob)
                
                object2 += objj+' ' if objj else ''
                if obj2 and relll: 
                    object2 += ' and is ' if attr_desc else 'which is '
                    object2 += R(relll)+' '+obj2
    
    
    if object2 and relations and temp_checked_obj_sc: 
        update_checked_obj_sc(temp_checked_obj_sc[-1][0],temp_checked_obj_sc[-1][1],temp_checked_obj_sc[-1][2],temp_checked_obj_sc[-1][3],temp_checked_obj_sc[-1][4],temp_checked_obj_sc[-1][5])
    elif temp_checked_obj_sc and new_object_created: temp_checked_obj_sc.pop(-1)
    
    if object2 and relations:
        if land1: land += [land1]; land_obj_id += [land_id]
        if traj1: traj += [traj1]; traj_obj_id == [traj_id]
        if sp_ind1: sp_ind += [sp_ind1]
    
    return object2, relations, more_obj

def W2(obj, forbiden = None):
    
    global recent_objs
    if forbiden == None: forbiden = []
    rels = objs_rels[scene_num]
    r_Q = []
    
    for obj_obj in rels:
        if obj_obj[0][0] == obj and obj_obj in checked_obj_obj and obj_obj[0][1] not in forbiden:
            r_Q.append(obj_obj)
    if r_Q:
        x_list = [x for x in range(len(r_Q))]
        x = random.choice(x_list)
        relations = r_Q[x][1][0]
        object2 = obj_ide(r_Q[x][0][1])
        if 'number' not in object2: object2 = 'the '+object2
        
        return object2, relations,r_Q[x][0][1]
    
    else: return '','',''

    
def W3(O_R, obj, temp = False):
    
    global sc_rl, land, sp_ind
    rels = []
    
    for ind, _scn_rel in enumerate(O_R[obj][0]):
        if 'edge' in _scn_rel : rels.append(ind)
    rel = O_R[obj][0][random.choice(rels)] 

    sen = Rel(rel)
    update_checked_obj_sc(obj,'','','',sc_rl, temp = temp)
    sp_ind += [[sen]]
    sc_rl = ''
    return sen            

def check_has_touching(O_R, obj):

    global checked_obj_sc 
    ind = ind_check_obj(obj)
    if ind != None: 
        object_attrs = checked_obj_sc[ind]
        if object_attrs[4] != '': return False
    
    for _scn_rel in O_R[obj][0]:
        if 'edge' in _scn_rel: return True
        
    return False


def U(O_R):
    

    global clr, sz, sh, sc_rl, End_of_block, recent_objs, traj, land, sp_ind, temp_annot_sent, land_obj_id, traj_obj_id, scene_num
    
    traj1, land1, sp_ind1, obj_list = [], [], [], []
    traj_id, land_id, obj_id_list = [], [], []
    sen = ''
    object_i_rel, object_i= [], []
    
    
    ch_os = []
    for ch in checked_obj_sc: 
        if ch[0] not in ch_os: ch_os.append(ch[0])
    num_objs = 0
    def_objs = []
    for i, obj in enumerate(O_R):
        x = random.choice([0,1]) # choose or not to choose the object.
        if x and i not in ch_os:
            if object_i == []:
                new_object = s_num()+ new_obj(O_R,i)
                obj_list += [new_object]
                obj_id_list += [i]
                object_i.append(new_object)
                object_i_rel.append(Rel(obj[0][0]))
                update_checked_obj_sc(i, sz, clr, sh, sc_rl)
                clr, sz, sh, sc_rl = '','','',''
                def_objs = i
                num_objs +=1
            elif Rel(obj[0][0]) in object_i_rel: 
                new_object = s_num()+ new_obj(O_R,i)
                obj_list += [new_object]
                obj_id_list += [i]
                object_i.append(new_object)
                object_i_rel.append(Rel(obj[0][0]))
                update_checked_obj_sc(i, sz, clr, sh, sc_rl)
                clr, sz, sh, sc_rl = '','','',''
                def_objs = i
                num_objs +=1
            sc_rl = ''

    
    if def_objs and num_objs == 1:
        recent_objs= [[def_objs]]
    else: recent_objs = []
            
    
    same_rel = all(z == object_i_rel[0] for z in object_i_rel) if object_i_rel else False
    
    y = random.choice([0,1])
    #has, contains
    if y == 0 and object_i and object_i_rel: 
        sen3 = ''
        if random.choice([0,1]):
            sen += 'It '
            traj1 += ['it']
            
        else:
            sen += 'This block '
            traj1 += ['this block']
            
        traj_id += [100+scene_num]
        
        if len(ch_os) != 0: sen += 'also '
        if random.choice([0,1]):
            sen += 'has '
            sp_ind1 += ['has']
        else:
            sen += 'contains '
            sp_ind1 += ['contains']
            
        for h,z in enumerate(object_i):
            sen3+= ', 'if sen3 else '' 
            sen3 += z+' '
        land1 = obj_list
        land_id = obj_id_list
        sen3 = add_and(sen3)
        sen+= sen3
    # there is
    elif y == 1 and object_i and object_i_rel: 
        l=random.choice([0,1])
        this_block = 0
        if l: 
            sen3,n_o = '',0
            sen += 'There '
            sen += 'are ' if num_objs>1 and same_rel else 'is '
            if len(ch_os) != 0: sen += 'also '
            for h,z in enumerate(object_i):
                n_o +=1
                sen3 += ', 'if sen3 else '' 
                sen3 += z+' '
                if same_rel == False: 
                    if object_i_rel[h] != ' in':
                        sen3 += 'that is'
                    sen3 += object_i_rel[h]
                    sp_ind1 += [object_i_rel[h][1:]]
                    if this_block: 
                        sen3 += ' it '
                        land1 += ['it']
                    else:
                        sen3 += ' this block '
                        land1 += ['this block']
                    this_block = 1
                else:
                    sp_ind1 += [object_i_rel[0][1:]]
                    land1 += ['this block']
                land_id += [100+scene_num]
            
            traj1 = obj_list  
            traj_id = obj_id_list
            sen3 = add_and(sen3)
            sen += sen3+object_i_rel[0]+' this block' if same_rel else sen3
                
        else:
            sen3,n_o = '',0
            for h,z in enumerate(object_i):
                sen3+= ', 'if sen3 else '' 
                sen3 += z+' '
                n_o += 1
            traj1 = obj_list
            traj_id = obj_id_list
            sen3 = add_and(sen3)
            sen += sen3 
            sen += 'are ' if n_o>1 else 'is '
            if len(ch_os) != 0: sen += 'also'
            if same_rel: 
                sen += object_i_rel[0] +' this block'
                sp_ind1 += [object_i_rel[0][1:]]
            else:
                sen += ' in this block'
                sp_ind1 += ['in']
            land1 += ['this block']
            land_id = [100+scene_num]

    if len(O_R) == len(checked_obj_sc) and len(checked_obj_obj) >=  len(objs_rels[scene_num]): End_of_block = 1 
    if sen: 
        
        sen = start_word(sen)+'. '
        if land1: land += [land1] ; land_obj_id += [land_id]
        if traj1: traj += [traj1]; traj_obj_id += [traj_id]
        if sp_ind1: sp_ind += [sp_ind1]
        create_annotation(sen)

    return sen

def obj_desc(obj): # an element . describe other features of object
    features,article = '',0
    global sz, clr, sh, sc_rl

    for l,ch in enumerate(obj):
        tag_name = ''# name of the feature 
        if ch =='' and random.choice([0,1,1,1,1]):
            if l == 0 or l == 4: continue
            if l == 1: 
                features += ' and ' if features else ' '
                features+= size(scn_objs[scene_num][obj[0]][1]['size'])
            elif l == 2: 
                features += ' and ' if features else ' '
                features+= color(scn_objs[scene_num][obj[0]][1]['color'])
            elif l == 3: 
                features+= ' '+shape(scn_objs[scene_num][obj[0]][1]['type'])
                article = 1
            #elif l == 4: features+= Rel(scn_rels[scene_num][obj[0]][0])
    
    if article: features = ' a' + features
    
    update_checked_obj_sc(obj[0], sz, clr, sh, sc_rl)
    sz, clr, sh, sc_rl = '', '', '',''
    return features

def obj_ide(obj): # id of the object . The identification description for an object
    
    global traj, land, sp_ind, traj_obj_id, land_obj_id
    sen = ''
    obj_sha_name = sh_ob_single()
    s = []
    uniq_attr = unique_attr_check()
    ind_check = ind_check_obj(obj)
    uniq_id = ''
    s = [0]*6 
    for l,c in enumerate(checked_obj_sc[ind_check]):
        if c != '' and l!=0:
            if l != 4 and l !=5:
                # considering mentioned just by unique features

                s[l]=1
                    #always with all attributes if random.choice([1,1,0,1,1]): s[l]=1
            elif l == 4:
                continue
#                 if s.count(1) == 0: #there is not any attribute till now
#                     s[l] = 1
            else: s[l] = 1 #l == 5
                
    sen1, sen2,sen3 = '', '', ''
    if s[1] == 1: sen1 += checked_obj_sc[ind_check][1]['size']+' '
    if s[2] == 1: sen1 += checked_obj_sc[ind_check][2]['color']+' '
    if s[3] == 1: obj_sha_name = ''; sen1 += checked_obj_sc[ind_check][3]['type']+' '
    if s[4] == 1: sen2 += ' which is '+ checked_obj_sc[ind_check][4]['rel']+ ' the block '
    if s[5] == 1: sen3 +=  ' number ' + object_num(checked_obj_sc[ind_check][5]) +' '
    
    #has touching relation
#     if s[4] == 1:
#         traj += [['the '+sen1 + obj_sha_name+sen3]]
#         land += [['the block']]
#         sp_ind += [[checked_obj_sc[ind_check][4]['rel']]]
#         traj_obj_id += [[obj]]
#         land_obj_id += [[100+ scene_num]]
        
    sen += sen1 + obj_sha_name+sen3+sen2 
    return sen

def new_obj(O_R,obj, temp=''): #obj -> number
    
    global sz, clr, sh, sc_rl
    s= [1,1,1]

    Size = ' '+size(O_R[obj][1]['size']) if s[0] else ''
    Color = ' '+color(O_R[obj][1]['color']) if s[1] else ''
    Shape = ' '+shape(O_R[obj][1]['type']) 
    
    update_checked_obj_sc(obj, sz, clr, sh, sc_rl, temp = temp)
    sz, clr, sh, sc_rl = '', '', '',''
    return Size+Color+Shape
    
    
def ObjP(s = '', c = '', sh = ''):
    
    Size = ' '+size(s) if s else ''
    Color = ' '+color(c) if c else ''
    Shape = ' '+shape(sh) if sh else ' shape'
    
    return Size+Color+Shape


def obj_rel_scene(O_R, which, subject= '', verb = False): #check relations betwee objects and their scene, alongside check if objects have shared properties
                               # which ==1 -> exists, which == 0 there are or with, which == 2 has, contains 
    
    sen = ''
    global sz, clr, sh, sc_rl
    global checked_obj_sc
    global shared_prop, object_shared_prop, recent_objs
    global traj, land, sp_ind, traj_obj_id, land_obj_id
    _objects, _rel, _object_id = [], [], []
    object_shared_prop, shared_prop = [],[]
    number_of_obj = 0

    
    obj_sc_rel,obj_prop = [], []
    for i in range(len(O_R)):
        for j in range(i+1,len(O_R)):
            # check if their relations are similar
            check = set(O_R[i][0]).intersection(O_R[j][0])
            check.remove('in') #because all objects have this relation with the scene
            if check: obj_sc_rel.append([i,j,list(check)])
            #check if their properties are similar
            check_prop = set(O_R[i][1].items()).intersection(O_R[j][1].items())
            check_prop = [ z for z in check_prop if (('x_loc' not in z) and ('y_loc' not in z))]
            check_prop= reorder(check_prop)
            if check_prop and len(check_prop)>2: obj_prop.append([i,j,check_prop])
            

    xzy = 1#random.choice([0,1,1])
    if (obj_sc_rel or obj_prop) and xzy: #if any common relation exist #TODO

        if obj_sc_rel and obj_prop:

            x = 0#random.choice([0,0,0,1])
            if x: #start with relation in the scene
                for h,ob_sc in enumerate(obj_sc_rel):
                    num_shared, property = 2, []
                    x = random.choice([0,1,1,1])
                    ch_os = []
                    for ch in checked_obj_sc:
                        if ch[0] not in ch_os: ch_os.append(ch[0])
                    if x and ob_sc[0] not in ch_os and ob_sc[1] not in ch_os :
                        property = ob_sc[2]
                        objs_shared = [ob_sc[0],ob_sc[1]] 
                        prop = ''
                        for z in obj_prop:
                            if all(item in objs_shared for item in [z[0],z[1]]):
                                prop = z[2]
                        for j in range(len(obj_sc_rel)):
                            if all(item in obj_sc_rel[j][2] for item in property ):
                                if obj_sc_rel[j][0] not in objs_shared and obj_sc_rel[j][0] not in ch_os: objs_shared.append(obj_sc_rel[j][0]); num_shared+=1
                                if obj_sc_rel[j][1] not in objs_shared and obj_sc_rel[j][1] not in ch_os: objs_shared.append(obj_sc_rel[j][1]); num_shared+=1
                                for p in prop:
                                    if O_R[obj_sc_rel[j][0]][1][p[0]] != p[1] or O_R[obj_sc_rel[j][1]][1][p[0]] != p[1]: prop.remove((p[0],p[1]))
                        
                        shared_prop.append(prop)
                        object_shared_prop.append(objs_shared)
                        
                        number_of_obj+= num_shared
                        if sen: sen += ', '
                        sen11 = ''
                        sen11 += num_to_word(str(num_shared))+' other' if sen else num_to_word(str(num_shared))
                        shape = 1
                        for j in property:
                            for p in prop:
                                sen11 += ' '+globals()['shape'](p[1])+'s' if p[0] == 'type' else ' '+globals()[p[0]](p[1])
                                if p[0] == 'type': shape=0
                            if shape:
                                if which == 0 or which == 2 : sen11 += ' '+ sh_ob()+' '+ j
                                elif which == 1 : sen11 += ' '+ sh_ob()+' are ' +j
                            else: 
                                if which == 0 or which == 2: sen11 += ' '+ j
                                elif which == 1 : sen11 += ' are ' +j
                            Rel(j)
                            _rel+=[j]
                            for os in objs_shared:
                                update_checked_obj_sc(os, sz, clr, sh, sc_rl)
                            sz, clr, sh,sc_rl = '', '', '', ''
                        _objects+=[sen11]
                        _object_id += [-1]
                        sen += sen11
                sen = add_and(sen)
                if sen : sen+= ' '+subject
            else: # start with shared properties
                sen1 = ''
                prop_rel = [] 
                for h,ob_pr in enumerate(obj_prop): 
                    num_shared, property = 2, []
                    x = 1#random.choice([0,1,1,1])
                    relate,sen1 = '',''
                    ch_os = []
                    for ch in checked_obj_sc: 
                        if ch[0] not in ch_os: ch_os.append(ch[0])
                    if x and ob_pr[0] not in ch_os and ob_pr[1] not in ch_os:
                        property = ob_pr[2]
                        objs_shared = [ob_pr[0],ob_pr[1]] 
                        for z in obj_sc_rel:
                            if all(item in objs_shared for item in [z[0],z[1]]):
                                relate = z[2][0]
                                if len(relate)> 1: relate = random.choice(relate)
                                Rel(relate)
                        for j in range(len(obj_prop)):
                            if all(item in obj_prop[j][2] for item in property):
                                if obj_prop[j][0] not in objs_shared and obj_prop[j][0] not in ch_os: objs_shared.append(obj_prop[j][0]); num_shared+=1
                                if obj_prop[j][1] not in objs_shared and obj_prop[j][1] not in ch_os: objs_shared.append(obj_prop[j][1]); num_shared+=1
                                if O_R[obj_prop[j][0]][0] != relate or O_R[obj_prop[j][1]][0] != relate: relate = ''; sc_rl = ''
                        shared_prop.append(property)
                        object_shared_prop.append(objs_shared)
                        
                        sen1 += num_to_word(str(num_shared))
    
                        number_of_obj+= num_shared
                        shape = 1
                        for j in property:
                            sen1 += ' '+globals()['shape'](j[1])+'s' if j[0] == 'type' else ' '+globals()[j[0]](j[1])
                            if j[0] == 'type':
                                 shape = 0
                            for os in objs_shared:
                                update_checked_obj_sc(os, sz, clr, sh, sc_rl)
                            clr, sz, sh, sc_rl = '','','',''
                        if shape:
                            sen1 += ' '+sh_ob()
                        _objects+=[sen1]
                        _object_id += [-1]
                        if relate:
                            check = 1
                            for itr,item in enumerate(prop_rel):
                                if item[1] == relate:
                                    check = 0
                                    prop_rel[itr][0] += ' and '+sen1
                                    break
                            if check: prop_rel.append([sen1, relate])
                        else:
                            check = 1
                            for itr,item in enumerate(prop_rel):
                                if item[1] == 'in':
                                    check = 0
                                    prop_rel[itr][0] += ' and '+sen1
                                    break
                            if check: prop_rel.append([sen1, 'in'])

                in_rel, in_rel_num = 0, -1
                for itr,p_r in enumerate(prop_rel):
                    if p_r[1] == 'in':
                        in_rel = 1
                        in_rel_num = itr
                list_order = [h for h in range(len(prop_rel)) if h != in_rel_num]
                for itr in list_order:
                    if sen: sen += ','
                    sen += ' '+ prop_rel[0]+' are '+prop_rel[1] if which == 0 else ' '+prop_rel[0]+prop_rel[1]
                    _rel += [prop_rel[1]]
                sen = add_and(sen)

                if in_rel:
                    if sen: #before this it has other relation with scene
                        if which == 0: 
                            sen += ' and '+prop_rel[in_rel_num][0]+' in '+subject
                        elif which == 1:
                            sen += ' and '+ prop_rel[in_rel_num][0]+' are in '+subject
                        elif which == 2:
                            sen += ' '+subject+' and '+ prop_rel[in_rel_num][0]
                    else: 
                        if which == 0: 
                            sen += prop_rel[in_rel_num][0]+' in '+subject
                        elif which == 1:
                            sen += prop_rel[in_rel_num][0]+' are in '+subject
                        elif which == 2:
                            sen += prop_rel[in_rel_num][0]
                else: sen += ' '+subject
                    
                
        elif obj_sc_rel == [] and obj_prop:
            for h,ob_pr in enumerate(obj_prop):
                num_shared, property = 2, []
                x = 1#random.choice([0,1,1])
                ch_os = []
                for ch in checked_obj_sc: 
                    if ch[0] not in ch_os: ch_os.append(ch[0])
                if x and ob_pr[0] not in ch_os and ob_pr[1] not in ch_os :
                    property = ob_pr[2]
                    objs_shared = [ob_pr[0],ob_pr[1]] 
                    for j in range(len(obj_prop)):
                        if all(item in obj_prop[j][2] for item in property ):
                            if obj_prop[j][0] not in objs_shared and obj_prop[j][0] not in ch_os: objs_shared.append(obj_prop[j][0]); num_shared+=1
                            if obj_prop[j][1] not in objs_shared and obj_prop[j][1] not in ch_os: objs_shared.append(obj_prop[j][1]); num_shared+=1
                    shared_prop.append(property)
                    object_shared_prop.append(objs_shared)
                    if sen: sen += ', '
                    
                    number_of_obj+=num_shared
                    sen11 = ''
                    sen11 += num_to_word(str(num_shared))+ ' other' if sen else num_to_word(str(num_shared))
                    shape = 1
                    for j in property:
                        sen11 += ' '+globals()['shape'](j[1])+'s' if j[0] == 'type' else ' '+globals()[j[0]](j[1])
                        if j[0] == 'type':
                             shape = 0
                        for os in objs_shared:
                            update_checked_obj_sc(os, sz, clr, sh, sc_rl)
                        clr, sz, sh, sc_rl = '','','',''
                    if shape:
                        sen11 += ' '+sh_ob()
                    _objects+=[sen11]
                    _object_id += [-1]
                    sen += sen11
            sen = add_and(sen)

            if which ==0: sen += ' in '+subject
            elif which == 1: sen += ' are in '+subject

        if sen == '':
            sen, number_of_obj =  I(O_R, which) 
            if which < 2:
                sen += ' '+subject 
    else:

        x = 0
        if x:
            if len(O_R)>1:
        
                sen = num_to_word(str(len(O_R)))+' '

                sen += sh_ob()
                if which == 0: sen += ' in '+subject
                def_obj = []
                for itr in range(len(O_R)):
                    update_checked_obj_sc(itr, sz, clr, sh, sc_rl)
                    def_obj.append(itr)
                recent_objs= [def_obj]
                
            else:
                sen += sh_ob_single()
                if sen == 'object': sen = 'an '+sen
                else: sen = 'a '+sen
                if which == 0: sen += ' in '+subject
                update_checked_obj_sc(0, sz, clr, sh, sc_rl)
                recent_objs = [[0]]
                
        else:
            sen, number_of_obj = I(O_R,which)
            if which < 2:
                sen += ' '+subject 
                
    if sen == ' ' or sen == 'are in a block' or sen == 'is in a block' or sen == 'in a block':
        sen, number_of_obj = I(O_R,which)
        if which < 2:
            sen += ' '+subject 
    if which == 0:
        if _objects:
            traj += [_objects]
            traj_obj_id += [_object_id] 
            
        if _rel: sp_ind+=[_rel]
        else: sp_ind +=[['in']]
            
    elif which == 1:
        if _objects:
            traj += [_objects]
            traj_obj_id += [_object_id]
        sp_ind += [['in']]
    else:
        if _objects:
            land_obj_id += [_object_id]
            land += [_objects]
    

    if object_shared_prop: recent_objs = object_shared_prop; add_num_name(recent_objs)

    if verb: 
        sen = ' are '+sen if number_of_obj > 1 else ' is '+sen
    return sen

def update_checked_obj_sc(n, sz, clr, sh, sc_rl,nth='', temp = False):
    
    global checked_obj_sc, temp_checked_obj_sc
    
        
    if temp: 
        if len(temp_checked_obj_sc) == 0: temp_checked_obj_sc.append([n, sz, clr, sh, sc_rl,nth]); return 
        else:
            for i in temp_checked_obj_sc:
                if i[0] == n:
                    if sz: i[1] = sz
                    if clr: i[2] = clr
                    if sh: i[3] = sh
                    if sc_rl: i[4] = sc_rl
                    if nth: i[5] = nth
                    return 
                
            temp_checked_obj_sc.append([n, sz, clr, sh, sc_rl,nth]); return
        
    if checked_obj_sc:
        check = 1
        for che in range(len(checked_obj_sc)):
            if checked_obj_sc[che][0] == n:
                if sz: checked_obj_sc[che][1] = sz
                if clr: checked_obj_sc[che][2]= clr
                if sh: checked_obj_sc[che][3] = sh
                if sc_rl: checked_obj_sc[che][4] =  sc_rl
                check = 0   
                break
        if check: checked_obj_sc.append([n, sz, clr, sh, sc_rl,nth])

    else: checked_obj_sc.append([n, sz, clr, sh, sc_rl,nth])
    if not temp and temp_checked_obj_sc: temp_checked_obj_sc.pop(-1)
    
def check_id(obj):
    id_obj = -1
    for ind,i in enumerate(checked_obj_sc):
        if i[0] == obj: id_obj = ind
    return int(id_obj)

def I(O_R, which):
    sen =''
    global sz, clr, sh, sc_rl, recent_objs, traj, land, sp_ind, traj_obj_id, land_obj_id
    rel_num, num_obj = 0, 0
    def_obj, traj1, traj_id = [], [], []
    for j,i in enumerate(O_R):
        x = random.choice([0,1,1,1])
        if j == len(O_R)-1 and sen == '': x=1
        if x:
            num_obj += 1
            if sen: sen += ', '
            _object = s_num() +Obj(i)
            traj1 += [_object]
            traj_id += [j]
            sen += _object
            update_checked_obj_sc(j, sz, clr, sh, sc_rl)
            clr, sz, sh, sc_rl = '','','',''
            def_obj.append([j])
            if num_obj> 2: break
    sen = add_and(sen)
    
    if which <2: traj += [traj1]; traj_obj_id += [traj_id]
    else: land += [traj1]; land_obj_id += [traj_id]
    if which == 0:
        sen += ' in'
    elif which == 1:
        sen+= ' are in' if num_obj > 1 else ' is in'
        
    return sen, num_obj 


def Obj(x):
    s = [1,1,1]
    #remove random choosing
#     s[0] = random.choice([0,1,1,1])
#     s[1] = random.choice([0,1,1,1])
#     s[2] = random.choice([0,1,1,1,1,1,1])
    
#     if s[0] == 0 and s[1] == 0 and s[2] ==0:
#         z = random.choice([0,1,2])
#         s[z] = 1
        
    Size = ' '+size(x[1]['size']) if s[0] else ''
    Color = ' '+color(x[1]['color']) if s[1] else ''
    Shape = ' '+shape(x[1]['type']) if s[2] else ' '+sh_ob_single()
    
    return Size+Color+Shape

# chose just part of the description
def Obj_random(x):
    s = [0,0,0]
    s[0] = random.choice([0,1])
    s[1] = random.choice([0,1])
    s[2] = random.choice([0,1])
    
    if s[0] == 0 and s[1] == 0 and s[2] ==0:
        z = random.choice([0,1,2])
        s[z] = 1
        
    Size = ' '+size(x[1]['size']) if s[0] else ''
    Color = ' '+color(x[1]['color']) if s[1] else ''
    Shape = ' '+shape(x[1]['type']) #if s[2] else ' '+sh_ob_single()
    
    return Size+Color+Shape

def color(x):
    global clr
    if x == '#0099ff': x = 'blue'
    else: x = x.lower()
    clr = {'color': x}
    return x

def size(x):
    global sz
    z = ''
    i = x
    if type(i) == str : i = int(i)
    if i == 10: z= 'small'
    elif i == 20: z= 'medium'
    elif i == 30: z= 'big'
    else: z= 'unknown'
    sz = {'size': z}
    return z    

def shape(x):
    global sh
    x = x.lower()
    sh = {'type': x}
    return x

def Rel(x):
    global sc_rl
    if x != 'in':
        sc_rl = {'rel':x}
    rel = ' '+x 
    return rel

def R(x):
    return 'to the '+x+' of' if x == 'right' or x == 'left' else x

def wh_th():
    sen = ''
    sen += 'which' if random.choice([0,1,1,1]) else 'that'
    return sen
    
def s_num(): #choose between a or one for block
    y = random.choice([0,1])
    return 'a' if y else 'one'
def one_blk():
    return 'one' if random.choice([0,1]) else 'block'
def num_to_word(x):
    n_w = {'0':'zero','1':'one', '2':'two', '3':'three', '4':'four', '5':'five', '6':'six', '7':'seven', '8':'eight', '9':'nine'}
    return n_w[x]

def sh_ob():
    return 'shapes' if random.choice([0,1]) else 'objects'
def sh_ob_single():
    return 'shape' if random.choice([0,1]) else 'object'
def nth(x):
    z = ['first','second', 'third', 'fourth', 'fifth', 'sixth', 'seventh']
    return z[x]
def reverse(word):
    words={'left':'right', 'right':'left', 'above':'below', 'below':'above'}
    if word in words: return words[word]
    else: return word
    
def reorder(x):
    
    z = x.copy()
    for j,i in enumerate(z):
        if 'size' in i:
            x.remove(i)
            x.insert(0,i)
        elif 'type' in i:
            x.remove(i)
            x.append(i)
            
    return x

def start_word(x): # make first character uppercase
    for i in range(len(x)):
        if x[i] != ' ':
            z = x[i].upper()+x[i+1:]
            return z
    

def ind_check_obj(obj):
    global checked_obj_sc
    ind = None
    obj_attr = checked_obj_sc
    for ind1,o_a in enumerate(obj_attr):
        if o_a[0] == obj: ind = ind1; break
    return ind

# should be checked
def unique_attr_check():
    global checked_obj_sc
    unique,list_all_attrs = [], []
    obj_attr = checked_obj_sc
    for scn in range(_num_scenes):
#         print('%%', obj_attr)
        for i in obj_attr:
            list_all_attrs += i
    unique = [ x for x in list_all_attrs if list_all_attrs.count(x) == 1]
    return unique

def name_call():
    x = random.choice([0,1])
    if x: return 'named'
    else: return 'called'


def name_block(num):
    name = ['A', 'B','C']
    return name[num]
      
def name_block_all(num):
    
    sen = ''
    x = random.choice([0,1])
    # we have three blocks, A,B and C.
    if x: 
        if num == 2: sen +=', A and B.'
        elif num == 3: sen += ', A, B and C.'
        else: sen+= ' ERROR'
    # We/lets call them A,B and C.
    else:
        y = random.choice([0,1]) # 1 -> we, 0 -> lets
        sen += '. We call them ' if y else '. Lets call them '
        if num == 2: sen += 'A and B.'
        elif num == 3: sen+= 'A, B and C.'
        else: sen+= 'Error.'
    return sen     

def name_block_single(name, coref = False):
    
    sen = ''
    x =random.choice([0,1,2,3])
    if x==0: sen = 'We call'
    elif x == 1: sen ="We name"
    elif x == 2: sen = "let's call"
    else: sen = "let's name"
    sen += ' it '+name if coref else ' this block '+name
    return sen

def object_num(num):
    z = ['one','two', 'three', 'four', 'five', 'six', 'seven']
    return z[num]

def add_and(x):
    sen = x
    index = sen.rfind(',')
    if index != -1:
        sen = list(sen)
        sen[index] = 'and'
        sen.insert(index, ' ')
        sen = ''.join(sen)
    return sen

def unique_with_rel(obj1, rel, obj2):

    similar_obj =[]
    for obj_obj in checked_obj_obj:
        if obj2 == obj_obj[0][1] and rel in obj_obj[1] and obj1 != obj_obj[0][0]: similar_obj+=[obj_obj[0][0]]
            
    ind_obj1= ind_check_obj(obj1)
    differ= [i for i in checked_obj_sc[ind_obj1][1:4] if i != '']
    
    for i in similar_obj:
        ind_i= ind_check_obj(i)
        differ = [i for i in differ if i not in checked_obj_sc[ind_i] and i != '']
        
    
    if differ:
        f = random.choice(differ)
        for i in enumerate(f):
            value_differ = f[i[1]]
            return value_differ+' '+sh_ob_single() if i[1]!= 'type' else value_differ
    else: return -1
    
def add_num_name(recent_objs):
    
    global checked_obj_sc
    pre_defined = recent_objs if recent_objs else '' # knowing objects that are referenced in the previous sentence.

    #the order of object for mentin them by it. the first object, or the second one.
    if len(pre_defined) >1:
        for ind, p_d in enumerate(pre_defined):
            if len(p_d)>1:
                for ind1, p in enumerate(p_d):
                    if len(p_d) > 1 :checked_obj_sc[check_id(p)][5] = ind1 
    elif len(pre_defined) == 1 :
        for ind, p_d in enumerate(pre_defined[0]):
            if len(pre_defined[0])>1: checked_obj_sc[check_id(p_d)][5] = ind

def check_number_for_obj():
    
    global checked_obj_sc, checked_obj_obj
    for ind, obj in enumerate(checked_obj_sc):
        check = 0
        if obj[5] != '':
            for obj_obj in checked_obj_obj:
                if obj[0] in obj_obj[0]: check =1; break
            if check == 0:
                checked_obj_sc[ind][5] = ''
        
        
def edit_text_form(story):
    f_story = ''
    
    # remove extra space
    tokens = story.split() 
    f_story = " ".join(tokens)
    
    # remove space before "." or "?"
    f_story = f_story.replace(' .', '.')
    f_story = f_story.replace(' ?', '?')
    #remove extra "."s
    f_story = f_story.replace('...', '.')
    f_story = f_story.replace('..', '.')
    
    return f_story
#**********************************************************
#*************The end of describing functions**************
#**********************************************************


#**********************************************************
#******************Annotation functions********************
#**********************************************************

def create_annotation(sen):
    
    global annotation , land, traj, sp_ind, traj_obj_id, land_obj_id
    
    
#     print('sentence: ', sen)
#     print('trajector:', traj, '\n Lnadmark', land,'\nSp-ind', sp_ind)
#     print('traj id: ', traj_obj_id)
#     print('land id: ', land_obj_id)
    check_edge_exist()
    if traj == []: print('!!! ERROR empty traj', sen) 
    if land == []: print('!!! ERROR empty land', sen) 
    if sp_ind == []: print('!!! ERROR empty sp_ind', sen) 
        
    sen = edit_text_form(sen)
    if sen[-1] != '.': sen += '.'
    
    ann = {"sentence": sen , "spatial_description" : []} 
    
    
    for ind in range(len(traj)):
        
        
        #trajector
        for tr_ind,tr in enumerate(traj[ind]):
            
            trajector = {"entity_id": traj_obj_id[ind][tr_ind], "block_id": 100+scene_num if traj_obj_id[ind][tr_ind] not in [100,101,102] else traj_obj_id[ind][tr_ind], "phrase": '', "head": '', "properties": {}, "spatial_property": '', "SOT_text": {"start": '', "end": ''}, "SOT_sentence": {"start": '', "end": ''}}
            _traj = edit_text_form(tr)
            trajector['phrase'] = _traj
            trajector['head'], trajector['properties'], trajector['spatial_property'] = extract_properties(_traj)
        
            #landmark
            for ld_ind,ld in enumerate(land[ind]):
                landmark = {"entity_id": land_obj_id[ind][ld_ind], "block_id": 100+scene_num if land_obj_id[ind][ld_ind] not in [100, 101,102] else land_obj_id[ind][ld_ind], "phrase": '', "head": '', "properties": [], "spatial_property": '', "SOT_text": {"start": '', "end": ''}, "SOT_sentence": {"start": '', "end": ''}}
                _land = edit_text_form(ld)
                landmark['phrase'] = _land
                landmark['head'], landmark['properties'], landmark['spatial_property'] = extract_properties(_land)
                
                for sp in sp_ind[ind]:
                    spatial_ind = { "phrase" : '', "SOT_text": {"start": '', "end": ''}, "SOT_sentence": {"start": '', "end": ''}}
                    spatial_ind['phrase'] = sp

                    spatial_value, g_type, s_type= spatial_indicator(sp, _land)
                    
                    # add 
                    ann['spatial_description'].append({"spatial_value": spatial_value, "g_type": g_type, "s_type": s_type, "polarity": False, "FoR": 'Relative', "trajector": trajector, 'landmark': landmark, 'spatial_indicator': spatial_ind})
                    
    annotation['annotations'].append(ann)
    land, traj, sp_ind = [], [], []
    traj_obj_id, land_obj_id = [], []
    
    
def spatial_indicator(sp, land):
    
    spatial_value, g_type, s_type = '', '', ''
    
    val1 = ['left', 'right', 'above', 'below']
    val2 = ['far from', 'near to']
    val3 = ['touching']
    val4 = ['in', 'has', 'contains', 'have', 'contain'] #edge for touching edge 
    
    if sp in val1:
        g_type = 'Direction'
        s_type = 'Relative'
        spatial_value = sp.upper()
        
    elif sp in val2:
        g_type = 'Distance'
        s_type = 'Qualitative'
        if 'far from' in sp: spatial_value = 'FAR' 
        elif 'near to' in sp: spatial_value = 'NEAR'
            
    elif sp in val4:
        g_type = 'Region'
        s_type = 'RCC8'
        
        if 'in' in sp: spatial_value = 'NTPP'
        else: spatial_value = 'NTPPI'
        
        if 'contain' in sp: spatial_value = 'NTPPI'
        
    elif sp in val3:
        g_type = 'Region'
        s_type = 'RCC8'
        if 'edge' in land: spatial_value = 'TPP'
        else: spatial_value = 'EC'
    
    return spatial_value, g_type, s_type


def extract_properties(sen):
    
    properties = {"color": '', "size": '', "name": '', "number": ''}
    spatial_property = ''
    head = ''
    
    #head (object)
    if "square" in sen: 
        head = 'squares' if 'squares' in sen else 'square'
    elif "circle" in sen: 
        head = 'circles' if 'circles' in sen else 'circle'
    elif "triangle" in sen: 
        head = 'triangles' if 'triangles'in sen else 'triangle'
    
    #head (block)
    elif "A" in sen: head ='A'
    elif "B" in sen: head ='B'
    elif "C" in sen: head ='C'
    elif "block" in sen: head ='block'
    else: head = sen
    
    #color
    if "blue" in sen: properties['color'] = 'blue'
    elif "black" in sen: properties['color'] = 'black'
    elif "yellow" in sen: properties['color'] = 'yellow'
 
        
    #size
    if "small" in sen: properties['size'] = 'small'
    elif "medium" in sen: properties['size'] = 'medium'
    elif "big" in sen: properties['size'] = 'big'

        
    #name
    if "number" in sen: 
        start = sen.find('number')
        properties['name']= sen[start:]
        
    #number
    number = ['a', 'an', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']
    tokens = sen.split()
    if tokens[0] != '.' and tokens[0] in number: properties['number'] = tokens[0]  
    elif len(tokens)>1  and tokens[1] != '.' and tokens[1] in number: properties['number'] = tokens[1]
        
    if 'edge' in sen:
        start = sen.find('edge')
        spatial_property = sen[:start+4]
    
    return head, properties, spatial_property


def SOT(story):
    
    global annotation, entity_phrases
    sum_char = 0
    for ann in annotation['annotations']:
        sum_char =story.find(ann['sentence'])
        if sum_char == -1: print('!!! ERROR sum char')
        _annot =  ann['sentence'][0].lower() + ann['sentence'][1:]
        _temp_ind = {}
        
        
        for ind, sp_desc in enumerate(ann['spatial_description']):
            
            #trajector
            start = [m.start() for m in re.finditer(sp_desc['trajector']['phrase'], _annot)]
            if start == []: print('!!! ERROR traj', _annot, sp_desc['trajector']['phrase'])
            if len(start) ==1: start = start[0]
            else:
                start1 = start
                for j in start1:
                    if _annot[j-1] and (_annot[j-1].isalpha() or _annot[j+len(sp_desc['trajector']['phrase'])].isalpha()): start.remove(j)
                    if 'lock' not in sp_desc['trajector']['phrase'] and _annot[j-5:j-1] and _annot[j-5:j-1] == 'lock': start.remove(j) # e.g, remove block C from all C find
                if len(start) ==1: start = start[0]
                else: 
                    if sp_desc['trajector']['phrase'] == 'it': start = start[0]
                    else: print('ERROR more than one phrase in TRAJ | ', sp_desc['trajector']['phrase'], ' | ', _annot, ' | ', sp_desc)              
            end = start + len(sp_desc['trajector']['phrase']) #- 1
            sp_desc['trajector']['SOT_sentence']['start'], sp_desc['trajector']['SOT_sentence']['end'] = start, end
            sp_desc['trajector']['SOT_text']['start'], sp_desc['trajector']['SOT_text']['end'] = start + sum_char, end + sum_char
            
            
            traj_end = end 
    
    
            #landmark
            start = [m.start() for m in re.finditer(sp_desc['landmark']['phrase'], _annot)]
            if start == []: print('!!! ERROR land', _annot, sp_desc['landmark']['phrase'])
            if len(start) ==1: start = start[0]
            else:
                start1 = start
                for j in start1:
                    if _annot[j-1] and (_annot[j-1].isalpha() or _annot[j+len(sp_desc['landmark']['phrase'])].isalpha()): start.remove(j)
                    if 'lock' not in sp_desc['landmark']['phrase'] and _annot[j-5:j-1] and _annot[j-5:j-1] == 'lock': start.remove(j) # e.g, remove block C from all C find
                if len(start) ==1: start = start[0]
                else: 
                    if sp_desc['landmark']['phrase'] == 'it': start = start[-1]
                    else: print('ERROR more than one phrase in LAND | ',sp_desc['landmark']['phrase'],'|', _annot, ' | ', sp_desc)
                
            end = start + len(sp_desc['landmark']['phrase']) #- 1
            sp_desc['landmark']['SOT_sentence']['start'], sp_desc['landmark']['SOT_sentence']['end'] = start, end
            sp_desc['landmark']['SOT_text']['start'], sp_desc['landmark']['SOT_text']['end'] = start + sum_char, end + sum_char
            
            
            land_end = end
    
            #spatial_indicator
            start = [m.start() for m in re.finditer(sp_desc['spatial_indicator']['phrase'], _annot)]
            if len(start)>1: 
                if sp_desc['spatial_indicator']['phrase'] not in _temp_ind: _temp_ind[sp_desc['spatial_indicator']['phrase']] = 0

            if start == []: print('!!! ERROR sp')
            if len(start) == 1: start1 = start[0]
            else: 
                
                start2 = start
                for j in start2:
                    if _annot[j-1] and (_annot[j-1].isalpha() or _annot[j+len(sp_desc['spatial_indicator']['phrase'])].isalpha()): start.remove(j)
                
                
                start2 = start
                if _annot[traj_end+1: traj_end+5] == 'with' or _annot[traj_end+1: traj_end+6] == 'which' or _annot[traj_end+1: traj_end+5] == 'that': 
                    for j in start2:
                        if j < traj_end and land_end > traj_end: start.remove(j)
                        elif land_end < traj_end and j> traj_end: start.remove(j)
                if len(start) > 1: 
                    if 'with' in _annot or 'which' in _annot or 'and' in _annot: #start1 = start[0]
                        start1 = start[_temp_ind[sp_desc['spatial_indicator']['phrase']]]
                        _temp_ind[sp_desc['spatial_indicator']['phrase']] += 1
                else: start1 = start[0]
        
            end = start1 + len(sp_desc['spatial_indicator']['phrase']) #- 1
            sp_desc['spatial_indicator']['SOT_sentence']['start'], sp_desc['spatial_indicator']['SOT_sentence']['end'] = start1, end
            sp_desc['spatial_indicator']['SOT_text']['start'], sp_desc['spatial_indicator']['SOT_text']['end'] = start1 + sum_char, end + sum_char
        
        _temp_ind = {}    
        sum_char = 0
        

def check_edge_exist():
    
    global sp_ind, land
    _temp = sp_ind
    for ind, i in enumerate(_temp):
        if 'edge' in sp_ind[ind][0]:
            for j in range(len(land[ind])):
                start = sp_ind[ind][j].find('the')
                land[ind][j] = sp_ind[ind][j][start:] +' '+ land[ind][j]
                sp_ind[ind][j] = 'touching'
    
