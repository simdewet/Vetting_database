from django.shortcuts import render
from django.core.files import File
from django.views.generic import ListView
from next_prev import next_in_order, prev_in_order

from .models import Transient_files, Transient_fields
from .table import Transient_filesTable, Transient_fieldsTable, CandidatesTable


def fields_table(request):
	table = Transient_fieldsTable(Transient_fields.objects.all())
	return render(request, 'vetting/transient_fields.html', {'table': table})

def files_table(request, field_ID):
	table = Transient_filesTable(Transient_files.objects.filter(field_ID__field_ID=field_ID).order_by('mag_1', 'pk')) # only show entries from field 'field_ID', and order by 'mag_1' column
	return render(request, 'vetting/transient_files.html', {'table': table, 'field_ID': field_ID})

candidate_list=[] # list of ids of candidate transients

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

	return render(request, 'vetting/images.html', {'entry': entry, 'next_id': next_id, 'previous_id': previous_id, 'coords': coords})

candidate_list = [308, 310, 274, 311, 1507, 1523, 1567, 1519, 1568, 1566, 1556, 1538, 1580, 1571, 1464, 1453, 1495, 1473, 1451, 1457, 1444, 961, 249, 168, 175, 220, 157, 39, 388, 346, 568, 588, 606, 582, 942, 744, 926, 938, 557, 411, 448, 738, 700, 1207, 1214, 1073, 1091, 1410, 1380, 1333, 1022, 1023, 995]
show_candidates = [1022, 568, 560, 1023, 1073, 1091, 588, 1473, 311, 1566, 1556, 606, 220, 582, 157, 1333, 1571, 448, 1451, 1457]

def candidates(request):
	print (candidate_list)
	table = CandidatesTable(Transient_files.objects.filter(id__in=show_candidates).order_by('pk'))
	return render(request, 'vetting/candidates.html', {'table': table})

def candidates_image_view(request, ID):
	qs = Transient_files.objects.filter(id__in=show_candidates).order_by('pk')
	
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

	return render(request, 'vetting/candidate_images.html', {'entry': entry, 'next_id': next_id, 'previous_id': previous_id, 'coords': coords})



