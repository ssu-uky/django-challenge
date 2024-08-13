from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.http import Http404
from django.shortcuts import render
from django.urls import path, include
from fake_db import user_db

from todo.views import todo_list, todo_info, todo_create, todo_update, todo_delete
from todo.cb_views import TodoListView
from users import views as user_views


_db = user_db


def user_list(request):
    names = [{"id": key, "name": value["이름"]} for key, value in _db.items()]
    return render(request, "user_list.html", {"data": names})


def user_info(request, user_id):
    if user_id > len(_db):
        raise Http404("User not found")
    info = _db[user_id]
    return render(request, "user_info.html", {"data": info})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", user_list, name="user_list"),
    path("users/<int:user_id>/", user_info, name="user_info"),
    path("todo/", todo_list, name="todo_list"),
    path("todo/create/", todo_create, name="todo_create"),
    path("todo/<int:todo_id>/", todo_info, name="todo_info"),
    path("todo/<int:todo_id>/update/", todo_update, name="todo_update"),
    path("todo/<int:todo_id>/delete/", todo_delete, name="todo_delete"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/login/", user_views.login, name="login"),
    path("accounts/signup/", user_views.sign_up, name="signup"),
    path("cbv/", include("todo.urls")),
    path("summernote/", include("django_summernote.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
