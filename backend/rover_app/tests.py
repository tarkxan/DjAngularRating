from django.test import TestCase
from .models import Owner, Pet, Sitter, Stay

from django.urls import reverse
from .views import sitter_list, sitter_detail, sitter_list_by_rating

from django.test.client import RequestFactory
from .import utils
from django.db.models import Sum, Min, Max, Avg

"""------------------------- Test Models -------------------------"""
class OwnerTest(TestCase):

    def create_owner(self,
                     owner_name = 'Alex A.',
                     owner_image = 'https://images.dog.ceo/breeds/komondor/n02105505_938.jpg',
                     owner_phone_number = '+13193870401',
                     owner_email = 'aa@mail.com'):

        return Owner.objects.create(owner_name = owner_name,
                                    owner_image = owner_image,
                                    owner_phone_number = owner_phone_number,
                                    owner_email = owner_email)

    def test_create_owner(self):

        owner = self.create_owner()
        self.assertTrue(isinstance(owner,
                                   Owner))

        self.assertEqual(owner.__unicode__(),
                         owner.owner_name)


class PetTest(TestCase):

    def create_pet(self,
                   pet_name = 'Rexi'):

        owner = Owner.objects.create(owner_name = 'Alex A.',
                                     owner_image = 'https://images.dog.ceo/breeds/komondor/n02105505_938.jpg',
                                     owner_phone_number = '+13193870401',
                                     owner_email = 'aa@mail.com')

        return Pet.objects.create(pet_name = pet_name,
                                  owner = owner)

    def test_create_pet(self):

        pet = self.create_pet()
        self.assertTrue(isinstance(pet,
                                   Pet))

        self.assertEqual(pet.__unicode__(),
                         pet.pet_name)


class SitterTest(TestCase):

    def create_sitter(self,
                      sitter_name = 'Brandon B.',
                      sitter_image = 'https://images.dog.ceo/breeds/schnauzer-giant/n02097130_6156.jpg',
                      sitter_phone_number = '+13193870401',
                      sitter_email = 'bb@mail.com',
                      sitter_score = 0,
                      avg_rating_score = 0,
                      overall_sitter_rank = 0):


        return Sitter.objects.create(sitter_name = sitter_name,
                                     sitter_image = sitter_image,
                                     sitter_phone_number = sitter_phone_number,
                                     sitter_email = sitter_email,
                                     sitter_score = sitter_score,
                                     avg_rating_score = avg_rating_score,
                                     overall_sitter_rank = overall_sitter_rank)

    def test_create_sitter(self):

        sitter = self.create_sitter()
        self.assertTrue(isinstance(sitter,
                                   Sitter))

        self.assertEqual(sitter.__unicode__(),
                         sitter.sitter_name)

"""------------------------- Test Views -------------------------"""
class ViewsTest(TestCase):

    def test_sitters_list_view(self):

        s = SitterTest()
        sitter = s.create_sitter()

        url = reverse('sitter_list')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code,
                         200)

        self.assertIn(sitter.sitter_name,
                      str(resp.content))

    def test_sitters_detail_view(self):

        s = SitterTest()
        sitter = s.create_sitter()

        url = reverse('sitter_detail',
                      args = [sitter.id])
        resp = self.client.get(url)

        self.assertEqual(reverse('sitter_detail',
                                 args = [sitter.id]),
                         sitter.get_absolute_url())

        self.assertEqual(resp.status_code,
                         200)

        self.assertIn(sitter.sitter_name,
                      str(resp.content))

"""------------------------- Test Rest API -------------------------"""
class APITest(TestCase):

    def setUp(self):

        self.factory = RequestFactory()

        # upload CSV file with 1 row
        csv_file = 'reviews_1.csv'
        lines = utils.csv_file_upload(csv_file)

        # print('{} lines uploaded'.format(lines))

    def tearDown(self):

        sitter = Sitter.objects.filter(pk=1).get()
        sitter.delete()

    def test_sitters(self):

        # Create an instance of a GET request.
        request = self.factory.get('/sitters/')

        response = sitter_list(request)
        self.assertEqual(response.status_code, 200)

    def test_sitter(self):

        request = self.factory.get('/sitters/1')

        response = sitter_detail(request, 1)
        self.assertEqual(response.status_code, 200)

"""------------------------- Test CSV File Upload -------------------------"""

""" Test Sitter with one Stay """
class Test_OneSitterOneStay(TestCase):

    def setUp(self):

        # upload CSV file with 1 row
        csv_file = 'reviews_1.csv'
        lines = utils.csv_file_upload(csv_file)
        # print('{} lines uploaded'.format(lines))

    def tearDown(self):

        sitter = Sitter.objects.filter(pk=1).get()
        sitter.delete()

    def get_sitter_by_id(self,
                         sitter_id):

        return Sitter.objects.filter(pk=sitter_id).get()

    def test_sitter_score(self):

        sitter = self.get_sitter_by_id(1)
        if not sitter:
            self.assertTrue(False)

        sitter_score = round(float(sitter.sitter_score), 2)

        print('sitter_name: ', sitter.sitter_name)
        print('sitter_score: ', sitter_score)

        self.assertEqual(sitter_score, 1.35)

    def test_avg_rating_score(self):

        sitter = self.get_sitter_by_id(1)
        if not sitter:
            self.assertTrue(False)

        avg_rating_score = round(float(sitter.avg_rating_score), 2)

        # print('sitter_name: ', sitter.sitter_name)
        print('avg_rating_score: ', avg_rating_score)

        self.assertEqual(avg_rating_score, 5)

    def test_sitter_overall_sitter_rank(self):

        sitter = self.get_sitter_by_id(1)
        if not sitter:
            self.assertTrue(False)

        overall_sitter_rank = round(float(sitter.overall_sitter_rank), 2)

        # print('sitter_name: ', sitter.sitter_name)
        print('overall_sitter_rank: ', overall_sitter_rank)

        self.assertEqual(overall_sitter_rank, 1.71)

