import os
import sys
import shutil

def split_basename(basename):
    base=basename
    if basename.endswith(".txt"):
        base=basename.rstrip(".txt")
    elif basename.endswith(".png"):
        base=basename.rstrip(".png")
    splits=base.split("_")
    vid,cam,id = "".join(splits[:-2]) , splits[-2], splits[-1]
    return vid,cam,id
    
    
def parse_all_files(file):
    files_dict={}
    with open(file) as f:
        for line in f:
            line=line.rstrip("\n")
            basename=os.path.basename(line)
            vid,cam,id=split_basename(basename)
            vid_frame = vid+"_"+id
            if vid_frame in files_dict.keys():
                files_dict[vid_frame].append(line)
            else:
                files_dict[vid_frame]=[line]
    return files_dict

def get_file_list(batch_files, files_dict):
    file_list=[]
    for f in batch_files:
        with open(f) as fin:
            for line in fin:
                line=line.rstrip("\n")
                vid,cam,id=split_basename(line)
                vid_frame = vid+"_"+id
                if vid_frame in files_dict.keys():
                    file_list=file_list+files_dict[vid_frame]
                else:
                    print("Something wrong with file "+vid)
    return set(file_list)
                
def copy_in_output_folder(outfolder, img_selection):
    for img in img_selection:
        shutil.copy(img, outfolder)
    
if __name__=="__main__":
    
    batch_files=["batch1.txt","batch2.txt"]
    all_files="allfiles.txt"
    outfolder="/mnt/vision/DL/annotation/"
    
    files=parse_all_files(all_files)
    img_selection=get_file_list(batch_files, files)
    #print(img_selection)
    copy_in_output_folder(outfolder, img_selection)
    
    