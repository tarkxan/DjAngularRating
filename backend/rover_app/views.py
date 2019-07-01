from django.contrib.auth.models import User, Group

from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

# from .serializers import OwnerSerializer, SitterSerializer, PetSerializer, StaySerializer, SitterDetailsSerializer
from .serializers import SitterSerializer, SitterDetailsSerializer
from .models import Owner, Sitter, Pet, Stay

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.contrib import messages
from .import utils
import csv, io
from rest_framework.response import Response



# get all sitters sorted from the highest rank to lowest
@csrf_exempt
def sitter_list(request):

    if request.method == 'GET':
        sitters = Sitter.objects.order_by('-overall_sitter_rank')
        sitters_serializer = SitterSerializer(sitters, many=True)

        return JsonResponse(sitters_serializer.data, safe=False)
        # In order to serialize objects, we must set 'safe=False'

    elif request.method == 'POST':
        pass

    elif request.method == 'DELETE':
        pass

@csrf_exempt
def sitter_detail(request,
                  sitter_id):

    try:
        sitter = Sitter.objects.get(pk=sitter_id)

    except Sitter.DoesNotExist:

        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        sitter_serializer = SitterDetailsSerializer(sitter)
        return JsonResponse(sitter_serializer.data, safe=False)

    elif request.method == 'PUT':
        pass

    elif request.method == 'DELETE':
        pass

@csrf_exempt
def sitter_list_by_rating(request,
                          rating = 1):

    # rounded rating, for example: for rating 4 - return starting from rating 3.5
    filter_rating = int(rating) - 0.5
    sitters = Sitter.objects.filter(avg_rating_score__gte=filter_rating).order_by('-overall_sitter_rank')

    if request.method == 'GET':
        sitters_serializer = SitterSerializer(sitters, many=True)
        return JsonResponse(sitters_serializer.data, safe=False)
        # In order to serialize objects, we must set 'safe=False

    elif request.method == 'POST':
        pass

    elif request.method == 'DELETE':
        pass


# class SitterViewSet(viewsets.ModelViewSet):
#
#     # queryset = Sitter.objects.all()
#     queryset = Sitter.objects.order_by('-overall_sitter_rank')
#     serializer_class = SitterDetailsSerializer
#
#     def list(self,
#              request,
#              *args,
#              **kwargs):
#
#         # rating = args[0]
#
#         # print('\n\n\n\nRating: ', rating)
#
#         sitters = Sitter.objects.order_by('-overall_sitter_rank')
#         # sitters = Sitter.objects.filter(avg_rating_score__gte=3).order_by('-overall_sitter_rank')
#         # sitters = Sitter.objects.filter(avg_rating_score__gte=rating).order_by('-overall_sitter_rank')
#         serializer = SitterSerializer(sitters, many=True)
#         return Response(serializer.data)


# class OwnerViewSet(viewsets.ModelViewSet):
#
#     queryset = Owner.objects.all()
#     serializer_class = OwnerSerializer
#
#
# class PetViewSet(viewsets.ModelViewSet):
#
#     queryset = Pet.objects.all()
#     serializer_class = PetSerializer
#
# class StayViewSet(viewsets.ModelViewSet):
#
#     queryset = Stay.objects.all()
#     serializer_class = StaySerializer

from django import template
register = template.Library()

@register.filter(name='times')
def times(count):
    return range(int(count))


@permission_required('admin.can_add_log_entry')

def csv_file_upload(request):

    template = 'rover_app/csv_file_upload.html'
    prompt = {
        'order_header': 'Order in a CSV file should be:',
        'order_message': 'rating | sitter_image | end_date | text | owner_image | dogs | sitter | owner | '
                         'start_date | sitter_phone_number | sitter_email | owner_phone_number | owner_email'
    }

    if request.method == 'GET':
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request,
                       'This is not a CSV file')
        return

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)

    #skip the header
    next(io_string)

    sitters_id_set = set()
    for col in csv.reader(io_string, delimiter=',', quotechar='|'):

        owner, owner_created = Owner.objects.update_or_create(
            owner_name=col[7],
            owner_image=col[4],
            owner_phone_number=col[11],
            owner_email=col[12],
        )

        sitter, sitter_created = Sitter.objects.update_or_create(
            sitter_name=col[6],
            sitter_image=col[1],
            sitter_phone_number=col[9],
            sitter_email=col[10],
        )

        pets_lst = []
        for pt in col[5].split('|'):

            pet, pet_created = Pet.objects.update_or_create(
                pet_name = pt,
                owner = owner,
            )

            pets_lst.append(pet)

        stay, stay_created = Stay.objects.update_or_create(
            rating=col[0],
            text=col[3],
            start_date=col[8],
            end_date=col[2],
            # pets=set(pets_lst),
            owner=owner,
            sitter=sitter,
        )

        if stay_created:
            for pt in pets_lst:
                stay.pets.add(pt)

            # if a new rating added - add sitter_id to a set
            sitters_id_set.add(sitter.pk)


    # recalculate rating score only for newly added / updated
    if sitters_id_set:
        utils.calculate_sitter_scores(sitters_lst = sitters_id_set,
                                      sitter = None)

    context = {}
    return render(request, template, context)