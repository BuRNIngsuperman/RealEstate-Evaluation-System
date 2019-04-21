from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import pandas as pd
from sklearn.externals import joblib
import json
from urllib.request import urlopen, quote
import csv
import numpy as np
import os
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import guapai,lianjiainf
from .reptile import Reptile


# Create your views here.

def index(request):
    """应用的主页"""
    return render(request,'myapplication/index.html')

def shoreswitch(shore):
    likeswitch={
        '东': 6,
        '东北': 5,
        '东南': 10,
        '东西': 7,
        '北': 2,
        '南': 4,
        '南北': 3,
        '暂无': 1,
        '西': 9,
        '西北': 8,
        '西南': 11
    }
    shoremap=likeswitch.get(shore,'Unkown')
    return shoremap

def house_typeswitch(house_type):
    likeswitch={
        '公寓': 4,
        '别墅洋房': 2,
        '办公楼': 1,
        '商铺': 3,
        '里弄房': 5
    }
    house_typemap=likeswitch.get(house_type,'Unkown')
    return house_typemap

def fitmentswitch(fitment):
    likeswitch={
        '中装': 4,
        '暂无': 5,
        '毛坯': 1,
        '简装': 2,
        '精装': 3,
        '豪华装': 6,
        '豪装': 7
    }
    fitmentmap=likeswitch.get(fitment,'Unkown')
    return fitmentmap

def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = 'FadLj4MSbxS953RU5Lsrh8WaI8afHGuv'
    add = quote(address) #由于本文城市变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode() #将其他编码的字符串解码成unicode
    temp = json.loads(res) #对json数据进行解析
    return temp

@login_required
def textpost(request):
    shore=request.POST['shore']
    time=request.POST['time1']
    floor=request.POST['floor']
    acreage=request.POST['acreage']
    house_type=request.POST['house_type']
    fitment=request.POST['fitment']
    address=request.POST['address']

    shoremaped=shoreswitch(shore)
    house_typemaped=house_typeswitch(house_type)
    fitmentmaped=fitmentswitch(fitment)

    temp=getlnglat(address)
    if temp['status']==1:
        return HttpResponseRedirect(reverse('myapplication:index'))
    loc_x=temp['result']['location']['lng']
    loc_y=temp['result']['location']['lat']
    testdata=pd.DataFrame({'acreage':[acreage],
                           'floor':[floor],
                           'shore':[shoremaped],
                           'house_type':[house_typemaped],
                           'fitment':[fitmentmaped],
                           'time':[time],
                           'loc_x':[loc_x],
                           'loc_y':[loc_y],
                           })
    colx = ['acreage', 'floor', 'shore', 'house_type', 'fitment', 'time', 'loc_x', 'loc_y']
    testdata = testdata.ix[:, colx]
    RF = joblib.load('test.model')
    result=RF.predict(testdata)
    # add=np.array([30000])
    # result=result-add
    test=result.tolist()[0]
    test=float('%.2f' % test)
    context={'b':test}
    return render(request,'myapplication/search.html',context)

@login_required
def modeltrain(request):
    return render(request,'myapplication/modeltrain.html')

@login_required
def display1(request):
    signlist=guapai.objects.all()
    paginator=Paginator(signlist,10)
    page=request.GET.get('page')
    try:
        contacts=paginator.page(page)
    except PageNotAnInteger:
        contacts=paginator.page(1)
    except EmptyPage:
        contacts=paginator.page(paginator)
    return render(request,'myapplication/display1.html',{'hour':contacts})

@login_required
def display2(request):
    signlist=lianjiainf.objects.all()
    paginator=Paginator(signlist,10)
    page=request.GET.get('page')
    try:
        contacts=paginator.page(page)
    except PageNotAnInteger:
        contacts=paginator.page(1)
    except EmptyPage:
        contacts=paginator.page(paginator)
    return render(request,'myapplication/display2.html',{'hour':contacts})

@login_required
def search(request):
    return render(request,'myapplication/search.html')

@login_required
def display1search(request):
    getarea=request.GET.get('localarea')
    signlist=guapai.objects.filter(address_area=getarea)
    paginator=Paginator(signlist,10)
    page=request.GET.get('page')
    try:
        contacts=paginator.page(page)
    except PageNotAnInteger:
        contacts=paginator.page(1)
    except EmptyPage:
        contacts=paginator.page(paginator)
    return render(request,'myapplication/display1search.html',{'hour':contacts,'search':getarea})

@login_required
def display2search(request):
    getarea=request.GET.get('localarea')
    signlist=lianjiainf.objects.filter(area=getarea)
    paginator=Paginator(signlist,10)
    page=request.GET.get('page')
    try:
        contacts=paginator.page(page)
    except PageNotAnInteger:
        contacts=paginator.page(1)
    except EmptyPage:
        contacts=paginator.page(paginator)
    return render(request,'myapplication/display2search.html',{'hour':contacts,
                                                               'search':getarea})



# def show_progress(request):
#     return JsonResponse(num_progress, safe=False)

@login_required
def progress(request):
    if request.method=='post':
        myfile=request.FILES.get("inputfile").name,
    os.system("python modeltrain.py")
    return render(request,'myapplication/progress.html',)

@login_required
def reptile(request):
    return render(request,'myapplication/reptile.html')

@login_required
def reptileshow(request):
    pagenum=request.POST['pagenum']
    num=int(pagenum)+1
    re_data=Reptile(num)
    re_data.to_csv("D:\\djangotest\\挂牌.csv", encoding="utf-8")
    data=re_data.values.tolist()
    number=len(data)
    return render(request,'myapplication/reptileshow.html',{'data':data,'number':number})

@login_required
def datadislay1(request):
    return render(request,'myapplication/datadisplay1.html')

@login_required
def datadisplay2(request):
    return render(request,'myapplication/datadisplay2.html')

