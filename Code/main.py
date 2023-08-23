import os
import cv2
from distorter import pers_fixer, cropper, expander, rotator, stacker, resizer
import time

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
    
    for file in os.listdir('..\Input'):
        inpath = '..\\Input\\' + file
        img = cv2.imread(inpath)
        img = resizer(img,452)
        folder_maker('..\\Output\\PW_Image', file)
        for theta in range(-30,31.5):
            img_expanded = expander(img_mutated)
            img_rotated = rotator(img_expanded)
            cropped_img = cropper(img_rotated)
        outpath = '..\\Output\\PW_Image\\' + file + '\\'
        cv2.imwrite(outpath +'center_0.png',img)
        for x in orient:
            for i in range(5, 26, 5):
                img_mutated = pers_fixer(img, x, i)
                for theta in range(-30,31,5):
                    img_expanded = expander(img_mutated)
                    img_rotated = rotator(img_expanded)
                    cropped_img = cropper(img_rotated)
                    file_name = x + '_' + str(i) + '_' + theta + '.png'
                    outpath_for = outpath + file_name
                    print(file_name)
                    cv2.imwrite(outpath_for,cropped_img)

  



    
                
print('Done')
                

                
                

        

    