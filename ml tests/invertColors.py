"""Simple utility script for flipping
   the colors of images
"""
import os
from PIL import Image
import PIL.ImageOps

#hardcoded directories for changing the color. It's a simple utility file you don't need to be that abstract.
directories = ['EMNISTdata/digits/training', 'EMNISTdata/digits/testing']
directories.append('EMNISTdata/MNIST/training')
directories.append('EMNISTdata/MNIST/testing')

for directory in directories:
    for number in range(10):
        newDirectory = os.path.join(directory, str(number))
        newDirectoryTemp = newDirectory.replace('\\', '/')
        for filename in os.listdir(newDirectory):
            if filename.endswith(".png"):
                newDirectory = os.path.join(newDirectoryTemp, filename)
                newDirectory = newDirectory.replace('\\', '/')
                print(newDirectory)
                image = Image.open(newDirectory)
                PIL.ImageOps.invert(image).convert('RGB').save(newDirectory, "PNG", optimize=True)