#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function)
from PIL import Image
import six

import imagehash


def hamming2(s1, s2):
    bytesS1=bytes(s1, encoding="ascii")
    bytesS2=bytes(s2, encoding="ascii")
    diff=0;
    for i in range(min(len(bytesS1),len(bytesS2))):
        if(bytesS1[i]^bytesS2[i]!=0):
            diff+=1;
    return(diff)
    
"""
Demo of hashing
"""
def find_similar_images(userpaths, hashfunc = imagehash.average_hash):
    import os
    BASE_PATH="/mnt/vision/"
    def is_image(filename):
        f = filename.lower()
        return f.endswith(".png") or f.endswith(".jpg") or \
            f.endswith(".jpeg") or f.endswith(".bmp") or f.endswith(".gif") or '.jpg' in f
    
    image_filenames = []
    if len(userpaths)>1:
        for userpath in userpaths:
            image_filenames += [os.path.join(userpath, path) for path in os.listdir(userpath) if is_image(path)]
    elif len(userpaths)==1 and userpaths[0].endswith(".txt"):
        for line in open(userpaths[0],'r'):
            image_filenames.append(BASE_PATH+line.rstrip('\n')+".png" )
        
        
    images = {}
    hashes = []    
    for img in sorted(image_filenames):
        try:
            hash = hashfunc(Image.open(img))
        except Exception as e:
            print('Problem:', e, 'with', img)
        #if hash in images:
        #    print(img, '  already exists as', ' '.join(images[hash]))
        #    if 'dupPictures' in img:
        #        print('rm -v', img)
        to_add = True
        #print(len(hashes) )
        for h in hashes:
            d=h-hash
            #print(h-hash)
            if d<20:
                to_add=False
                break
        if to_add:
            hashes.append(hash)            
            images[hash] = img
    
    print("Total unique images: " + str(len(image.keys() ) ) )
    with open("unique_images.txt","w") as f:
        for k in images.keys():
            print(images[k])
    #for k, img_list in six.iteritems(images):
    #    if len(img_list) > 1:
    #        print(" ".join(img_list))


if __name__ == '__main__':
    import sys, os
    def usage():
        sys.stderr.write("""SYNOPSIS: %s [ahash|phash|dhash|...] [<directory>]

Identifies similar images in the directory.

Method: 
  ahash:      Average hash
  phash:      Perceptual hash
  dhash:      Difference hash
  whash-haar: Haar wavelet hash
  whash-db4:  Daubechies wavelet hash

(C) Johannes Buchner, 2013-2017
""" % sys.argv[0])
        sys.exit(1)
    
    hashmethod = sys.argv[1] if len(sys.argv) > 1 else usage()
    if hashmethod == 'ahash':
        hashfunc = imagehash.average_hash
    elif hashmethod == 'phash':
        hashfunc = imagehash.phash
    elif hashmethod == 'dhash':
        hashfunc = imagehash.dhash
    elif hashmethod == 'whash-haar':
        hashfunc = imagehash.whash
    elif hashmethod == 'whash-db4':
        hashfunc = lambda img: imagehash.whash(img, mode='db4')
    else:
        usage()
    userpaths = sys.argv[2:] if len(sys.argv) > 2 else "."
    find_similar_images(userpaths=userpaths, hashfunc=hashfunc)
    

