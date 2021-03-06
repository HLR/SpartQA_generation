import json
import random
import re
from tqdm import tqdm
from Random_choice import random_choice
from Creating_story import creating_story
from Creating_questions import creating_questions
from Change_Words import change_words, change_words_ans
from Annotation import creating_annotation
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--nlvr_data",help="Name of the sets in the NLVR dataset", type= str, default='test')
parser.add_argument("--name",help="Name of the set in spartqa dataset", type= str, default='test')

parser.add_argument("--num_image", help="Number of image, 6660 for train, 1000 for other", type= int, default=1000)
parser.add_argument("--story_per_image",help="How many story do you want to create for each image", type= int, default=2)
parser.add_argument("--num_question",help="number of question for each question type.", type= int, default=2)
parser.add_argument("--question_type",help="name of the question types: all, YN, FB, FR, CO", type= str, default='all')
parser.add_argument("--no_save", help="just testing generation phase", action='store_true', default = False)
parser.add_argument("--seed_num",help="add seed number for random choices.", type= int, default=None)
parser.add_argument("--skip_except",help="skip all examples expcept story X", type= int, default=None)


args = parser.parse_args()

# consistency just created for test set
nlvr_data = args.nlvr_data
file_name = args.name
data = [json.loads(line) for line in open('NLVR/'+nlvr_data+'.json', 'r')]

num_of_stories, num_story_per_img, num_q_qtype, pass_num = args.num_image, args.story_per_image, args.num_question, 0

f2 = open('Dataset/'+file_name+'.txt','w')

dataset = {"name": "SPaRTQA" ,"data" : []}
annotation = {"name": "SpaRTQA_Annotation", "data": []}
SpRL_annotation = {"name": "SpaRTQA_SpRL_Annotation", "data": []}

for per_img in tqdm(range(num_story_per_img)):
    len_story =len(data[:num_of_stories])
    for each_data in tqdm(range(len_story)):
        if args.skip_except and each_data != args.skip_except: continue
        zxy = args.seed_num if args.seed_num else (len_story*(per_img))+each_data 
        random.seed(zxy)
        
        # print("sample ", (len_story*per_img)+each_data+1 , ' done!')
        print("**************** story ", (len_story*per_img)+each_data+1," ****************", file = f2)
         
        
        story = data[each_data]
        
            
        try:
            story_prop = creating_story(story, f2)
            #_final_story,scn_scn_rels, objs_attrs_f, objs_objs_f, _num_scenes= creating_story(story, f2)
            
        except KeyboardInterrupt:
            raise
        except:
            pass_num += 1
            raise
            continue
        
        if story_prop == -1 : pass_num +=1; continue
        else: _final_story,scn_scn_rels, objs_attrs_f, objs_objs_f, annotation_main,_num_scenes = story_prop
        
