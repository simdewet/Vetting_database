import django_tables2 as tables
from django_tables2.utils import A # alias for accessor
from .models import Transient_files, Transient_fields
import itertools

class Transient_fieldsTable(tables.Table):
	# Add hyperlinks to first column
	field_ID = tables.LinkColumn("vetting:files_table", args=[A("field_ID")]) # args is the argument from model which is passed to "vetting:files_table" view function
	
	# Table properties
	class Meta:
		model = Transient_fields
		template_name = "django_tables2/bootstrap.html"
		fields = ("field_ID", "nights", "number")

class Transient_filesTable(tables.Table):
	# Add linked column showing row number
	ID = tables.LinkColumn("vetting:images", text=lambda Transient_files: Transient_files.pk, args=[A("field_ID"), A("pk")]) # first argument is name of url to go to

	# Table properties
	class Meta:
		model = Transient_files
		template_name = "django_tables2/bootstrap.html"
		fields = ("ID", "date_observed", "coords", "file_1", "file_2", "filter_1", "filter_2", "scorr_1", "scorr_2", "mag_1", "mag_2")   
  
class CandidatesTable(tables.Table):
	# Add linked column showing row number
	ID = tables.LinkColumn("vetting:images", text=lambda Transient_files: Transient_files.pk, args=[A("field_ID"), A("pk")]) # first argument is name of url to go to

	# Table properties
	class Meta:
		model = Transient_files
		template_name = "django_tables2/bootstrap.html"
		fields = ("ID", "field_ID", "date_observed", "coords", "file_1", "file_2", "filter_1", "filter_2", "scorr_1", "scorr_2", "mag_1", "mag_2") 