
from django.db.models import Avg
from . import models
# from . models import Owner, Pet, Sitter, Stay
import csv, io

""" ----------- calculate ----------- """
def get_avg_rating_score(sitter_id):

    return models.Stay.objects.filter(sitter__exact=sitter_id).aggregate(Avg('rating'))

def get_sitter_score(sitter_name):

    return 5 * len(set([val.lower() for val in sitter_name if val.isalpha()])) / 26

def get_overall_sitter_rank(avg_rating,
                            sitter_score,
                            sitter_id):

    if not avg_rating:
        return sitter_score

    stays = models.Stay.objects.filter(sitter_id=sitter_id).count()

    if stays >= 10:
        return avg_rating

    # return (avg_rating - sitter_score) / 10 * stays + sitter_score
    return (avg_rating - sitter_score) / 10 * stays * avg_rating / 5 + sitter_score

""" recalculate rating score for created / updated sitters rating scores """
def calculate_sitter_scores(sitters_lst,
                            sitter):

    if sitters_lst:
        for sitter_id in sitters_lst:

            sitter = models.Sitter.objects.filter(pk=sitter_id).first()

            if not sitter:
                return

            # get average rating score
            avg_rating = get_avg_rating_score(sitter_id)

            # get sitter score
            sitter_score = get_sitter_score(sitter.sitter_name)

            # if a sitter has no rating
            overall_sitter_rank = get_overall_sitter_rank(avg_rating['rating__avg'],
                                                          sitter_score,
                                                          sitter_id)

            sitter = models.Sitter.objects.filter(pk=sitter_id).first()
            setattr(sitter, 'sitter_score', sitter_score)
            if avg_rating['rating__avg']:
                setattr(sitter, 'avg_rating_score', avg_rating['rating__avg'])
            else:
                setattr(sitter, 'avg_rating_score', 0)
            setattr(sitter, 'overall_sitter_rank', overall_sitter_rank)
            sitter.save()

    elif sitter:

        # get average rating score
        avg_rating = get_avg_rating_score(sitter.id)

        # get sitter score
        sitter_score = get_sitter_score(sitter.sitter_name)

        # if a sitter has no rating
        overall_sitter_rank = get_overall_sitter_rank(avg_rating['rating__avg'],
                                                      sitter_score,
                                                      sitter.id)

        #sitter = models.Sitter.objects.filter(pk=sitter.id).first()
        setattr(sitter, 'sitter_score', sitter_score)
        if avg_rating['rating__avg']:
            setattr(sitter, 'avg_rating_score', avg_rating['rating__avg'])
        else:
            setattr(sitter, 'avg_rating_score', 0)
        setattr(sitter, 'overall_sitter_rank', overall_sitter_rank)
        sitter.save()

""" ---------------------- upload data for test purposes ---------------------- """
def csv_file_upload(filepath):

    if not filepath.endswith('.csv'):

        print('Not a CSV file format')
        return

    sitters_id_set = set()
    rows = 0

    with open(filepath) as csvfile:

        for row in csv.reader(csvfile, delimiter=',', quotechar='|'):

            rows += 1
            # print('row: ', row)

            # skip headers line
            if rows == 1:
                continue

            owner, owner_created = models.Owner.objects.update_or_create(
                owner_name=row[7],
                owner_image=row[4],
                owner_phone_number=row[11],
                owner_email=row[12],
            )

            sitter, sitter_created = models.Sitter.objects.update_or_create(
                sitter_name=row[6],
                sitter_image=row[1],
                sitter_phone_number=row[9],
                sitter_email=row[10],
            )

            pets_lst = []
            for pt in row[5].split('|'):

                pet, pet_created = models.Pet.objects.update_or_create(
                    pet_name = pt,
                    owner = owner,
                )

                pets_lst.append(pet)

            stay, stay_created = models.Stay.objects.update_or_create(
                rating=row[0],
                text=row[3],
                start_date=row[8],
                end_date=row[2],
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
        calculate_sitter_scores(sitters_lst = sitters_id_set,
                                sitter = None)

    return rows - 1
