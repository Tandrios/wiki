from django.http import HttpResponse
import markdown2

from django.shortcuts import redirect, render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    try:    
        return render(request, "encyclopedia/entry.html", {
            "entry_name": name.capitalize(),
            "entry": markdown2.markdown(util.get_entry(name.capitalize())),
        })
    except TypeError:
        return render(request, "encyclopedia/404.html", {
            "entry": name.capitalize(),
        })

def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()
    results = []

    for entry in entries:
        if entry.lower().find(query.lower()) != -1:
            results.append(entry)

    return render(request, "encyclopedia/search.html", {
        "entries": results
    })

def new(request):
    if request.method =="POST":
        title = request.POST.get('title')
        entrytext = request.POST.get('entrytext')
        entries = util.list_entries()

        if not title or not entrytext:
            return render(request, "encyclopedia/new.html", {
                "alarm": "Fill in all the fields"
            })
        
        for entry in entries:
            if entry.lower() == title.lower():
                return render(request, "encyclopedia/new.html", {
                    "alarm": "Entry already exists"
                })
        
        util.save_entry(title.capitalize(), entrytext)

        return redirect(f"/{title}")
    
    else:
        return render(request, "encyclopedia/new.html")