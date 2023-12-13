import os
import shutil
import cv2
from distorter import pers_fixer, cropper, expander, rotator, stacker, resizer
import time
import json
import math
import copy
import numpy as np

def hello_world():
    print('Hello World')
    
def nihility():
    pass

def folder_maker(path,name):
    dir_existence = os.path.exists(path + '/' + name)
    if(dir_existence == False):
        # print(f'{name} does not exist, creating new directory...')
        os.mkdir(path + '/' + name)
    else:
        # print(f'{name} already existed on the specified path, continuing other operation...')
        pass

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
           
if __name__ == "__main__":


    folder_maker('..','Input')
    folder_maker('..','Output')
    
    class_list = ["5gen11front","5gen11back","10gen11front","10gen11back","20gen11front","20gen11back","100gen11front","100gen11back","500gen11front","500gen11back",
                  "10gen12front","10gen12back","20gen12front","20gen12back","100gen12front","100gen12back",
                  "50gen13front","50gen13back","500gen13front","500gen13back",
                  "100gen14front","100gen14back","500gen14front","500gen14back","1000gen14front","1000gen14back",
                  "20gen15front","20gen15back","50gen15front","50gen15back","100gen15front","100gen15back","500gen15front","500gen15back","1000gen15front","1000gen15back",
                  "20gen16front","20gen16back","50gen16front","50gen16back","100gen16front","100gen16back","500gen16front","500gen16back","1000gen16front","1000gen16back",
                  "20gen17front","20gen17back","50gen17front","50gen17back","100gen17front","100gen17back","500gen17front","500gen17back","1000gen17front","1000gen17back",
                  "memo1987front","memo1987back","memo1990front","memo1992back","memo1992front","memo1992back","memo1995front","memo1995back","memo1996front","memo1996back",
                  "memo1999front","memo1999back","memo2000front","memo2000back","memo2004front","memo2004back","memo2006front","memo2006back","memo2007front","memo2007back",
                  "memo2010front","memo2010back","memo2011front","memo2011back","memo2012.10front","memo2012.10back","memo2012.kqfront","memo2012.kqback","memo2015front","memo2015back",
                  "memo2016.kfront","memo2016.kback","memo2016.qfront","memo2016.qback","memo2017front","memo2017back","memo2019front","memo2019back"]
    for class_name in class_list:
        folder_maker('..\\Input',class_name)
    
    for i in range(5):
        print(".")        
    img_list = []
    for dir in os.listdir("../Input"):
        for file in os.listdir("../Input/" + dir):
            if (file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.PNG')):
                img_list.append(file)
    if len(img_list) == 0:
        print('Please Insert image to continue')
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

    outdirfilename = input("Enter the Output name :")
    if outdirfilename == "":
        outdirfilename = "untitled"
    now = time.strftime("(%Y-%m-%d)%H-%M", time.localtime())
    outdirfilename = now + '_' + outdirfilename
    folder_maker('..\\Output\\',outdirfilename)
    
    orient = ['top','left','right','bot']
    folder_maker('..\\Output\\' + outdirfilename,"Fore")
    
    for class_name in class_list:
        folder_maker('..\\Output\\' + outdirfilename + "\\Fore",class_name)
        
    for dir in os.listdir("..\\Input"):
        if (len(os.listdir("..\\Input\\" + dir)) == 0):
            pass
        else:
            for images in os.listdir("..\\Input\\" + dir):
                if (images.endswith('.jpg') or images.endswith('.png') or images.endswith('.jpeg') or images.endswith('.PNG')):
                            inpath = "..\\Input\\" + dir + '\\' + images
                            img = cv2.imread(inpath,cv2.IMREAD_UNCHANGED)
                            img = resizer(img,452)
                            img_center = pers_fixer(img, 'top', 0)
                            for theta in range(-30,31,5):
                                img_expanded = expander(img_center)
                                img_rotated = rotator(img_expanded,theta)
                                cropped_img = cropper(img_rotated)
                                folder_maker('..\\Output\\' + outdirfilename + "\\Fore\\" + dir,images)
                                outpath_center = '..\\Output\\' + outdirfilename + "\\Fore\\" + dir + '\\' + images + '\\center_0' + '_' + str(theta) + '.png'
                                print('center_0' + '_' + str(theta) + '.png')
                                cv2.imwrite(outpath_center,cropped_img)
                            for x in orient:
                                for i in range(5, 26, 5):
                                    img_mutated = pers_fixer(img, x, i)
                                    for theta in range(-30,31,5):
                                        img_expanded = expander(img_mutated)
                                        img_rotated = rotator(img_expanded,theta)
                                        cropped_img = cropper(img_rotated)
                                        file_name = x + '_' + str(i) + '_' + str(theta) + '.png'
                                        outpath_for = '..\\Output\\' + outdirfilename + "\\Fore\\"  + dir + '\\' + images + '\\' + file_name
                                        print(file_name)
                                        cv2.imwrite(outpath_for,cropped_img)
    print('Transparent Image Batches Generated!')
    
    bg_path = '../Background'
    folder_maker('..\\Output\\' + outdirfilename,"Dataset")
    for dir in os.listdir("..\\Output\\" + outdirfilename + "\\Fore"):
        if (len(os.listdir("..\\Output\\" + outdirfilename + "\\Fore\\" + dir)) == 0):
            pass
        else:
            for imset in os.listdir("..\\Output\\" + outdirfilename + "\\Fore\\" + dir):
                print('=====' + imset)
                for img in os.listdir("..\\Output\\" + outdirfilename + "\\Fore\\" + dir + '\\' + imset):
                    print(img)
                    for bg in os.listdir(bg_path):
                        bg_file = bg_path + '/' + bg
                        fg_file = "..\\Output\\" + outdirfilename + "\\Fore\\" + dir + '\\' + imset + "\\" + img
                        bg_uint = cv2.imread(bg_file,cv2.IMREAD_UNCHANGED)
                        fg_uint = cv2.imread(fg_file,cv2.IMREAD_UNCHANGED)
                        img_stacked,x,y,h,w = stacker(fg_uint,bg_uint)
                        out_name = dir + ';' + str(x) + ';' + str(y) + ';' + str(w) + ';' + str(h) + ';' + bg + imset + img
                        out_dest = '..\\Output\\' + outdirfilename + "\\Dataset\\" + out_name 
                        cv2.imwrite(out_dest,img_stacked)
    
    print('Shuffling..')
    
    file_amount = len(os.listdir('..\\Output\\' + outdirfilename + "\\Dataset"))
    
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
    files = os.listdir('..\\Output\\' + outdirfilename + "\\Dataset")
    folder_maker('..\\Output\\' + outdirfilename + "\\Dataset",'test')
    folder_maker('..\\Output\\' + outdirfilename + "\\Dataset",'train')
    folder_maker('..\\Output\\' + outdirfilename + "\\Dataset",'valid')
    i = 0
    for file in files:
            if shuffler[i] == 0:
                batch = 'train'
            elif shuffler[i] == 1:
                batch = 'valid'
            elif shuffler[i] == 2:
                batch = 'test'
            shutil.move('..\\Output\\' + outdirfilename + "\\Dataset\\" + file, '..\\Output\\' + outdirfilename + "\\Dataset\\" + batch )
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
    for class_name in class_list:
        anno['categories'].append({'id' : i, 'supercategory': "none", 'name': class_name})
        i = i + 1
        
    i = 0    
    for section in os.listdir('..\\Output\\' + outdirfilename + "\\Dataset"):
        anno_tempo = copy.deepcopy(anno)
        for anno_img in os.listdir('..\\Output\\' + outdirfilename + "\\Dataset\\" + section):
            img = cv2.imread('..\\Output\\' + outdirfilename + "\\Dataset\\" + section + '\\' + anno_img)
            param = anno_img.split(';')
            bbox = [int(param[1]),int(param[2]),int(param[3]),int(param[4]),]
            anno_tempo['images'].append({'id' : i, 
                                            'file_name': anno_img, 
                                            'height': img.shape[0],
                                            'width': img.shape[1]})
            anno_tempo['annotations'].append({'id': i , 
                                                'image_id': i, 
                                                'category_id': class_list.index(param[0]), 
                                                'bbox': bbox, 
                                                'iscrowd': 0, 
                                                'area': (int(param[3])*int(param[4])),
                                                'segmentation': []})
            print(str(i)+'/'+str(file_amount))
            i = i + 1
        with open('..\\Output\\' + outdirfilename + "\\Dataset\\" + section + "/_annotations.coco.json", "w") as outfile:
            json.dump(anno_tempo, outfile)
        
    shutil.rmtree('..\\Output\\' + outdirfilename + "\\Fore")
    print("Done!")