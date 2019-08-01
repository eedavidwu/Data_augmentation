#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os, sys, pdb, numpy
from PIL import Image, ImageChops, ImageOps, ImageDraw

from os import listdir, getcwd

import shutil

wd=getcwd()
input_path=os.path.join(wd,'images')
in_label_path=os.path.join(wd,'labels')

output_path=os.path.join(wd,'out_images')
out_label_path=os.path.join(wd,'out_labels')


def gen_crop(i, w, h):
    numpy.random.seed(4 * i)
    x0 = numpy.random.random() * (w / 6)
    y0 = numpy.random.random() * (h / 6)
    x1 = w - numpy.random.random() * (w / 6)
    y1 = h - numpy.random.random() * (h / 6)
    print(int(x1-x0),'/',w,int(y1-y0),'/',h)
    return (int(x0), int(y0), int(x1), int(y1))



# the main fonction to call
# takes a image input path, a transformation and an output path and does the transformation

def gen_trans(imgfile, trans, outfile):
    for trans in trans.split('*'):
        print("process %s" % imgfile)
        image = Image.open(imgfile)
        w, h = image.size
        if trans == "flip":
            ImageOps.mirror(image).save(outfile, "JPEG", quality=100)
        elif trans.startswith("crop"):
            c = 1
            image.crop(gen_crop(c, w, h)).save(outfile, "JPEG", quality=100)
        else:
            assert False, "Unrecognized transformation: " + trans
        imgfile = outfile  # in case we iterate




if __name__ == "__main__":
    file_name = [name for name in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, name))]

    print(len(file_name))
    count_big=0
    count_small=0
    trans = ['flip','crop']


    for k in file_name:
        for t in trans:
            img_input_path = os.path.join(input_path,k)
            img_outfile=  os.path.join(output_path, '%s_%s' % (t, k))
            gen_trans(img_input_path, t, img_outfile)

            label_input_path=os.path.join(in_label_path,k).replace('.jpg','.txt')
            label_file=open(label_input_path,'r')
            label=label_file.readline()

            out_label=os.path.join(out_label_path, '%s_%s' % (t, k)).replace('.jpg','.txt')
            label_out_file = open(out_label, 'w')
            label_out_file.write(label)

            label_file.close()
            label_out_file.close()


    print ('Finished:\n' ,'images store in', output_path,'\n','labels store in:',out_label_path)
    #print ('Generating transformations:\n','images store in', output_path,'\n','labels store in:',out_label_path )
    
