import random
import re
from Creating_story import name_block, reverse, R, Rel, size, color, shape, object_num, start_word, wh_th, s_num, edit_text_form

story_f,scn_scn,obj_attr,obj_obj,_num_scenes = '',[] ,[],[] ,-1
step_reasoning, step_r = 2, 0
pre_question_forbiden = []
steps_of_reasoning = 0
annotations = []
treshhold, max_tresh, min_tresh = 0, 2, 2
trajector, landmark, spatial_ind, _traj_or_land, _phrase = [], [], [], '',[]


def creating_questions(q_type, final_story, scn_scn1, obj_attr1, obj_obj1, num_scenes, forbiden_from_pre_Q):
    
    global story_f, scn_scn, obj_attr, obj_obj, _num_scenes,treshhold, max_tresh, min_tresh,step_reasoning, step_r, pre_question_forbiden, annotations, trajector, landmark, spatial_ind, main, _traj_or_land
    
    story_f,scn_scn,obj_attr,obj_obj,_num_scenes = '',[] ,[],[] ,-1
    step_reasoning, step_r = 2, 0
    steps_of_reasoning = 0
    treshhold, max_tresh, min_tresh = 0, 2, 2
    question, answer, start_end_c, candidate_answer, consistency, contrast, annotations, reasoning_type, indifinite = '', '',[],[] ,[], [],[], '', False
    
    story_f = final_story
    scn_scn = scn_scn1
    obj_attr = obj_attr1
    obj_obj = obj_obj1
    _num_scenes = num_scenes
    pre_question_forbiden = forbiden_from_pre_Q


    q_func_name = q_type+'_create_question'
    x, x_tresh = 0, 20
    while 1:
        
        x+=1
        if x>x_tresh: return -1
        
        annotations, trajector, landmark, spatial_ind, main, _traj_or_land= [], [], [], [], [], []
        try: 
            _temp = globals()[q_func_name]()
            if _temp == -1: continue
            else: question, answer, start_end_c, candidate_answer, consistency, contrast, reasoning_type, indifinite = _temp
            break
        except:
            raise
            pass
        
    
    question = edit_text_form(question)
#     print(annotations)
    return [question, answer, start_end_c, candidate_answer, consistency, contrast, annotations, reasoning_type, indifinite, pre_question_forbiden]


temporary_objs, first_temp = [], 1

def one_obj(obj11 = '', obj12='',scn11 = '',scn12 = '',set_scn = None):
    scn1,obj1 = '',''
    # choose object 1 from random scene and object on it
    if set_scn != None:
        scn1 = set_scn
    else:
        j=1
        while j:
            scn1 = random.choice(range(_num_scenes))
            if len(obj_attr[scn1]): j =0
    obj_ids1 = [x for x in range(len(obj_attr[scn1]))]
    if obj11 != '' and scn11 == scn1: obj_ids1.remove(obj11)
    if obj12 != '' and scn12 == scn1: obj_ids1.remove(obj12)
    if obj_ids1: obj1 = random.choice(obj_ids1)
    else: 
        j=1
        while j:
            scn1 = random.choice(range(_num_scenes))
            
            obj_ids1 = [x for x in range(len(obj_attr[scn1]))]
            if obj11 != '' and scn11 == scn1: obj_ids1.remove(obj11)
            if obj12 != '' and scn12 == scn1: obj_ids1.remove(obj12)
            if obj_ids1: obj1 = random.choice(obj_ids1)
            if len(obj_attr[scn1]) and obj1 != '': j =0
                
    
    return obj1,scn1

def one_obj_restricted(obj1, scn1,obj2= '',scn2=''):
    obj, scn = '',''
    while 1:
        scn = random.choice(range(_num_scenes))
        obj_list = [obj_attr[scn][x][0] for x in range(len(obj_attr[scn]))]
        if scn == scn1: obj_list.remove(obj1)
        if scn == scn2: obj_list.remove(obj2)
        if len(obj_list)== 0 : continue
        obj = random.choice(obj_list)
        break
    return obj, scn
    
def two_objs():
    
    obj1, obj2 = None,None
    
    # choose object 1 from random scene and object on it
    j = 1
    while j:
        scn1 = random.choice(range(_num_scenes))
        if len(obj_attr[scn1]): j = 0
    obj_ids1 = [x for x in range(len(obj_attr[scn1]))]
    obj1 = random.choice(obj_ids1)
    
    # choose object 2 from random scene and object on it
    scn_list = []
    for x in range(_num_scenes):
        if len(obj_attr[scn1])>1:
            scn_list += [x]*3 if x == scn1 else [x]
        else: 
            if x != scn1: scn_list += [x]*3
                
    j = 1
    while j:
        scn2 = random.choice(scn_list)
        if len(obj_attr[scn2]): j =0
    if scn1 == scn2: obj_ids2 = [x for x in range(len(obj_attr[scn2])) if x != obj1]
    else: obj_ids2 = [x for x in range(len(obj_attr[scn2]))]
    obj2 = random.choice(obj_ids2)
    
    return obj1,scn1, obj2,scn2

def two_objs_not_random(qtype = 'FR'):
    
    global pre_question_forbiden
    forbiden_list = []
    obj1,scn1, obj2, scn2 = None,None,None,None
    reasoning_type = ''
    if qtype == 'FR' or qtype== 'YN':

        obj1, scn1 = one_obj()
        
        for i in pre_question_forbiden:
            if [obj1,scn1] in i: forbiden_list += [x for x in i if x != [obj1, scn1]]
        
        rels_for_obj, other_rels_for_obj = all_rels_for_obj(obj1, scn1, forbiden_list= forbiden_list)
        
        trans_rels, reverse_rels = trans_reverse(rels_for_obj, obj1, scn1)

        if rels_for_obj and other_rels_for_obj:
            #decide chooce from the object in the same block or out of block
            if trans_rels: obj2, scn2 = random.choice(trans_rels)[0] , scn1; reasoning_type = 'transitivity'
            else: 
                x = random.choice([0,0,1])
                if x: # from the same block
                    #if trans_rels: obj2, scn2 = random.choice(trans_rels)[0] , scn1; reasoning_type = 'transitivity'
                    if reverse_rels: obj2, scn2 = random.choice(reverse_rels)[0] , scn1 ; reasoning_type = 'reverse'
                else:
                    choose =  random.choice(other_rels_for_obj)
                    obj2, scn2 = choose[0], choose[2]
                    reasoning_type = 'block'
                
        elif rels_for_obj: 
            if trans_rels: obj2, scn2 = random.choice(trans_rels)[0] , scn1; reasoning_type = 'transitivity'
            elif reverse_rels: obj2, scn2 = random.choice(reverse_rels)[0] , scn1 ; reasoning_type = 'reverse'         
        
        elif other_rels_for_obj:
            choose =  random.choice(other_rels_for_obj)
            obj2, scn2 = choose[0], choose[2]
            reasoning_type = 'block'
            
        else: 
            obj2, scn2 = one_obj_restricted(obj1, scn1)
            reasoning_type = 'none'
            if [obj2, scn2] in forbiden_list: return -1
            
    return obj1, scn1, obj2, scn2, reasoning_type

def trans_reverse(objs_rels, obj, scn):
    
    trans_list, reverse_list = [], []
    
    for i in objs_rels:
        check = 0
        for o_o in obj_obj[scn]:
            if [i[0], obj] in o_o: check = 1; reverse_list += [i]
        if check == 0:
            trans_list+= [i]
    return trans_list, reverse_list
    
def three_obj_not_random():
    obj, scn, obj1, scn1, obj2, scn2, relation= '','','','','','',''
    type_creating = None
    h, h_tresh = 0, 20
    while 1:
        obj, scn = one_obj()
        rels_for_obj, other_rels_for_obj = all_rels_for_obj(obj, scn, [], no_direct = True)
        
        total_rel = rels_for_obj
        total_rel.extend(other_rels_for_obj)
        if len(total_rel)>3:
            z, z_treshhold = 0, 20
            while 1:
                rel = random.choice(total_rel)
                rel_opt = []
                for x in total_rel:
                    if x[1] not in rel:
                        rel_opt += [x]
                if rel_opt: 
                    rel2 = random.choice(rel_opt)
                    if len(rel)==2: obj1, scn1, relation = rel[0], scn, reverse(rel[1])
                    elif len(rel) == 3: obj1, scn1, relation = rel[0], rel[2], reverse(rel[1])
                
                    if len(rel2) == 2: obj2, scn2 = rel2[0], scn  
                    elif len(rel2) == 3: obj2, scn2 = rel2[0], rel2[2]
                        
                    type_creating = 1
                    break
                z +=1
                if z > z_treshhold: break
            
            if z > z_treshhold:
                rels = random.sample(total_rel, 2)
                if len(rels[0]) ==2: obj1, scn1, relation = rels[0][0], scn, reverse(rels[0][1])
                elif len(rels[0]) == 3: obj1, scn1, relation = rels[0][0], rels[0][2], reverse(rels[0][1])
                    
                if len(rels[1]) ==2: obj2, scn2 = rels[1][0], scn
                elif len(rels[1]) == 3: obj2, scn2 = rels[1][0], rels[1][2]
                type_creating = 2 
                break
        elif len(total_rel)>2:
            all_rels = [x[1] for x in total_rel]
            relation = reverse(random.choice(all_rels))
            obj1, scn1 = one_obj_restricted(obj, scn)
            obj2, scn2 = one_obj_restricted(obj, scn, obj1, scn1)
            type_creating = 3
            break
        else: 
            h+=1
            if h > h_tresh: break
            continue
        
        if relation: break
        h+=1
        if h > h_tresh: break
    
    return obj, scn, obj1, scn1, obj2, scn2, relation, type_creating, total_rel
    
#**************************************
#***********Question part**************
#**************************************

