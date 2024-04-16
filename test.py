import os

import sunpy.map
import matplotlib.pyplot as plt
from astropy.io.fits import CompImageHDU
from sunpy.data.sample import AIA_171_IMAGE  # Sample data
from astropy import units as u
from Models.app_models import TestAnimatedFrame

test_frame = TestAnimatedFrame("horizontal", 50, 600)
frame = test_frame.get_frame_by_t(0.1)
plt.imshow(frame, cmap='gray', vmin=0, vmax=255)
plt.show()






