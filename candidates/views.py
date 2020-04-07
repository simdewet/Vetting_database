from django.shortcuts import render
from django.core.files import File
from django.views.generic import ListView
from next_prev import next_in_order, prev_in_order

from vetting.models import Transient_files
from .models import Candidates
from .table import CandidatesTable

candidate_list = [556, 558, 496, 559, 2634, 2660, 2711, 2712, 2709, 2749, 2734, 2715, 2718, 2742, 2735, 2717, 2569, 2545, 2608, 2542, 2554, 1784, 1820, 418, 286, 295, 373, 266, 438, 77, 177, 696, 1007, 1070, 1209, 995, 1051, 1108, 1781, 1427, 1757, 1740, 1496, 987, 729, 964, 982, 797, 1417, 1274, 1425, 1405, 2200, 2210, 2016, 2128, 2493, 2357, 2454, 1889]

def candidates(request):
	# Ensure that candidate_list transients are added to Candidates database
	current_ids = Candidates.objects.all().values_list('Transient_file_id', flat=True) # IDs in database
	candidates_in_database_not_in_list = list(set(current_ids).difference(candidate_list)) # find IDs in database not in list
	Candidates.objects.filter(Transient_file_id__in=candidates_in_database_not_in_list).delete() # remove them
	current_ids = Candidates.objects.all().values_list('Transient_file_id', flat=True) # IDs in database after removal
	for i in range(len(candidate_list)):
		if candidate_list[i] in current_ids: # if entry is in database, don't add again
			pass
		elif candidate_list[i] not in current_ids:
			entry = Candidates.objects.create(Transient_file_id=candidate_list[i]) # if entry not in database, add to database
			entry.save()

	table = CandidatesTable(Candidates.objects.all().order_by('Transient_file_id'))
	return render(request, 'candidates/candidates.html', {'table': table})

def candidates_image_view(request, ID):
	qs = Candidates.objects.all().order_by('pk')
	
	first = qs.first()
	last = qs.last()
	entry = Candidates.objects.get(id=ID)
	coords = entry.Transient_file.coords.replace('(','').replace(')','')
	
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

	return render(request, 'candidates/candidate_images.html', {'entry': entry, 'next_id': next_id, 'previous_id': previous_id, 'coords': coords})