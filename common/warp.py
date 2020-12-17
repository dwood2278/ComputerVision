"""
Module for warping images.
"""
import numpy as np
from scipy import ndimage
from common import homography

def image_in_image(im1,im2,tp):
    """ Put im1 in im2 with an affine transformation
    such that corners are as close to tp as possible.
    tp are homogeneous and counter-clockwise from top left. """

    # points to warp from
    m,n = im1.shape[:2]
    fp = np.array([[0,m,m,0],[0,0,n,n],[1,1,1,1]])

    # compute affine transform and apply
    H = homography.Haffine_from_points(tp,fp)
    im1_t = ndimage.affine_transform(im1,H[:2,:2],
            (H[0,2],H[1,2]),im2.shape[:2])
    alpha = (im1_t > 0)

    # Fix the alpha mask which is false anywhere the embedded image is black.
    # This will make any columns true between the first and last true in a row.
    for row in alpha:
        true_cols = np.where(row)[0]
        if len(true_cols) > 0:
            row[min(true_cols):max(true_cols)] = True

    # np.where uses the mask to return im1_t where true, im2 where false.
    return np.where(alpha, im1_t, im2)

def alpha_for_triangle(points,m,n):
    """ Creates alpha map of size (m,n)
    for a triangle with corners defined by points
    (given in normalized homogeneous coordinates). """

    alpha = np.zeros((m,n))
    for i in range(min(points[0]),max(points[0])):
        for j in range(min(points[1]),max(points[1])):
            x = np.linalg.solve(points,[i,j,1])
            if min(x) > 0: #all coefficients positive
                alpha[i,j] = 1

    return alpha
