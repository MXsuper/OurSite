"""
-------------------------------------------------
   Author :        lin
   date：          2019/2/28 9:52
-------------------------------------------------
"""
__author__ = 'lin'
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import os,gc
# from myproject.settings import MEDIA_ROOT,STATIC_ROOT,CLASSIFY_MODEL
import sys
from OurSite.settings import net


def classify(img):
    '''
    :param img:  图片路径
    :return:
    '''
    global net
    # 模型
    # return '测试'
    # try:
        # img = os.path.join(MEDIA_ROOT,img)
        # model_path = os.path.join(MEDIA_ROOT,CLASSIFY_MODEL)
        # net = torchvision.models.vgg16_bn(pretrained=False)
        # net.classifier[0] = torch.nn.Linear(32768, 4096, bias=True)
        # net.classifier[6] = torch.nn.Linear(4096, 2, bias=True)
        # net.load_state_dict(torch.load(model_path, map_location=lambda storage, loc: storage))
    transform = transforms.Compose(
        [transforms.Resize((256, 256)),
         transforms.CenterCrop((256, 256)),
         transforms.ToTensor(),
        transforms.Normalize((0.4476, 0.2356, 0.1305), (0.1594, 0.1125, 0.0838))])
    net.eval()
    if isinstance(img, str):
        img = transform(Image.open(img).convert('RGB')).unsqueeze(0)
        if torch.cuda.is_available():
            img = img.cuda()
            net.cuda()
        print('img',sys.getsizeof(img))
        out = net(img)
        print('out',sys.getsizeof(out))
        # return "测试"
        del img
        print('del img')
        gc.collect()
        pred = torch.max(F.softmax(out, dim=1), 1)[1]
        del out
        del net
        print('del net out')
        gc.collect()
        if pred == 0:
            result = "阴性"
        elif pred == 1:
            result = "阳性"
    elif isinstance(img, list):
        for i in range(len(img)):
            temp = transform(Image.open(img[i]).convert('RGB')).unsqueeze(0)
            imglist = temp if i == 0 else torch.cat((imglist, temp), 0)
        if torch.cuda.is_available():
            img = imglist.cuda()
            net.cuda()
        out = net(img)
        img = None
        pred = torch.max(F.softmax(out, dim=1), 1)[1]
        result = list(map(lambda x: "阳性" if x else "阴性", pred))

    return result
    # except Exception as e:
    #     return "诊断失败请重试.."
