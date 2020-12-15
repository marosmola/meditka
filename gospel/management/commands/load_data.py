import re
import locale
import ebooklib
import xml.etree.ElementTree as ET

from datetime import datetime
from ebooklib import epub
from tqdm import tqdm

from django.db import transaction
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from ...models import Day, Gospel


class Command(BaseCommand):
    # help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):

        locale.setlocale(locale.LC_TIME, "sk_SK.UTF-8")

        file_path = options['file_path']
        print(file_path)

        book = epub.read_epub(file_path)
        files = [x for x in book.get_items_of_type(ebooklib.ITEM_DOCUMENT)]

        for item in tqdm(files):
            item_name = item.get_name()
            iso8601 = re.compile(r'^(?P<full>(?P<date>((?P<year>\d{4})([/-]?(?P<mon>(0[1-9])|(1[012]))([/-]?(?P<mday>(0[1-9])|([12]\d)|(3[01]))))))(?P<html>(.html)))$')
            m = iso8601.match(item_name)

            if m is None:
                continue

            body_content = item.get_body_content()
            fixed_content = body_content.decode('utf-8').replace('\xa0', ' ')
            body = ET.fromstring(fixed_content)

            date_str = body.find('.//span[@class="lcMD"]').text + body.find('.//span[@class="lcMY"]').text
            date_object = timezone.datetime.strptime(date_str.strip(), '%d. %B %Y')

            # Create or update Day
            try:
                day = Day.objects.create(
                    date=date_object,
                    dayofweek=body.find('.//span[@class="lcWD"]').text,
                    nameday=body.find('.//span[@class="lcND"]').text,
                    saintsday=None
                )
            except IntegrityError:
                day = Day.objects.get(date=date_object)
                day.dayofweek=body.find('.//span[@class="lcWD"]').text
                day.nameday=body.find('.//span[@class="lcND"]').text
                day.saintsday=None
                day.save()

            # Creato or update Gospel
            citania = body.findall('.//div[@class="lcCITANIE"]')
            for citanie in citania:
                if citanie.find('./p[@class="lcVPEblock"]') is not None:

                    plist = [p.text if p.text is not None else '' for p in citanie.findall('.//p') ]
                    text = " ".join(plist)

                    try:
                        Gospel.objects.create(
                            day=day,
                            chapter=citanie.find('.//h4/span').text,
                            chapter_title=citanie.find('.//h5').text if citanie.find('.//h5') is not None else None,
                            gospel_from=citanie.find('.//h4').text,
                            verse=citanie.find('.//span[@class="lcVERS"]').text,
                            text=text
                        )
                    except IntegrityError:
                        gospel = Gospel.objects.get(day=day, chapter=citanie.find('.//h4/span').text)
                        gospel.chapter_title = citanie.find('.//h5').text if citanie.find('.//h5') is not None else None
                        gospel.gospel_from = citanie.find('.//h4').text
                        gospel.verse = citanie.find('.//span[@class="lcVERS"]').text
                        gospel.text = text

                    # # Text in paragraphs
                    # for z in citanie.findall('.//p'): # .//p[not(@class)]
                    #     if z.text is not None:
                    #         print(z.text)

