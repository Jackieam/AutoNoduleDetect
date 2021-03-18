import imgaug.augmenters as iaa
import matplotlib.pyplot as plt
import random
import cv2
import numpy as np


class ImageAugment(object):
    """
    class for augment the training data using imgaug
    """
    def __init__(self):
        self.key = 0
        self.choice = 1
        self.rotate = np.random.randint(-15, 15)
        self.scale_x = random.uniform(0.8, 1.2)
        self.scale_y = random.uniform(0.8, 1.2)
        self.translate_x = random.uniform(-0.2, 0.2)
        self.translate_y = random.uniform(-0.2, 0.2)
        self.brightness = np.random.randint(-10, 10)
        self.linear_contrast = random.uniform(0.5, 2.0)
        self.alpha = random.uniform(0, 1.0)
        self.lightness = random.uniform(0.75, 1.5)
        self.Gaussian = random.uniform(0.0, 0.05*255)
        self.Gaussian_blur = random.uniform(0, 3.0)

    def aug(self, image, label, sequence, color=True):
        """
        :param image: need size (H, W, C) one image once
        :param label: need size same as image or (H, W)(later translate to size(1, H, W, C))
        :param sequence: collection of augment function
        :return:
        """
        if color:
            label = np.expand_dims(label, axis=-1)
        image_aug, label_aug = sequence(image=image, segmentation_maps=np.expand_dims(label, axis=0))
        if color:
            label_aug = np.squeeze(label_aug, axis=-1)
        label_aug = np.squeeze(label_aug, axis=0)
        return image_aug, label_aug

    def rd(self, hehe):
        seed = np.random.randint(0, hehe)
        return seed

    def aug_sequence(self):
        sequence = self.aug_function()
        seq = iaa.Sequential(sequence, random_order=True)
        return seq

    def aug_function(self):
        sequence = []
        if self.rd(2) == self.key:
            sequence.append(iaa.Fliplr(1.0))  # 50% horizontally flip all batch images
        # if self.rd(2) == self.key:
        #     sequence.append(iaa.Flipud(1.0))  # 50% vertically flip all batch images
        if self.rd(2) == self.key:
            sequence.append(iaa.Affine(
                scale={"x": self.scale_x, "y": self.scale_y},  # scale images to 80-120% of their size
                translate_percent={"x": self.translate_x, "y": self.translate_y},  # translate by -20 to +20 percent (per axis)
                rotate=(self.rotate),  # rotate by -45 to +45 degrees
            ))
        if self.rd(2) == self.key:
            sequence.extend(iaa.SomeOf((1, self.choice),
                                       [
                                           iaa.OneOf([
                                               iaa.GaussianBlur(self.Gaussian_blur),  # blur images with a sigma between 0 and 3.0
                                               # iaa.AverageBlur(k=(2, 7)),  # blur images using local means with kernel size 2-7
                                               # iaa.MedianBlur(k=(3, 11))  # blur images using local medians with kernel size 3-11
                                           ]),
                                           # iaa.Sharpen(alpha=self.alpha, lightness=self.lightness),  # sharpen images
                                           # iaa.LinearContrast(self.linear_contrast, per_channel=0.5),  # improve or worse the contrast
                                           # iaa.Add(self.brightness, per_channel=0.5),  # change brightness
                                           # iaa.AdditiveGaussianNoise(loc=0, scale=0.1, per_channel=0.5)  # add gaussian n
                                       ]))
        return sequence


def show_aug(image, label):
    plt.figure(figsize=(10, 10), facecolor="#FFFFFF")
    for i in range(1, len(image)+1):
        plt.subplot(len(image), 2, 2*i-1)
        plt.imshow(image[i-1])
        plt.subplot(len(image), 2, 2*i)
        plt.imshow(label[i-1])
    plt.show()


"""
see the data augment
"""
# name = "data_eye_train/seq_13/left_frames/frame003.png"
# label = cv2.imread("data_eye_train/seq_13/labels/frame003.png")  # , cv2.IMREAD_GRAYSCALE
# label = cv2.cvtColor(label, cv2.COLOR_BGR2RGB)
# label = cv2.resize(label, (448, 448), interpolation=cv2.INTER_NEAREST)
# image = cv2.imread(name)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# image = cv2.resize(image, (448, 448), interpolation=cv2.INTER_NEAREST)
# wbw = ImageAugment()
# seq = wbw.aug_sequence()
# image_aug, label_aug = wbw.aug(image, label, seq, color=False)
# show_aug([image_aug, label_aug], [image, label])