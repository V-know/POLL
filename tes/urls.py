from django.urls import path
from . import views

urlpatterns = [
    # /tes/
    path('', views.index, name='homepage'),

    # 投票功能
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/audit/', views.audit, name='audit'),
    path('<int:question_id>/audit_del/', views.audit_del, name='audit_del'),
    #  登陆
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    #  实现功能
    path('add_polls/', views.add_polls, name='add_polls'),
    path('polls_list/', views.polls_list, name='polls_list'),
    path('polls_list_my', views.polls_list_my, name='polls_list_my'),
    path('polls_detail/<int:questions_id>/', views.polls_detail, name='polls_detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('polls_audit/', views.polls_audit, name='polls_audit'),
    path('polls_audit_detail/<int:questions_id>/', views.polls_audit_detail,name='polls_audit_detail')
]
