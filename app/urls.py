
from django.conf.urls import url


from app.views import get_data

# urls используется для связывания форм и функций.
# buttonClick вызывается в пространстве app

from .views import ChartData

app_name = 'app'

urlpatterns = [
    url(r'^$', get_data, name="app-data"),
    url(r'^api/chart/data$', ChartData.as_view()),
]