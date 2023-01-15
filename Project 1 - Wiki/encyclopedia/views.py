from dis import dis
from logging import PlaceHolder
from mimetypes import init
from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

import markdown2
import random

from . import util

class SearchForm(forms.Form):
    query = forms.CharField(label = "", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))


class CreatePagesForm(forms.Form):
    title = forms.CharField(label = "", widget=forms.Textarea(attrs={'placeholder': 'Title', 'style': 'height: 3em;'}))
    text_area = forms.CharField(label = "", widget=forms.Textarea(attrs={'placeholder': 'Entry', 'style': 'height: 30em'}))


class EditForm(forms.Form):
    title = forms.CharField(label = "", widget=forms.Textarea(attrs={'placeholder': 'Title', 'style': 'height: 3em;', 'readonly': 'readonly'}))
    text_area = forms.CharField(label = "", widget=forms.Textarea(attrs={'placeholder': 'Entry', 'style': 'height: 30em'}))



def index(request):
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = SearchForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the title from the 'cleaned' version of form data
            query = form.cleaned_data['query']

            # If query matches the name of an encyclopedia entry, user is redirected to that entry's page
            entries_list = [x.lower() for x in util.list_entries()]
            if query.lower() in entries_list:
                return HttpResponseRedirect(reverse("entry_page", args=[query]))

            # Else, if the query does not match the name of an encyclopedia entry, user is taken to a search result page that displays a list of encyclopedia entries that have the
            # query as a substring
            else:
                sub_query = [x for x in entries_list if query.lower() in x]
                return render(request, "encyclopedia/search.html", {
                    "query": query,
                    "entries": [x for x in util.list_entries() if x.lower() in sub_query],
                    "form": SearchForm()
                })

    # Return to index page
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


def entry_page(request, title):
    # if the entry exists, returns a page that displays the content of the entry
    if util.get_entry(title) != None:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2.markdown(util.get_entry(title)),
            "form": SearchForm()})

    # else, returns an error page indicating that the requested page was not found
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "form": SearchForm()})


def new_page(request):
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = CreatePagesForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            # Get the 'cleaned' version of form data
            title = form.cleaned_data['title']
            text_area = form.cleaned_data['text_area']

            # If an encyclopedia entry already exists with the provided title, user is presented with an error message
            entries_list = [x.lower() for x in util.list_entries()]
            if title.lower() in entries_list:
                return render(request, "encyclopedia/newpage_error.html", {
                    "title": title,
                    "form": SearchForm()})

            # Otherwise, entry is saved to disk, and user is taken to the new entry's page
            else:
                util.save_entry(title, text_area)
                return HttpResponseRedirect(reverse("entry_page", args=[title]))

    return render(request, "encyclopedia/new_page.html", {
        "form": SearchForm(),
        "newpage_form": CreatePagesForm()
    })


def edit_page(request, title):
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = EditForm(request.POST)

        # Check if form data is valid (server-side) 
        if form.is_valid():
            # Get the 'cleaned' version of form data
            text_area = form.cleaned_data['text_area']

            # Update the markdown file
            util.save_entry(title, text_area)

            # Redirected to that entry's page
            return HttpResponseRedirect(reverse("entry_page", args=[title]))

    return render(request, "encyclopedia/edit_page.html", {
        "form": SearchForm(),
        "editpage_form": EditForm(initial={'title': title, 'text_area': util.get_entry(title)}),
        "title": title
    })


def random_page(request):
    # get a random title from all the entries
    entries = util.list_entries()
    title = random.choice(entries)

    # redirect to that title
    return HttpResponseRedirect(reverse("entry_page", args=[title]))