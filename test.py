import math
import os

import numpy as np
import numpy.typing as npt
import sunpy.map
import matplotlib.pyplot as plt
from astropy.io.fits import CompImageHDU
from sunpy.data.sample import AIA_171_IMAGE  # Sample data
from astropy import units as u
from Models.app_models import TestAnimatedFrame
from scipy.ndimage import zoom

array = np.arange(12).reshape((3, 4))
res = array.sum(axis=0)
res2 = array.mean(axis=0)
pass



