# #oops code
# import numpy as np
# import cv2
# from scipy import fftpack as fftp
# from matplotlib import pyplot as plt

# class CompressionDetector:
#     def __init__(self, threshold=0.5):
#         self.threshold = threshold

#     def check_compression(self, image):
#         image = cv2.imread(image)
#         #plt.imshow(image)
#         image_shape = image.shape
#         result = ""

#         # Deciding 8x8 shape
#         if image_shape[0] % 8 != 0:
#             rows = image_shape[0] + 8 - image_shape[0] % 8
#         else:
#             rows = image_shape[0]
#         if image_shape[1] % 8 != 0:
#             columns = image_shape[1] + 8 - image_shape[1] % 8
#         else:
#             columns = image_shape[1]

#         # Preparing image blocks
#         image_dct = np.zeros((rows, columns, 3), np.uint8)
#         image_dct[0:image_shape[0], 0:image_shape[1]] = image

#         # Extracting y channel
#         y_channel = cv2.cvtColor(image_dct, cv2.COLOR_BGR2YCR_CB)[:, :, 0]
#         y_shape = y_channel.shape[0]
#         y_reshaped = y_channel.reshape(y_shape // 8, 8, -1, 8).swapaxes(1, 2).reshape(-1, 8, 8)

#         quantized_DCT = []
#         # Quantizing DCT coefficients
#         for block in range(0, y_reshaped.shape[0]):
#             quantized_DCT.append(cv2.dct(np.float32(y_reshaped[block])))
#         quantized_DCT = np.asarray(quantized_DCT, dtype=np.float32)

#         # Normalizing the DT coefficients
#         quantized_DCT = np.rint(quantized_DCT - np.mean(quantized_DCT, axis=0)).astype(np.int32)

#         # Plotting the points
#         p1, p2 = plt.subplots(8, 8)
#         p2 = p2.ravel()

#         for id, p in enumerate(p2):
#             data = quantized_DCT[:, int(id / 8), int(id % 8)]
#             # Makin a histogram
#             value, key = np.histogram(data, bins=np.arange(data.min(), data.max() + 1))
#             # Applying fft and extracting peaks
#             fft_dct = np.absolute(fftp.fft(value))
#             fft_dct = np.reshape(fft_dct, (len(fft_dct), 1))
#             # Rotating the fft
#             rotate_fft = np.roll(fft_dct, int(len(fft_dct) / 2))
#             # Calculating peaks
#             slope = rotate_fft[1:] - rotate_fft[:-1]
#             indices = [i + 1 for i in range(len(slope) - 1) if slope[i] > 0 > slope[i + 1]]
#             peak_count = sum(rotate_fft[peak][0] > self.threshold for peak in indices)

#             # Thresholding the value and checking the third block
#             if id == 3:
#                 if peak_count >= 20:
#                     result = "Image is compressed"
#                 else:
#                     result = "Image is not compressed"

#         return result

# # # Usage
# # detector = CompressionDetector()
# # image_path = r"D:\C DOWNLOADS\imagecompressor (1)\Picture3-min.png"
# # compression_result = detector.check_compression(image_path)
# # print(compression_result)

import numpy as np
import cv2
from scipy import fftpack as fftp
from matplotlib import pyplot as plt
from io import BytesIO

class CompressionDetector:
    def __init__(self, threshold=0.5):
        self.threshold = threshold

    def check_compression(self, image_file):
        # Read the image data from the file object
        image_data = image_file.read()

        # Decode the image data using BytesIO
        image_bytes = BytesIO(image_data)
        image = cv2.imdecode(np.fromstring(image_bytes.getvalue(), np.uint8), cv2.IMREAD_COLOR)

        image_shape = image.shape
        result = ""

        # Deciding 8x8 shape
        if image_shape[0] % 8 != 0:
            rows = image_shape[0] + 8 - image_shape[0] % 8
        else:
            rows = image_shape[0]
        if image_shape[1] % 8 != 0:
            columns = image_shape[1] + 8 - image_shape[1] % 8
        else:
            columns = image_shape[1]

        # Preparing image blocks
        image_dct = np.zeros((rows, columns, 3), np.uint8)
        image_dct[0:image_shape[0], 0:image_shape[1]] = image

        # Extracting y channel
        y_channel = cv2.cvtColor(image_dct, cv2.COLOR_BGR2YCR_CB)[:, :, 0]
        y_shape = y_channel.shape[0]
        y_reshaped = y_channel.reshape(y_shape // 8, 8, -1, 8).swapaxes(1, 2).reshape(-1, 8, 8)

        quantized_DCT = []
        # Quantizing DCT coefficients
        for block in range(0, y_reshaped.shape[0]):
            quantized_DCT.append(cv2.dct(np.float32(y_reshaped[block])))
        quantized_DCT = np.asarray(quantized_DCT, dtype=np.float32)

        # Normalizing the DT coefficients
        quantized_DCT = np.rint(quantized_DCT - np.mean(quantized_DCT, axis=0)).astype(np.int32)

        # Plotting the points
        p1, p2 = plt.subplots(8, 8)
        p2 = p2.ravel()
        for id, p in enumerate(p2):
            data = quantized_DCT[:, int(id / 8), int(id % 8)]

            # Making a histogram
            value, key = np.histogram(data, bins=np.arange(data.min(), data.max() + 1))

            # Applying fft and extracting peaks
            fft_dct = np.absolute(fftp.fft(value))
            fft_dct = np.reshape(fft_dct, (len(fft_dct), 1))

            # Rotating the fft
            rotate_fft = np.roll(fft_dct, int(len(fft_dct) / 2))

            # Calculating peaks
            slope = rotate_fft[1:] - rotate_fft[:-1]
            indices = [i + 1 for i in range(len(slope) - 1) if slope[i] > 0 > slope[i + 1]]
            peak_count = sum(rotate_fft[peak][0] > self.threshold for peak in indices)

            # Thresholding the value and checking the third block
            if id == 3:
                if peak_count >= 20:
                    result = "Image is compressed"
                else:
                    result = "Image is not compressed"

        return result