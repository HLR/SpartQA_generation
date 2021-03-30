sprl_annotation = []

def creating_annotation(story, block_rels, objects_desc, objects_rels, _sprl_annotation):
    
    global sprl_annotation
    sprl_annotation = _sprl_annotation
    
    annotation = {"story":[story], "blocks": [], "relations_between_blocks":[]}
    
    annotation['blocks'], annotation['relations_between_blocks'] = blocks(block_rels)
    
    for i in range(len(annotation['blocks'])):
        annotation['blocks'][i]['objects'],annotation['blocks'][i]['relations_between_objects'] = objects(i,objects_desc, objects_rels)
    
    return annotation

def blocks(blocks_rels):
    all_blocks = []
    blocks_name = ['A','B','C']
    for i in range(len(blocks_rels)+1):
        blocks = {"id": -1, "name": '', "phrases":[] ,"objects": [], "relations_between_objects": []}
        blocks['name'] = blocks_name[i]
        blocks['id'] = i+100
        blocks['phrases'] = find_phrases(i+100, i+100)
        all_blocks.append(blocks)
    
    block_relations = []
    for rel in blocks_rels:
        block_relations.append({'trejector': rel[0][0]+100, 'landmark': rel[0][1]+100, 'spatial_indicator': rel[1] })


    return all_blocks,block_relations

def objects(block_num, objects_desc, objects_rels):
    
    object_name = []
    for obj in objects_desc[block_num]:
        if obj:
            obj = {"id": obj[0], "phrases": find_phrases(obj[0], 100+block_num), "shape": obj[3]['type'] if obj[3] else '', "color": obj[2]['color'] if obj[2] else '', "size": obj[1]['size'] if obj[1] else '',  "number": obj[5] if obj[5] != '' else '', 'rel_with_block': obj[4]['rel'] if obj[4] != '' else 'in' }
            #add this after debugging the problem of adding rel without existing in story  "relation_to_block": obj[4]['rel'] if obj[4] else '',
            object_name.append(obj)
            
    object_relation = []
    for rel in objects_rels[block_num]:
        if rel:
            object_relation.append({'trejector': rel[0][0], 'landmark': rel[0][1], 'spatial_indicator': rel[1] })

    return object_name, object_relation



def find_phrases(obj_id, block_id):
    
    all_phrases = []
    for annot in sprl_annotation['annotations']:
        
        for triplet in annot['spatial_description']:
#             print(triplet)
#             print(type(obj_id), type(block_id), type(triplet['trajector']['entity_id']), type(triplet['trajector']['block_id']))

            if triplet['trajector']['entity_id'] == obj_id and triplet['trajector']['block_id'] == block_id: 
        
                all_phrases += [{"phrase": triplet['trajector']["phrase"], "SOT_sentence": triplet['trajector']["SOT_sentence"], "SOT_text":triplet['trajector']["SOT_text"]}]

            elif triplet['landmark']['entity_id'] == obj_id and triplet['landmark']['block_id'] == block_id: 
                
                all_phrases += [{"phrase": triplet['landmark']["phrase"], "SOT_sentence": triplet['landmark']["SOT_sentence"], "SOT_text":triplet['landmark']["SOT_text"]}]
    
    
    return all_phrases
            
            
        