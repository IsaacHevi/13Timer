from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('events/<str:name>', views.event, name='event'),
    path('pastevents/', views.past, name='past'),
    path('create/', views.create, name='create'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('add_to_watchlist/<str:name>/', views.addToWatchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<str:name>/', views.removeFromWatchlist, name='remove_from_watchlist'),
    path('search/', views.search, name='search'),
    path('delete/<str:name>/', views.delete, name='delete'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]