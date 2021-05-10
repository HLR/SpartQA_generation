## SpartQA

We take advantage of the ground truth of NLVR images, design CFGs to generate stories, and use spatial reasoning rules to ask and answer spatial reasoning questions. This automatically generated data is called SpartQA-Auto.

Without processing the raw text, which is error-prone, we generate questions by only looking at the stored data. 

There are four types of questions (q-types). 
(1)**FR**: find relation between two objects. 
(2) **FB**: find the block that contains certain object(s). 
(3)**CO**: choose between two objects mentioned in the question that meets certain criteria. 
(4) **YN**: a yes/no question that tests if a claim on spatial relationship holds.

All four types of questions are formulated as multiple-choice questions.
Specifically, FB, FR, and CO questions receive a list of candidate answers, and YN questions are choosing from Yes, No, or ``DK''~(Do not Know). The `` DK'' option is due to the open-world assumption of the stories, where if something is not described in the text, it is not considered false.


For generating the data samples:
1. Create a Dataset and NLVR directory. 
2. Put the NLVR train.json, test.json. dev.json in the NLVR directory. 
3. In Dataset_gen.py set "file_name1" to the NLVR file (e.g. "test", "dev," or "train") and "file_name" to the desire set name (e.g. "test", "unseentest", "train_24k" and etc.)
4. Set the values of num_of_stories, num_story_per_img, num_q_qtype.     
5. Run the Dataset_gen.py file in terminal.


There are three types of annotation for each set. 
1. Annotation: has the scene graph of each scene
2. SpRL: has the annotation regrading the Spatial Role and Relation extraction
3. The main file which has stories, questions, answers, candidate answers, consistency and contrast set (if appliable).

Dataset is provided in SpartQA.zip : https://github.com/HLR/SpartQA_generation/blob/main/SpartQA.zip

To see the implemented baselines on this dataset check : https://github.com/HLR/SpartQA-baselines