#         print(_final_story,scn_scn_rels, objs_attrs_f, objs_objs_f)
        
        #removing \n from stories.
        characters_to_remove = "\n"
        for character in characters_to_remove:
            story_f = _final_story.replace(character, "")
        
        #set value for unseen test
        random_change = 1 if file_name == 'unseen_test' else 0
        if random_change:
            rel_rand = [random.choice([0,1]) for i in range(5)]
            shape_rand = [random.choice([0,1]) for i in range(3)]
            size_rand = [random.choice([0,1]) for i in range(3)]
            color_rand = [random.choice([0,1]) for i in range(3)]
            
        #annotation
        if file_name != 'unseen_test':
            annotation_main['story'] = story_f
            annot = {"story": annotation_main, "questions": []}
        else: annot = {}
        
        #create unseen test by changing words
        story_ff = change_words(story_f, rel_rand, shape_rand, size_rand, color_rand) if random_change == 1 else story_f
        
        #creating annotation
        annotation['data'].append(creating_annotation(story_ff, scn_scn_rels, objs_attrs_f, objs_objs_f, annotation_main))
        
        print(story_ff, file = f2)

        
        single_story = {"identifier": story['identifier'], "directory": story['directory'],"seed_id": zxy, "story":[story_ff], "questions": []}
        
        Question_name = ["YN","CO","FR","FB"]  #["YN"]#["YN","CO","FR","FB"] #"FA","FO", "YN"
        q_index = 0
        for q_type in Question_name:
            object_id_from_pre_Q = []
            for i in range(num_q_qtype):
                
                if args.question_type != 'all' and q_type != args.question_type: continue
                # if _final_story != "We have two blocks, A and B. Block A is to the left of B. Block A has a medium yellow square. Block B contains two medium blue squares and two other medium black squares. Medium blue square number one is below medium black square number two and medium blue square number two. Below medium black square number two and medium black square number one there is medium blue square number two. Medium black square number one is below medium black square number two.": continue
                if q_type == "FB" and _num_scenes == 1: continue 
                
                try:
                    question_prop = creating_questions(q_type, _final_story, scn_scn_rels, objs_attrs_f, objs_objs_f, _num_scenes, object_id_from_pre_Q)

                except:
                    raise 
                    continue
                
                if question_prop == -1: continue
                else: question, answer, start_end_char, candidate_answer, consistency, contrast, q_annotation, reasoning_type, indifinite, object_id_from_pre_Q = question_prop
                # print('answer', _final_story, question,answer, candidate_answer)
                
                if 'DK' in question: continue #or 'edge' in question: continue
                    
                consistency_list = []
                if nlvr_data == "test": 
                    for ind,consist in enumerate(consistency):
                        ques = change_words(consist[0], rel_rand, shape_rand, size_rand, color_rand) if random_change else consist[0]
                        ans = change_words_ans(consist[1], rel_rand, shape_rand, size_rand, color_rand) if random_change else consist[1]
                        cand = change_words_ans(consist[3], rel_rand, shape_rand, size_rand, color_rand) if random_change else consist[3]
                        start_end = None if random_change else consist[2]
                        
                        consistency_list.append({"consistency_id": ind,  "question": ques, "answer": ans, "candidate_answers": cand, "start_end_char": start_end}) 
                
                #Contrast set
                contrast_list = []
                if nlvr_data == "test":
                    for ind,cont in enumerate(contrast):
                        ques = change_words(cont[0], rel_rand, shape_rand, size_rand, color_rand) if random_change == 1 else cont[0]
                        ans = change_words_ans(cont[1], rel_rand, shape_rand, size_rand, color_rand) if random_change == 1 else cont[1]
                        cand = change_words_ans(cont, rel_rand, shape_rand, size_rand, color_rand) if random_change == 1 else cont[3]
                        start_end = None if random_change else cont[2]
                        
                        contrast_list.append({"contrast_id": ind, "question": ques, "answer": ans, "candidate_answers": cand, "start_end_char": start_end})
                
                
                question_f = change_words(question, rel_rand, shape_rand, size_rand, color_rand) if random_change == 1 else question
                answer_f = change_words_ans(answer, rel_rand, shape_rand, size_rand, color_rand) if random_change == 1 else answer
                candidate_answer_f = change_words_ans(candidate_answer, rel_rand, shape_rand, size_rand, color_rand) if random_change == 1 else candidate_answer
                
                print('\n',q_type, ': ',question_f, answer_f, file = f2)
               
                if file_name != 'unseen_test':
                    annot['questions'].append({"q_type": q_type, "question": question_f, "annotation": q_annotation})
            
                single_story['questions'].append({"q_id": q_index, "q_type": q_type, "reasoning_type": reasoning_type ,"indifinite": indifinite, "question": question_f, "answer": answer_f, "candidate_answers": candidate_answer_f, "start_end_char": start_end_char, "consistency_check": consistency_list, "contrast_set": contrast_list})
                q_index += 1
                
        SpRL_annotation['data'].append(annot)        
        dataset['data'].append(single_story)
        
f2.close()
print("\nTotal number of stories: ", (len(data[:num_of_stories]) * num_story_per_img) - pass_num)

if not args.no_save:
    with open('Dataset/'+file_name+'.json', 'w') as outfile:
        json.dump(dataset, outfile)
        
    with open('Dataset/annotation_'+file_name+'.json', 'w') as outfile:
        json.dump(annotation, outfile)
        
    with open('Dataset/SpRL_annotation_'+file_name+'.json', 'w') as outfile:
        json.dump(SpRL_annotation, outfile)