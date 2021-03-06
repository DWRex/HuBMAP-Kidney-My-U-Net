from common  import *
from hubmap_v2  import *


'''
           id                                           encoding
0   2f6ecfcdf  296084587 4 296115835 6 296115859 14 296147109...
1   8242609fa  96909968 56 96941265 60 96972563 64 97003861 6...
2   aaa6a05cc  30989109 59 31007591 64 31026074 68 31044556 7...
3   cb2d976f4  78144363 5 78179297 15 78214231 25 78249165 35...
4   b9a3865fc  61271840 4 61303134 13 61334428 22 61365722 30...
5   b2dc8411c  56157731 21 56172571 45 56187411 51 56202252 5...
6   0486052bb  101676003 6 101701785 8 101727568 9 101753351 ...
7   e79de561c  7334642 14 7350821 41 7367001 67 7383180 82 73...
8   095bf7a1f  113277795 21 113315936 53 113354083 87 1133922...
9   54f2eec69  124967057 36 124997425 109 125027828 147 12505...
10  4ef6695ce  137041956 58 137081912 65 137121869 72 1371618...
11  26dc41664  245832956 28 245869925 2 245871115 33 24590808...
12  c68fe75ea  21256809 3 21283644 10 21310479 17 21337315 22...
13  afa5e8098  65837968 7 65874765 11 65874827 12 65911562 15...
14  1e2425f28  49453112 7 49479881 22 49506657 31 49533433 40...

(15, 2) 

'''
# <todo> make difference scale tile




#make tile train image
def run_make_train_tile():

    tile_scale = 0.25
    tile_min_score = 0.25
    tile_size = 320  #480 #
    tile_average_step = 160 #240  # 192


    train_tile_dir = '/home/glennsu/Kaggle Competition Dataset/HuBMAP - Hacking the Kidney/Pre-Data/tile/0.25_320_160_train'
    #train_tile_dir = '/root/share1/kaggle/2020/hubmap/data/hubmap-kidney-segmentation/etc/tile/0.25_480_240_train_corrected'
    #train_tile_dir = '/root/share1/kaggle/2020/hubmap/data/hubmap-kidney-segmentation/etc/tile/0.25_320_240_train_corrected'
    #---

    df_train = pd.read_csv(data_dir + '/Code/train.csv')
    print(df_train)
    print(df_train.shape)

    os.makedirs(train_tile_dir, exist_ok=True)
    for i in range(0,len(df_train)):
        id, encoding = df_train.iloc[i]

        image_file = data_dir + '/train/%s.tiff' % id
        image = read_tiff(image_file)

        height, width = image.shape[:2]
        mask = rle_decode(encoding, height, width, 255)
#        try:
#            mask_file = data_dir + '/train/%s.corrected_shift_mask.png' % id
#            mask = read_mask(mask_file)
#        except:
#            mask_file = data_dir + '/train/%s.corrected_mask.png' % id
#            mask = read_mask(mask_file)

        structure = draw_strcuture_from_hue(image, fill=255, scale=tile_scale/32)
        print(id)

        #make tile
        tile = to_tile(image, mask, structure, tile_scale, tile_size, tile_average_step, tile_min_score)

        coord = np.array(tile['coord'])
        df_image = pd.DataFrame()
        df_image['cx']=coord[:,0].astype(np.int32)
        df_image['cy']=coord[:,1].astype(np.int32)
        df_image['cv']=coord[:,2]

        # --- save ---
        os.makedirs(train_tile_dir+'/%s'%id, exist_ok=True)

        tile_id =[]
        num = len(tile['tile_image'])
        for t in range(num):
            cx,cy,cv   = tile['coord'][t]
            s = 'y%08d_x%08d' % (cy, cx)
            tile_id.append(s)

            tile_image = tile['tile_image'][t]
            tile_mask  = tile['tile_mask'][t]
            cv2.imwrite(train_tile_dir + '/%s/%s.png' % (id, s), tile_image)
            cv2.imwrite(train_tile_dir + '/%s/%s.mask.png' % (id, s), tile_mask)

