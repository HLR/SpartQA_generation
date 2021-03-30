# import json
import random
import numpy as np
from Find_Relations import scene_obj_relation, obj_obj_relation


def total_number_func(story):
    num = 0
    for i in story['structured_rep']:
        num += len(i)
    return num

def random_choice(story):
    
    total_number = total_number_func(story)
    if total_number < 5: return -1
    
    # Choose how many block we should consider.
    weighted_random = [1] * 5 + [2] * 9 + [3] * 6
    # Choose scenes and their relations (Randomly) 
    num_scenes = random.choice(weighted_random)
    
    directions= ['left','right','below','above'] #Left, Right, Below, Above
    rels_scenes = []
    choose1, choose2, notchoose= '', '', -1

    for i in range(num_scenes-1):
        first= random.choice(range(num_scenes))
        if choose1 == first:
            notchoose = choose2
        elif choose2 == first:
            notchoose = choose1
        sec= random.choice([i for i in range(num_scenes) if i != first and i != notchoose])
        choose1 = first
        choose2 = sec
        rels_scenes.append([[first, sec], directions[random.choice(range(4))]])

    scenes = ['']*num_scenes


    #Choose object in the scene and its relation with the scene
    for i in range(num_scenes):

        # choose if each object can exist in the scene or not
        objects_in_scene = []
        num_obj = len(story['structured_rep'][i])
        for j in range(num_obj):
            exist = random.choice([0,1]) if total_number > 8 else random.choice([0,0,1,1,1,1,1])
            if exist == 1:
                rels = scene_obj_relation(story, i, j)
                rels.append('in') # NTTP
                objects_in_scene.append([rels, story['structured_rep'][i][j]])

            elif j == num_obj-1 and not objects_in_scene:
                rels = scene_obj_relation(story, i, j)
                rels.append('in') # NTTP
                objects_in_scene.append([rels, story['structured_rep'][i][j]])       
        scenes[i]= objects_in_scene


    #Choose relation between objects
    total_num_of_objs = 0
    relations_objects_in_scenes, temporary = [], []
    for scene in scenes:
        num_objs = len(scene)
        num_rels = int(num_objs * (num_objs-1) / 2)
        num_rels = num_rels if num_rels <= 5 else 5
        if num_objs > 1:
            objs_relations = []
            for i, obj in enumerate(scene):
                for j in [x for x in range(num_objs) if x != i]:
                    obj_rel = obj_obj_relation(scene, i, j, objs_relations)
                    if obj_rel:
                        objs_relations+=[[[i,j],obj_rel]]
            relations_objects_in_scenes.append(choose_between_rels(num_rels, objs_relations))

            
            total_num_of_objs += num_objs
            
        elif num_objs == 1:
            relations_objects_in_scenes+= [[]]
            total_num_of_objs += num_objs
        

    if total_num_of_objs > 4:
        
#         print("\n\nRelation between the scene are: \n")
#         for i in rels_scenes:
#             print(i)
#         print("\n\nRelation of objects in each scene: \n")
#         for i in scenes:
#             print(i)
#         print("\n\nRelation between objects: \n")
#         for i in relations_objects_in_scenes:
#             print(i)
        return [rels_scenes, scenes, relations_objects_in_scenes]
    
    else:
        return []


def choose_between_rels(num, rels):
    
    rels_copy = rels
    num_of_rels = 0
    random_choose = []
    
    while num_of_rels < num:
        sample = rels_copy.pop(random.choice(range(len(rels_copy))))

        choosed_rels = random.sample(sample[1], random.choice(range(len(sample[1])))+1)
        if 'touching' in sample[1] and 'touching' not in choosed_rels: choosed_rels+=['touching']
        if choosed_rels:
            random_choose += [[sample[0], choosed_rels]]

            num_of_rels+= len(choosed_rels)
    return random_choose