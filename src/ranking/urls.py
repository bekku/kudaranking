from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'ranking'
urlpatterns = [
    path('',views.IndexList.as_view(), name='index'),
    path('rankpage/<int:ranking_id>/', views.rankpage, name='rankpage'),
    path('new/', views.new,name='new'),
    #path('preview/', views.preview,name='preview'),
    path('search_results/',views.search_results.as_view(),name='search_results'),
    path('Soaring_ranking/', views.Soaring_ranking.as_view(),name='Soaring_ranking'),
    path('newest_ranking/', views.newest_ranking.as_view(),name='newest_ranking'),

    path('rankpaged/<int:ranking_id>/', views.rankpaged,name='rankpaged'),

    path('user/<int:user_id>/', views.userpage,name='userpage'),
    path('user/user_edit/', views.user_edit,name='user_edit'),
    path('user/user_edit_result/', views.user_edit_result,name='user_edit_result'),
    path('delete_ranking/<int:ranking_id>', views.delete_ranking, name='delete_ranking'),

    path('Created_ranking_user/<int:pk>/', views.Created_ranking_user.as_view(),name='Created_ranking_user'),
    path('Posted_ranking_user/<int:pk>/', views.Posted_ranking_user.as_view(),name='Posted_ranking_user'),

    path('TermsofUse/', views.TermsofUse,name='TermsofUse'),
    path('aboutpage/', views.aboutpage,name='aboutpage'),
    path('ads.txt', TemplateView.as_view(template_name='ranking/ads.txt', content_type='text/plain')),

]
