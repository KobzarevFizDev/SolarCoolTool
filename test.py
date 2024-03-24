import sunpy.map
import matplotlib.pyplot as plt
from sunpy.data.sample import AIA_171_IMAGE  # Sample data
from astropy import units as u

p = "D:\\SolarImages\\aia.lev1_euv_12s.2010-07-25T135922Z.94.image_lev1.fits"
#p = "D:\\SolarImages\\aia.lev1_euv_12s.2010-07-25T135937Z.171.image_lev1.fits"

my_map = sunpy.map.Map(p)
fig = plt.figure()
ax = fig.add_subplot(projection=my_map)
my_map.plot(axes=ax, clip_interval=(0+20, 100.0)*u.percent)
plt.colorbar()
plt.show()

'''
solar_map = sunpy.map.Map(p)
#solar_map = sunpy.map.Map(AIA_171_IMAGE)
plt.figure()
solar_map.plot()
plt.colorbar()  # Add a colorbar to show the pixel values
plt.title("Solar Image")

# Show the plot
plt.show()
'''