#            image_show('tile_image', tile_image)
#            image_show('tile_mask', tile_mask)
#            cv2.waitKey(1)


        df_image['tile_id']=tile_id
        df_image[['tile_id','cx','cy','cv']].to_csv(train_tile_dir+'/%s.csv'%id, index=False)
        #------


#make single tile train image
def run_make_single_train_tile(single_id):

    tile_scale = 0.25
    tile_min_score = 0.25
    tile_size = 320  #480 #
    tile_average_step = 160 #240  # 192


    train_tile_dir = '/home/glennsu/Kaggle Competition Dataset/HuBMAP - Hacking the Kidney/Pre-Data/tile/0.25_320_160_train'
    #train_tile_dir = '/root/share1/kaggle/2020/hubmap/data/hubmap-kidney-segmentation/etc/tile/0.25_480_240_train_corrected'
    #train_tile_dir = '/root/share1/kaggle/2020/hubmap/data/hubmap-kidney-segmentation/etc/tile/0.25_320_240_train_corrected'
    #---

    df_train = pd.read_csv(data_dir + '/Code/train.csv')
#    print(df_train)
#    print(df_train.shape)

    os.makedirs(train_tile_dir, exist_ok=True)
#    for i in range(0,len(df_train)):
    id, encoding = df_train.iloc[df_train[df_train['id']==single_id].index[0]]

    image_file = data_dir + '/train/%s.tiff' % id
    image = read_tiff(image_file)

    height, width = image.shape[:2]
    mask = rle_decode(encoding, height, width, 255)
#        try:
#            mask_file = data_dir + '/train/%s.corrected_shift_mask.png' % id
#            mask = read_mask(mask_file)
#        except:
#            mask_file = data_dir + '/train/%s.corrected_mask.png' % id
#            mask = read_mask(mask_file)

    structure = draw_strcuture_from_hue(image, fill=255, scale=tile_scale/32)
    print(id)

    #make tile
    tile = to_tile(image, mask, structure, tile_scale, tile_size, tile_average_step, tile_min_score)

    coord = np.array(tile['coord'])
    df_image = pd.DataFrame()
    df_image['cx']=coord[:,0].astype(np.int32)
    df_image['cy']=coord[:,1].astype(np.int32)
    df_image['cv']=coord[:,2]

    # --- save ---
    os.makedirs(train_tile_dir+'/%s'%id, exist_ok=True)

    tile_id =[]
    num = len(tile['tile_image'])
    for t in range(num):
        cx,cy,cv   = tile['coord'][t]
        s = 'y%08d_x%08d' % (cy, cx)
        tile_id.append(s)

        tile_image = tile['tile_image'][t]
        tile_mask  = tile['tile_mask'][t]
        cv2.imwrite(train_tile_dir + '/%s/%s.png' % (id, s), tile_image)
        cv2.imwrite(train_tile_dir + '/%s/%s.mask.png' % (id, s), tile_mask)

#            image_show('tile_image', tile_image)
#            image_show('tile_mask', tile_mask)
#            cv2.waitKey(1)


    df_image['tile_id']=tile_id
    df_image[['tile_id','cx','cy','cv']].to_csv(train_tile_dir+'/%s.csv'%id, index=False)
    #------



#make tile train image
def run_make_test_tile():

    tile_scale = 0.25
    tile_min_score = 0.25
    tile_size = 320  # 480 #
    tile_average_step = 160 #240  # 160 #192


    test_tile_dir = '/home/glennsu/Kaggle Competition Dataset/HuBMAP - Hacking the Kidney/Pre-Data/tile/0.25_320_160_test'
    #---


    os.makedirs(test_tile_dir, exist_ok=True)
    for id in [
        '2ec3f1bb9',
        '3589adb90',
        'd488c759a',
        'aa05346ff',
        '57512b7f1',
    ]:
        print(id)

        image_file = data_dir + '/test/%s.tiff' % id
        json_file  = data_dir + '/test/%s-anatomical-structure.json' % id

        image = read_tiff(image_file)
        height, width = image.shape[:2]

        mask = None
        structure = draw_strcuture(read_json_as_df(json_file), height, width, structure=['Cortex'])
        # structure = draw_strcuture_from_hue(image, fill=255, scale=tile_scale/32)

        #make tile
        tile = to_tile(image, mask, structure, tile_scale, tile_size, tile_average_step, tile_min_score)

        coord = np.array(tile['coord'])
        df_image = pd.DataFrame()
        df_image['cx']=coord[:,0].astype(np.int32)
        df_image['cy']=coord[:,1].astype(np.int32)
        df_image['cv']=coord[:,2]

        # --- save ---
        os.makedirs(test_tile_dir+'/%s'%id, exist_ok=True)

        tile_id =[]
        num = len(tile['tile_image'])
        for t in range(num):
            cx,cy,cv   = tile['coord'][t]
            s = 'y%08d_x%08d' % (cy, cx)
            tile_id.append(s)

            tile_image = tile['tile_image'][t]
            cv2.imwrite(test_tile_dir + '/%s/%s.png' % (id, s), tile_image)
