import json
import dateparser
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from parser_app.models import Category
from .tasks import generate_and_send

@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == 'GET':
        #obtaining categories to show in template
        categories = Category.objects.values('category_name').order_by('category_name')

        context = {
            'categories': categories,
        }

        return render(request, 'index.html', context)

    elif request.method == 'POST':
        request_body = json.loads(request.body.decode('utf-8'))

        begin_date = dateparser.parse(request_body['start_date'], settings={'TIMEZONE': 'Europe/Moscow'})
        end_date = dateparser.parse(request_body['end_date'], settings={'TIMEZONE': 'Europe/Moscow'})
        category = list(request_body['category']) if type(request_body['category']) is not list else request_body['category']
        e_mail = request_body['email']

        print("[MAIN]: Parameters received: begin_date:{0}, end_date:{1}, "
              "category:{2}, e_mail:{3}".format(begin_date, end_date, category, e_mail))

        generate_and_send.delay(begin_date=begin_date, end_date=end_date, category=category, email=e_mail)

        return redirect(index)



