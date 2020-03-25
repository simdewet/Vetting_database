from django.db import models


class Transient_fields(models.Model):
	field_ID = models.CharField('Field ID', max_length=5, default='')
	nights = models.CharField('Dates of nights with matching pairs', max_length=100, default='')
	number = models.IntegerField('Number of matching pairs', default='')
	
	class Meta:
		ordering = ['field_ID']
	
	def __str__(self):
		return "%s" % self.field_ID

class Transient_files(models.Model):
	field_ID = models.ForeignKey(Transient_fields, on_delete=models.CASCADE)
	file_1 = models.CharField('File 1', max_length=100, default='')
	file_2 = models.CharField('File 2', max_length=100, default='')
	filter_1 = models.CharField('Filter 1', max_length=1, default='')
	filter_2 = models.CharField('Filter 2', max_length=1, default='')
	scorr_1 = models.CharField('Scorr 1', max_length=10, null=True) 
	scorr_2 = models.CharField('Scorr 2', max_length=10, null=True)
	mag_1 = models.CharField('Mag 1', max_length=10, null=True)
	mag_2 = models.CharField('Mag 2', max_length=10, null=True)
	date_observed = models.CharField('Date-observed', max_length=2, default='')
	coords = models.CharField('Coordinates (degrees)', max_length=50, default='')
	img = models.ImageField(blank=True, null=True,upload_to='vetting/')


	class Meta:
		ordering = ['date_observed']


	def __str__(self):
		return self.pk






	