""" Test Sitter with Stays = 0 (overal rating = sitter score)"""
class Test_SitterZeroStays(TestCase):

    def setUp(self):

        # upload CSV file with 1 row
        csv_file = 'reviews_1.csv'
        lines = utils.csv_file_upload(csv_file)
        # print('{} lines uploaded'.format(lines))

    def tearDown(self):

        # sitter = Sitter.objects.filter(pk=1).get()
        # sitter.delete()
        pass

    def get_sitter_by_id(self,
                         sitter_id):

        return Sitter.objects.filter(pk=sitter_id).get()

    def remove_sitter_stays(self,
                            sitter_id):

        Stay.objects.filter(pk=1).delete()
        return Stay.objects.count()

    def test_sitter_overall_sitter_rank(self):

        sitter = self.get_sitter_by_id(1)
        if not sitter:
            self.assertTrue(False)

        # remove all stays
        if self.remove_sitter_stays(sitter.id) > 0:
            print('Failed to remove stays')
            self.assertTrue(False)

        # invoke rating recalculation
        print('\n\n\nKUKU: ', sitter)

        utils.calculate_sitter_scores(None,
                                      sitter)

        sitter_score = round(float(sitter.sitter_score), 2)
        avg_rating_score = round(float(sitter.avg_rating_score), 2)
        overall_sitter_rank = round(float(sitter.overall_sitter_rank), 2)

        print('\n\n\n--------sitter_score: ', sitter_score)
        print('overall_sitter_rank: ', overall_sitter_rank)

        self.assertEqual(sitter_score,
                         1.35)

        # if no stays - rating score = 0
        self.assertEqual(avg_rating_score,
                         0)

        # if no stays - overall sitter rank = sitter rank
        self.assertEqual(overall_sitter_rank,
                         sitter_score)


""" Test Sitter with Stays between 0 and 10 (not inclusive)"""
class Test_SitterMultStays(TestCase):

    def setUp(self):

        # upload CSV file with 5 rows
        csv_file = 'reviews_2.csv'
        lines = utils.csv_file_upload(csv_file)
        # print('{} lines uploaded'.format(lines))

    def tearDown(self):

        sitter = Sitter.objects.filter(pk=1).get()
        sitter.delete()

    def get_sitter_by_id(self,
                         sitter_id):

        return Sitter.objects.filter(pk=sitter_id).get()

    def test_avg_rating_score(self):

        sitter = self.get_sitter_by_id(1)
        if not sitter:
            self.assertTrue(False)

        avg_rating_score = round(float(sitter.avg_rating_score), 2)

        # print('sitter_name: ', sitter.sitter_name)
        print('avg_rating_score: ', avg_rating_score)

        self.assertEqual(avg_rating_score, 3)

    def test_sitter_overall_sitter_rank(self):

        sitter = self.get_sitter_by_id(1)
        if not sitter:
            self.assertTrue(False)

        overall_sitter_rank = round(float(sitter.overall_sitter_rank), 2)

        # print('sitter_name: ', sitter.sitter_name)
        print('overall_sitter_rank: ', overall_sitter_rank)

        self.assertEqual(overall_sitter_rank, 1.54)

""" Test Sitter with Stays >= 10 (overal rating = avg)"""
class Test_SitterAllStays(TestCase):

    def setUp(self):

        # upload CSV file with all rows
        csv_file = 'reviews_500.csv'
        lines = utils.csv_file_upload(csv_file)
        # print('{} lines uploaded'.format(lines))


    def tearDown(self):

        pass

    # Leilani R. has 12 stays
    def get_user_with_max_stays(self,
                                sitter_name):

        return Sitter.objects.filter(sitter_name__exact=sitter_name).get()

    def test_avg_rating_score(self):

        sitter_name = 'Leilani R.'
        sitter = self.get_user_with_max_stays(sitter_name)
        if not sitter:
            self.assertTrue(False)

        avg_rating_score = round(float(sitter.avg_rating_score), 2)

        # print('sitter_name: ', sitter.sitter_name)
        print('avg_rating_score: ', avg_rating_score)

        self.assertEqual(avg_rating_score, 3.5)


    def test_sitter_overall_sitter_rank(self):

        sitter_name = 'Leilani R.'
        sitter = self.get_user_with_max_stays(sitter_name)
        if not sitter:
            self.assertTrue(False)

        avg_rating_score = round(float(sitter.avg_rating_score), 2)
        overall_sitter_rank = round(float(sitter.overall_sitter_rank), 2)

        # print('sitter_name: ', sitter.sitter_name)
        print('\n\nif stays >= 10, then overall_sitter_rank {} = avg_rating_score {} '.format(
            overall_sitter_rank, avg_rating_score))

        # if stays >= 10, then overall_sitter_rank = avg_rating_score
        self.assertEqual(overall_sitter_rank,
                         avg_rating_score)

