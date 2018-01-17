import os
import sys
import glob
import util.annotation
import numpy as np

if __name__ == "__main__":
    if len(sys.argv)!=5:
        print("    Use python check_objects.py <input_folder> <class> <min_amount> <output_file>")
        exit()
        
    input_folder = sys.argv[1]
    filter_class=sys.argv[2]
    num_obj=int(sys.argv[3])
    output_file=sys.argv[4]
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
    
    print("Total valid files: " + str(len(valid_files) )+ " out of "+ str(total_files) )
    print("Avg no. of objects per valid file " + str(np.sum(samples_file)/len(valid_files)  ) ) 
    print("Avg no. of objects on total files " + str(np.sum(samples_file)/total_files) )
    #print("Valid samples:")
    
    with open(output_file, 'w') as f:
        for name in valid_files:
            f.write(name+'\n')