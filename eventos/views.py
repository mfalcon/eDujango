from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django import http
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags

from eventos.models import Noticia2
from eventos.forms import NoticiaForm

from django.forms.models import model_to_dict
import forms

@login_required
def noticias(request):
    notis = Noticia2.objects.all()
    categorias = []
    categorias = [n.categoria for n in Noticia2.objects.all() if n.categoria not in categorias]
    
    context = {
        'noticias': notis, 'categorias': categorias,
    }
    return render_to_response(
        'eventos/noticias.html',
        context,
        context_instance = RequestContext(request),
    )
    
@login_required
def nueva_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(data=request.POST)
        if form.is_valid():
            '''
            noti = form.save(commit=False)
            noti.titulo = Alumno.objects.get(pk=st_id)
            informe.maestra = request.user.get_profile().content_object
            informe.texto = strip_tags(informe.texto)
            form.save()  
            '''
            return HttpResponseRedirect(reverse('noti_index'))
            
    else:
        form = NoticiaForm()
    
    context = {
        'noticia_form': form,
    }
    return render_to_response(
        'eventos/nueva_noticia.html',
         context,
         context_instance = RequestContext(request),
    )
    
@login_required
def modificar_noticia(request, noti_id):
    noti = Noticia2.objects.get(id=noti_id)
    dictionary = model_to_dict(noti, fields=[], exclude=[])
    #form = forms.InformeForm(dictionary)
    if request.method == 'POST':
        form = NoticiaForm(data=request.POST)
        if form.is_valid():
            noti.titulo = form.cleaned_data['titulo'] 
            noti.texto = strip_tags(form.cleaned_data['texto'])
            noti.fecha = form.cleaned_data['fecha']
            noti.save()  
            return HttpResponseRedirect(reverse('noti_index'))
            
    else:
        form = forms.NoticiaForm(dictionary)
    
    context = {
        'noticia_form': form,
    }
    return render_to_response(
        'eventos/modificar_noticia.html',
         context,
         context_instance = RequestContext(request),
    )

@login_required
def mod_not(request):
    noti = Noticia2.objects.get(id=3)
    dictionary = model_to_dict(noti, fields=[], exclude=[])
    #form = forms.InformeForm(dictionary)
    if request.method == 'POST':
        form = NoticiaForm(data=request.POST)
        if form.is_valid():
            noti.titulo = form.cleaned_data['titulo'] 
            noti.texto = strip_tags(form.cleaned_data['texto'])
            noti.fecha = form.cleaned_data['fecha']
            noti.save()  
            return HttpResponseRedirect(reverse('noti_index'))
            
    else:
        form = forms.NoticiaForm(dictionary)
    
    context = {
        'noticia_form': form,
    }
    return render_to_response(
        'eventos/modificar_noticia.html',
         context,
         context_instance = RequestContext(request),
    )
