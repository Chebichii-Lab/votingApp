from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings



urlpatterns=[
    path(r'',views.index,name='index'),
    path('register/',views.signup, name='registration'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('list/', views.polls_list, name='list'),
    path('add/', views.polls_add, name='add'),
    path('edit/<int:poll_id>/', views.polls_edit, name='edit'),
    path('delete/<int:poll_id>/', views.polls_delete, name='delete_poll'),
    path('edit/<int:poll_id>/choice/add/', views.add_choice, name='add_choice'),
    path('edit/choice/<int:choice_id>/', views.choice_edit, name='choice_edit'),
    path('delete/choice/<int:choice_id>/',views.choice_delete, name='choice_delete'),
    path('<int:poll_id>/vote/', views.poll_vote, name='vote'),
    path('<int:poll_id>/', views.poll_detail, name='detail'),
    path('end/<int:poll_id>/', views.endpoll, name='end_poll'),
    path('list/user/', views.list_by_user, name='list_by_user'),
]