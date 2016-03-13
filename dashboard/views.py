from django.core import serializers
from django.http import HttpResponseRedirect
from django.shortcuts import render
import utils
from models import User, Classes
from forms import SignInForm
import json
import ast

# Create your views here.
def router(request):
    user = User.objects.first()
    if user is None:
        return render(request, "sign-in.html", {})
    else:
        if Classes.objects.first(): #and class Has been updated this hour:
            class_info = []
            for Class in Classes.objects.all():
                class_info.append({'course_title':Class.course_title, 'course_code':Class.course_code, 'course_grade':Class.course_grade, 'grade_scale':ast.literal_eval(Class.grade_scale), 'cid':Class.cid})

            return render(request, "dash.html", {'class_info':json.dumps(class_info)})
        else:
            utils.make_class_list(user.netid, user.password)
            class_info = serializers.serialize('json', Classes.objects.all())
            return render(request, "dash.html", {class_info})

def sign_up(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            netid = request.POST['netid']
            password = request.POST['password']
            valid = utils.could_sign_in(netid, password)
            if valid:
                User.objects.create(netid=netid, password=password)
                return HttpResponseRedirect('/dashboard/')
            else:
                return HttpResponseRedirect('/dashboard/?learningSuiteFail=true')
        else:
            return HttpResponseRedirect('/dashboard/?formFail=true')
