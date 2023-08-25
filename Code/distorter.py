import numpy as np
import cv2
import os
import math


def nihility(x): # Trackbar Function Fodder. Ignore This.
    pass


def pers_fixer(img,side,crimp): # Main Function to be used in Main.py (img = image, side = either top bot left right, crimp = between 0 - 100)
    srcPer = np.float32([[0, 0], 
                             [img.shape[1] - 1, 0], 
                             [0, img.shape[0] - 1], 
                             [img.shape[1] - 1, img.shape[0] - 1]])
    # match(side):
    #     case 'top': 
    #         dstPer = np.float32([[((img.shape[1] - 1)*(crimp/100)), ((img.shape[0] - 1)*0)], 
    #                          [((img.shape[1] - 1)*((100 - crimp)/100)), ((img.shape[0] - 1)*0)], 
    #                          [((img.shape[1] - 1)*0), ((img.shape[0] - 1)*1)], 
    #                          [((img.shape[1] - 1)*1), ((img.shape[0] - 1)*1)]])
    #     case 'left': 
    #         dstPer = np.float32([[((img.shape[1] - 1)*0), ((img.shape[0] - 1)*(crimp/100))], 
    #                          [((img.shape[1] - 1)*1), ((img.shape[0] - 1)*0)], 
    #                          [((img.shape[1] - 1)*0), ((img.shape[0] - 1)*((100 - crimp)/100))], 
    #                          [((img.shape[1] - 1)*1), ((img.shape[0] - 1)*1)]])
    #     case 'right':
    #         dstPer = np.float32([[((img.shape[1] - 1)*0), ((img.shape[0] - 1)*0)], 
    #                          [((img.shape[1] - 1)*1), ((img.shape[0] - 1)*(crimp/100))], 
    #                          [((img.shape[1] - 1)*0), ((img.shape[0] - 1)*1)], 
    #                          [((img.shape[1] - 1)*1), ((img.shape[0] - 1)*((100 - crimp)/100))]])
    #     case 'bot':
    #         dstPer = np.float32([[((img.shape[1] - 1)*0), ((img.shape[0] - 1)*0)], 
    #                          [((img.shape[1] - 1)*1), ((img.shape[0] - 1)*0)], 
    #                          [((img.shape[1] - 1)*(crimp/100)), ((img.shape[0] - 1)*1)], 
    #                          [((img.shape[1] - 1)*((100 - crimp)/100)), ((img.shape[0] - 1)*1)]])
    #     case _:
    #         print('Invalid Input.')
    if(side == 'top'):
        dstPer = np.float32([[((img.shape[1] - 1)*(crimp/100)), ((img.shape[0] - 1)*0)], 
                            [((img.shape[1] - 1)*((100 - crimp)/100)), ((img.shape[0] - 1)*0)], 
                            [((img.shape[1] - 1)*0), ((img.shape[0] - 1)*1)], 
                            [((img.shape[1] - 1)*1), ((img.shape[0] - 1)*1)]])
    elif(side == 'left'):
        dstPer = np.float32([[((img.shape[1] - 1)*0), ((img.shape[0] - 1)*(crimp/100))], 
                            [((img.shape[1] - 1)*1), ((img.shape[0] - 1)*0)], 
                            [((img.shape[1] - 1)*0), ((img.shape[0] - 1)*((100 - crimp)/100))], 
                            [((img.shape[1] - 1)*1), ((img.shape[0] - 1)*1)]])
    elif(side == 'right'):
        dstPer = np.float32([[((img.shape[1] - 1)*0), ((img.shape[0] - 1)*0)], 
                            [((img.shape[1] - 1)*1), ((img.shape[0] - 1)*(crimp/100))], 
                            [((img.shape[1] - 1)*0), ((img.shape[0] - 1)*1)], 
                            [((img.shape[1] - 1)*1), ((img.shape[0] - 1)*((100 - crimp)/100))]])
    elif(side == 'bot'):
        dstPer = np.float32([[((img.shape[1] - 1)*0), ((img.shape[0] - 1)*0)], 
                            [((img.shape[1] - 1)*1), ((img.shape[0] - 1)*0)], 
                            [((img.shape[1] - 1)*(crimp/100)), ((img.shape[0] - 1)*1)], 
                            [((img.shape[1] - 1)*((100 - crimp)/100)), ((img.shape[0] - 1)*1)]])
    else:
        print('Invalid Input.')
    mat = cv2.getPerspectiveTransform(srcPer,dstPer)
    img_warped = cv2.warpPerspective(img, mat, (img.shape[1], img.shape[0]))
    mask = np.zeros((img.shape[0],img.shape[1])).astype('uint8')
    points = np.int32([dstPer[0, :],dstPer[1, :],dstPer[3, :],dstPer[2, :]])
    cv2.fillPoly(mask, pts=[points], color=(255, 0, 0))
    img_rgba = cv2.cvtColor(img_warped, cv2.COLOR_RGB2RGBA)
    img_rgba[:, :, 3] = mask
    return img_rgba


