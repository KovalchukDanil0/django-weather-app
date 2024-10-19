from django.urls import path

from .views import DetailViewClass, IndexView, ResultsView, vote

app_name = "polls"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("<int:pk>/", DetailViewClass.as_view(), name="detail"),
    path("<int:pk>/results/", ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", vote, name="vote"),
]
