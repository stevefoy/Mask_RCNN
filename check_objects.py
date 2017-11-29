import os
import sys
import glob
import util.annotation
import numpy as np

if __name__ == "__main__":
    if len(sys.argv)!=4:
        print("    Use python check_objects.py <input_folder> <class> <min_amount>")
        exit()
        
    input_folder = sys.argv[1]
    filter_class=sys.argv[2]
    num_obj=sys.argv[3]
    valid_files=[]
    samples_file=[]
    total_files = 0
    
    for file in glob.glob(input_folder + "/*.json"):
        ped_cont = 0
        filename = os.path.basename(file).rstrip(".json")
        preds = util.annotation.ImageDBAnnotation()
        preds.load(file) 
        for annot in preds.imageAnnotation.annotation:
            if filter_class in annot.tags:
                ped_cont=ped_cont+1
        if ped_cont>=num_obj:
            valid_files.append(filename)
            samples_file.append(ped_cont)
        total_files=total_files+1
    
    print("Total valid files: " + str(len(valid_files) ) )
    print("Avg no. of objects per valid file " + str(np.sum(samples_file)/len(valid_files)  ) ) 
    print("Avg no. of objects on total files " + str(np.sum(samples_file)/total_files) )
    print("Valid samples:")
    for f in valid_files:
        print(f)