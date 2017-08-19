
from django.conf.urls import include, url


from app.views import post_list

# urls используется для связывания форм и функций.
# buttonClick вызывается в пространстве app

app_name = 'app'

urlpatterns = [
    url(r'^$', post_list, name="post_list"),
]
