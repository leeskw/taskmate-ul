from django.contrib import admin
from django.urls import include, path

from todolist_app import views as todolist_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', todolist_views.index, name='index'),
    path('account/', include('users_app.urls')),
    path('todolist/', include('todolist_app.urls')),
    path('contact/', todolist_views.contact, name='contact'),
    path('about-us/', todolist_views.about, name='about'),
]
