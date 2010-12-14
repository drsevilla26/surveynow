from django.conf.urls.defaults import *
from polls.models import Poll

info_dict = {
    'queryset': Poll.objects.all(),
}

urlpatterns = patterns('',
   (r'^register/$', 'polls.views.registro'),
   (r'^login/$', 'polls.views.login'),
   (r'^publish/$', 'polls.views.publicar'),
   (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
    #(r'^$', 'django.views.generic.list_detail.object_list', info_dict), 
    (r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict),
    url(r'^(?P<object_id>\d+)/results/$', 'django.views.generic.list_detail.object_detail', dict(info_dict, template_name='polls/resultados.html'), 'poll_results'),
    (r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
    
)


 
