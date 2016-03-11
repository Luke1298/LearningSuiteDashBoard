from django.core import serializers
from django.shortcuts import render
import utils
from models import User, Classes

# Create your views here.
def router(request):
    user = User.objects.first()
    if user is None:
        return render(request, "sign-in.html", {})
    else:
        if Classes.objects.first():
            class_info = serializers.serialize('json', Classes.objects.all())
            return render(request, "dash.html", {class_info})
        else:
            utils.make_class_list(user.netid, user.password)
            class_info = serializers.serialize('json', Classes.objects.all())
            return render(request, "dash.html", {class_info})
