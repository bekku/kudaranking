from django.shortcuts import render, get_object_or_404,redirect
from django.utils.safestring import mark_safe
from .models import comenting
import json


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    coment_log=comenting.objects.all().order_by('-id')
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'logs':coment_log,
    })

"""
Djangoではtemplateに渡した文字列にhtmlタグがあった場合、
自動でエスケープされるようになっていますが、mark_safeをつけることで、
htmlタグはそのままhtmlタグとして表示されます。
views.py等でhtmlタグを含んだ文字列を作成したい場合には、
mark_safeを使うことになります。
"""
