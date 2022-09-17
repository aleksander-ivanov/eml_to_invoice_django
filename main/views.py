import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import HttpResponse
from django.shortcuts import render

from main.models import Company
from main.modules.zipper.zipper import Zipper


logger = logging.getLogger(__name__)  # TODO: fix

# https://pylessons.com/django-website


def homepage(request):
    return render(request, 'main/homepage.html')


def about(request):
    return render(request, 'main/about.html')


@login_required()
def build(request):
    logger.info('file upload requested')
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            req_file = request.FILES['file']
            invoice_number = int(request.POST['invoice-number'])
            company = Company.objects.get(pk=1)
            user = request.user

            zip_file = Zipper.build_zip(req_file, company, user, invoice_number)

            response = HttpResponse(zip_file, content_type="application/zip", )
            response['Content-Disposition'] = 'attachment;filename=invoices.zip'
            return response
        except Exception as e:
            return HttpResponseBadRequest(str(e))
    else:
        return render(request, 'main/build.html')
