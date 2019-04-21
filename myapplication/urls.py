from django.urls import path,re_path

from . import  views


urlpatterns= [
    #home
    path('index/',views.index,name='index'),

    path('search/',views.search,name='search'),

    path('index/test/',views.textpost,name='textpost'),

    path('modeltrain/',views.modeltrain,name='modeltrain'),

    path('display1/',views.display1,name='display1'),

    path('display1search/',views.display1search,name='display1search'),

    path('display2/',views.display2,name='display2'),

    path('display2search/',views.display2search,name='display2search'),

    path('progress/',views.progress,name='progress'),

    path('reptile/',views.reptile,name='reptile'),

    path('reptileshow/',views.reptileshow,name='reptileshow'),

    path('datadisplay1/',views.datadislay1,name='datadisplay1'),

    path('datadisplay2/',views.datadisplay2,name='datadisplay2')
]
app_name = 'myapplication'