def YN_create_question():
    
    global treshhold, temporary_objs, max_tresh, first_temp
    global trajector, landmark, spatial_ind, _traj_or_land, _phrase
    max_tresh = 1
    sen, answer, relation = '','', ''
    obj1,scn1,obj2,scn2 = two_objs()
    resoning_type = ''
    any_or_all,any_or_all_4,any_or_all_5 = [0,0],[0,0],[0,0] # 0 for if there is any object with this rel and 1 for checking all obj with this rel 
    contrast_set = []
    # sentences and answers for contrast set
    sen1, answer1 = '', '' # reverse the relation
    sen2, answer2 = '', '' # change the objects 
    sen3, answer3 = '', '' # reverse the relation and change the objects 
    sen4, answer4 = '', '' # contrast set -> change a,any to all
    sen5, answer5 = '', '' # contrast set -> change all to a,any
    
    
    correct_rel = FR_correct(obj1,scn1,obj2,scn2)
    x = random.choice([0,0,0,0,1])
    if x or ('NC' in correct_rel) or ('DK' in correct_rel) or (correct_rel == []): 
        relation = random.choice(['left','right','above','below','near to', 'far from', 'touching'])
    else:
        z = random.choice(range(len(correct_rel)))
        relation = correct_rel[z]
    obj1_defined, obj1s_temp = obj_definition(obj1, scn1, [obj2], obj2, scn2)

    traj1, land1, sp1, _phrase1 = trajector, landmark, spatial_ind, obj1_defined #_phrase1: start of object 1 definition
    traj1_len = len(traj1)

    traj = _traj_or_land if _traj_or_land else obj1_defined 
    trajector, landmark, spatial_ind, _traj_or_land =[], [], [], ''
    
    obj2_defined, obj2s_temp = obj_definition(obj2, scn2, [obj1], obj1, scn1)
    land = _traj_or_land if _traj_or_land else obj2_defined
    
    # start of object 2 definition
    _phrase = obj2_defined
    
    if obj1s_temp == [] or obj2s_temp == []: return -1
    trajector_len = len(trajector) # lenth of new trajector before adding other relations
    _phrase_main = ''
    
    if len(obj1s_temp) == 1 and len(obj2s_temp) == 1: # when the objects are unique by their definition
        z = random.choice([0,1])
        if z: 
            if add_the(obj1_defined): 
                obj1_defined = 'the '+obj1_defined; traj = 'the '+traj; 
                if traj1: traj1[-1][0] = 'the '+traj1[-1][0]; _phrase1 = 'the '+_phrase1
            if add_the(obj2_defined): 
                obj2_defined = 'the '+obj2_defined; land = 'the '+land; _phrase = 'the '+_phrase 
                if trajector: trajector[-1][0] = 'the '+trajector[-1][0]#; _phrase
            sen += 'Is '+obj1_defined+', '+R(relation)+' '+obj2_defined+'?'
            sen1 += 'Is '+obj1_defined+', '+R(reverse(relation))+' '+obj2_defined+'?'
            sen2 += 'Is '+obj2_defined+', '+R(relation)+' '+obj1_defined+'?'
            sen3 += 'Is '+obj2_defined+', '+R(reverse(relation))+' '+obj1_defined+'?'
            
            _phrase_main = obj1_defined[-5:]+', '+R(relation)+' '
            trajector, landmark, spatial_ind = [[traj]]+traj1+ trajector, [[land]]+land1+ landmark, [[relation]]+sp1+ spatial_ind
        else:
            if add_the(obj1_defined): 
                obj1_defined = 'a '+obj1_defined; traj = 'a ' + traj; 
                if traj1: traj1[-1][0] = 'a '+traj1[-1][0]; _phrase1 = 'a '+_phrase1
            if add_the(obj2_defined): 
                obj2_defined = 'a '+obj2_defined; land = 'a ' + land; 
                if trajector: trajector[-1][0] = 'a '+trajector[-1][0]; _phrase = 'a '+_phrase
                    
            sen += 'Is there '+obj1_defined+', '+R(relation)+' '+obj2_defined+'?'
            sen1 += 'Is there '+obj1_defined+', '+R(reverse(relation))+' '+obj2_defined+'?'
            sen2 += 'Is there '+obj2_defined+', '+R(relation)+' '+obj1_defined+'?'
            sen3 += 'Is there '+obj2_defined+', '+R(reverse(relation))+' '+obj1_defined+'?'
            
            _phrase_main = obj1_defined[-5:]+', '+R(relation)+' '
            trajector, landmark, spatial_ind = [[traj]]+traj1+ trajector, [[land]]+land1+ landmark, [[relation]]+sp1+ spatial_ind
        
    elif len(obj1s_temp) == 1 or len(obj2s_temp) == 1: 
        
        if len(obj1s_temp) == 1: 
            z = random.choice([0,1,2])
            if z==0: 
                if add_the(obj1_defined): 
                    obj1_defined = 'the '+obj1_defined; traj = 'the '+ traj; 
                    if traj1: traj1[-1][0] = 'the '+traj1[-1][0]; _phrase1 = 'the '+_phrase1
                sen += 'Is '+obj1_defined+', '+R(relation)+' all '+make_plural(obj2_defined, root = land)+'?'
                any_or_all = [0,1]
                sen1 += 'Is '+obj1_defined+', '+R(reverse(relation))+' all '+make_plural(obj2_defined, root = land)+'?'
                sen2 += 'Are all '+make_plural(obj2_defined, root = land)+', '+R(relation)+' '+obj1_defined+'?'
                sen3 += 'Are all '+make_plural(obj2_defined, root = land)+', '+R(reverse(relation))+' '+obj1_defined+'?'
                #contrast
                if add_the(obj2_defined): obj2_defined = 'a '+obj2_defined
                sen4 += 'Is '+obj1_defined+', '+R(relation)+' '+obj2_defined+'?'
                
                _phrase_main = obj1_defined[-5:]+', '+R(relation)+' all '
                _phrase = 'all '+make_plural(_phrase, root = land)
                land =  'all '+make_plural(land)
                if trajector: trajector[-1][0] = land
                trajector, landmark, spatial_ind = [[traj]]+traj1+ trajector, [[land]]+land1+ landmark, [[relation]]+sp1+ spatial_ind
                
            elif z == 1: 
                if add_the(obj1_defined): 
                    obj1_defined = 'the '+obj1_defined; traj = 'the '+ traj; 
                    if traj1: traj1[-1][0] = 'the '+traj1[-1][0]; _phrase1 = 'the '+_phrase1
                sen += 'Is '+obj1_defined+', '+R(relation)+' a '+obj2_defined+'?'
                sen1 += 'Is '+obj1_defined+', '+R(reverse(relation))+' a '+obj2_defined+'?'
                sen2 += 'Is a '+obj2_defined+', '+R(relation)+' '+obj1_defined+'?'
                sen3 += 'Is a '+obj2_defined+', '+R(reverse(relation))+' '+obj1_defined+'?'
                #contrast
                sen4 += 'Is '+obj1_defined+', '+R(relation)+' all '+make_plural(obj2_defined, root = land)+'?'; any_or_all_4= [0,1]
                
                _phrase_main = obj1_defined[-5:]+', '+R(relation)+' a '
                _phrase = ' a '+_phrase
                land = 'a '+ land
                if trajector: trajector[-1][0] = land
                trajector, landmark, spatial_ind = [[traj]]+traj1+ trajector, [[land]]+land1+ landmark, [[relation]]+sp1+ spatial_ind
                
            else: 
                if add_the(obj1_defined): 
                    obj1_defined = 'the '+obj1_defined; traj = 'the '+ traj; 
                    if traj1: traj1[-1][0] = 'the '+traj1[-1][0]; _phrase1 = 'the '+_phrase1
                sen += 'Is '+obj1_defined+', '+R(relation)+' any '+ make_plural(obj2_defined, root = land)+'?'
                sen1 += 'Is '+obj1_defined+', '+R(reverse(relation))+' any '+ make_plural(obj2_defined, root = land)+'?'
                sen2 += 'Is there any '+make_plural(obj2_defined, root = land)+', '+R(relation)+' '+ obj1_defined+'?'
                sen3 += 'Is there any '+make_plural(obj2_defined, root = land)+', '+R(reverse(relation))+' '+ obj1_defined+'?'
                #contrast
                sen4 += 'Is '+obj1_defined+', '+R(relation)+' all '+make_plural(obj2_defined, root = land)+'?'; any_or_all_4= [0,1]
                
                _phrase_main = obj1_defined[-5:]+', '+R(relation)+' any '
                _phrase = 'any '+make_plural(_phrase, root = land)
                land = 'any '+make_plural(land)
                if trajector: trajector[-1][0] = land
                trajector, landmark, spatial_ind = [[traj]]+traj1+ trajector, [[land]]+land1+ landmark, [[relation]]+sp1+ spatial_ind
        else:
            z = random.choice([0,1, 2])
            if z ==0 :
                if add_the(obj2_defined): 
                    obj2_defined = 'the '+obj2_defined; land = 'the '+ land ; 
                    if trajector: trajector[-1][0] = 'the '+trajector[-1][0]; _phrase = 'the '+_phrase
                sen += 'Are all '+make_plural(obj1_defined, root = traj)+', '+R(relation)+' '+obj2_defined+'?'
                any_or_all = [1,0]
                sen1 += 'Are all '+make_plural(obj1_defined, root = traj)+', '+R(reverse(relation))+' '+obj2_defined+'?'
                sen2 += 'Is '+obj2_defined+', '+R(relation)+' all '+make_plural(obj1_defined, root = traj)+'?'
                sen3 += 'Is '+obj2_defined +', '+R(reverse(relation))+' all ' +make_plural(obj1_defined, root = traj)+'?'
                #contrast
                sen4 += 'Is there any'+make_plural(obj1_defined, root = traj)+', '+R(relation)+' '+obj2_defined+'?'
                
                _phrase_main = make_plural(obj1_defined, root = traj)[-5:]+', '+R(relation)+' '
                _phrase1 = 'all '+make_plural(_phrase1, root = traj)
                traj = 'all '+make_plural(traj)
                if traj1: traj1[-1][0] = traj
                trajector, landmark, spatial_ind = [[traj]]+traj1+ trajector, [[land]]+land1+ landmark, [[relation]]+sp1+ spatial_ind
                
            elif z == 1: 
                if add_the(obj2_defined): 
                    obj2_defined = 'the '+obj2_defined; land = 'the '+ land; 
                    if trajector: trajector[-1][0] = 'the '+trajector[-1][0]; _phrase = 'the '+_phrase
                sen += 'Is there a '+obj1_defined+', '+R(relation)+' '+obj2_defined+'?'
                sen1 += 'Is there a '+obj1_defined+', '+R(reverse(relation))+' '+obj2_defined+'?'
                sen2 += 'Is'+obj2_defined+', '+R(relation)+' a '+obj1_defined+'?'
                sen3 += 'Is '+obj2_defined+', '+R(reverse(relation))+' a '+obj2_defined+'?'
                #contrast
                sen4 += 'Are all '+make_plural(obj1_defined, traj)+', '+R(relation)+' '+obj2_defined+'?'; any_or_all_4= [1,0]
                
                _phrase_main = obj1_defined[-5:]+', '+R(relation)+' '
                _phrase1 = 'a '+_phrase1
                traj = 'a '+ traj
                if traj1: traj1[-1][0] = traj
                trajector, landmark, spatial_ind = [[traj]]+traj1+ trajector, [[land]]+land1+ landmark, [[relation]]+sp1+ spatial_ind
            else:
                if add_the(obj2_defined): 
                    obj2_defined = 'the '+obj2_defined ; land = 'the '+ land; 
                    if trajector: trajector[-1][0] = 'the '+trajector[-1][0]; _phrase = 'the '+_phrase
                sen += 'Is there any '+make_plural(obj1_defined, root = traj)+', '+R(relation)+' '+obj2_defined+'?'
                sen1 += 'Is there any '+make_plural(obj1_defined, root = traj)+', '+R(reverse(relation))+' '+obj2_defined+'?'
                sen2 += 'Is '+obj2_defined+', '+R(relation)+' any '+make_plural(obj1_defined, root = traj)+'?'
                sen3 += 'Is '+obj2_defined+', '+R(reverse(relation))+' any '+make_plural(obj1_defined, root = traj)+'?'
                #contrast
                sen4 += 'Are all '+make_plural(obj1_defined, root = traj)+', '+R(relation)+' '+obj2_defined+'?'; any_or_all_4= [1,0]
                
                _phrase_main = make_plural(obj1_defined, root = traj)[-5:]+', '+R(relation)+' '
                _phrase1 = 'any '+make_plural(_phrase1, root = traj)
                traj = 'any '+make_plural(traj)
                if traj1: traj1[-1][0] = traj
                trajector, landmark, spatial_ind = [[traj]]+traj1+ trajector, [[land]]+land1+ landmark, [[relation]]+sp1+ spatial_ind
    
    else: 
        z = random.choice([0,1,2,3])
        if z==0: 
            sen += 'Is there any '+make_plural(obj1_defined, root = traj)+', '+R(relation)+' a '+obj2_defined+'?'
            sen1 += 'Is there any '+make_plural(obj1_defined, root = traj)+', '+R(reverse(relation))+' a '+obj2_defined+'?'
            sen2 += 'Is a '+obj2_defined +', '+R(relation)+' any '+make_plural(obj1_defined, root = traj)+'?'
            sen3 += 'Is a '+obj2_defined+', '+R(reverse(relation))+' any '+make_plural(obj1_defined, root = traj)+'?'
            #contrast
            sen4 += 'Are all '+make_plural(obj1_defined, root = traj)+', '+R(relation)+' a '+obj2_defined+'?'; any_or_all_4= [1,0]
            sen5 += 'Is there any '+make_plural(obj1_defined, root = traj)+', '+R(relation)+' all '+make_plural(obj2_defined, root = land)+'?'; any_or_all_5= [0,1]
            
            _phrase_main = make_plural(obj1_defined, root = traj)[-5:]+', '+R(relation)+' a '
            _phrase1 = 'any '+make_plural(_phrase1, root = traj)
            _phrase = 'a '+_phrase
            traj, land =  'any '+ make_plural(traj) , 'a '+ land
            if trajector: trajector[-1][0] = land
            if traj1: traj1[-1][0] = traj
            trajector, landmark, spatial_ind = [[traj]]+traj1+ trajector, [[land]]+land1+ landmark, [[relation]]+sp1+ spatial_ind
            
        elif z == 1: 
            sen += 'Is there a '+obj1_defined+', '+R(relation)+' all '+make_plural(obj2_defined, root = land)+'?'
            any_or_all = [0,1]
            sen1 += 'Is there a '+obj1_defined+', '+R(reverse(relation))+' all '+make_plural(obj2_defined, root = land)+'?'
            sen2 += 'Are all '+make_plural(obj2_defined, root = land)+', '+R(relation)+' a '+obj1_defined+'?'
            sen3 += 'Are all '+make_plural(obj2_defined, root = land)+', '+R(reverse(relation))+' a '+obj1_defined +'?'
            #contrast
            sen4 += 'Are all '+make_plural(obj1_defined, root = traj)+', '+R(relation)+' all '+make_plural(obj2_defined, root = land)+'?'; any_or_all_4= [1,1]
            sen5 += 'Is there a '+obj1_defined+', '+R(relation)+' a '+obj2_defined+'?'
            
            _phrase_main = obj1_defined[-5:]+', '+R(relation)+' all '
            _phrase = 'all '+make_plural(_phrase, root = land)
            _phrase1 = 'a '+_phrase1
            traj, land = 'a '+ traj, 'all '+ make_plural(land)
            if trajector: trajector[-1][0] = land
            if traj1: traj1[-1][0] = traj
            trajector, landmark, spatial_ind = [[traj]]+traj1+ trajector, [[land]]+land1+ landmark, [[relation]]+sp1+ spatial_ind
            
        elif z == 2: 
            sen += 'Are all '+make_plural(obj1_defined, root = traj)+', '+R(relation)+' a '+obj2_defined+'?'
            any_or_all = [1,0]
            sen1 += 'Are all '+make_plural(obj1_defined, root = traj)+', '+R(reverse(relation))+' a '+obj2_defined+'?'
            sen2 += 'Is a '+obj2_defined+', '+R(relation)+' all '+make_plural(obj1_defined, root = traj)+'?'
            sen3 += 'Is a '+obj2_defined+', '+R(reverse(relation))+' all '+make_plural(obj1_defined, root = traj)+'?'
            #contrast
            sen4 += 'Are all '+make_plural(obj1_defined, root = traj)+', '+R(relation)+' all '+make_plural(obj2_defined, root = land)+'?'; any_or_all_4= [1,1]
            sen5 += 'Is there a '+obj1_defined+', '+R(relation)+' a '+obj2_defined+'?'
            
            _phrase_main = make_plural(obj1_defined, root = traj)[-5:]+', '+R(relation)+' a '
            _phrase1 = 'all '+make_plural(_phrase1, root = traj)
            _phrase = 'a '+_phrase
            traj, land = 'all '+ make_plural(traj), 'a '+ land
            if trajector: trajector[-1][0] = land
            if traj1: traj1[-1][0] = traj
            trajector, landmark, spatial_ind = [[traj]]+traj1+ trajector, [[land]]+land1+ landmark, [[relation]]+sp1+ spatial_ind
            
        else:
            sen += 'Are all '+make_plural(obj1_defined, root = traj)+', '+R(relation)+' all '+make_plural(obj2_defined, root = land)+'?'
            any_or_all = [1,1]
            sen1 += 'Are all '+make_plural(obj1_defined, root = traj)+', '+R(reverse(relation))+' all '+make_plural(obj2_defined, root = land)+'?'
            sen2 += 'Are all '+make_plural(obj2_defined, root = land)+', '+R(relation)+' all '+make_plural(obj1_defined, root = traj)+'?'
            sen3 += 'Are all '+make_plural(obj2_defined, root = land)+', '+R(reverse(relation))+' all '+make_plural(obj1_defined, root = traj)+'?';
            #contrast
            sen4 += 'Are all '+make_plural(obj1_defined, root = traj)+', '+R(relation)+' any '+make_plural(obj2_defined, root = land)+'?'; any_or_all_4= [1,0]
            sen5 += 'Is there a '+obj1_defined+', '+R(relation)+' all '+make_plural(obj2_defined, root = land)+'?'; any_or_all_5= [0,1]
            
            _phrase_main = make_plural(obj1_defined, root = traj)[-5:]+', '+R(relation)+' all '
            _phrase, _phrase1 = 'all '+make_plural(_phrase, root = land), 'all '+make_plural(_phrase1, root = traj)
            traj, land = 'all '+ make_plural(traj), 'all '+ make_plural(land)
            if trajector: trajector[-1][0] = land
            if traj1: traj1[-1][0] = traj
            trajector, landmark, spatial_ind = [[traj]]+traj1+ trajector, [[land]]+land1+ landmark, [[relation]]+sp1+ spatial_ind
    
    
    answer = answer_YN(obj1,scn1,obj1s_temp, obj2, scn2, obj2s_temp, relation, any_or_all)
    
    _phrase = [[_phrase_main]]+[[_phrase1]]*traj1_len +[[_phrase]]*trajector_len
    create_annotation(sen, 0)
    #consistency
    answer1 = answer_YN(obj1,scn1,obj1s_temp, obj2, scn2, obj2s_temp, reverse(relation), any_or_all)
    answer2 = answer_YN(obj2,scn2,obj2s_temp, obj1, scn1, obj1s_temp, relation, [any_or_all[1],any_or_all[0]])
    answer3 = answer_YN(obj2,scn2,obj2s_temp, obj1, scn1, obj1s_temp, reverse(relation), [any_or_all[1],any_or_all[0]])
    
    consistency_list = [[edit_text_form(sen1), answer1, [], []],[edit_text_form(sen2), answer2, [], []],[edit_text_form(sen3), answer3, [], []]]
    consistency_random = random.choice([0,1,2])
    consistency_list.pop(consistency_random)
    
    #contrast
    if sen4: 
        answer4 = answer_YN(obj1,scn1,obj1s_temp, obj2, scn2, obj2s_temp, relation, any_or_all_4)
        if answer4 != answer:
            contrast_set.append([edit_text_form(sen4), answer4, [], []])
    if sen5: 
        answer5 = answer_YN(obj1,scn1,obj1s_temp, obj2, scn2, obj2s_temp, relation, any_or_all_5)
        if answer5 != answer:
            contrast_set.append([edit_text_form(sen5), answer5, [], []])
    
    max_tresh = 2
    
    
    indifinite = True if 'DK' in answer else False
    
    return [sen, answer, [], [], consistency_list, contrast_set, resoning_type, indifinite]
    
