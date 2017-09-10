
from django.conf.urls import url


from app.views import get_data

# urls используется для связывания форм и функций.
# buttonClick вызывается в пространстве app

app_name = 'app'

urlpatterns = [
    url(r'^$', get_data, name="api-data"),
]