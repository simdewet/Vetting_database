from django.shortcuts import render
from django.core.files import File
from django.views.generic import ListView
from next_prev import next_in_order, prev_in_order

from .models import Transient_files, Transient_fields
from .table import Transient_filesTable, Transient_fieldsTable 

candidate_list=[]

def fields_table(request):
	table = Transient_fieldsTable(Transient_fields.objects.all())
	return render(request, 'vetting/transient_fields.html', {'table': table})

def files_table(request, field_ID):
	table = Transient_filesTable(Transient_files.objects.filter(field_ID__field_ID=field_ID).order_by('mag_1', 'pk')) # only show entries from field 'field_ID', and order by 'mag_1' column
	return render(request, 'vetting/transient_files.html', {'table': table, 'field_ID': field_ID})

def image_view(request, field_ID, ID):
	qs = Transient_files.objects.filter(field_ID__field_ID=field_ID).order_by('mag_1', 'pk')
	
	first = qs.first()
	last = qs.last()
	entry = Transient_files.objects.get(id=ID)
	coords = entry.coords.replace('(', '').replace(')', '')
	
	# If user is on first image page, previous button keeps them on same page. If they are on last image page, next button keeps them on same page.
	if entry.pk == first.pk:
		next_entry = next_in_order(entry, qs=qs)
		previous_entry = entry 
	elif entry.pk == last.pk:
		next_entry = entry
		previous_entry = prev_in_order(entry, qs=qs)
	else:
		next_entry = next_in_order(entry, qs=qs)
		previous_entry = prev_in_order(entry, qs=qs)
	
	next_id = next_entry.pk
	previous_id = previous_entry.pk

	""" If user clicks Add button, then pk of post should be saved to 'candidates' list"""
	if request.POST.get('pair_id') == 'Add':
		candidate_list.append(entry.pk)
	if request.POST.get('pair_id') == 'Remove':
		candidate_list.remove(entry.pk)

	return render(request, 'vetting/images.html', {'entry': entry, 'next_id': next_id, 'previous_id': previous_id, 'coords': coords, 'candidate_list': candidate_list})






