import random
from django.http import HttpResponse
import markdown2

from django.shortcuts import redirect, render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    for entry in util.list_entries():
        if name.lower() == entry.lower():
            return render(request, "encyclopedia/entry.html", {
                "entry_name": entry,
                "entry": markdown2.markdown(util.get_entry(entry)),
            })
    return render(request, "encyclopedia/404.html", {
        "entry": name,
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

def edit(request):
    if request.method == "POST":
        title = request.POST.get('title')
        entrytext = request.POST.get('entrytext')

        if not entrytext:
            return render(request, "encyclopedia/edit.html", {
                "alarm": "Fill in the entry!"
            })

        util.save_entry(title.capitalize(), entrytext)

        return redirect(f"/{title}")
    else:
        title = request.GET.get('title')
        print(title)

        entrytext = util.get_entry(title)
        print(entrytext)

        return render(request, "encyclopedia/edit.html", {
            "entry_name": title,
            "entry_text": entrytext,
        })

def random_page(request):
    entries = util.list_entries()

    random.seed()
    entrynr = random.randrange(0, len(entries), 1)

    entry = entries[entrynr]

    return render(request, "encyclopedia/entry.html", {
        "entry_name": entry,
        "entry": markdown2.markdown(util.get_entry(entry)),
    })
    