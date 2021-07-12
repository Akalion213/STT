from django.core.management.base import BaseCommand, CommandError
from STTWEBMAIN.tagging import generate_tags
from STTWEBMAIN.models import Videos
import os
import time


class Command(BaseCommand):

    def handle(self, *args, **options):
        print(generate_tags('8V2b4YGr2sA.en.txt'))