def CO_create_question():
    
    global treshhold, temporary_objs, min_tresh, max_tresh, first_temp
    global trajector, landmark, spatial_ind, _traj_or_land, _phrase
    _phrase_temp = []
    sen, answer, reasoning_type = '','', ''
    obj, scn = '',''
    obj1,obj2,scn1,scn2 = '','','',''
    start_end_c, candidate_answer = [], []
    contrast_set,consistency_list = [],[]
    #for contrast set
    sen1, answer1, candidate_answer1 = '', [], []
    sen2, answer2, candidate_answer2 = '', [], []
    sen3, answer3, candidate_answer3 = '', [], []
    sen4, answer4, candidate_answer4 = '', [], []
    
    unique_obj = False #if we have a unique obj then we can ask question in two form. what is below the ob? which obj is below a obj? 
    unique_obj1_2 = False

    obj, scn, obj1, scn1, obj2, scn2, relation, type_of_creating, anchor_total_rel = three_obj_not_random()
    
    #if there is not any obj1 and obj2 back to choosing object again.
    if not obj1 and not obj2: return -1
    #defining object in the question
    forbiden_list = []
    if scn1 == scn: forbiden_list.append(obj1)
    if scn2 == scn: forbiden_list.append(obj2)
    max_tresh = 1
    max_treshhold = 1
    obj_defined, objs_temp = obj_definition(obj, scn, forbiden_list=forbiden_list, max_treshhold = max_treshhold)
    len_traj = len(trajector)


    _land = _traj_or_land if _traj_or_land else obj_defined
    
    if len(objs_temp) == 1 and [obj, scn] in objs_temp: unique_obj = True  
        
    # defining the first object
    obj1_defined, obj1s_temp = obj_definition(obj1, scn1, [obj2, obj], obj2, scn2, max_treshhold = max_treshhold)
        
    if(len(obj1s_temp) == 1 and [obj1,scn1] in obj1s_temp) or ( len(obj1s_temp)==2 and [obj1,scn1] in obj1s_temp and [obj2,scn2] in obj1s_temp):
        unique_obj1_2 = True
        x = random.choice([0,1]) if unique_obj else 1
    elif unique_obj: x = 0
    else: return -1
    
    len_traj_obj1 = len(trajector) - len_traj


    
    # defining the second object
    obj2_defined, obj2s_temp = obj_definition(obj2, scn2, [obj1, obj], obj1, scn1,max_treshhold = max_treshhold)
    if not ((len(obj2s_temp) == 1 and [obj2,scn2] in obj2s_temp) or ( len(obj2s_temp)==2 and [obj1,scn1] in obj2s_temp and [obj2,scn2] in obj2s_temp)) or obj1_defined == obj2_defined: return -1
    
    if obj1_defined == obj2_defined: print('THE SAME ',obj1, scn1, obj2, scn2,'\n', obj1_defined,'\n',obj2_defined)
    
    len_traj_obj2 = len(trajector) - len_traj_obj1 - len_traj


    order = 0
    
    _sen = ''
    spatial_ind = [[relation]] + spatial_ind
    
    if x == 1:
        sen += 'Which object is '+ R(relation)+' a '+obj_defined +'? '
        #_sen = sen

        landmark = [['a '+_land]] + landmark
        
        if reverse(relation) != relation: sen2 = 'Which object is '+ R(reverse(relation))+' a '+obj_defined +'? '#sen
        if len_traj > 0: trajector[0][0] = 'a '+ trajector[0][0]
        
        #add the to objects definition
#         ob1, ob2 = False, False
        if add_the(obj1_defined):

#             ob1 = True
            obj1_defined = 'the '+obj1_defined
            if len_traj_obj1 >0: 
                if len_traj_obj1 > 1 and trajector[len_traj][0] == trajector[len_traj+1][0]:
                    trajector[len_traj+1][0] = 'the '+trajector[len_traj+1][0]
                trajector[len_traj][0] = 'the '+trajector[len_traj][0]
        
        if add_the(obj2_defined): 

#             ob2 = True
            obj2_defined = 'the '+obj2_defined
            if len_traj_obj2 > 0: 
                if len_traj_obj2 > 1 and trajector[len_traj+len_traj_obj1 + 1] == trajector[len_traj+len_traj_obj1]:
                    trajector[len_traj+len_traj_obj1+1][0] = 'the '+trajector[len_traj+len_traj_obj1+1][0]
                trajector[len_traj+len_traj_obj1][0] = 'the '+trajector[len_traj+len_traj_obj1][0]
                
        # the order of object 1 and 2 in question
        if random.choice([0,1]):
            candidate_answer = [obj1_defined, obj2_defined, "both of them", "none of them"]
            sen += obj1_defined+' or '+obj2_defined+'?'
            sen1 += obj1_defined+' or '+obj2_defined+'?'
            if reverse(relation) != relation: sen2 += obj1_defined+' or '+obj2_defined+'?'
            sen4 += obj1_defined+' or '+obj2_defined+'?'
            order = 1
        else:
            candidate_answer = [obj2_defined, obj1_defined, "both of them", "none of them"]
#             if add_the(obj1_defined): obj1_defined = 'the '+obj1_defined
#             if add_the(obj2_defined): obj2_defined = 'the '+obj2_defined
            sen += obj2_defined+' or '+obj1_defined+'?'
            sen1 += obj2_defined+' or '+obj1_defined+'?'
            if reverse(relation) != relation: sen2 += obj2_defined+' or '+obj1_defined+'?'
            sen4 += obj2_defined+' or '+obj1_defined+'?'
            order = 0
            
        candidate_answer2 = candidate_answer
        
        if len_traj_obj1: 
            obj_d = obj1_defined# if ob1 else 'the '+ obj1_defined 
            _phrase_temp += [[obj_d]]*(len_traj_obj1)
        if len_traj_obj2: 
            obj_d = obj2_defined #if ob2 else 'the '+ obj2_defined
            _phrase_temp += [[obj_d]]*(len_traj_obj2)
        _phrase = [[' is ']]+[['a '+obj_defined ]]*len_traj+ _phrase_temp if len_traj>0 else [[' is ']]+ _phrase_temp
    
    else:
        if add_the(obj_defined): 
            obj_defined = 'the '+obj_defined;
            _land = 'the '+_land
            if len_traj > 0: trajector[0][0] = 'the '+ trajector[0][0]
                
        sen += 'What is '+ R(relation)+' '+obj_defined +'? '
        #_sen = sen
#         _phrase = [['What'],[' the '+obj_defined ]]+ _phrase_temp if len_traj>1 else [['What']]+ _phrase_temp
        landmark = [[_land]] + landmark
        if reverse(relation) != relation: sen2 = 'What is '+ R(reverse(relation))+' '+obj_defined +'? '#sen
        if random.choice([0,1]):
            sen += 'a '+obj1_defined+' or a '+obj2_defined+'?'
            sen1 += 'a '+obj1_defined+' or a '+obj2_defined+'?'
            if reverse(relation) != relation:sen2 += 'a '+obj1_defined+' or a '+obj2_defined+'?'
            sen4 += 'a '+obj1_defined+' or a '+obj2_defined+'?'
            candidate_answer = [obj1_defined, obj2_defined, "both of them", "none of them"]
            order = 1
        else:
            sen += 'a '+obj2_defined+' or a '+obj1_defined+'?'
            sen1 += 'a '+obj2_defined+' or a '+obj1_defined+'?'
            if reverse(relation) != relation: sen2 += 'a '+obj2_defined+' or a '+obj1_defined+'?'
            sen4 += 'a '+obj2_defined+' or a '+obj1_defined+'?'
            candidate_answer = [obj2_defined, obj1_defined, "both of them", "none of them"]
            order = 0
        candidate_answer2 = candidate_answer
        
        if len_traj_obj1 > 0: 
            if len_traj_obj1 > 1 and trajector[len_traj][0] == trajector[len_traj+1][0]:
                trajector[len_traj+1][0] = 'a '+trajector[len_traj+1][0]
            trajector[len_traj][0] = 'a '+trajector[len_traj][0]
        
        if len_traj_obj2 > 0: 
            if len_traj_obj2 > 1 and trajector[len_traj+len_traj_obj1][0] == trajector[len_traj+len_traj_obj1+1][0]:
                trajector[len_traj+len_traj_obj1+1][0] = 'a '+trajector[len_traj+len_traj_obj1+1][0]
            trajector[len_traj+len_traj_obj1][0] = 'a '+trajector[len_traj+len_traj_obj1][0]
        
        if len_traj_obj1: _phrase_temp += [['a '+obj1_defined]]*(len_traj_obj1)
        if len_traj_obj2: _phrase_temp += [['a '+obj2_defined]]*(len_traj_obj2)
        _phrase = [[' is ']]+[[obj_defined ]]*len_traj+  _phrase_temp if len_traj>0 else [[' is ']]+ _phrase_temp


    answer = answer_CO_0(obj,scn,objs_temp, obj1, scn1, obj1s_temp, obj2, scn2, obj2s_temp, relation, obj1_defined, obj2_defined, order, x)
    trajector = [['']] + trajector

    create_annotation(sen, 0)
    
    #Another consistency
    rel = None
    if answer == [0]:
        if order == 1: #obj1
            if scn2 != scn: 
                try: rel = random.choice([y for y in find_rel_two_scn(scn2,scn) if y != relation])  
                except: pass
            else:  
                try: rel = random.choice([y for y in find_rel_two_objs(scn2, obj2, obj) if y != relation]) # from different scene    
                except: pass
        else: #obj2
            if scn1 != scn: 
                try: rel = random.choice([y for y in find_rel_two_scn(scn1,scn) if y != relation])  
                except: pass
            else: 
                try: rel = random.choice([y for y in find_rel_two_objs(scn1, obj1, obj) if y != relation]) # from different scene
                except: pass
    elif answer == [1]:
        if order == 1: # obj2
            if scn1 != scn: 
                try: rel = random.choice([y for y in find_rel_two_scn(scn1,scn) if y != relation])  
                except: pass
            else: 
                try: rel = random.choice([y for y in find_rel_two_objs(scn1, obj1, obj) if y != relation]) # from different scene
                except: pass
        else: #obj1
            if scn2 != scn: 
                try: rel = random.choice([y for y in find_rel_two_scn(scn2,scn) if y != relation])  
                except: pass
            else: 
                try: rel = random.choice([y for y in find_rel_two_objs(scn2, obj2, obj) if y != relation]) # from different scene
                except: pass

    elif answer == [2]:
        rel = random.choice([ y[1] for y in anchor_total_rel if y[1]!= relation])
    else:
        rel1, rel2 = '', ''
        if scn1 != scn: 
            try: rel1 = random.choice([y for y in find_rel_two_scn(scn1,scn) if y != relation])  
            except: pass
        else:  
            try: rel =random.choice([y for y in find_rel_two_objs(scn1, obj1, obj) if y != relation])
            except: pass
        
        if scn2 != scn: 
            try: rel2 = random.choice([y for y in find_rel_two_scn(scn2,scn) if y != relation])  
            except: pass
        else:  
            try: rel =random.choice([y for y in find_rel_two_objs(scn2, obj2, obj) if y != relation])
            except: pass
        
        if rel1 and rel2: rel = random.choice([rel1, rel2])
        elif rel1: rel = rel1
        elif rel2: rel = rel2
    
    if rel != None:        
        answer4 = answer_CO_0(obj,scn,objs_temp, obj1, scn1, obj1s_temp, obj2, scn2, obj2s_temp, rel, obj1_defined, obj2_defined, order, x)
        if x == 1 and add_the(obj_defined): obj_def4 = 'a '+ obj_defined
        elif x == 0 and add_the(obj_defined): obj_def4 = 'the '+ obj_defined
        else: obj_def4 = obj_defined
        sen4 = 'What is '+ R(rel)+' '+obj_def4 +'? '+ sen4
        consistency_list += [[sen4, answer4, [], candidate_answer]] 
    
        
    rel11 = random.choice(['left', 'right', 'above', 'below','left', 'right', 'above', 'below','left', 'right', 'above', 'below', 'near to', 'far from', 'touching'])
    if x == 1 and add_the(obj_defined): obj_def2 = 'a '+ obj_defined
    elif x == 0 and add_the(obj_defined): obj_def2 = 'the '+ obj_defined
    else: obj_def2 = obj_defined
    sen1 = 'Which object is '+ R(rel11)+' '+obj_def2 +'?'+ sen1
    sen1 = edit_text_form(sen1)
        
    answer1 = answer_CO_0(obj,scn,objs_temp, obj1, scn1, obj1s_temp, obj2, scn2, obj2s_temp, rel11, obj1_defined, obj2_defined, order, x)
    candidate_answer1 = candidate_answer

    if answer1 != answer: contrast_set += [[sen1, answer1, start_end_c, candidate_answer1]]
        
    #consistency
    answer2 = answer_CO_0(obj,scn,objs_temp, obj1, scn1, obj1s_temp, obj2, scn2, obj2s_temp, reverse(relation), obj1_defined, obj2_defined, order, x)
    if reverse(relation) != relation: consistency_list += [[sen2, answer2, start_end_c, candidate_answer2]]
    

    return [sen, answer, start_end_c, candidate_answer, consistency_list, contrast_set, reasoning_type, False]



def FB_create_question():
    
    global treshhold, temporary_objs, min_tresh, max_tresh, first_temp
    global trajector, landmark, spatial_ind, _traj_or_land, _phrase
    
    sen,answer ='',''
    obj, scn = one_obj()
    objs_temp =[]
    start_end_c = []
    max_treshhold = 2
    
    candidate_answer = ['A', 'B'] if _num_scenes == 2 else ['A', 'B', 'C'] # one block stories do not have FB questions
    
    if _num_scenes > 1:
        obj_defined, objs_temp = obj_definition(obj, scn, max_treshhold = max_treshhold)
        

        len_land = len(landmark)
        _article = ''
        x =random.choice([0,1])
        sen += 'Which blocks have a '+ obj_defined+ '?'
        answer, start_end_c = answer_FB(obj,scn,objs_temp)
        
        polarity = False
        _article = 'a '
        
        if x: # do not have
            sen = "Which blocks don't have any "+ obj_defined+ '?'
            polarity, _article = True, 'any '
            
            spatial_ind = [['have']] + spatial_ind
            if trajector: trajector[-1][0] = 'any '+ trajector[-1][0]
            trajector = [['']] + trajector
            _phrase = [['Which']] + [['any '+obj_defined]]*len_land
            #consistency
            sen1 = 'Which blocks have any '+ obj_defined+ '?'
            answer1 = answer
            consistency_list = [[sen1, answer1, [], candidate_answer]]
            
            answer = [item for item in candidate_answer if item not in answer]
            
        else: #have 
            spatial_ind = [['have']] + spatial_ind
            if trajector: trajector[-1][0] = 'a '+ trajector[-1][0]
            trajector = [['']] + trajector
            #consistency
            sen1 = "Which blocks don't have any "+ obj_defined+ '?'
            answer1 = [item for item in candidate_answer if item not in answer]
            consistency_list = [[sen1, answer1, [], candidate_answer]]
        
            _phrase = [['Which']] + [['a '+obj_defined]]*len_land
            
        landmark = [[_article+_traj_or_land]] + landmark if _traj_or_land else [[_article+obj_defined]] + landmark
        create_annotation(sen, main = 0, polarity = polarity)
        
    else: sen = 'Cannot create a FB question!'
    
    #Contast set
    contrast_set= []
    
    return [sen, answer, start_end_c, candidate_answer, consistency_list, contrast_set, '', False]