def cropper(img): # crop image to content and use as bounding box later
    mask = img[:, :, 3]
    ret,thresh = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)
    cntr,hier = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    x,y,w,h = cv2.boundingRect(cntr[0])
    cropped_img = img[y:y+h, x:x+w,:]
    return cropped_img

def expander(img): 
    max_dim = max(img.shape[0],img.shape[1])
    blank = np.zeros((int(max_dim*math.sqrt(2)),int(max_dim*math.sqrt(2)))).astype('uint8')
    blank_alpha = cv2.cvtColor(blank,cv2.COLOR_GRAY2RGBA)
    blank_alpha[:,:,3] = blank
    yoff = round((blank_alpha.shape[0] - img.shape[0])/2)
    xoff = round((blank_alpha.shape[1] - img.shape[1])/2)
    # print(blank_alpha.shape)
    # print(img.shape)
    # print(xoff,'|',yoff)
    img_expanded = blank_alpha.copy()
    img_expanded[yoff : yoff + img.shape[0], xoff : xoff + img.shape[1]] = img 
    return img_expanded

def rotator(img,theta):
    center = (img.shape[1]/2, img.shape[0]/2)
    rot_mat = cv2.getRotationMatrix2D(center, theta, 1.0)
    img_rotated = cv2.warpAffine(img, rot_mat, (img.shape[1], img.shape[0]))
    return img_rotated

def stacker(img_fore,img_back):
    big_mask = np.zeros((img_back.shape[0],img_back.shape[1])).astype('uint8')
    yoff = round((img_back.shape[0] - img_fore.shape[0])/2)
    xoff = round((img_back.shape[1] - img_fore.shape[1])/2)
    big_mask_punched = big_mask.copy()
    big_mask_punched[yoff : (yoff + img_fore.shape[0]), xoff : (xoff + img_fore.shape[1])] = img_fore[:, :,3]
    big_mask_punched = cv2.cvtColor(big_mask_punched,cv2.COLOR_GRAY2RGB)
    big_mask_punched[big_mask_punched == 255] = 1
    back_sec = cv2.multiply(1 - (big_mask_punched), img_back)
    fore_sec = cv2.cvtColor(big_mask,cv2.COLOR_GRAY2RGB)
    fore_sec[yoff : (yoff + img_fore.shape[0]), xoff : (xoff + img_fore.shape[1])] = img_fore[:,:,:3]
    img_stacked = cv2.add(fore_sec,back_sec)
    return img_stacked

def resizer(img,size):
    max_side = np.argmax(img.shape[:2])
    if(max_side == 0):
        outdim = (int(math.floor(size*img.shape[1]/img.shape[0])),size)
    if(max_side == 1):
        outdim = (size,int(math.floor(size*img.shape[0]/img.shape[1])))
    # outdim = (200,300)
    return cv2.resize(img,outdim)
    
    
