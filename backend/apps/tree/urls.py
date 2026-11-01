from django.urls import path
from .views import AdminTreeView, GenerationsView, MyTreeView, RecalculateTreeView

urlpatterns = [
    path('my-tree/', MyTreeView.as_view()),
    path('generations-table/', GenerationsView.as_view()),
    path('admin-tree/', AdminTreeView.as_view()),
    path('recalculate/', RecalculateTreeView.as_view()),
]