def FR_create_question():
    
    global temporary_objs, first_temp, max_tresh, pre_question_forbiden
    global trajector, landmark , spatial_ind, _traj_or_land, _phrase
    _phrase_temp = []
    sen =''
    x_treshhold = 20
    __temp = two_objs_not_random('FR')
    if __temp == -1: return -1
    else: obj1, scn1, obj2, scn2, reasoning_type = __temp
        
    obj1s_temp, obj2s_temp =[],[]
    traj, land, sp_ind = [], [], []
    forb = []
    
    x = 0 # a treshhold for using unique objects
    while 1:
        trajector, landmark, spatial_ind, _traj_or_land = [], [], [], []
        forb = [obj2] if scn1 == scn2 else []
        obj1_defined, obj1s_temp, inter_obj_1 = obj_definition(obj1, scn1, forb, obj2, scn2, intermediate_obj= True)
        if len(obj1s_temp) == 1 and [obj1, scn1] in obj1s_temp: break
        x+=1
        if x > x_treshhold: 
            trajector, landmark, spatial_ind, _traj_or_land = [], [], [], []
            obj1_defined, obj1s_temp, inter_obj_1 = obj_definition(obj1, scn1, forb, obj2, scn2, max_treshhold = 1, intermediate_obj= True)
            if len(obj1s_temp) == 1 and [obj1, scn1] in obj1s_temp: break
            return -1
    if add_the(obj1_defined): 
        obj1_defined = 'the '+obj1_defined
        if trajector and not (trajector[-1][0].startswith('a ') and trajector[-1][0].startswith('the ')) : trajector[-1][0] = 'the '+ trajector[-1][0]
        
    if len(trajector)>0: _phrase_temp += [[obj1_defined]] * len(trajector)
    if _traj_or_land and 'number' not in _traj_or_land: _traj_or_land = 'the '+_traj_or_land     
    trajector = [[_traj_or_land]] + trajector if _traj_or_land else [[obj1_defined]] + trajector
    traj, land, sp_ind =  trajector, landmark, spatial_ind
    
    
    x = 0
    while 1:
        trajector, landmark, spatial_ind, _traj_or_land = [], [], [], []
        forb = [obj1] if scn1 == scn2 else []
        obj2_defined, obj2s_temp, inter_obj_2 = obj_definition(obj2, scn2, forb, obj1, scn1, intermediate_obj= True)
        if len(obj2s_temp) == 1 and [obj2, scn2] in obj2s_temp: break
        x+=1
        if x > x_treshhold: 
            trajector, landmark, spatial_ind, _traj_or_land = [], [], [], []
            obj2_defined, obj2s_temp, inter_obj_2 = obj_definition(obj2, scn2, forb, obj1, scn1, max_treshhold = 1, intermediate_obj= True)
            if len(obj2s_temp) == 1 and [obj2, scn2] in obj2s_temp: break
            return -1
        
    if add_the(obj2_defined): 
        obj2_defined = 'the '+obj2_defined
        if trajector and not (trajector[-1][0].startswith('a ') and trajector[-1][0].startswith('the ')) : trajector[-1][0] = 'the '+ trajector[-1][0]
    if len(trajector)>0: _phrase_temp += [[obj2_defined]] * len(trajector)
    



    sen += 'What is the relation between '+obj1_defined+' and '+obj2_defined+'?'
    main = len(spatial_ind)
    trajector = traj + trajector
    landmark = land + landmark
    if _traj_or_land and 'number' not in _traj_or_land: _traj_or_land = 'the '+_traj_or_land
    landmark = [[_traj_or_land]] + landmark if _traj_or_land else [[obj2_defined]] + landmark
    spatial_ind = [['']] + sp_ind + spatial_ind
    _phrase = [['and']] + _phrase_temp
    create_annotation(sen, main = 0)
    answer, start_end_c= answer_FR(obj1, scn1, obj2, scn2, obj1s_temp, obj2s_temp)

    

    candidate_answer = ["left", "right", "above", "below", "near to", "far from", "touching", "DK"]
    

    #Contrast
    contrast_set = []
    # change objects
    ct_treshhold = 50
    if inter_obj_1:
        forb1 =[[obj1,scn1], [obj2,scn2]]
        rels_for_obj, other_rels_for_obj = all_rels_for_obj(inter_obj_1[0], inter_obj_1[1], forbiden_list= forb1)
        check = False # a treshhold for using unique objects

        if rels_for_obj and other_rels_for_obj: rel_choose = random.choice([0,1,1,1])
        elif rels_for_obj: rel_choose = 0
        elif other_rels_for_obj: rel_choose = 1
        else: rel_choose = 0 
        
        if rel_choose == 1: #rel with other block
            while other_rels_for_obj:
                rand_rel = random.choice(other_rels_for_obj)
                obj11, scn11= rand_rel[0], rand_rel[2]
                forb1 = []
                predefine_obj = [1, reverse(rand_rel[1]), [inter_obj_1[0], inter_obj_1[1]]]
                check_def, obj1s_temp_cont = obj_definition(obj11, scn11, forb1, obj2, scn2, predef_rel = predefine_obj)
                if len(obj1s_temp_cont) == 1 and [obj11, scn11] in obj1s_temp_cont: obj1_defined_cont = check_def; check = 1; break
                else: other_rels_for_obj.remove(rand_rel)
            if not check: rel_choose = 0    
                
        if rel_choose == 0: # rel in one block
            while rels_for_obj:
                rand_rel = random.choice(rels_for_obj)
                obj11, scn11= rand_rel[0],  inter_obj_1[1]
                forb1 = []
                predefine_obj = [0, reverse(rand_rel[1]), [inter_obj_1[0], inter_obj_1[1]]]
                check_def, obj1s_temp_cont = obj_definition(obj11, scn11, forb1, obj2, scn2, predef_rel = predefine_obj)
                if len(obj1s_temp_cont) == 1 and [obj11, scn11] in obj1s_temp_cont: obj1_defined_cont = check_def; check =1; break
                else: rels_for_obj.remove(rand_rel)
            
        if check: # start to create contrast set
            if add_the(obj1_defined_cont): obj1_defined_cont = 'the '+obj1_defined_cont
            sen_cont = edit_text_form('What is the relation between '+obj1_defined_cont +' and '+obj2_defined+'?')
            answer_cont, _= answer_FR(obj11, scn11, obj2, scn2, obj1s_temp_cont, obj2s_temp) # the answer
    
            if answer_cont != answer: contrast_set += [[sen_cont, answer_cont, [],candidate_answer]]
        
    if inter_obj_2:
        forb2 = [[obj1,scn1], [obj2,scn2]]
        rels_for_obj, other_rels_for_obj = all_rels_for_obj(inter_obj_2[0], inter_obj_2[1], forbiden_list= forb2)

        check = False # a treshhold for using unique objects
        
        if rels_for_obj and other_rels_for_obj: rel_choose = random.choice([0,1,1,1])
        elif rels_for_obj: rel_choose = 0
        elif other_rels_for_obj: rel_choose = 1
        else: rel_choose = 0
        
        if rel_choose == 1: #rel with other block
            
            while other_rels_for_obj:
                rand_rel = random.choice(other_rels_for_obj)
                obj22, scn22= rand_rel[0], rand_rel[2]
                forb2 = []
                predefine_obj = [1, reverse(rand_rel[1]), [inter_obj_2[0], inter_obj_2[1]]]
                check_def, obj2s_temp_cont = obj_definition(obj22, scn22, forb2, obj1, scn1, predef_rel = predefine_obj)
                if len(obj2s_temp_cont) == 1 and [obj22, scn22] in obj2s_temp_cont: obj2_defined_cont = check_def; check = True; break
                else: other_rels_for_obj.remove(rand_rel)
                    
        elif rel_choose == 0: # rel in one block
            
            while rels_for_obj:
                rand_rel = random.choice(rels_for_obj)
                obj22, scn22= rand_rel[0],  inter_obj_2[1]
                forb2 = []
                predefine_obj = [0, reverse(rand_rel[1]), [inter_obj_2[0], inter_obj_2[1]]]
                check_def, obj2s_temp_cont = obj_definition(obj22, scn22, forb2, obj1, scn1, predef_rel = predefine_obj)
                if len(obj2s_temp_cont) == 1 and [obj22, scn22] in obj2s_temp_cont : obj2_defined_cont = check_def; check = True; break
                else: rels_for_obj.remove(rand_rel)
            
        if check: # start to create contrast set
            if add_the(obj2_defined_cont): obj2_defined_cont = 'the '+obj2_defined_cont
            sen_cont = edit_text_form('What is the relation between '+obj1_defined +' and '+obj2_defined_cont+'?')
            answer_cont, _= answer_FR(obj1, scn1, obj22, scn22, obj1s_temp, obj2s_temp_cont) # the answer
    
            if answer_cont != answer: contrast_set += [[sen_cont, answer_cont, [],candidate_answer]]   
            
    #Consistency Check
    consistency_list = []
    #reorder
    sen_r = edit_text_form('What is the relation between '+obj2_defined+' and '+obj1_defined+'?')
    answer_r = []
    for ans in answer:
        answer_r += [candidate_answer.index(reverse(candidate_answer[ans]))] 
    consistency_list += [[sen_r, answer_r, [],candidate_answer]]
    
    #describe with different relation
    obj1_defined_cons, obj1s_temp_cons, obj2_defined_cons, obj2s_temp_cons = '','','',''
    forb = []
    obj1_check, obj2_check, check_if_exist = False, False, False
    x = 0 # a treshhold for using unique objects
    while 1:
        forb = [obj2] if scn1 == scn2 else []
        check_def, obj1s_temp_cons = obj_definition(obj1, scn1, forb, obj2, scn2)

        if len(obj1s_temp_cons) == 1 and [obj1, scn1] in obj1s_temp_cons and check_def != obj1_defined: obj1_defined_cons = check_def; obj1_check= True; break
        x+=1
        if x > x_treshhold: 
            check_def, obj1s_temp_cons = obj_definition(obj1, scn1, forb, obj2, scn2, max_treshhold = 1)
            if len(obj1s_temp_cons) == 1 and [obj1, scn1] in obj1s_temp_cons and check_def != obj1_defined: obj1_defined_cons = check_def; obj1_check= True; 
            break
                
    if obj1_check:
        if add_the(obj1_defined_cons): obj1_defined_cons = 'the '+obj1_defined_cons
        sen_r = edit_text_form('What is the relation between '+obj1_defined_cons +' and '+obj2_defined+'?')
        consistency_list += [[sen_r, answer, [],candidate_answer]]
        check_if_exist = True
    
    x = 0
    while 1:
        forb = [obj1] if scn1 == scn2 else []
        check_def, obj2s_temp_cons = obj_definition(obj2, scn2, forb, obj1, scn1)

        if len(obj2s_temp_cons) == 1 and [obj2, scn2] in obj2s_temp_cons and check_def != obj2_defined: obj2_defined_cons = check_def; obj2_check= True; break
        x+=1
        if x > x_treshhold: 
            check_def, obj2s_temp_cons = obj_definition(obj2, scn2, forb, obj1, scn1, max_treshhold= 1)
            if len(obj2s_temp_cons) == 1 and [obj2, scn2] in obj2s_temp_cons and check_def != obj2_defined: obj2_defined_cons = check_def; obj2_check= True; 
            break
    
    if obj2_check:
        if add_the(obj2_defined_cons): obj2_defined_cons = 'the '+obj2_defined_cons
        sen_r = edit_text_form('What is the relation between '+obj1_defined +' and '+obj2_defined_cons+'?')
        consistency_list += [[sen_r, answer, [],candidate_answer]]
        check_if_exist = True
    
    if not check_if_exist: consistency_list = []
        
    indifinite = True if 7 in answer else False
    
    pre_question_forbiden += [[[obj1,scn1],[obj2, scn2]]] 
    
    return [sen, answer, start_end_c, candidate_answer, consistency_list, contrast_set, reasoning_type, indifinite]

    
def obj_definition(obj, scn1, forbiden_list = None, obj2 = None, scn2 = None, pre_def_attr = None, max_treshhold = max_tresh, intermediate_obj= False, predef_rel = None):
    
    global temporary_objs, first_temp, treshhold
    
    obj_defined, inter_obj = obj_def_q(obj, scn1, forbiden_list, obj2, scn2, pre_def_attr, max_treshhold, predef_rel)
    treshhold = 0
    objs_temp = temporary_objs
    temporary_objs, first_temp = [], 1
    
    if intermediate_obj:
        return obj_defined, objs_temp, inter_obj  
    else:
        return obj_defined, objs_temp
    
def obj_def_q(obj, scn1, forbiden_list = None, obj2 = None, scn2 = None, pre_def_attr = None, max_treshhold = max_tresh, predef_rel = None):
    
    global treshhold, trajector, landmark, spatial_ind, _traj_or_land
    treshhold += 1
    if forbiden_list == None: forbiden_list = []
    if pre_def_attr == None: pre_def_attr = []
    max_treshh = max_treshhold
    rels_for_obj, other_rels_for_obj, predef = None, None, None
    intermediate_obj = []
    sen = ''
    
    forbiden_list += [obj]
    if predef_rel:
        predef = 1 if predef_rel[0] == 1 else 2
    else:    
        rels_for_obj, other_rels_for_obj = all_rels_for_obj(obj, scn1 , obj2, scn2)
        random_x = random.choice([0,1])
    
    if predef == 1 or (other_rels_for_obj and random_x and treshhold < max_treshh):

        if predef:
            
            relation = R(predef_rel[1])
            
            object2,_ = obj_def_q(predef_rel[2][0],predef_rel[2][1],forbiden_list, obj2,scn2, pre_def_attr = pre_def_attr)
            temp_update(relation = reverse(predef_rel[1]))
            
            object_def = obj_ide_attr(obj, scn1, pre_def_attr = pre_def_attr)
            
            if add_the(object2): object2 = 'a '+object2
            sen += object_def+' '+wh_th()+' is '+relation+' '+object2
            
            
            spatial_ind += [[predef_rel[1]]]
            
        else:

            rels_id = random.choice(other_rels_for_obj) # id of relation for obj and other object which is choosed

            relation = R(rels_id[1])

            object2,_ = obj_def_q(rels_id[0],rels_id[2],forbiden_list, obj2,scn2, pre_def_attr = pre_def_attr) 
            temp_update(relation = reverse(rels_id[1]))

            object_def = obj_ide_attr(obj,scn1, pre_def_attr = pre_def_attr)
            
            if add_the(object2): 
                object2 = 'a '+object2
                if treshhold == 2 and trajector: trajector[0][0] = 'a '+trajector[0][0] 
            sen += object_def+' '+wh_th()+' is '+relation+' '+object2
            intermediate_obj = [rels_id[0],rels_id[2]]
            
            spatial_ind += [[rels_id[1]]]
        
        landmark += [['a '+_traj_or_land if _traj_or_land else object2]] 
        _traj_or_land = object_def 
        trajector += [[object_def]]
          
        
    elif predef == 2 or (rels_for_obj and treshhold < max_treshh):

        if predef: 
            relation = R(predef_rel[1])
            
            object2,_ = obj_def_q(predef_rel[2][0],predef_rel[2][1],forbiden_list, obj2,scn2, pre_def_attr = pre_def_attr)
            temp_update(relation = reverse(predef_rel[1]))
            
            object_def = obj_ide_attr(obj, scn1, pre_def_attr = pre_def_attr)

            if add_the(object2): object2 = 'a '+object2
            sen += object_def+' '+wh_th()+' is '+relation+' '+object2
            
            spatial_ind += [[predef_rel[1]]]
            
        else:
            rels_id = random.choice(rels_for_obj) # id of relation for obj and other object which is choosed
            relation = R(rels_id[1])

            object2,_ = obj_def_q(rels_id[0],scn1,forbiden_list, obj2,scn2, pre_def_attr = pre_def_attr) 
            temp_update(relation = reverse(rels_id[1]))

            object_def = obj_ide_attr(obj,scn1, pre_def_attr = pre_def_attr)

            if add_the(object2): 
                object2 = 'a '+object2
                if treshhold == 2 and trajector: trajector[0][0] = 'a '+trajector[0][0] 
            sen += object_def+' '+wh_th()+' is '+relation+' '+object2
            intermediate_obj = [rels_id[0],scn1]
            spatial_ind += [[rels_id[1]]]
            
        landmark += [['a '+_traj_or_land if _traj_or_land else object2]]
        _traj_or_land = object_def 
        trajector += [[object_def]]
    
    else:

        o_attrs = obj_attr[scn1][ind_obj_attr(obj,scn1)]
        if o_attrs[1] == '' and o_attrs[2] == '' and o_attrs[3] == '' and o_attrs[4] == '': z = None
        
        object_def = obj_ide_attr(obj,scn1, obj2 = obj2, scn2 = scn2, pre_def_attr = pre_def_attr, single_def = True)
        sen += object_def 
    return sen, intermediate_obj
    
