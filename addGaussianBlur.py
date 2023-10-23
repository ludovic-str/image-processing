from PIL import Image
import math
import copy
import argparse

def computeGaussian(x, y, sigma):
    left = (1 / (2 * math.pi * sigma**2))
    right = math.exp(-(x**2 + y**2) / (2 * sigma**2))
    return left * right

def getArgs():
    parser = argparse.ArgumentParser(description="Add Gaussian blur to an image")
    parser.add_argument("image", help="Path to the image to be blurred")
    parser.add_argument("-r", "--radius", help="Radius of the Gaussian blur", type=int, default=1)
    return parser.parse_args()

def getKernel(radius, sigma):
    sum = 0
    kernel = []
    kernelCurrentValue = 0

    for x in range(-radius, radius + 1):
        row = []
        for y in range(-radius, radius + 1):
            kernelCurrentValue = computeGaussian(x, y, sigma)
            sum += kernelCurrentValue
            row.append(kernelCurrentValue)
        kernel.append(row)
    
    for x in range(0, 2 * radius + 1):
        for y in range(0, 2 * radius + 1):
            kernel[x][y] /= sum
    return kernel

def listToDoubleArray(list, width, height):
    array = []
    for x in range(width):
        row = []
        for y in range(height):
            row.append(list[x * height + y])
        array.append(row)
    return array

def doubleArrayToList(array):
    list = []
    for row in array:
        for value in row:
            list.append(value)
    return list

def processImage(path, kernel, radius):
    try:
        img = Image.open(path).convert('RGB')
        width, height = img.size
        imageData = listToDoubleArray(list(img.getdata()), height, width)
        newImageData = copy.deepcopy(imageData)

        for x in range(radius, height - radius):
            for y in range(radius, width - radius):
                red = 0
                green = 0
                blue = 0

                for kernelX in range(-radius, radius):
                    for kernelY in range(-radius, radius):
                        kernalValue = kernel[kernelX + radius][kernelY + radius]
                        red += imageData[x - kernelX][y - kernelY][0] * kernalValue
                        green += imageData[x - kernelX][y - kernelY][1] * kernalValue
                        blue += imageData[x - kernelX][y - kernelY][2] * kernalValue
                newImageData[x][y] = (int(red), int(green), int(blue))
        
        img.putdata(doubleArrayToList(newImageData))
        img.save("blurred.png")
    except Exception as prin:
        print("Error: error while processing image")
        return

def checkKernelValidity(kernel):
    sum = 0
    for row in kernel:
        for value in row:
            sum += value
    return sum

def printKernel(kernel):
    for row in kernel:
        print(row)

def main():
    args = getArgs()
    sigma = max(args.radius / 2, 1)
    kernel = getKernel(args.radius, sigma)
    processImage(args.image, kernel, args.radius)
    
main()