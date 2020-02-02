#!/usr/bin/env python3
# cython: language_level=3
from libc.stdio cimport printf
from cython.view cimport array as cvarray
import numpy as np


cpdef unvectorizedBlurCython(image):
    """Algorithm made for Cython that blurs the input image and returns
    a new blurred image. The algorithm loops through all pixels,
    using y,x coordinates, in the image and calculate the mean from all
    the neighbours color channel. The color channel represent the
    BGR colors for each pixel. This function specifies types for
    variables so that it is possible to get C speed during execution.

    The format for a parameter is:
    image (ndarray):
        A image represented in a ndarray. 3-dimensional ndarray.
    Returns:
        A new ndarray representing the blurred image.
    """
    image = image.astype("uint32")
    blur = np.empty((image.shape[0] - 2, image.shape[1] - 2, image.shape[2]))
    blur = blur.astype("uint32")
    cdef int height = image.shape[0] - 1
    cdef int width = image.shape[1] - 1
    cdef int channel = image.shape[2]
    cdef int h, w, c
    cdef double calcMean

    # Cython memoryview of numpy array to make speedy Cython array operations
    cdef int[:, :, :] image_view = image.astype(np.dtype("i"))
    cdef double[:, :, :] blur_view = blur.astype(np.dtype('d'))

    for h in range(1, height):
        for w in range(1, width):
            for c in range(channel):
                calcMean = (image_view[h, w, c] + image_view[h - 1, w, c] +
                            image_view[h + 1, w, c] + image_view[h, w - 1, c] +
                            image_view[h, w + 1, c] + image_view[h - 1, w - 1, c] +
                            image_view[h - 1, w + 1, c] + image_view[h + 1, w - 1, c] +
                            image_view[h + 1, w + 1, c]) / 9
                blur_view[h-1, w-1, c] = calcMean

    blur[:, :, :] = blur_view
    return blur


cpdef vectorizedBlurCython(image):
    """Algorithm made for Cython that blurs the input image and returns
    a new blurred image. The algorithm uses a vectorized arithmetical
    operation for calculating the mean of all the neighbours color channel.
    The color channel represent the BGR colors for each pixel. This
    function specifies types for variables so that it is possible to get C
    speed during execution.

    The format for a parameter is:
    image (ndarray):
        A image represented in a ndarray. 3-dimensional ndarray.
    Returns:
        A new ndarray representing the blurred image.
    """
    image = image.astype("uint32")
    blur = (image[:-2, :-2, :] + image[1:-1, :-2, :] + image[2:, :-2, :] +
            image[:-2, 1:-1, :] + image[1:-1, 1:-1, :] + image[2:, 1:-1, :] +
            image[:-2, 2:, :] + image[1:-1, 2:, :] + image[2:, 2:, :]) / 9
    return blur
