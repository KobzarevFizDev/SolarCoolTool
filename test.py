import math
import os

import numpy as np
import numpy.typing as npt
import sunpy.map
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from astropy.io.fits import CompImageHDU
from sunpy.data.sample import AIA_171_IMAGE  # Sample data
from astropy import units as u
from Models.app_models import TestAnimatedFrame
from scipy.ndimage import zoom

im = np.arange(900).reshape((30,30))
im = gaussian_filter(im, sigma=7)
plt.imshow(im, cmap="gray")
plt.show()


