from datetime import date
from django.core.management.base import BaseCommand
from schools.invoices.models import create_invoices
import calendar
import re
class Command(BaseCommand):
    help = '''Create invoices for specified dates. When no date is specified, then create invoices for actual month.
        Format of the date:
        2009/01 2008/02
    '''
    def handle(self, *args, **options):
        if args:
            dates = []
            for invoice_time in args:
                match = re.match(r'(\d{4})/([0-1]?\d)', invoice_time)
                if match:
                    start = date(int(match.group(1)), int(match.group(2)), 1)
                    end = date.replace(start, day=calendar.monthrange(start.year, start.month)[1])
                    dates.append((start, end))
        else:
            today = date.today()
            start = date.replace(today, day=1)
            end = date.replace(today, day=calendar.monthrange(today.year, today.month)[1])
            dates = [(start, end)]
        self._create_invoices(dates)

    def _create_invoices(self, dates):
        for start, end in dates:
            invoices = create_invoices(start, end)
            for invoice in invoices:
                print 'Created invoice for %s' % invoice.company
        