def obj_ide_attr(obj,scn, obj2= None, scn2 = None , pre_def_attr=None, single_def = False): 
    # id of the object . The identification description for an object
    # if obj2 == -1 it means that the object was described by its relations
    # pre_def_attr is for prevent to using attributes which are used in previous objects

    global trajector, landmark, spatial_ind, _traj_or_land
    s = [0]*6
    unique_list = unique_attr()
    uni_id = None
    block_number = ''
    if pre_def_attr == None: pre_def_attr = []
    
    obj_attributes = obj_attr[scn][ind_obj_attr(obj,scn)]
    dif_attr_obj1, dif_attr_obj2 = None, None
    for ind, attr in enumerate(obj_attributes):
        if attr != '' and attr in unique_list and ind != 0 and ind not in pre_def_attr:
            uni_id = ind
            break
            
    if obj2 != None:
        obj2_attributes = obj_attr[scn2][ind_obj_attr(obj2,scn2)]
        
        if uni_id is not None: s[uni_id] = 1 
        
        dif_attr_obj1 = find_difference(obj_attributes, obj2_attributes, pre_def_attr)
        if dif_attr_obj1: 
            z = random.choice(range(len(dif_attr_obj1)))
            dif_attr_obj2 = dif_attr_obj1[z] 
            s[dif_attr_obj2]=1
        elif obj_attributes[5] != '': s[5]=1;
        else: # there is a same object in both block -> so it should mentioned by their block number.
            block_number = ' '+wh_th()+' is in block '+name_block(scn)
        if obj_attributes[4] != '' and single_def: s[4] =1; 
            
    if uni_id is None:
        for ind,a in enumerate(obj_attributes):
            if ind ==0 or ind == 4 or ind == 5: continue
            if a != '' and ind not in pre_def_attr:  s[ind]=1
        num_1 = s.count(1)
        if single_def:
            if num_1 == 0 and obj_attributes[5] != '': s[5]=1
            if num_1 > 2 :
                if treshhold > 1:
                    if s[4] ==1 and dif_attr_obj2 != 4: s[4] =0
                    elif s[4] ==0:
                        z = random.choice([1,2,3])
                        s[z] = 0
                else: 
                    if s[4] ==1 and dif_attr_obj2 != 4: s[4] =0
        else:
            if num_1 > 1:
                z = random.choice([1,2,3])
                if z != dif_attr_obj2 and z not in pre_def_attr:s[z]=0
            if num_1 > 2 :
                z = random.choice([1,2,3])
                if z != dif_attr_obj2 and z not in pre_def_attr: s[z]=0
                    
    elif not single_def:
        
        s[uni_id] == 0
        for ind,a in enumerate(obj_attributes):
            if ind ==0 or ind == 4 or ind == 5 or ind == uni_id: continue
            if a != '' and ind not in pre_def_attr: s[ind]=1
    else:
        z =random.choice([0,1])
        if z and uni_id:
            s[uni_id] = 1
        else: 
            for ind,a in enumerate(obj_attributes):
                if ind ==0 or ind == 4 or ind == 5 or ind == uni_id: continue
                if a != '' and ind not in pre_def_attr: s[ind]=1
        
    attr_value, attr_value4 = '','' 
    if s[1]:
        attr_value += obj_attributes[1]['size']+' '
    if s[2]:
        attr_value += obj_attributes[2]['color']+' '
    if s[3]:
        attr_value += obj_attributes[3]['type']+' '
    else:
        attr_value += definite_pointer()
    if s[4]:
        attr_value4 += ' '+wh_th()+' is '+ obj_attributes[4]['rel']+' a block '
    
    if s[5]: attr_value += ' number '+object_num(int(obj_attributes[5]))
    
    main_obj = attr_value
    
    attr_value+= attr_value4
    if attr_value4: 
        _traj_or_land = main_obj
        trajector += [[main_obj]]
        landmark += [[obj_attributes[4]['rel'][9:]+' a block']]
        spatial_ind += [['touching']]
        
    if single_def and ((s.count(1) == 1 and s[5] == 1) or s.count(1) == 0):
    #there is a same object in both block -> so it should mentioned by their block number.
        block_number = ' in block '+ name_block(scn)
    
    bl_n = 0
    if block_number: 
        bl_n = 1
        _traj_or_land = main_obj
        trajector += [[main_obj]]
        landmark += [['block '+name_block(scn)]]
        spatial_ind += [['in']]
    temp_update(features = [obj, scn, obj_attributes, s, bl_n]) 
    attr_value += block_number
    
    return attr_value

def find_same_attr(obj,scn, forbiden_list):
    sen = ''
    attrs = []
    
    ind = ind_obj_attr(obj,scn)
    attr_list = obj_attr[scn][ind]
    sim = []
    
    # set a random choose for choose an object and check if they have similar attributes
    i, id_scn, id_list, upper_bond, upper_bondk, u,k = 1, None, None, 10, 10, 0,0
    checked = []
    while i:
        id_scn = random.choice(range(_num_scenes))
        if len(obj_attr[id_scn])>0: id_list = random.choice(range(len(obj_attr[id_scn])))
        else: continue
        
        if [id_list,id_scn] in checked or (id_scn == scn and id_list == obj): 
            k += 1
            if k > upper_bondk: i =0; continue
            checked.append([id_list,id_scn])
            continue    
        
        if id_list in forbiden_list:
            u += 1
            if u > upper_bond: i =0
            continue
        
        sim = find_similarity(attr_list, obj_attr[id_scn][id_list])
        if sim: i =0; continue
        else: checked.append([id_list,id_scn])
            
    if sim:
        z = random.choice(range(len(sim)))
        sim = sim[z]
        f_list = forbiden_list if id_scn == scn else []
        object2 = obj_def_q(obj_attr[id_scn][id_list][0],id_scn, forbiden_list= f_list, pre_def_attr= [sim])
        temp_update(same_rel=sim)
        attrs = sim
        attribute = ''
        #type of similarity
        if sim == 1: attribute ='size'
        elif sim == 2: attribute = 'color'
        elif sim == 3: attribute = 'type'
        elif sim == 4: attribute = 'position to the block'
        sen += wh_th()+' has the '+sa_sim()+' '+ attribute +' as '+object2
    return attrs, sen

def find_similarity(attr_list1, attr_list2):
    sim = []
    if attr_list1[1] == attr_list2[1] and attr_list1[1] != '': sim.append(1)
    if attr_list1[2] == attr_list2[2] and attr_list1[2] != '': sim.append(2)
    if attr_list1[3] == attr_list2[3] and attr_list1[3] != '': sim.append(3)
    if attr_list1[4] == attr_list2[4] and attr_list1[4] != '': sim.append(4)
    return sim

def find_difference(attr_list1, attr_list2, pre_def_attr):
    dif =[]
    if attr_list1[1] != '' and attr_list1[1] != attr_list2[1] and 1 not in pre_def_attr: dif.append(1)
    if attr_list1[2] != '' and attr_list1[2] != attr_list2[2] and 2 not in pre_def_attr: dif.append(2)
    if attr_list1[3] != '' and attr_list1[3] != attr_list2[3] and 3 not in pre_def_attr: dif.append(3)
    if attr_list1[4] != '' and attr_list1[4] != attr_list2[4] and 4 not in pre_def_attr: dif.append(4)
    return dif

def temp_update(features=None, relation = '', same_rel=''):
    
    global temporary_objs, first_temp
    
    obj, scn, obj_attribute, used_attr = '','',[],[]
    if features == None: features = []
    if features:
        
        obj = features[0]
        scn = features[1]
        obj_attribute = features[2]
        used_attr = features[3]
        block_num = features[4]
        
        obj_attt = []          
        
        for ind,i in enumerate(used_attr):
            if i ==0:obj_attt.append('')
            else: obj_attt.append(obj_attribute[ind])
        objs = []
        if first_temp == 0: # already have a list of object just based on the features choose between them.
            for i in temporary_objs:
                o_attr = obj_attr[i[1]][ind_obj_attr(i[0],i[1])]
                if block_num:
                    if i[1] == scn and issubset(obj_attt[1:],o_attr):
                        if i not in objs: objs.append(i) # first element id of object and the second one is id of block 
                else:
                    if issubset(obj_attt[1:],o_attr):
                        if i not in objs: objs.append(i) # first element id of object and the second one is id of block 
            temporary_objs = objs    
            
        else: # first consideration of objects
            first_temp = 0
            for i in range(_num_scenes):
                for obj_at in obj_attr[i]:

                    if block_num:
                        if i == scn and issubset(obj_attt[1:],obj_at):
                            if [obj_at[0],i] not in objs: objs.append([obj_at[0],i]) # first element id of object and the second one is id of block 
                    else:
                        if issubset(obj_attt[1:],obj_at):
                            if [obj_at[0],i] not in objs: objs.append([obj_at[0],i]) # first element id of object and the second one is id of block 
            temporary_objs = objs    
            
        
    elif relation: # update relations
        objs=[]
        for temp in temporary_objs:
            in_scene, out_scene = all_rels_for_obj(temp[0], temp[1])
            for i in in_scene:
                if i[1] == relation:
                    if [i[0],temp[1]] not in objs: objs.append([i[0],temp[1]])
            for i in out_scene:
                if i[1] == relation:
                    if [i[0],i[2]] not in objs: objs.append([i[0],i[2]])
        
        temporary_objs = objs    
            
            
    elif same_rel: # update same attr
        
        same_rel = int(same_rel)
        objs=[]
        for temp in temporary_objs:
            obj_attribute = obj_attr[temp[1]][ind_obj_attr(temp[0],temp[1])]
            if obj_attribute[same_rel]:
                for i in range(_num_scenes):
                    for o_at in obj_attr[i]:
                        if o_at[same_rel] and o_at[same_rel] == obj_attribute[same_rel] and [o_at[0],i] not in objs: objs.append([o_at[0],i])
        
        temporary_objs = objs    
        
def choose_attr(obj, scn, ind = '', attr_type = 1):
    
    sen, attr = '', []
    if ind == '': ind = ind_obj_attr(obj,scn) 
    o_attr = obj_attr[scn][ind]
    attr_options = []
    for i,val in enumerate(o_attr):
        if attr_type and i ==0 or i >= 4: continue
        if val != '': attr_options.append(i)
    if attr_options:
        x = random.choice(range(len(attr_options)))
        attr = attr_options[x]
        if attr_type:
            if attr == 1: sen = 'size'
            elif attr == 2: sen = 'color'
            elif attr == 3: sen = 'shape'
#             elif attr == 4: sen = 'position regarding to the block'
        else:
            if attr == 1: sen = o_attr[attr]['size']
            elif attr == 2: sen = o_attr[attr]['color']
            elif attr == 3: sen = o_attr[attr]['type']
            elif attr == 4: sen = o_attr[attr]['rel']
            
    return attr, sen, attr_options

def find_relation(obj, scn, obj2='', scn2='', has_obj2 = False):
    relation= ''
    rels, rels_id = [],[]
    object2 = []
    same_scene = scn != scn2
    x = -1
    
    #with 10% probability there is not any objects, with 30% there are from different block and with 60% there are from the same block
    # unless there is not enough object with relation or just one block exists
    if _num_scenes == 1: x = random.choice([0,1,1,1,1])
    else:    
        if len(obj_obj[scn]) > 1: x = random.choice([0,1,1,1,1,1,1,2,2,2]) 
        elif len(obj_obj[scn]) == 1:  x = random.choice([0,1,2,2,2])
        else: x = random.choice([0,2,2,2])
    if x == 1:
        for i in obj_attr[scn]:
            if i[0] == obj: continue
            if has_obj2:
                find_rels = find_rel_two_objs(scn, obj, i[0], [obj2])
                find_rels = [h for h in find_rels if h != 'DK']
                if find_rels: 
                    rels += [find_rels]
                    object2 += [i[0]]
            else:
                find_rels = find_rel_two_objs(scn, obj, i[0])
                find_rels = [h for h in find_rels if h != 'DK']
                if find_rels: 
                    rels += [find_rels]
        if rels:
            z = random.choice(range(len(rels)))
            relation = random.choice(rels[z])
            object2 = [object2[z], scn] if object2 else []
        
    elif x == 2:
        scns = []
        rels1 = []
        for i in range(_num_scenes):
            if i != scn and len(obj_attr[i]) > 0: 
                find_rel = find_rel_two_scn(scn, i)
                if find_rel and 'NC' not in find_rel and (i != scn2 or len(obj_attr[i])>1): scns += [i]; rels1 += find_rel
        if scns:
            z = random.choice(range(len(scns)))        
            if isinstance(rels1[z], str) :relation = rels1[z]
            elif isinstance(rels1[z], list):
                relation = random.choice(rels1[z])
            if has_obj2:
                object2 = ['', scns[z]]
    
    if relation == '': x = 0
    if x == 0:
        relation = random.choice(['left','right','above','below','near to', 'far from', 'touching'])
           

        
    if has_obj2:
        return relation, object2
    else:
        return relation

