from vetting.models import Transient_fields, Transient_files
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.visualization import (ZScaleInterval,ImageNormalize)
from astropy.io import fits
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
from astropy.nddata import Cutout2D
import sys
import glob
import io
from datetime import datetime

plt.style.use(astropy_mpl_style)

def image(file,filter,type,coords, new_fields_entry):
	if type == 'red':
		fname = file+'_red.fits.fz'
	elif type == 'diff':
		fname = file+'_red_D.fits.fz'
	elif type == 'scorr':
		fname = file+'_red_Scorr.fits.fz'
	elif type == 'ref':
		fname = '/Volumes/Seagate_Backup_Plus_Drive/new_transients_reference_images/0%s/ML1_%s_red.fits.fz' % (new_fields_entry,filter) 

	hdul = fits.open(fname)
	data = hdul[1].data
	wcs = WCS(header=hdul[1].header)
	size = u.Quantity((1, 1), u.arcmin)
	cutout = Cutout2D(data, coords, size, wcs=wcs)
	return cutout.data, (fname.split('/')[-1]+' filter: '+filter)

# Make 2 x 4 plot using image function
def plot_image(file1, file2, filter1, filter2, coords1, coords2, new_fields_entry):
	plt.close()
	figure = io.BytesIO()
	startTime = datetime.now() # Start timer
	red1 = image(file1,filter1,'red',coords1, new_fields_entry)[0]
	red2 = image(file2,filter2,'red',coords2, new_fields_entry)[0]
	fname1 = image(file1,filter1,'red',coords1, new_fields_entry)[1]
	fname2 = image(file2,filter2,'red',coords2, new_fields_entry)[1]
	ref1 = image(file1,filter1,'ref',coords1, new_fields_entry)[0]
	ref2 = image(file2,filter2,'ref',coords2, new_fields_entry)[0]
	diff1 = image(file1,filter1,'diff',coords1, new_fields_entry)[0]
	diff2 = image(file2,filter2,'diff',coords2, new_fields_entry)[0]
	scorr1 = image(file1,filter1,'scorr',coords1, new_fields_entry)[0]
	scorr2 = image(file2,filter2,'scorr',coords2, new_fields_entry)[0]

	fig, ((ax1,ax2,ax3,ax4),(ax5,ax6,ax7,ax8)) = plt.subplots(2,4)
	norm1 = ImageNormalize(red1, interval=ZScaleInterval())
	ax1.imshow(np.flipud(np.rot90(red1)), origin='lower',cmap='gray',norm=norm1)
	ax1.axis('off')
	fig.text(0.5,0.9,fname1.replace('_red.fits.fz', ''),fontsize='small',ha='center')
	fig.text(0.5,0.5,fname2.replace('_red.fits.fz', ''),fontsize='small',ha='center')

	norm2 = ImageNormalize(ref1, interval=ZScaleInterval())
	ax2.imshow(np.flipud(np.rot90(ref1)), origin='lower',cmap='gray',norm=norm2)
	ax2.axis('off')

	norm3 = ImageNormalize(diff1, interval=ZScaleInterval())
	ax3.imshow(np.flipud(np.rot90(diff1)), origin='lower',cmap='gray',norm=norm3)
	ax3.axis('off')

	norm4 = ImageNormalize(scorr1, interval=ZScaleInterval())
	ax4.imshow(np.flipud(np.rot90(scorr1)), origin='lower',cmap='gray',norm=norm4)
	ax4.axis('off')

	norm5 = ImageNormalize(red2, interval=ZScaleInterval())
	ax5.imshow(np.flipud(np.rot90(red2)), origin='lower',cmap='gray',norm=norm5)
	ax5.axis('off')

	norm6 = ImageNormalize(ref2, interval=ZScaleInterval())
	ax6.imshow(np.flipud(np.rot90(ref2)), origin='lower',cmap='gray',norm=norm6)
	ax6.axis('off')

	norm7 = ImageNormalize(diff2, interval=ZScaleInterval())
	ax7.imshow(np.flipud(np.rot90(diff2)), origin='lower',cmap='gray',norm=norm7)
	ax7.axis('off')

	norm8 = ImageNormalize(scorr2, interval=ZScaleInterval())
	ax8.imshow(np.flipud(np.rot90(scorr2)), origin='lower',cmap='gray',norm=norm8)
	ax8.axis('off')

	print(datetime.now() - startTime) # Print time it took to run function
	plt.savefig(figure, format='png', dpi=300)
	return figure

def populate_models(directory):	
	# Delete existing data in database so we don't get duplicates everytime we runserver
	#Transient_fields.objects.all().delete()
	#Transient_files.objects.all().delete()
	
	# Populate Transient_fields database
	for field in glob.glob(directory): # Use '/Users/simdewet/Desktop/matching_pairs/*
		field_ID = field.split('/')[-1]
		nights = []; numbers = []
		
		for combined_file in glob.glob(field+'/*/*combined.fits'):
			nights.append(combined_file.split('/')[-2])
			hdul = fits.open(combined_file)
			data = hdul[1].data
			numbers.append(len(data))
		
		nights.sort()
		nights = ', '.join(nights) # output as comma-separated values instead of list
		number = sum(numbers)
		new_fields_entry = Transient_fields.objects.create(field_ID=field_ID, nights=str(nights), number=number)
		new_fields_entry.save()

		# Populate Transient_files database
		for combined_file in glob.glob(field+'/*/*combined.fits'):
			hdul = fits.open(combined_file)
			data = hdul[1].data
			wcs = WCS(header=hdul[1].header)
			size = u.Quantity((1, 1), u.arcmin)

			for i in range(len(data)):
					filename1 = data['FILE1'][i].replace('_red_trans.fits', ''); filename2 = data['FILE2'][i].replace('_red_trans.fits', '')
					file_1 = filename1.split('/')[-1]; file_2 = filename2.split('/')[-1]
					filter_1 = filename1.split('/')[-3]; filter_2 = filename2.split('/')[-3]
					date_observed = filename1.split('/')[-2] 
					ra1 = data['RA_PEAK_1'][i]; ra2 = data['RA_PEAK_2'][i]
					dec1 = data['DEC_PEAK_1'][i]; dec2 = data['DEC_PEAK_2'][i]
					scorr_1 = data['SCORR_PEAK_1'][i]; scorr_2 = data['SCORR_PEAK_2'][i]
					mag_1 = data['MAG_PEAK_1'][i]; mag_2 = data['MAG_PEAK_2'][i]
					coords = "(%.5f, %.5f)" % ((ra1+ra2)*.5,(dec1+dec2)*.5)
					c1 = SkyCoord(ra1, dec1, frame="icrs", unit="deg"); c2 = SkyCoord(ra2, dec2, frame="icrs", unit="deg")
					new_files_entry = Transient_files.objects.create(field_ID=new_fields_entry, file_1=file_1, file_2=file_2, filter_1=filter_1, filter_2=filter_2, scorr_1=scorr_1, scorr_2=scorr_2, mag_1=mag_1, mag_2=mag_2, date_observed=date_observed, coords=coords)
					new_files_entry.img.save('vetting.', plot_image(filename1, filename2, filter_1, filter_2, c1, c2, new_fields_entry))

populate_models('/Users/simdewet/Desktop/matching_pairs_10/*')