#            image_show('tile_image', tile_image)
#            cv2.waitKey(1)


        df_image['tile_id']=tile_id
        df_image[['tile_id','cx','cy','cv']].to_csv(test_tile_dir+'/%s.csv'%id, index=False)
        #------

# run_make_test_tile()
# exit(0)
#
#



#make tile train image
def run_make_train_mask():

    df_train = pd.read_csv(data_dir + '/Code/train.csv')
    print(df_train)
    print(df_train.shape)

    for i in range(0,len(df_train)):
        id, encoding = df_train.iloc[i]

        image_file = data_dir + '/train/%s.tiff' % id
        image = read_tiff(image_file)

        height, width = image.shape[:2]
        mask = rle_decode(encoding, height, width, 255)

        cv2.imwrite(data_dir + '/train/%s.mask.png' % id, mask)
        
        
#make single tile train image
def run_make_single_train_mask(single_id):

    df_train = pd.read_csv(data_dir + '/Code/train.csv')
    print(df_train)
    print(df_train.shape)

#    for i in range(0,len(df_train)):
    id, encoding = df_train.iloc[df_train[df_train['id']==single_id].index[0]]

    image_file = data_dir + '/train/%s.tiff' % id
    image = read_tiff(image_file)

    height, width = image.shape[:2]
    mask = rle_decode(encoding, height, width, 255)

    cv2.imwrite(data_dir + '/train/%s.mask.png' % id, mask)