def all_rels_for_obj(obj, scn1 , obj2 = None, scn2 = None, forbiden_list= None, no_direct= False):
    
    global obj_obj 
    rels_for_obj,rels_for_obj_others = [],[]
    if forbiden_list == None: forbiden_list = []
    objects_scn1 = []
    for i in obj_attr[scn1]:
        if i[0] != obj2 and i[0] != obj and ([i[0], scn1] not in forbiden_list):
            objects_scn1.append(i[0])
            
    # transitivity and reverse
    for i in objects_scn1:
        rels = find_rel_two_objs(scn1, obj,i, no_direct=no_direct)
        if 'NC' in rels: rels.remove('NC')
        if 'DK' in rels: rels.remove('DK')
        if rels:
            for rel in rels:
                rels_for_obj.append([i,rel]) 
    
    # relation between two scenes
    for s_s in range(len(scn_scn)+1):
        if s_s != scn1:
            scn2_2 = s_s
            rels = find_rel_two_scn(scn1,s_s)
            if 'NC' in rels: rels.remove('NC')
            if 'DK' in rels: rels.remove('DK')
            if rels:
                objects_scn2 = []
                for i in obj_attr[scn2_2]: 
                    if (scn2_2 != scn2 or i[0] != obj2) and ([i[0], scn2_2] not in forbiden_list):
                        objects_scn2.append(i[0])
                for i in objects_scn2:
                    if i != obj2 and scn2_2 != scn2 : rels_for_obj_others.append([i,random.choice(rels),scn2_2])
    return rels_for_obj, rels_for_obj_others

#**************************************
#************Answer part***************
#**************************************

def answer_CO_0(obj,scn,objs_temp, obj1, scn1, obj1s_temp, obj2, scn2, obj2s_temp, relation, obj1_defined, obj2_defined, order, CO_Q_type): # CO_Q_type ==0 -> what is ... , CO_Q_type == 1 -> which obj is ...
    
    S_answer =''
    correct= [False]*2
    if scn == scn1:
        rel = find_rel_two_objs(scn, obj1, obj)
        if relation in rel:
            correct[0] = True
    else:
        rel = find_rel_two_scn(scn1 , scn)
        if relation in rel:
            correct[0] = True
    if scn == scn2:
        rel = find_rel_two_objs(scn, obj2, obj)
        if relation in rel:
            correct[1] = True
    else:
        rel = find_rel_two_scn(scn2 , scn)
        if relation in rel:
            correct[1] = True

    # check temp
    if CO_Q_type == 0: #CO_Q_type == 0 -> obj unique 
        if not correct[0]: #check for those that are false
            for t1 in obj1s_temp:
                if objs_temp[0][1] == t1[1]:
                    rel = find_rel_two_objs(objs_temp[0][1], t1[0], objs_temp[0][0])
                    if relation in rel:
                        correct[0] = True
                else:
                    rel = find_rel_two_scn(t1[1] , scn)
                    if relation in rel:
                        correct[0] = True
        if not correct[1]:    
            for t2 in obj2s_temp:
                if objs_temp[0][1] == t2[1]:
                    rel = find_rel_two_objs(objs_temp[0][1], t2[0], objs_temp[0][0])
                    if relation in rel:
                        correct[1] = True
                else:
                    rel = find_rel_two_scn(t2[1] , scn)
                    if relation in rel:
                        correct[1] = True
    else: #CO_Q_type == 1 -> obj1 and obj2 are unique
        if not correct[0]: #check for those that are false
            for t in objs_temp:
                if t[1] == obj1s_temp[0][1]:
                    rel = find_rel_two_objs(t[1], obj1s_temp[0][0], t[0])
                    if relation in rel:
                        correct[0] = True
                else:
                    rel = find_rel_two_scn(scn1 , t[1])
                    if relation in rel:
                        correct[0] = True
        if not correct[1]:    
            for t in objs_temp:
                if t[1] == obj2s_temp[0][1]:
                    rel = find_rel_two_objs(t[1], obj2s_temp[0][0], t[0])
                    if relation in rel:
                        correct[1] = True
                else:
                    rel = find_rel_two_scn(scn2 , t[1])
                    if relation in rel:
                        correct[1] = True
            
    if correct[0] == correct[1] == True: S_answer=[2];
    elif correct[0] == correct[1] == False: S_answer=[3]
    elif correct[0] == True: S_answer = [0] if order else [1]
    elif correct[1] == True: S_answer = [1] if order else [0]
    else: S_answer = [4]
    
    return S_answer 

def answer_FO(obj,scn, temp, relation):
    
    ans_list, start_end_c = [],[]
    L_answer, S_answer = [], []
    ans_list = Find_obj_with_rel(obj, scn, relation)
    for t in temp:
        ans = Find_obj_with_rel(t[0], t[1], relation, forbiden_list = ans_list)
        if ans and ans[0] not in ans_list: ans_list += ans
        
    for a in ans_list:
        ind = ind_obj_attr(a[0], a[1])
        if obj_attr[a[1]][ind][3] != '':
            obj_def = obj_complete_def(a[0], a[1])
            start_end_c += [start_end("FO",obj_def,1)] # 1 if the obj has type attribute else got 0
            S_answer += [obj_def]
        else:
            obj_def = obj_complete_def_start_end(a[0], a[1])
            start_end_c_temp, obj_def = start_end("FO",obj_def,0)
            start_end_c += [start_end_c_temp]
            S_answer += [obj_def]
    if ans_list == []: S_answer = ["None"] ; start_end_c= []#None
    
    return S_answer, start_end_c 

def answer_FA(obj, scn, temp, attr):
    
    answer =[]
    answer_obj = []
    ind = ind_obj_attr(obj, scn)
    start_end_c = []
    attribute = ''
    obj_attributes = obj_attr[scn][ind]
    if attr != 4:
        answer = [list(obj_attributes[attr].values())[0]]
    else: 
        answer = obj_block_rel(obj_attributes[attr]['rel'])

    object_desc = obj_complete_def_start_end(obj, scn)
    start_end_c = start_end("FA", answer, object_desc)
    
    return answer, start_end_c

def answer_FB(obj, scn, temp):
    
    S_answer = [name_block(scn)]
    for t in temp:
        if t[1] != scn and name_block(t[1]) not in S_answer: S_answer += [name_block(t[1])]
    
    
    return S_answer, [] 

def answer_YN(obj1,scn1,temp1, obj2, scn2, temp2, relation, any_or_all):
    
    answer = ''
    possible_ans = ''
    #if len(temp1) == 0 or len(temp2) == 0: return -1
    if len(temp1) == 1 and len(temp2)== 1 : #obj1 and obj2 are unique.
        a_list = FR_correct(obj1,scn1,obj2,scn2)
        if relation in a_list: possible_ans = 'Yes'
        elif reverse(relation) in a_list: possible_ans = 'No'
        elif relation == 'touching' and scn1 != scn2: possible_ans = 'No'
        else: possible_ans = 'DK'
    else:
        loop_1, loop_2 = False, False
        if any_or_all == [1,1]:
            no_ans = None
            DK_exists= False
            for t1 in temp1:
                no_ans = False
                for t2 in temp2:
                    if t1 != t2:
                        a_list1 = FR_correct(t1[0], t1[1], t2[0], t2[1])
                        if reverse(relation) in a_list1: no_ans = True; DK_exists=False; break
                        elif relation == 'touching' and t1[1] != t2[1]: no_ans = True; DK_exists=False; break
                        elif reverse(relation) not in a_list1 and relation not in a_list1:  yes_ans = False; DK_exists = True
                    else: no_ans = True; DK_exists=False; break
                if no_ans: break
                elif DK_exists: break
            if no_ans == False: 
                 possible_ans = 'DK' if DK_exists else 'Yes'
            else: possible_ans = 'No'
        
        elif any_or_all == [1,0]:
            DK_exists, DK_total = False, False
            for t2 in temp2:
                yes_ans = True
                for t1 in temp1:
                    if t1 != t2:
                        if relation == 'touching' and t1[1] != t2[1]: yes_ans = False; DK_exists=False; break
                        a_list1 = FR_correct(t2[0], t2[1], t1[0], t1[1])
                        if relation in a_list1: yes_ans = False; DK_exists=False; break
                        elif relation not in a_list1 and reverse(relation) not in a_list1:  yes_ans = False; DK_exists = True 
                    else: yes_ans = False; DK_exists=False; break
                if yes_ans: break
                if DK_exists == True: DK_total = DK_exists
            if yes_ans == False: 
                 possible_ans = 'DK' if DK_total else 'No'
            else: possible_ans = 'Yes'
            
        elif any_or_all == [0,1]:
            yes_ans =None
            DK_exists, DK_total = False, False
            for t1 in temp1:
                yes_ans = True
                for t2 in temp2:
                    if t1 != t2:
                        if relation == 'touching' and t1[1] != t2[1]: yes_ans = False; DK_exists=False; break
                        a_list1 = FR_correct(t1[0], t1[1], t2[0], t2[1])
                        if reverse(relation) in a_list1: yes_ans = False; DK_exists=False; break
                        elif reverse(relation) not in a_list1 and relation not in a_list1: yes_ans = False; DK_exists = True 
                    else: yes_ans = False; DK_exists=False; break
                if yes_ans: break
                if DK_exists == True: DK_total = DK_exists
            if yes_ans == False: 
                 possible_ans = 'DK' if DK_total else 'No'
            else: possible_ans = 'Yes'
            
        else: # [0,0]
            DK_exists = False
            for t1 in temp1:
                DK_exists = False
                for t2 in temp2:
                    if t1 != t2:
                        a_list1 = FR_correct(t1[0], t1[1], t2[0], t2[1])
                        if relation in a_list1: possible_ans = 'Yes'; loop_1 = True; break
                        elif reverse(relation) not in a_list1 and (relation != 'touching' or t1[1] == t2[1]): DK_exists = True 
                if loop_1: break 
            if loop_1 == False:
                possible_ans = 'DK' if DK_exists else 'No'
            
    # start and end of word and character index of answer in story
    start_end_c = []
    return [possible_ans]
        
    
def answer_FR(object1, scene1, object2, scene2, temp_objs1, temp_objs2):
    
    answer, answer_1 = [], []
    scn1, scn2 = scene1, scene2
    obj1, obj2 = object1, object2
    temp1, temp2 = temp_objs1, temp_objs2
    a_list = FR_correct(obj1,scn1,obj2,scn2)
    for i in a_list:
        if i not in answer: answer += [i]
    if answer == []: answer = ['DK']
        
    start_end_c = []
    
    candidate_answer = ['left', 'right', 'above', 'below', 'near to', 'far from', 'touching', 'DK']
    for i in answer:
        answer_1 += [candidate_answer.index(i)]
        
    return answer_1, start_end_c

def Find_obj_with_rel(obj, scn, relation, forbiden_list = None):
    
    objects = [] # [obj,scn]
    if forbiden_list == None: forbiden_list = []
    reverse_relation = reverse(relation)
    
    # first check all the objects of other block based on the relation between blocks
    if _num_scenes >1:
        for i in range(_num_scenes):
            for j in range(i+1 , _num_scenes):
                if scn == i:
                    rel = find_rel_two_scn(j,i) # rel between scene j and i
                    if rel[0] == relation:
                        for o in obj_attr[j]:
                            if [o[0],j] not in forbiden_list: objects.append([o[0],j]) # objects in j are to the relation of the obj
                elif scn == j:
                    rel = find_rel_two_scn(i,j) # rel between scene i and j
                    if rel[0] == relation:
                        for o in obj_attr[i]:
                            if [o[0],j] not in forbiden_list: objects.append([o[0],i]) # objects in j are to the relation of the obj                      
                         
    # Check the relation between objects of a block
    rels_for_obj = []    
    for o in obj_attr[scn]:
        if o[0] != obj:
            rels_for_obj = find_rel_two_objs(scn, obj, o[0])
            if reverse_relation in rels_for_obj: 
                if [o[0],scn] not in forbiden_list: objects.append([o[0],scn])
    
    return objects
    
    
def FR_correct(obj1,scn1,obj2,scn2):
       

    answer = []
    if scn1 != scn2: # objects are in different blocks
        answer = find_rel_two_scn(scn1, scn2)
        
    else:
        answer = find_rel_two_objs(scn1, obj1,obj2)
    
    return answer   

def find_rel_two_scn(scn1,scn2):
    
    answer = []
    rels =['']*2
    multi_hop = 0
    direct = False
    for i in scn_scn:
        if scn1 in i[0] and scn2 in i[0]:
            direct = True
            if [scn1, scn2] == i[0]: answer += [i[1]];break
            elif [scn2, scn1] == i[0]: answer += [(reverse(i[1]))]; multi_hop=1; break
        elif scn1 in i[0]:
            if scn1 == i[0][0]: rels[0] = i[1]  
            else:  rels[0] = reverse(i[1]); multi_hop+=1
        elif scn2 in i[0]:
            if scn2 == i[0][1]: rels[1] = i[1]  
            else: rels[1] = reverse(i[1]); multi_hop+=1
    
    if rels[0] and rels[1]:
        if rels[0] == rels [1]: answer += [rels[0]]; multi_hop += 1; #print("####")
        else: answer += ['DK']; multi_hop = 0
    elif not direct: multi_hop = 0
    
    return answer
        

def find_rel_two_objs(scn1, obj1,obj2,forbiden_list = None, no_direct = False):
    
    rels, rels_f, multi_hop = [],[],[]
    if forbiden_list == None: forbiden_list = []
    f_list = forbiden_list
    
    rels = search_two_objs(scn1, obj1,obj2, no_direct= no_direct) #direct relation
    if obj1 not in f_list: f_list.append(obj1)

    
    obj_id_list = [x for x in range(len(obj_attr[scn1])) if x not in f_list and x != obj2] # find the relation between obj2 and 

    
    for o in obj_id_list:
        rels1 = search_two_objs(scn1,obj1, o)
        if rels1: 
            rels2 = find_rel_two_objs(scn1, o, obj2, f_list)
            if rels2: 
                rels3 = check_transitivity(rels1, rels2)
                if rels3 not in rels: rels += rels3
    
    rels_f = rels
    
    relss_f = []
    if rels_f == []: relss_f =['DK']
    else:
        for i in rels_f:
            if i != 'DK':
                relss_f += [i]
    return relss_f
        
def search_two_objs(scn1, obj1,obj2, no_direct = False): 
    
    rels = []
    multi_hop = []
    for o_o in obj_obj[scn1]: #direct relation found
        #if we have direct direction
        if o_o[0] == [obj1,obj2] and not no_direct:
            for r in o_o[1]:
                if r not in rels: rels.append(r)
                multi_hop.append(0)
        #if we have direct direction but in the reverse form
        elif o_o[0] == [obj2,obj1]: 
            #considering sysmetry for distances and "touching" -> reverse function return the same relation for these
            for r in o_o[1]:
                if reverse(r) not in rels: rels.append(reverse(r))
                multi_hop.append(1)
    
    #consider the obj-scn relation
    ind1 = ind_obj_attr(obj1,scn1)
    obj1_attributes = obj_attr[scn1][ind1]
    obj1_rel = obj_block_rel(obj1_attributes[4]['rel'])[0] if obj1_attributes[4] != '' else ''
    
    ind2 = ind_obj_attr(obj2,scn1)
    obj2_attributes = obj_attr[scn1][ind2]
    obj2_rel = obj_block_rel(obj2_attributes[4]['rel'])[0] if obj2_attributes[4] != '' else ''
    
    if obj1_rel:
        #consider directions and distances
        if obj1_rel == 'top':
            if obj2_rel == 'bottom': 
                if 'far from' not in rels: rels+=['far from']
                if 'above' not in rels: rels+=['above']
