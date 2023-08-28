import os
import shutil
import cv2
from distorter import pers_fixer, cropper, expander, rotator, stacker, resizer
import time
import json
import math
import numpy as np

def hello_world():
    print('Hello World')
    
def nihility():
    pass

def folder_maker(path,name):
    dir_existence = os.path.exists(path + '/' + name)
    if(dir_existence == False):
        print(f'{name} does not exist creating new directory...')
        os.mkdir(path + '/' + name)
    else:
        print(f'{name} already existed on the specified path, continuing other operation...')
           
if __name__ == "__main__":

    folder_maker('..','Input')
    folder_maker('..','Output')
            
    img_list = []
    for file in os.listdir("../Input"):
        if (file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.PNG')):
            img_list.append(file)
    if len(img_list) == 0:
        print('Input and Output folder have been created put Image inside Input folder to continue.')
        exit()
    print(f'Found {len(img_list)} Images in the Input folder')
    
    while(1):
        selection = input('Proceed with all the image in input folder?(Y/n) :')
        if selection == 'Y':
            break
        elif selection == 'n':
            print("Remove unwanted Photo then try again")
            exit()
        else: pass

    orient = ['top','left','right','bot']
    folder_maker('..\Output',"PW_Image")
    
    for file in img_list:
        inpath = '..\\Input\\' + file
        img = cv2.imread(inpath,cv2.IMREAD_UNCHANGED)
        img = resizer(img,452)
        folder_maker('..\\Output\\PW_Image', file)
        outpath = '..\\Output\\PW_Image\\' + file + '\\' 
        img_center = pers_fixer(img, 'top', 0)
        for theta in range(-30,31,5):
            img_expanded = expander(img_center)
            img_rotated = rotator(img_expanded,theta)
            cropped_img = cropper(img_rotated)
            outpath_center = outpath + 'center_0' + '_' + str(theta) + '.png'
            cv2.imwrite(outpath_center,cropped_img)
        for x in orient:
            for i in range(5, 26, 5):
                img_mutated = pers_fixer(img, x, i)
                for theta in range(-30,31,5):
                    img_expanded = expander(img_mutated)
                    img_rotated = rotator(img_expanded,theta)
                    cropped_img = cropper(img_rotated)
                    file_name = x + '_' + str(i) + '_' + str(theta) + '.png'
                    outpath_for = outpath + file_name
                    print(file_name)
                    cv2.imwrite(outpath_for,cropped_img)

    print('Transparent Image Batches Generated!')
    print('Stacking will now begin...')
    
    #The triple for loop of death.
    bg_path = '../Background'
    now = time.strftime("(%Y-%m-%d)%H-%M", time.localtime())
    folder_maker('../Output',now)
    for folder in os.listdir("../Output/PW_Image"): # Folder selection
        path_PW = '../Output/PW_Image/' + folder 
        for file in os.listdir(path_PW): # for each file inside the folder
            for bg in os.listdir(bg_path): # stack with the 10 backgrouds prepared
                bg_file = bg_path + '/' + bg
                fg_file = path_PW + '/' + file
                bg_uint = cv2.imread(bg_file,cv2.IMREAD_UNCHANGED)
                fg_uint = cv2.imread(fg_file,cv2.IMREAD_UNCHANGED)
                img_stacked,x,y,h,w = stacker(fg_uint,bg_uint)
                out_name = folder + ';' + str(x) + ';' + str(y) + ';' + str(w) + ';' + str(h) + ';' + bg
                out_dest = '../Output/' + now + '/' + out_name
                print(out_name)
                cv2.imwrite(out_dest,img_stacked)
    
    print('Image Ready to be annotated!')
    print('Splitting Files in to Training batch...')
    
    file_amount = len(os.listdir('../Output/' + now))
    percent_train = 70
    percent_valid = 20
    percent_test = 10
    train_size = int(math.floor((percent_train*0.01)*file_amount))
    valid_size = int(math.floor((percent_valid*0.01)*file_amount))
    test_size = int(math.floor((percent_test*0.01)*file_amount))
    excess = (file_amount - train_size - valid_size - test_size)
    train_size = train_size + excess
    shuffler = np.zeros(train_size).tolist()
    tempo = np.zeros(valid_size)
    tempo.fill(1)
    shuffler = np.append(shuffler,tempo)
    tempo = np.zeros(test_size)
    tempo.fill(2)
    shuffler = np.append(shuffler,tempo)
    np.random.shuffle(shuffler)
    files = os.listdir('../Output/' + now)
    folder_maker('../Output/' + now,'test')
    folder_maker('../Output/' + now,'train')
    folder_maker('../Output/' + now,'valid')
    i = 0
    for file in files:
            if shuffler[i] == 0:
                batch = 'train'
            elif shuffler[i] == 1:
                batch = 'valid'
            elif shuffler[i] == 2:
                batch = 'test'
            shutil.move('../Output/' + now + '/' + file, '../Output/' + now + '/' + shuffler[i] )
            i = i + 1

    print('Annotating...')
        
    anno = {}
    anno['info'] = {}
    anno['licenses'] = []
    anno['categories'] = []
    anno['images'] = []
    anno['annotations'] = []
    
    desc = 'Dataset from data augmentation script'
    
    anno['info'] = {'description': desc , 'date_created': time.strftime("%Y/%m/%d", time.localtime())}
    i = 0
    categories = os.listdir("../Output/PW_Image")
    for folder in categories:
        anno['categories'][str(i)] = {}
        anno['categories'][str(i)]= {'id' : i, 'supercategory': "none", 'name': folder}
        i = i + 1
    i = 0    
    for section in os.listdir('../Output' + now):
        anno_tempo = anno.copy()
        for anno_img in os.listdir('../Output/' + now + '/' + section):
            img = cv2.imread('../Output/' + now + '/' + section + '/' + anno_img)
            param = anno_img.split(';')
            bbox = [int(param[1]),int(param[2]),int(param[3]),int(param[4]),]
            anno_tempo['images'].append({'id' : i, 
                                         'file_name': anno_img, 
                                         'height': img.shape(0),
                                         'width': img.shape(1)})
            anno_tempo['annotations'].append({'id': i , 
                                              'image_id': i, 
                                              'category_id': categories.index(param[0]), 
                                              'bbox': bbox, 
                                              'iscrowd': 0, 
                                              'area': (int(param[3])*int(param[4])),
                                              'segmentation': []})
            i = i + 1
        with open("_annotations.coco.json", "w") as outfile:
            json.dump(anno, outfile)
        
    print('Done')
            

                

                
                

        

    