def run_make_train_sample_overlay():
    train_tile_dir = '/home/glennsu/Kaggle Competition Dataset/HuBMAP - Hacking the Kidney/Pre-Data/tile/0.25_320_160_train'

    df_train = pd.read_csv(data_dir + '/Code/train.csv')
    print(df_train)
    print(df_train.shape)

    scale = 0.25
    for i in range(0,len(df_train)):
        id, encoding = df_train.iloc[i]

        image_file = data_dir + '/train/%s.tiff' % id
        image = read_tiff(image_file)

        image_small = cv2.resize(image, dsize=None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

        df = pd.read_csv(train_tile_dir + '/%s.csv'% (id) )
        coord = df[['cx','cy','cv']].values

        overlay = image_small.copy()
        for cx,cy,cv in coord:
            cx = int(cx)
            cy = int(cy)
            cv = int(255 * cv)
            cv2.circle(overlay, (cx, cy), 64, [cv,cv,cv], -1)
            cv2.circle(overlay, (cx, cy), 64, [0, 0, 255],16)


        overlay = cv2.resize(overlay, dsize=None, fx=0.1, fy=0.1, interpolation=cv2.INTER_LINEAR)
#         image_show('overlay', overlay)
#         cv2.waitKey(0)

        cv2.imwrite(train_tile_dir + '/%s.sample.png'% (id), overlay)





#make tile train image
def run_make_pseudo_tile():

    pseudo_tile_dir = '/home/glennsu/Kaggle Competition Dataset/HuBMAP - Hacking the Kidney/Pre-Data/tile/0.25_320_160_pseudo'
    #---

    #df_train = pd.read_csv(data_dir + '/train.csv')
    df_pseudo = pd.read_csv('/home/glennsu/Kaggle Competition Dataset/HuBMAP - Hacking the Kidney/Code/sample_submission.csv')
    print(df_pseudo)
    print(df_pseudo.shape)

    os.makedirs(pseudo_tile_dir, exist_ok=True)
    for i in range(0,len(df_pseudo)):
        id, encoding = df_pseudo.iloc[i]

        image_file = data_dir + '/test/%s.tiff' % id
        image = read_tiff(image_file)

        height, width = image.shape[:2]
        mask = rle_decode(encoding, height, width, 255)

        #make tile
        tile = to_tile(image, mask, tile_scale, tile_size, tile_average_step, tile_min_score)
        #mask, scale, size, step, min_score

        coord = np.array(tile['coord'])
        df_image = pd.DataFrame()
        df_image['cx']=coord[:,0].astype(np.int32)
        df_image['cy']=coord[:,1].astype(np.int32)
        df_image['cv']=coord[:,2]

        # --- save ---
        os.makedirs(pseudo_tile_dir + '/%s'%id, exist_ok=True)

        tile_id =[]
        num = len(tile['tile_image'])
        for t in range(num):
            cx,cy,cv   = tile['coord'][t]
            s = 'y%08d_x%08d' % (cy, cx)
            tile_id.append(s)

            tile_image = tile['tile_image'][t]
            tile_mask  = tile['tile_mask'][t]
            cv2.imwrite(pseudo_tile_dir + '/%s/%s.png' % (id, s), tile_image)
            cv2.imwrite(pseudo_tile_dir + '/%s/%s.mask.png' % (id, s), tile_mask)

#            image_show('tile_image', tile_image)
#            image_show('tile_mask', tile_mask)
#            cv2.waitKey(1)


        df_image['tile_id']=tile_id
        df_image[['tile_id','cx','cy','cv']].to_csv(pseudo_tile_dir+'/%s.csv'%id, index=False)
        #------


#################################################################



def run_check_tile():

    #load a train image
    id = 'e79de561c'
    image_file = data_dir + '/train/%s.tiff' % id
    image = read_tiff(image_file)
    height, width = image.shape[:2]

    #load a mask
    df = pd.read_csv(data_dir + '/Code/train.csv', index_col='id')
    encoding = df.loc[id,'encoding']
    mask = rle_decode(encoding, height, width, 255)

    #make tile
    tile = to_tile(image, mask)


    if 1: #debug
        overlay = tile['image_small'].copy()
        for cx,cy,cv in tile['coord']:
            cv = int(255 * cv)
            cv2.circle(overlay, (cx, cy), 64, [cv,cv,cv], -1)
            cv2.circle(overlay, (cx, cy), 64, [0, 0, 255], 16)
        for cx,cy,cv in tile['reject']:
            cv = int(255 * cv)
            cv2.circle(overlay, (cx, cy), 64, [cv,cv,cv], -1)
            cv2.circle(overlay, (cx, cy), 64, [255, 0, 0], 16)

        #---
        num = len(tile['coord'])
        cx, cy, cv = tile['coord'][num//2]
        cv2.rectangle(overlay,(cx-tile_size//2,cy-tile_size//2),(cx+tile_size//2,cy+tile_size//2), (0,0,255), 16)

#        image_show('overlay', overlay, resize=0.1)
#        cv2.waitKey(1)

    # make prediction for tile
    # e.g. predict = model(tile['tile_image'])
    tile_predict = tile['tile_mask'] # dummy: set predict as ground truth

    # make mask from tile
    height, width = tile['image_small'].shape[:2]
    predict = to_mask(tile_predict, tile['coord'],  height, width)

    truth = tile['mask_small']#.astype(np.float32)/255
    diff = np.abs(truth-predict)
    print('diff', diff.max(), diff.mean())

#    if 1:
#        image_show_norm('diff', diff, min=0, max=1, resize=0.2)
#        image_show_norm('predict', predict, min=0, max=1, resize=0.2)
#        cv2.waitKey(0)


# main #################################################################
if __name__ == '__main__':
    run_make_single_train_tile('54f2eec69')
    run_make_single_train_mask('54f2eec69')
    run_make_single_train_tile('e79de561c')
    run_make_single_train_mask('e79de561c')
#    run_make_train_tile()
#    run_make_test_tile()
#    run_make_train_mask()
#    run_make_train_sample_overlay()

#    run_make_pseudo_tile()
