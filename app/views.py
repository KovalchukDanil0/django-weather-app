from json import loads
from urllib.request import urlopen

from django.db.models import F
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView

from .models import Choice, Question


def index(request: HttpRequest, template_name="app/home.html"):

    with urlopen(
        "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    ) as response:
        json = loads(response.read())

    args = {"latitude": json["latitude"]}
    return render(request, template_name, args)


class DetailViewClass(DetailView):
    model = Question
    template_name = "app/detail.html"


class ResultsView(DetailView):
    model = Question
    template_name = "app/results.html"


def vote(request: HttpRequest, question_id: int):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "app/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("app:results", args=(question.id,)))