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

3. Use below arguments on Dataset_gen.py for generting the data:


    "--num_image",  help="Number of image, 6660 for train, 1000 for other", type= int, default=1000
    
    "--story_per_image",  help="How many story do you want to create for each image", type= int, default=2
    
    "--num_question",  help="number of question for each question type.", type= int, default=2
    
    "--question_type",  help="name of the question types: all, YN, FB, FR, CO", type= str, default='all'
    
    "--no_save",  help="just testing generation phase", action='store_true', default = False
    
    "--seed_num", help="add seed number for random choices.", type= int, default=None
    
    "--skip_except", help="skip all examples expcept story X", type= int, default=None

  

    for example:       python3 Dataset_gen.py --name dev --nlvr_data dev
    
    or :                      python3 Dataset_gen.py --name train --nlvr_data train --num_image 6660

  
  
  

There are three types of annotation for each set.

1. Annotation: has the scene graph of each scene

2. SpRL: has the annotation regrading the Spatial Role and Relation extraction

3. The main file which has stories, questions, answers, candidate answers, consistency and contrast set (if appliable).

  

Dataset is provided in SpartQA.zip : https://drive.google.com/file/d/12s2olGDV0ruywPtLhGL5M-1e4CbQrA8k/view?usp=sharing

  

To see the implemented baselines on this dataset check : https://github.com/HLR/SpartQA-baselines



To cite the paper use below Bibtex:

  @inproceedings{mirzaee-etal-2021-spartqa,
      title = "{SPARTQA}: A Textual Question Answering Benchmark for Spatial Reasoning",
      author = "Mirzaee, Roshanak  and
        Rajaby Faghihi, Hossein  and
        Ning, Qiang  and
        Kordjamshidi, Parisa",
      booktitle = "Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies",
      month = jun,
      year = "2021",
      address = "Online",
      publisher = "Association for Computational Linguistics",
      url = "https://aclanthology.org/2021.naacl-main.364",
      doi = "10.18653/v1/2021.naacl-main.364",
      pages = "4582--4598",
  }
