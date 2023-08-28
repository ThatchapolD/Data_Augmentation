import os
import cv2
from distorter import pers_fixer, cropper, expander, rotator, stacker, resizer
import time
import splitfolders

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
    print('Splitting Files in to Traing batch...')
    
    splitfolders.ratio('Data', output="output", seed=1337, ratio=(.8, 0.1,0.1)) 

    print('Annotating...')
    
print('Done')
                

                
                

        

    