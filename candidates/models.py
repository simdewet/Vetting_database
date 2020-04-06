from django.db import models

class Candidates(models.Model):
	Transient_file = models.OneToOneField('vetting.Transient_files', on_delete=models.CASCADE)
	comment = models.TextField('Comment', null=True)
	simbad = models.URLField('Link to Simbad', null=True)
	TNS = models.URLField('Link to TNS', null=True)
	gaia = models.URLField('Link to Gaia', null=True)
	lightcurve = models.ImageField('Lightcurve', blank=True, null=True, upload_to='candidates/lightcurves/')
	image_series = models.ImageField('Image series', blank=True, null=True, upload_to='candidates/image_series/')

	def __str__(self):
		return self.pk