#             else: # object2 can be anywhere, so if there is any object above the object2 in that case object2 is below the object1
#                 for o_o in obj_obj[scn1]:
#                     if ('above' in o_o[1] and o_o[0][1] == obj2) or ('below' in o_o[1] and o_o[0][0] == obj2): 
#                         if 'above' not in rels: rels+=['above']
        elif obj1_rel == 'bottom':
            if obj2_rel == 'top': 
                if 'far from' not in rels: rels+=['far from']
                if 'below' not in rels: rels+=['below']
#             else: # object2 can be anywhere, so if there is any object above the object2 in that case object2 is below the object1
#                 for o_o in obj_obj[scn1]:
#                     if ('below' in o_o[1] and o_o[0][1] == obj2) or ('above' in o_o[1] and o_o[0][0] == obj2): 
#                         if 'below' not in rels: rels+=['below']
        
        elif obj1_rel == 'right':
            if obj2_rel == 'left': 
                if 'far from' not in rels: rels+=['far from']
                if 'right' not in rels: rels+=['right']
#             else: # object2 can be anywhere, so if there is any object above the object2 in that case object2 is below the object1
#                 for o_o in obj_obj[scn1]:
#                     if ('right' in o_o[1] and o_o[0][1] == obj2) or ('left' in o_o[1] and o_o[0][0] == obj2): 
#                         if 'right' not in rels: rels+=['right']; multi_hop += [2]
        
        elif obj1_rel == 'left':
            if obj2_rel == 'right': 
                if 'far from' not in rels: rels+=['far from']
                if 'left' not in rels: rels+=['left']
#             else: # object2 can be anywhere, so if there is any object above the object2 in that case object2 is below the object1
#                 for o_o in obj_obj[scn1]:
#                     if ('left' in o_o[1] and o_o[0][1] == obj2) or ('right' in o_o[1] and o_o[0][0] == obj2):
#                         if 'left' not in rels:  rels+=['left']; multi_hop += [2]
                
#     elif obj2_rel: # we know that obj1_rel == ''
#         if obj2_rel == 'top':
#             # object1 can be anywhere, so if there is any object above the object1 in that case object1 is below the object1
#             for o_o in obj_obj[scn1]:
#                 if ('above' in o_o[1] and o_o[0][1] == obj1) or ('below' in o_o[1] and o_o[0][0] == obj1): 
#                     if 'below' not in rels: rels+=['below']; multi_hop += [2]
                    
#         elif obj2_rel == 'bottom':
#             # object2 can be anywhere, so if there is any object above the object2 in that case object2 is below the object1
#             for o_o in obj_obj[scn1]:
#                 if ('below' in o_o[1] and o_o[0][1] == obj1) or ('above' in o_o[1] and o_o[0][0] == obj1): 
#                     if 'above' not in rels: rels+=['above']; multi_hop += [2]
        
#         elif obj2_rel == 'right':
#             # object2 can be anywhere, so if there is any object above the object2 in that case object2 is below the object1
#             for o_o in obj_obj[scn1]:
#                 if ('right' in o_o[1] and o_o[0][1] == obj1) or ('left' in o_o[1] and o_o[0][0] == obj1):
#                     if 'left' not in rels:  rels+=['left']; multi_hop += [2]
        
#         elif obj2_rel == 'left':
#             # object2 can be anywhere, so if there is any object above the object2 in that case object2 is below the object1
#             for o_o in obj_obj[scn1]:
#                 if ('left' in o_o[1] and o_o[0][1] == obj1) or ('right' in o_o[1] and o_o[0][0] == obj1): 
#                     if 'right' not in rels: rels+=['right']; multi_hop += [2]
#     print('rels after block relations', rels, ' for ', obj1_rel, obj2_rel)
    return rels


def check_transitivity(rel1, rel2):
    
    relations = []
    for r1 in rel1:
        for r2 in rel2:
            if r1 == r2: 
                if r1 != 'near to' and r1 != 'far from' and r1 != 'touching': 
                    relations.append(r2)
                else: relations.append('DK')
            elif r1 == reverse(r2):
                relations.append('DK')
            
    return relations

#**************************************
#************Shared part***************
#**************************************

def obj_complete_def(obj,scn):
    
    sen,sen1 ='',''
    check = 0
    ind = ind_obj_attr(obj,scn)
    obj_attributes = obj_attr[scn][ind]
    for ix,attr in enumerate(obj_attributes[1:]):
        if ix == 0 and attr: sen += list(attr.values())[0]
        elif ix == 1 and attr:  
            if sen: sen += ' '
            sen += list(attr.values())[0]
        elif ix == 2:
            if attr:
                if sen: sen += ' '
                sen += list(attr.values())[0]
            else: 
                if sen: sen += ' '
                sen += definite_pointer()
                
        elif ix == 3: continue  
                
        else:
            if attr != '' :
                sen += ' number '+object_num(attr)
                
    if sen: sen = sen+sen1
    
    return sen    

def obj_complete_def_start_end(obj,scn):
    
    sen,sen1 ='',''
    check = 0
    ind = ind_obj_attr(obj,scn)
    obj_attributes = obj_attr[scn][ind]
    for ix,attr in enumerate(obj_attributes[1:]):
        if ix == 0 and attr: sen += list(attr.values())[0]
        elif ix == 1 and attr:  
            if sen: sen += ' '
            sen += list(attr.values())[0]
        elif ix == 2:
            if attr:
                if sen: sen += ' '
                sen += list(attr.values())[0]
            else:
                sen1 = sen
                sen+= ' shape'
                sen1 += ' object'
        elif ix == 3: continue
        else:
            if attr != '' :
                sen += ' number '+object_num(attr)
                if sen1: sen1+= ' number '+object_num(attr)
    if sen1: return [sen, sen1]
    else: return [sen]    

def ind_obj_attr(obj,scn):
    ind = None
    for ind1,o_a in enumerate(obj_attr[scn]):
        if o_a[0] == obj: ind = ind1; break
    return ind

def issubset(t2,t1):
    check = 1
    for i in t2:
        if i != '' and i not in t1: check = 0; break
    return check

def definite_pointer():
    sen = ' '
    x = random.choice([0,1,2])
    if x == 0: sen = 'thing'
    elif x == 1: sen = 'shape'
    else: sen = 'object'
    return sen

def wh_th():
    sen = ''
    sen += 'which' if random.choice([0,0,0,1]) else 'that'
    return sen

def sa_sim():
    sen = ''
    sen += 'same' 
    return sen


def unique_attr():
    global obj_attr
    unique,list_all_attrs = [], []
    for scn in range(_num_scenes):
        for i in obj_attr[scn]:
            list_all_attrs += i
    unique = [ x for x in list_all_attrs if list_all_attrs.count(x) == 1]
    return unique
    
def obj_block_rel(rel):
    sen = []
    rels = {'touching the top edge of': 'top', 'touching the bottom edge of': 'bottom', 'touching the left edge of': 'left','touching the right edge of ': 'right', 'at the top of': 'top', 'at the bottom of': 'bottom' }
    if rel in rels:
        sen += [rels[rel]]
    return sen

def start_end(q_type, answer, obj_defs = None):
    
    global story_f
    start_end = []
    if obj_defs == None: obj_defs = []
        
    if q_type == "FA":
        
        story_f_1 = story_f.lower()
        start_ends = []
        answer_1 = [a.lower() for a in answer][0] 

        start_ans = [m.start() for m in re.finditer(answer_1, story_f_1)]
        end_ans = [m.end() for m in re.finditer(answer_1, story_f_1)]
        for obj_def in obj_defs:
            start_obj = [m.start() for m in re.finditer(obj_def, story_f_1)]
            end_obj = [m.end() for m in re.finditer(obj_def, story_f_1)]
            start_ends = limit_start_end(start_ans, end_ans, start_obj, end_obj, start_ends)
        return start_ends

        
    elif q_type == "FO":
        story_f_1 = story_f.lower()
        start_end_c = []
        if obj_defs:
            answer = answer.lower()
            start_ans = [m.start() for m in re.finditer(answer, story_f_1)]
            end_ans = [m.end() for m in re.finditer(answer, story_f_1)]
            
            for i, val in enumerate(start_ans):
                if before_words(story_f_1 ,val): start_end_c += [[start_ans[i], end_ans[i]]]  
            return start_end_c
        else:
            answer = [ans.lower() for ans in answer]
            sh_ob = [0,0]
            
            for ind, obj_def in enumerate(answer):
                answer_1 = obj_def.lower()
                start_ans = [m.start() for m in re.finditer(answer_1, story_f_1)]
                end_ans = [m.end() for m in re.finditer(answer_1, story_f_1)]
                for i, val in enumerate(start_ans):
                    if before_words(story_f_1 ,val): start_end_c += [[start_ans[i], end_ans[i]]] ; sh_ob[ind]=1
            if sh_ob[0] == 1 and sh_ob[1] == 1: answer_1 =  answer[0] if random.choice([0,1]) else answer[1]
            elif sh_ob[0] == 1: answer_1 =  answer[0]
            elif sh_ob[1] == 1: answer_1 =  answer[1]
            return start_end_c, answer_1

    
    answer = [ans.lower() for ans in answer]
    if 'dk' in answer[0] or 'nc' in answer[0] or 'both' in answer[0] or 'none' in answer[0] or 'none' in answer[0] or 'yes' in answer[0] or 'no' in answer[0]:
        return start_end
        
def limit_start_end(s_ans, e_ans, s_obj, e_obj, start_end):
    n = []
    n += start_end
    for i in range(len(s_ans)):
        for j in range(len(s_obj)):
            if s_ans[i] >= s_obj[j] and e_ans[i]<= e_obj[j] and [s_ans[i], e_ans[i]] not in n: n +=[[s_ans[i], e_ans[i]]]
    return n

def before_words(story, val):
    
    if story[val-5:val-1] == ' the' or story[val-5:val-1] == ' one' or story[val-5:val-1] == ' two' or story[val-7:val-1] == ' three' or story[val-6:val-1] == ' four' or story[val-6:val-1] == 'five' or story[val-5:val-1] == ' six' or story[val-7:val-1] == ' seven' or story[val-3:val-1] == ' a': return True
    else: return False

def make_plural(obj, root = ''):
    _root = root
    end_point = obj.find(root) + len(root)
    if root:
        if 'object' in root and 'objects' not in root: root = root.replace('object', 'objects')
        elif 'shape' in root and 'shapes' not in root: root = root.replace('shape', 'shapes')
        elif 'thing' in root and 'things' not in root: root = root.replace('thing', 'things')
        elif 'triangle' in root and 'triangles' not in root: root = root.replace('triangle', 'triangles')
        elif 'circle' in root and 'circles' not in root: root = root.replace('circle', 'circles')
        elif 'square' in root and 'squares' not in root: root = root.replace('square', 'squares')
        
        obj = obj[:end_point].replace(_root, root)+ obj[end_point:]
        
        end_is = obj.find('is')+2
        obj = obj[:end_is].replace('is', 'are')+ obj[end_is:]
        #if 'is' in root: root = root.replace('is', 'are')
            
    else: 
        if 'object' in obj and 'objects' not in obj: obj = obj.replace('object', 'objects')
        elif 'shape' in obj and 'shapes' not in obj: obj = obj.replace('shape', 'shapes')
        elif 'thing' in obj and 'things' not in obj: obj = obj.replace('thing', 'things')
        elif 'triangle' in obj and 'triangles' not in obj: obj = obj.replace('triangle', 'triangles')
        elif 'circle' in obj and 'circles' not in obj: obj = obj.replace('circle', 'circles')
        elif 'square' in obj and 'squares' not in obj: obj = obj.replace('square', 'squares')
    
        if 'is' in obj: obj = obj.replace('is', 'are')
    
    return obj

def add_the(sen):
    
    start1 = -1
    start = sen.find('that')
    start1 = sen.find('which')
    
    if start != -1 and start1 != -1:
        min_start = min(start, start1)
    elif start != -1: min_start = start
    else: min_start = start1
        
    if 'number' not in sen[:min_start]: return True
    else: return False
    
#**************************************
#*********Consistency part*************
#**************************************

def consistency_check(q_type, q_data, obj_data):
   
    consistency_list = [] # list of consistency questions and answers
    
    FR, FO, CO, YN = False, False, False, False
    if q_type == "FR": FO= True; CO= True; YN= True
    elif q_type == "FO": FR= True; CO= True; YN= True
    elif q_type == "CO": FO= True; FR= True; YN= True
    elif q_type == "YN": FO= True; CO= True; FR= True

    if FR: # create FR based on the object that are passed
        if q_type == "YN":
            if q_data["obj1_uniq"] and q_data["obj2_uniq"]: # FR can only accept unique object definition

                answer = ''
                if q_data["answer"] == ['Yes']: answer = q_data["relation"]
                elif q_data["answer"] == ['No']: answer = reverse(q_data["relation"])
                else: answer = 'DK' 
                consistency_list += FR_consis(q_data["obj1_def"], q_data["obj2_def"],answer)
                consistency_list[-1].append("FR")
        elif q_type == "CO":
            if q_data["answer"] == 0 and q_data["obj_uniq"] and q_data["obj1_uniq"]:
                answer = q_data["relation"]
                consistency_list += FR_consis(q_data["obj1_def"], q_data["obj_def"],answer)
                consistency_list[-1].append("FR")
            elif q_data["answer"] == 1 and q_data["obj_uniq"] and q_data["obj2_uniq"]:   
                answer = q_data["relation"]
                consistency_list += FR_consis(q_data["obj2_def"], q_data["obj_def"],answer)
                consistency_list[-1].append("FR")
            elif q_data["answer"] == 2 and q_data["obj_uniq"] and q_data["obj2_uniq"] and q_data["obj1_uniq"]:
                answer = q_data["relation"]
                consistency_list += FR_consis(q_data["obj1_def"], q_data["obj_def"],answer)
                consistency_list[-1].append("FR")
                consistency_list += FR_consis(q_data["obj2_def"], q_data["obj_def"],answer)
                consistency_list[-1].append("FR")
        else: # q_type == "FO"
            answer = q_data["relation"]
            if q_data["obj2_uniq"]:
                obj1_list = random.sample(q_data["obj1_def"], 3) if len(q_data["obj1_def"])>3 else q_data["obj1_def"]
                for obj in obj1_list:
                    consistency_list += FR_consis([obj], q_data["obj2_def"],answer)
                    consistency_list[-1].append("FR")
                
        
    if YN:
        if q_type == "FR":
            answer = 'Yes' if "DK" not in q_data["relation"] else 'DK'
            consistency_list += YN_consis(q_data["obj1_def"], q_data["obj1_uniq"], q_data["obj2_def"], q_data["obj2_uniq"],q_data["relation"], answer)
            consistency_list[-1].append("YN")
        elif q_type == "CO":
            answer = ['No','No']
            if q_data["answer"] == 0: answer[0] = 'Yes'
            elif q_data["answer"] == 1: answer[1] = 'Yes'
            elif q_data["answer"] == 2: answer = ['Yes','Yes']
            consistency_list += YN_consis(q_data["obj1_def"], q_data["obj1_uniq"], q_data["obj_def"], q_data["obj_uniq"],q_data["relation"], answer[0])
            consistency_list[-1].append("YN")
            consistency_list += YN_consis(q_data["obj2_def"], q_data["obj2_uniq"], q_data["obj_def"], q_data["obj_uniq"],q_data["relation"], answer[1])
            consistency_list[-1].append("YN")
        else: 
            
            if q_data["obj1_def"] != ['None']:
                obj1_list = random.sample(q_data["obj1_def"], 3) if len(q_data["obj1_def"])>3 else q_data["obj1_def"]
                for obj in obj1_list:
                    consistency_list += YN_consis([obj], q_data["obj1_uniq"], q_data["obj2_def"], q_data["obj2_uniq"],q_data["relation"], 'Yes')
                    consistency_list[-1].append("YN")
    if CO:
        if q_type == "FR":
            if "DK" not in q_data["relation"]:
                try:
                    consistency_list += CO_consis(q_data["obj1_def"], q_data["obj1_uniq"], q_data["obj2_def"], q_data["obj2_uniq"],q_data["relation"], obj_data["obj1"], obj_data["scn1"],obj_data["obj2"], obj_data["scn2"], obj_data["obj2s_temp"])
                    consistency_list[-1].append("CO")
                except:
                    raise
                    pass
        
        elif q_type == "YN":
            if q_data["obj1_uniq"] and q_data["obj2_uniq"] and q_data["answer"] == ["Yes"]: 
                try:
                    consistency_list += CO_consis(q_data["obj1_def"], q_data["obj1_uniq"], q_data["obj2_def"], q_data["obj2_uniq"],q_data["relation"], obj_data["obj1"], obj_data["scn1"],obj_data["obj2"], obj_data["scn2"], obj_data["obj2s_temp"])
                    consistency_list[-1].append("CO")
                except:
                    raise
                    pass
        
        elif q_type == "FO":
            if q_data["obj1_def"] != ['None']: 
                try:
                    obj = random.choice(q_data["obj1_def"])
                    consistency_list += CO_consis([obj], q_data["obj1_uniq"], q_data["obj2_def"], q_data["obj2_uniq"],q_data["relation"], -1, -1, obj_data["obj"], obj_data["scn"], obj_data["objs_temp"])
                    consistency_list[-1].append("CO")
                except:
                    raise
                    pass
 
    return consistency_list    

