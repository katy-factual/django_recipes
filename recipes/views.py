from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from models import Recipe
from forms import ContactForm, RecipeForm, UnitForm

#def object_list(request, model):
#    obj_list = model.objects.all()
#    template_name = 'recipes/%s_list.html' % model.__name__.lower()
#    return render_to_response(template_name, {'object_list': obj_list})

def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/recipes/recipe/add/thanks/')
    else:
        form = RecipeForm()
    return render_to_response('recipes/recipe_add.html', {'form': form})

#def recipe_list(request, page="1"):
#    pass

def recipe_view(request, id):
    r = Recipe.objects.get(id=id)

def search(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(title__icontains=query) |
            Q(summary__icontains=query)
        )
        results = Recipe.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("recipes/search.html", {
        "results": results,
        "query": query
    })

def contact(request):
    # If user just submitted
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            #Process form data
            topic = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            sender = form.cleaned_data.get('sender', 'noreply@example.com')
            send_mail(
                'Feeback from your site, topic: %s' % topic,
                message,
                sender,
                ['davidgrant@gmail.com']
            )
            return HttpResponseRedirect('/contact/thanks/')

    # Else if user just loaded page
    else:
        form = ContactForm(initial={'sender': 'user@example.com'})

    return render_to_response('contact.html', {'form': form})