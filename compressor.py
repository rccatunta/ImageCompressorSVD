import numpy
from PIL import Image


# FUNCTION DEFINTIONS:

# open the image and return 3 matrices, each corresponding to one channel (R, G and B channels)
def openImage(imagePath):
    imOrig = Image.open(imagePath)
    im = numpy.array(imOrig)

    aRed = im[:, :, 0]
    aGreen = im[:, :, 1]
    aBlue = im[:, :, 2]

    return [aRed, aGreen, aBlue, imOrig]


# compress the matrix of a single channel
def compressSingleChannel(channelDataMatrix, singularValuesLimit):
    uChannel, sChannel, vhChannel = numpy.linalg.svd(channelDataMatrix)
    aChannelCompressed = numpy.zeros((channelDataMatrix.shape[0], channelDataMatrix.shape[1]))
    k = singularValuesLimit

    leftSide = numpy.matmul(uChannel[:, 0:k], numpy.diag(sChannel)[0:k, 0:k])
    aChannelCompressedInner = numpy.matmul(leftSide, vhChannel[0:k, :])
    aChannelCompressed = aChannelCompressedInner.astype('uint8')
    return aChannelCompressed


# MAIN PROGRAM:
def compressImage(nameImage):
    print('Starting Compression')
    aRed, aGreen, aBlue, originalImage = openImage(nameImage)
    # image width and height:
    imageWidth,imageHeight = originalImage.size
    # number of singular values to use for reconstructing the compressed image
    singularValuesLimit = 300
    #Compress in single channel for each color
    aRedCompressed = compressSingleChannel(aRed, singularValuesLimit)
    aGreenCompressed = compressSingleChannel(aGreen, singularValuesLimit)
    aBlueCompressed = compressSingleChannel(aBlue, singularValuesLimit)
    #reconstruct image
    imr = Image.fromarray(aRedCompressed, mode=None)
    img = Image.fromarray(aGreenCompressed, mode=None)
    imb = Image.fromarray(aBlueCompressed, mode=None)
    newImage = Image.merge("RGB", (imr, img, imb))
    originalImage.show()
    newImage.show()
    #SAVE IN HDD THE NEW IMAGE
    newImage = newImage.save("nuevafoto.jpg")
    #Convert RGB to Grayscale
    imgGs = Image.open('nuevafoto.jpg').convert('LA')
    imgGs.save('greyscalefoto.png')
    imgGs.show()

    #Print some info
    mr = imageHeight
    mc = imageWidth
    originalSize = mr * mc * 3
    compressedSize = singularValuesLimit * (1 + mr + mc) * 3
    ratio = compressedSize * 1.0 / originalSize
    print('original size:')
    print(originalSize)
    print('compressed size:')
    print(compressedSize)
    print('Compressed image size is ' + str(round(ratio * 100, 2)) + '% of the original image ')
    print('DONE - Compressed the image')

compressImage('foto.jpg')