def YN_consis(obj1_def, obj1_uniq, obj2_def, obj2_uniq, rel, ans):
    
    sen, relation = '',''
    answer = [ans]
    
    if rel != "DK": relation = rel
    else: relation = random.choice(['left','right','above','below','near to', 'far from', 'touching'])
    obj1_defined = obj1_def
    obj1s_uniq = obj1_uniq
    obj2_defined = obj2_def
    obj2s_uniq = obj2_uniq
        
    if obj1s_uniq and obj2s_uniq: # when the objects are unique by their definition
        z = random.choice([0,1])
        if z: sen += 'Is the '+obj1_defined[0]+' '+R(relation)+' the '+obj2_defined[0]+'?'
        else: sen += 'Is there a '+obj1_defined[0]+' '+R(relation)+' a '+obj2_defined[0]+'?'
    elif obj1s_uniq or obj2s_uniq: 
        if obj1s_uniq: 
            z = random.choice([0,1])
            if z == 1: sen += 'Is the '+obj1_defined[0]+' '+R(relation)+' a '+obj2_defined[0]+'?'
            else: sen += 'Is the '+obj1_defined[0]+' '+R(relation)+'  any '+ make_plural(obj2_defined[0])+'?'
        else:
            z = random.choice([0,1])
            if z == 1: sen += 'Is there a '+obj1_defined[0]+' '+R(relation)+' the '+obj2_defined[0]+'?'
            else: sen += 'Is there any '+make_plural(obj1_defined[0])+' '+R(relation)+' the '+obj2_defined[0]+'?'
    else: 
        sen += 'Is there any '+make_plural(obj1_defined[0])+' '+R(relation)+' a '+obj2_defined[0]+'?'
    
    sen = edit_text_form(sen)
    return [[sen, answer, [], []]]
    
def CO_consis(obj1_def, obj1_uniq, obj2_def, obj2_uniq,rel, _obj1, _scn1,_obj2, _scn2, _obj2s_temp):
    
    global treshhold, temporary_objs, min_tresh, max_tresh, first_temp
    sen, answer = '',''
    start_end_c, candidate_answer = [], []
    obj, scn, objs_temp = _obj2, _scn2, _obj2s_temp
    obj1, scn1 = '','' 
    if _obj1 != -1: obj1 = _obj1; scn1 = _scn1 
    unique_obj = False #if we have a unique obj then we can ask question in two form. what is below the ob? which obj is below a obj? 
    unique_obj1_2 = False
    x = -1 #  0 for what is below the obj? 1 for which obj is below a obj? 
    relation = rel
    #defining object in the question
    obj_defined = obj2_def
    obj_unique = unique_obj = obj2_uniq
    obj1_defined = obj1_def
    obj1_unique = obj1_uniq
    x, x_tresh = 0, 10
    while 1:
        obj2, scn2 = one_obj_restricted(obj, scn,obj1, scn1)
        rel = FR_correct(obj, scn, obj2, scn2)
        if relation not in rel: break
        x+=1
        if x > x_tresh: return -1
    
    forbiden_list = []
    if scn == scn2: forbiden_list.append(obj)
    if scn1 == scn2: forbiden_list.append(obj1)
    max_tresh = 1
    min_treshhold = 1  
    obj2_defined = obj_def_q(obj2, scn2, forbiden_list=forbiden_list, min_treshhold = min_treshhold)
    treshhold = 0
    obj2s_temp = temporary_objs
    temporary_objs, first_temp = [], 1
    
    obj2_unique = True if len(obj2s_temp) == 1 else False
    
    if obj1_unique and obj2_unique:
        unique_obj1_2 = True
        x = random.choice([0,1]) if unique_obj else 1
    elif unique_obj: x = 0
    else: return -1
            
    max_tresh = 2
    if x == 1:
        sen += 'Which object is '+ R(relation)+' a '+obj_defined[0] +'? '
        if random.choice([0,1]):
            sen += 'the '+obj1_defined[0]+' or the '+obj2_defined+'?'  
            candidate_answer = [obj1_defined[0], obj2_defined, "both of them", "none of them"]
            answer = [0]
        else:
            sen += 'the '+obj2_defined+' or the '+obj1_defined[0]+'?'
            candidate_answer = [obj2_defined, obj1_defined[0], "both of them", "none of them"]
            answer = [1]
    else:
        sen += 'What is '+ R(relation)+' the '+obj_defined[0] +'? '
        if random.choice([0,1]):
            sen += 'a '+obj1_defined[0]+' or a '+obj2_defined+'?'  
            candidate_answer = [obj1_defined[0], obj2_defined, "both of them", "none of them"]
            answer = [0]
        else:
            sen += 'a '+obj2_defined+' or a '+obj1_defined[0]+'?'
            candidate_answer = [obj2_defined, obj1_defined[0], "both of them", "none of them"]
            answer = [1]
    
    sen = edit_text_form(sen)    
    return [[sen, answer, start_end_c, candidate_answer]]

def FO_consis(obj2_def, obj1_def, rel, obj2, scn2, obj2s_temp):
    global treshhold, temporary_objs, min_tresh, first_temp
    sen, answer = '',''
    obj, scn = obj2, scn2
    relation = rel
    obj_defined = obj2_def[0]
    objs_temp = obj2s_temp

    
    sen += 'Which object is/objects are '+R(relation)+' a '+obj_defined+'?'
    answer, start_end_c = answer_FO(obj,scn,objs_temp, relation)
    sen = edit_text_form(sen)
    return [[sen, answer, start_end_c, '']]
    

def FR_consis(obj1_def, obj2_def, ans):
    
    sen, answer = '',''
    
    obj1_defined = obj1_def
    obj2_defined = obj2_def

    sen += 'What is the relation between the '+obj1_defined[0]+' and the '+obj2_defined[0]+'?'
    
    candidate_answer = ["left", "right", "above", "below", "near to", "far from", "touching", "DK"]
    answer = [candidate_answer.index(ans)]
    sen = edit_text_form(sen)
    return [[sen, answer, [], candidate_answer]]




#**********************************************************
#******************Annotation functions********************
#**********************************************************

def create_annotation(sen, main = -1, polarity = False):
    
    global annotations 
    global trajector, landmark, spatial_ind, _traj_or_land, _phrase
    
    traj, land, sp_ind = trajector, landmark, spatial_ind
    
#     print('sentence: ', sen)
#     print('trajector:', traj, '\n Lnadmark', land,'\nSp-ind', sp_ind, '\nphrase', _phrase)
    
    if traj == []: print('!! ERROR empty traj') 
    if land == []: print('!! ERROR empty land') 
    if sp_ind == []: print('!! ERROR empty sp_ind') 
        
    sen = edit_text_form(sen)
    
    ann = {"main_description": main ,"spatial_description" : []}
    
    
    for ind in range(len(traj)):
        
        
        #trajector
        for tr in traj[ind]:
            trajector = {"phrase": '', "head": '', "properties": {}, "spatial_property": '', "SOT_sentence": {"start": '', "end": ''}}
            if tr:
                _traj = edit_text_form(tr)
                trajector['phrase'] = _traj
                trajector['head'], trajector['properties'], trajector['spatial_property'] = extract_properties(_traj)
        
            #landmark
            for ld in land[ind]:
                landmark = {"phrase": '', "head": '', "properties": [], "spatial_property": '', "SOT_sentence": {"start": '', "end": ''}}
                if ld:
                    _land = edit_text_form(ld)
                    landmark['phrase'] = _land
                    landmark['head'], landmark['properties'], landmark['spatial_property'] = extract_properties(_land)
                
                for sp in sp_ind[ind]:
                    spatial_value, g_type, s_type = '','',''
                    spatial_ind = { "phrase" : '',  "SOT_sentence": {"start": '', "end": ''}}
                    if sp:
                        spatial_ind['phrase'] = sp
                        spatial_value, g_type, s_type = spatial_indicator(sp, _land)
                    
                    # add 
                    ann['spatial_description'].append({"spatial_value":spatial_value, "g_type": g_type, "s_type": s_type , "polarity": polarity if ind == main else False, "FoR": 'Relative', "trajector": trajector, 'landmark': landmark, 'spatial_indicator': spatial_ind})
                    
    annotations.append(ann)
    SOT(sen)
    
    trajector, landmark, spatial_ind, _traj_or_land, _phrase = [], [], [], [], []
    
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
    
    elif "object" in sen: head = 'object'
    elif "thing" in sen: head = 'thing'
    elif "shape" in sen: head = 'shape'
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


def SOT(question):
    
    global annotations, _phrase
    sum_char = 0

    for ann in annotations:
        
        _annot =  question
        for ind, sp_desc in enumerate(ann['spatial_description']):
            phrase = edit_text_form(_phrase[ind][0])

            #trajector
            if sp_desc['trajector']['phrase']:
                
                start1 = None
                x = [m.start() for m in re.finditer(phrase, _annot)]
                start_phrase = 0 if ind == 0 else x[0]
                end_phrase = len(_annot) if ind == 0 else [m.end() for m in re.finditer(phrase, _annot)][0]
                
                _start = [m.start() for m in re.finditer(sp_desc['trajector']['phrase'], _annot)]
                start = [j for j in _start if j>= (start_phrase-4) and j <= end_phrase]
                
                if start == []: print('!! ERROR traj', _annot, ' | ', phrase,' | ', sp_desc['trajector']['phrase'],'\n', start_phrase, end_phrase, start); return -1
                    
                if len(start) ==1 or ind == 0: start1 = start[0]
                else:
                    start2 = start
                    for j in start2:
                        if _annot[j-1] and (_annot[j-1].isalpha() or _annot[j+len(sp_desc['trajector']['phrase'])].isalpha()): start.remove(j)
                    
                    
                    if 'block' in sp_desc['landmark']['phrase']: start1 = start[-1]
                    else: start1 = start[0]

                end = start1 + len(sp_desc['trajector']['phrase']) #- 1
                sp_desc['trajector']['SOT_sentence']['start'], sp_desc['trajector']['SOT_sentence']['end'] = start1 , end 
            
            #landmark
            if sp_desc['landmark']['phrase']:
                
                start1 = None
                
                x = [m.start() for m in re.finditer(phrase, _annot)]
                    
                start_phrase = x[0]
                end_phrase = len(_annot) if ind == 0 else [m.end() for m in re.finditer(phrase, _annot)][0]
                
                _start = [m.start() for m in re.finditer(sp_desc['landmark']['phrase'], _annot)]
                start = [j for j in _start if j>= (start_phrase-4) and j <= end_phrase]
                
                if start == []: print('!! ERROR land', _annot, sp_desc['landmark']['phrase'])
                if len(start) ==1 or ind == 0 : start1 = start[0]
                else:
                    start2 = start
                    for j in start2:
                        if _annot[j-1] and (_annot[j-1].isalpha() or _annot[j+len(sp_desc['landmark']['phrase'])].isalpha()): start.remove(j)
                    
                    start1 = start[-1]
                        
                end = start1 + len(sp_desc['landmark']['phrase']) #- 1
                sp_desc['landmark']['SOT_sentence']['start'], sp_desc['landmark']['SOT_sentence']['end'] = start1, end 
            
    
            #spatial_indicator
            if sp_desc['spatial_indicator']['phrase']:
                start1 = None
                x = [m.start() for m in re.finditer(phrase, _annot)]
                if len(x)>1 and 'is' not in phrase: return -1    
                start_phrase = 0 if ind == 0 else x[0]
                end_phrase = len(_annot) if ind == 0 else [m.end() for m in re.finditer(phrase, _annot)][0]
                
                _start = [m.start() for m in re.finditer(sp_desc['spatial_indicator']['phrase'], _annot)]
                start = [j for j in _start if j>= (start_phrase - 4) and j <= (end_phrase) and _annot[j-1] == ' ']
                if start == []: print('!! ERROR sp',_annot, sp_desc['spatial_indicator']['phrase'])
                if len(start) == 1: start1 = start[0]  
                else: #if ind == 0: #more than one similar indicator
                    start2 = start
                    for j in start2:
                        if _annot[j-1] and (_annot[j-1].isalpha() or _annot[j+len(sp_desc['spatial_indicator']['phrase'])].isalpha()): start.remove(j)
                    
    
                    # the nearest indicator before the main landmark
                    main_land_start = sp_desc['landmark']['SOT_sentence']['start']
                    before_land_start = [ j for j in start if j < main_land_start]
                    start1 = max(before_land_start)

                    
                end = start1 + len(sp_desc['spatial_indicator']['phrase']) #- 1
                sp_desc['spatial_indicator']['SOT_sentence']['start'], sp_desc['spatial_indicator']['SOT_sentence']['end'] = start1 , end 