if __name__ == '__main__': # Experimental Zone
    img = cv2.imread(r'..\Input\fa0d2780ab161375.jpg')
    img = cv2.resize(img,(512,362))
    # cv2.imshow('towa', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    cv2.namedWindow('Trackbars')
    cv2.resizeWindow('Trackbars', 800, 350)
    cv2.createTrackbar('Top_Lx','Trackbars',0,100,nihility)
    cv2.createTrackbar('Top_Ly','Trackbars',0,100,nihility)
    cv2.createTrackbar('Top_Rx','Trackbars',100,100,nihility)
    cv2.createTrackbar('Top_Ry','Trackbars',0,100,nihility)
    cv2.createTrackbar('Bot_Lx','Trackbars',0,100,nihility)
    cv2.createTrackbar('Bot_Ly','Trackbars',100,100,nihility)
    cv2.createTrackbar('Bot_Rx','Trackbars',100,100,nihility)
    cv2.createTrackbar('Bot_Ry','Trackbars',100,100,nihility)
    
    while(1):
        tlX = (cv2.getTrackbarPos('Top_Lx','Trackbars')/100)
        tlY = (cv2.getTrackbarPos('Top_Ly','Trackbars')/100)
        trX = (cv2.getTrackbarPos('Top_Rx','Trackbars')/100)
        trY = (cv2.getTrackbarPos('Top_Ry','Trackbars')/100)
        blX = (cv2.getTrackbarPos('Bot_Lx','Trackbars')/100)
        blY = (cv2.getTrackbarPos('Bot_Ly','Trackbars')/100)
        brX = (cv2.getTrackbarPos('Bot_Rx','Trackbars')/100)
        brY = (cv2.getTrackbarPos('Bot_Ry','Trackbars')/100)
        
        srcPer = np.float32([[0, 0], 
                             [img.shape[1] - 1, 0], 
                             [0, img.shape[0] - 1], 
                             [img.shape[1] - 1, img.shape[0] - 1]])
        
        dstPer = np.float32([[((img.shape[1] - 1)*tlX), ((img.shape[0] - 1)*tlY)], 
                             [((img.shape[1] - 1)*trX), ((img.shape[0] - 1)*trY)], 
                             [((img.shape[1] - 1)*blX), ((img.shape[0] - 1)*blY)], 
                             [((img.shape[1] - 1)*brX), ((img.shape[0] - 1)*brY)]])
        mat = cv2.getPerspectiveTransform(srcPer,dstPer)
        img_warped = cv2.warpPerspective(img, mat, (img.shape[1], img.shape[0]))
        cv2.imshow('test', img_warped)
        key = cv2.waitKey(1)
        if key == 27:
            break
        if key == 13:
            mask = np.zeros((img.shape[0],img.shape[1])).astype('uint8')
            points = np.int32([[((img.shape[1] - 1)*tlX), ((img.shape[0] - 1)*tlY)], 
                             [((img.shape[1] - 1)*trX), ((img.shape[0] - 1)*trY)], 
                             [((img.shape[1] - 1)*brX), ((img.shape[0] - 1)*brY)], 
                             [((img.shape[1] - 1)*blX), ((img.shape[0] - 1)*blY)]])
            cv2.fillPoly(mask, pts=[points], color=(255, 0, 0))
            img_rgba = cv2.cvtColor(img_warped, cv2.COLOR_RGB2RGBA)
            img_rgba[:, :, 3] = mask
            
            if os.path.exists(r'..\Output\test.png') == False:
                print('file saved in Output folder')
                cv2.imwrite(r'..\Output\test.png',img_rgba)
            else: 
                print('overwriting old file...')
                os.remove(r'..\Output\test.png')
                cv2.imwrite(r'..\Output\test.png',img_rgba)
            break
    cv2.destroyAllWindows()

