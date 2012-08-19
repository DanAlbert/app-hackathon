from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse

from apps.models import Vote

def index(request):
    vote_list = Vote.objects.all().order_by('-count')
    return render_to_response('apps/index.html',
                              {'votes': vote_list},
                              context_instance=RequestContext(request))

def vote(request, vote_id):
    v = get_object_or_404(Vote, pk=vote_id)
    v.increment()
    v.save()
    return HttpResponseRedirect(reverse('apps.views.index'))

def rules(request):
    return render_to_response('apps/rules.html')

def about(request):
    return render_to_response('apps/about.html')

def ideas(request):
    if request.method == 'GET':
        return render_to_response('apps/ideas.html',
                                  context_instance=RequestContext(request))
    elif request.method == 'POST':
        return HttpResponseRedirect(reverse('apps.views.ideas'))
    else:
        raise Http404

def submission(request):
    return render_to_response('apps/submission.html',
                              context_instance=RequestContext(request))