import django_tables2 as tables
from django_tables2.utils import A # alias for accessor
from candidates.models import Candidates
import itertools



class CandidatesTable(tables.Table):
	# Add linked column showing row number
	#ID = tables.Column(accessor="pk")
	row_number = tables.Column(empty_values=())
	Transient_file_ID = tables.LinkColumn("candidates:candidates_image", text=lambda Candidates: Candidates.Transient_file.pk, args=[A("pk")]) # first argument is name of url to go to
	Field_ID = tables.Column(accessor="Transient_file.field_ID")
	coords = tables.Column(accessor="Transient_file.coords")
	scorr_1 = tables.Column(accessor="Transient_file.scorr_1")
	scorr_2 = tables.Column(accessor="Transient_file.scorr_2")
	external_links = tables.TemplateColumn('{% if record.simbad %} <a href="{{record.simbad}}" target="_blank">Simbad</a> {% endif %} {% if record.gaia %} <a href="{{record.gaia}}" target="_blank">Vizier_gaia</a> {% endif %} {% if record.TNS %} <a href="{{record.TNS}}" target="_blank">TNS</a> {% endif %}')
	image_series = tables.TemplateColumn('{% extends "candidates/image_modal.html" %}{% block content %}{% if record.image_series %} <a href="javascript:void(0)"> <img class="img-responsive" src="{{record.image_series.url}}" width="50px"> </a>{% endif %}{% endblock %}')
	light_curves = tables.TemplateColumn('{% extends "candidates/image_modal.html" %}{% block content %}{% if record.lightcurve %} <a href="javascript:void(0)"> <img class="img-responsive" src="{{record.lightcurve.url}}" width="100px"> </a>{% endif %}{% endblock %}')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.counter = itertools.count()

	def render_row_number(self):
		return "%d" % (next(self.counter)+1)
	# Table properties
	class Meta:
		model = Candidates
		template_name = "django_tables2/bootstrap.html"
		fields = ("row_number", "Transient_file_ID", "Field_ID", "coords", "scorr_1", "scorr_2", "comment", "image_series", "light_curves", "external_links") 