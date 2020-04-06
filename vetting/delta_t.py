from vetting.models import Transient_files
from astropy.io import fits
from astropy.time import Time
from astropy import units as u

entries = Transient_files.objects.all()

for entry in entries:
	hdul_1 = fits.open('/Volumes/Seagate_Backup_Plus_Drive/new_transients/%s/%s/%s/%s_red.fits.fz' % (entry.field_ID, entry.filter_1, entry.date_observed, entry.file_1))
	header_1 = hdul_1[1].header
	t1 = Time(header_1['DATE-OBS'], format='isot', scale='utc')
	
	ref_hdul_1 = fits.open('/Volumes/Seagate_Backup_Plus_Drive/new_transients_reference_images/0%s/ML1_%s_red.fits.fz' % (entry.field_ID,entry.filter_1))
	ref_header_1 = ref_hdul_1[1].header
	ref_t1 = Time(ref_header_1['DATE-OBS'], format='isot', scale='utc')

	delta_t1 = round((t1 - ref_t1).to_value(u.d),4)  # time between reference image and science image being taken, in units of days
	
	
	hdul_2 = fits.open('/Volumes/Seagate_Backup_Plus_Drive/new_transients/%s/%s/%s/%s_red.fits.fz' % (entry.field_ID, entry.filter_2, entry.date_observed, entry.file_2))
	header_2 = hdul_2[1].header
	t2 = Time(header_2['DATE-OBS'], format='isot', scale='utc')
	
	ref_hdul_2 = fits.open('/Volumes/Seagate_Backup_Plus_Drive/new_transients_reference_images/0%s/ML1_%s_red.fits.fz' % (entry.field_ID,entry.filter_2))
	ref_header_2 = ref_hdul_2[1].header
	ref_t2 = Time(ref_header_2['DATE-OBS'], format='isot', scale='utc')

	delta_t2 = round((t2 - ref_t2).to_value(u.d),4) 

	entry.dt_1 = delta_t1
	entry.dt_2 = delta_t2
	entry.save()
	 