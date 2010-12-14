# Create your views here.
from polls.models import Poll, Choice
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from models import *
from django.contrib.auth.models import User
from django.conf.urls.defaults import *
from django.contrib.auth import authenticate, login as authlogin, logout as authlogout
import datetime
import random


#def index(request):
#    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
#    return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list})
#
#def detail(request, poll_id):
#    p = get_object_or_404(Poll, pk=poll_id)
#    return render_to_response('polls/detail.html', {'poll': p}, context_instance=RequestContext(request))
    
#def results(request, poll_id):
#    p = get_object_or_404(Poll, pk=poll_id)
#    return render_to_response('polls/results.html', {'poll': p})
# [request.POST['correo']+'@unitec.edu']

def registro(request):
	if 'correo' in request.POST:
		temp = ''
		mensa = ''
		for x in range(10):
			pwd=random.randrange(0,9)
			temp=temp+str(pwd)
		try:
			send_mail('Bienvenido a  SurveyNow!', 'Este es tu password: '+str(temp), 'DontReply@surveynow.com',[request.POST['correo']+'@unitec.edu'], fail_silently=False)
			user = User.objects.create_user(request.POST['correo'], request.POST['correo']+'@unitec.edu', temp)
			mensa = 'Thank You! Your password has been e-mailed to you'
			
		except:
			mensa = 'El usuario ya existe, o el correo no es valido'
	return render_to_response('polls/registro.html',locals(),context_instance=RequestContext(request))

# sin uso por los momentos
def logout(request):
    authlogout(request)
    return redirect('/polls/login')

def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['usuario'], password=request.POST['clave'])
        if user is None:
            mensaje = 'Usuario y/o clave incorrecto'
            return render_to_response('polls/login.html', locals(), context_instance=RequestContext(request))
        else:
            authlogin(request, user)
            return redirect('/polls/publish/')
    else:
	return render_to_response('polls/login.html', locals(), context_instance=RequestContext(request))
    

@login_required
def publicar(request):
        if request.user.is_authenticated():
        
		if 'pregunta' in request.POST:
		
			p = Poll(question=request.POST['pregunta'], pub_date=datetime.datetime.now())
			p.save()
			p.choice_set.create(choice='Si', votes=0)
			p.choice_set.create(choice='No', votes=0)
		
		return render_to_response('polls/publish.html',locals(),context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/polls/login/')


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('polls/poll_detail.html', {
            'object': p,
            'error_message': "No elegiste una opcion.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))

