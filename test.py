import os

import sunpy.map
import matplotlib.pyplot as plt
from astropy.io.fits import CompImageHDU
from sunpy.data.sample import AIA_171_IMAGE  # Sample data
from astropy import units as u

"""
p = "D:\\PreparatedSolarImages\\A171\\aia.lev1_euv_12s.2010-07-25T133013Z.171.image_lev1.fits"
p2 = "D:\\PreparatedSolarImages\\A171\\aia.lev1_euv_12s.2010-07-25T153001Z.171.image_lev1.fits"
#p = "D:\\SolarImages\\aia.lev1_euv_12s.2010-07-25T135937Z.171.image_lev1.fits"
p3 = "1.fits"
my_map = sunpy.map.Map(p3)
fig = plt.figure()
ax = fig.add_subplot(projection=my_map)
#clip_interval=(0+20, 100.0)*u.percent
my_map.plot(axes=ax)
my_map.fits_header.set('BITPIX',32)
#my_map.fits_header.update(BITPIX=32)
print(my_map.fits_header.get("BITPIX"))
my_map.save("1.fits", hdu_type=CompImageHDU, overwrite=True)
plt.colorbar()
plt.show()
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 07:35:54 2024

@author: pfize
"""

'''
def fitfunc(p,elem,res,inds):
    val = []
    for i in elem:
        r = np.linalg.norm(np.array(i)*dom1.scale-np.array([5,5]))
        theta = np.arctan2(i[1]-5,i[0]-5)
        a = p[0]
        for j in range(4):
            a += r**j*(p[2*j+1]*np.sin(j*theta)+p[2*j+2]*np.cos(j*theta))
        val.append(a - res[inds[i]])
    return val



fitres = least_squares(fitfunc, x0 = np.ones(9),args = (elem,res,dom1.inds))
'''








