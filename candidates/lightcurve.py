import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy import units as u
import glob
import sys
import io
from datetime import datetime

from candidates.models import Candidates

def data(field, filter, coords):
	# first list all catalogue files of this particular field and in this filter
	files = glob.glob('/Volumes/Seagate_Backup_Plus_Drive/new_transients/%s/%s/*/*_red_cat.fits' % (field, filter))

	# now loop through all these files, find closest source, and store lightcurve data in arrays
	mjd_detection = []; mag = []; mag_err = []; mjd_non_detection = []; limmag = []
	for file in files:
		hdul = fits.open(file)
		data = hdul[1].data
		header = hdul[1].header
		catalog = SkyCoord(ra=data['ALPHAWIN_J2000']*u.deg, dec=data['DELTAWIN_J2000']*u.deg, frame='icrs')

		# don't use empty catalogs
		if len(catalog) == 0:
			pass
		else:
			d2d = c.separation(catalog)
			idxcatalog = np.argsort(d2d) # return indices of d2d sorted in ascending order
			
			if d2d[idxcatalog][0] < 1*u.arcsec: # if source has a match within 1", then this is is a 'detection'
				mjd_detection.append(header['MJD-OBS'])
				mag.append(data['MAG_OPT'][idxcatalog][0])
				mag_err.append(data['MAGERR_OPT'][idxcatalog][0])

			else: # if source does not have match within 1", we regard this as a non-detection, so we use the limiting magnitude
				mjd_non_detection.append(header['MJD-OBS'])
				limmag.append(header['LIMMAG'])

	#print('Number of %s-band detections: %s' % (filter, len(mjd_detection)))
	#print('Number of %s-band non-detections: %s' % (filter, len(mjd_non_detection)))

	return np.column_stack((mjd_detection, mag, mag_err)), np.column_stack((mjd_non_detection, limmag))

def plot_light_curve(field, coords):
	plt.close()
	figure = io.BytesIO()
	startTime = datetime.now() # Start timer

	plt.errorbar(data(field, 'u', c)[0][:,0]-58709, data(field, 'u', c)[0][:,1], yerr=data(field, 'u', c)[0][:,2], fmt='b^', label='u') # plot detections
	plt.errorbar(data(field, 'u', c)[1][:,0]-58709, data(field, 'u', c)[1][:,1], fmt='b|') # plot non-detections
	plt.errorbar(data(field, 'q', c)[0][:,0]-58709, data(field, 'q', c)[0][:,1], yerr=data(field, 'q', c)[0][:,2], fmt='go', label='q') # plot detections
	plt.errorbar(data(field, 'q', c)[1][:,0]-58709, data(field, 'q', c)[1][:,1], fmt='g|') # plot non-detections
	plt.errorbar(data(field, 'i', c)[0][:,0]-58709, data(field, 'i', c)[0][:,1], yerr=data(field, 'i', c)[0][:,2], fmt='rv', label='i') # plot detections
	plt.errorbar(data(field, 'i', c)[1][:,0]-58709, data(field, 'i', c)[1][:,1], fmt='r|') # plot non-detections
	plt.xlabel('MJD-58709')
	plt.ylabel('Magnitude')
	plt.gca().invert_yaxis()
	plt.legend()
	
	print(datetime.now() - startTime) # Print time it took to run function
	plt.savefig(figure, format='png', dpi=300)
	return figure



# entries = Candidates.objects.all()

# for entry in entries:
# 	coords = entry.Transient_file.coords
# 	field = entry.Transient_file.field_ID
	
# 	print('Creating lightcurve for source at (%s) in field %s' % (coords, field))
# 	# Create SkyCoord object using coordinates
# 	ra = coords.split(',')[0].replace('(','')
# 	dec =coords.split(',')[1].replace(')','')
# 	c = SkyCoord(ra, dec, frame="icrs", unit="deg")
# 	entry.lightcurve.save('lightcurve.png', plot_light_curve(field, c))




