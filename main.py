import cv2 as cv
import torch
from torch import functional as F

from extract_nums import digital_segmentation
from LeNet5 import LeNet5

def main(filepath):

    src = cv.imread(filepath)  #读取图片

    # 手写数字定位分割
    number_image, min_areas_idx = digital_segmentation(src)

    # 根据分割图像进行识别

    model = LeNet5()
    model.load_state_dict(torch.load('best.mdl'))
    print('手写数字为：', end='')
    for i in range(len(number_image)):
        if i == min_areas_idx:
            print('.', end='')
        else:
            x = cv.imread('./get_nums_img/' + str(i) + '.png')
            x = cv.cvtColor(x, cv.COLOR_BGR2GRAY)
            # x = x*(1/255)
            x = cv.resize(x, (28,28))
            x = torch.from_numpy(x)
            x = x.reshape(1, 1, 28, 28)
            x = x.type(torch.FloatTensor)
            #model = LeNet5().to(device)
            model = LeNet5()
            #x = x.to(device)
            model.load_state_dict(torch.load('best.mdl'))

            logits = model(x)
            #logits = F.
            pred = logits.argmax(dim=1)# dim = 1代表表在[b ， 10]中0-9的一个最大值的索引
            pred = pred.numpy()
            print(pred[0], end='')



    cv.waitKey(0)   #等待用户操作，里面等待参数是毫秒，我们填写0，代表是永远，等待用户操作
    cv.destroyAllWindows()  #销毁所有窗口

if __name__ == '__main__':


    main("./test/test3.png")
