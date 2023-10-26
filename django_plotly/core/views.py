from django.shortcuts import render
import plotly.express as px
import plotly.graph_objects as go
import folium
from core.models import FINEDUST, CITY_FINEDUST, NUM_NEWS, STATION_LOCATION, STATION_LOCATION2,NURAK
from core.forms import DateForm
from folium.plugins import FastMarkerCluster,MarkerCluster
from django.conf import settings
import json
from bs4 import BeautifulSoup
import requests
from django.http import HttpResponse
# Create your views here.

def chart(request):
    
    ## 미세먼지 농도 전국인구 가중평균 선 그래프 ## 
    finedust=FINEDUST.objects.all()
    fig = px.line(
        x= [f.date for f in finedust],
        y= [f.weighted_average for f in finedust],
        title="전국인구 가중평균 미세먼지 농도 (2015~2022)",
        labels={"x": "연도", "y": "미세먼지 농도(전국 가중평균)"}
    )
    
    fig.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5
    }, width=1100)
    
    chart = fig.to_html()
    
    
    ## 도시별 미세먼지 농도(2015~2022) ## 
    year = CITY_FINEDUST.objects.values_list('date', flat=True)
    city = CITY_FINEDUST.objects.values_list('seoul', flat=True)
    search_city = request.GET.get('search_city')
    
    if search_city:
        city = CITY_FINEDUST.objects.values_list(f"{search_city}", flat=True)
    
    city_x = year
    city_y = city
    
    fig2 = px.bar(x=city_x,
                 y=city_y,
                 labels={"x": "연도", "y": "미세먼지 농도"}
                 )
    
    city_dict = {"seoul": "서울",
                 "busan": "부산",
                 "daegu": "대구",
                 "incheon": "인천",
                 "gwangju": "광주",
                 "daejeon": "대전",
                 "ulsan": "울산",
                 "sejong": "세종",
                 "gyeonggi": "경기",
                 "gangwon": "강원",
                 "chungbuk": "충북",
                 "chungnam": "충남",
                 "jeonbuk": "전북",
                 "jeonnam": "전남",
                 "gyeongbuk": "경북",
                 "gyeongnam": "경남",
                 "jeju": "제주"
                }
    
    if search_city is None:
        fig2.update_layout(title_text=f"도시별 미세먼지 농도 (서울) (2015~2022)")
    else:   
        fig2.update_layout(title_text=f"도시별 미세먼지 농도 ({city_dict[search_city]}) (2015~2022)")
    
    fig2.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5},
         width=1100)
    
    chart2 = fig2.to_html()
    
    
    
    
    ## 연도별 미세먼지 관련 뉴스 개수 ##
    
    num_news = NUM_NEWS.objects.all()
    
    fig3 = go.Figure(data=[go.Table(header=dict(values=['연도', "뉴스기사개수"]),
                                    cells=dict(values=[[news.date for news in num_news], [news.num_news for news in num_news]])
                                    )])
    
  
    
    fig3.update_layout(title_text="연도별 미세먼지 관련 뉴스기사 개수(2015~2023)", 
                       title={
                           'font_size': 22,
                           'xanchor': 'center',
                           'x': 0.5},
                       width=1100
                       )
    
    chart3 = fig3.to_html()
    
    ## 지도에 표시하기 ##
    
    stations = STATION_LOCATION.objects.all()
    
    # create a Folium map 
    m = folium.Map(location=[36, 127], zoom_start=7, width=1000, height=600)
    
    with open(f"{settings.BASE_DIR / 'data' / 'skorea-provinces-2018-geo.json'}", "r", encoding="cp949") as gfile:
        jsondata = json.load(gfile)
        folium.GeoJson(jsondata, name="대한민국 경계").add_to(m)
    
    # add a marker to the map for each station 
    for station in stations:
        coordinates = (station.latitude, station.longitude)
        folium.Marker(coordinates, popup=f"<b>{station.station_name}</b>", icon=folium.Icon(color='red')).add_to(m)
    # latitudes = [station.latitude for station in  stations]
    # longitudes = [station.longitude for station in  stations]
    
    # FastMarkerCluster(data=list(zip(latitudes, longitudes)), name=[station.station_name for station in stations]).add_to(m)
    
    
    ## 미세먼지 구성성분 이미지 파일 가져오기 ##
    url = "https://www.air.go.kr/contents/view.do?contentsId=9&menuId=41"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tag = soup.find(name='img')
    image_src = image_tag.get('src')
    image_url = "https://www.air.go.kr" + image_src
    
    context = {'chart': chart,
               'form': DateForm(),
               'chart2': chart2,
               'chart3':chart3,
               'map': m._repr_html_(),
               'img_src': image_url}
    
    return render(request, 'core/chart.html', context=context)


def use_template(request):
    
    #### 1번 차트 ####
    finedust=FINEDUST.objects.all()
    fig = px.line(
        x= [f.date for f in finedust],
        y= [f.weighted_average for f in finedust],
        labels={"x": "연도", "y": "가중평균 미세먼지 농도(㎍/㎡)"}
    )
    
    fig.update_layout(width=1100)
    
    fig.update_layout(title_text=f"전국인구 가중평균 미세먼지 농도 (2015~2022)")
    
    
    fig.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5},
         width=1100)
    
    chart = fig.to_html()
    
    
    #######################################################
    
    
    ## 도시별 미세먼지 농도(2015~2022) ## 
    year = CITY_FINEDUST.objects.values_list('date', flat=True)
    city = CITY_FINEDUST.objects.values_list('seoul', flat=True)
    # jsonObject = json.loads(request.body)
    # print(jsonObject.get('search_city'))
    
    search_city = request.GET.get('search_city')
    # search_city = jsonObject.get('search_city')
    print(f"here: {search_city}")
    
    if search_city:
        city = CITY_FINEDUST.objects.values_list(f"{search_city}", flat=True)
    
    city_x = year
    city_y = city
    
    fig2 = px.bar(x=city_x,
                 y=city_y,
                 labels={"x": "연도", "y": "미세먼지 농도(㎍/㎡)"}
                 )
    
    city_dict = {"seoul": "서울",
                 "busan": "부산",
                 "daegu": "대구",
                 "incheon": "인천",
                 "gwangju": "광주",
                 "daejeon": "대전",
                 "ulsan": "울산",
                 "sejong": "세종",
                 "gyeonggi": "경기",
                 "gangwon": "강원",
                 "chungbuk": "충북",
                 "chungnam": "충남",
                 "jeonbuk": "전북",
                 "jeonnam": "전남",
                 "gyeongbuk": "경북",
                 "gyeongnam": "경남",
                 "jeju": "제주"
                }
    
    if search_city is None:
        fig2.update_layout(title_text=f"도시별 미세먼지 농도 (서울) (2015~2022)")
    else:   
        fig2.update_layout(title_text=f"도시별 미세먼지 농도 ({city_dict[search_city]}) (2015~2022)")
    
    fig2.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5},
         width=1100)
    
    chart2 = fig2.to_html()
    
    ####### 미세먼지 성분 파이 차트 #######
    
    
    labels = ['황산염, 질염 등', '탄소류와 검댕', '광물', '기타']
    values = [58.3, 16.8, 6.3, 18.6]
    
    pie_chart = go.Figure(data=[go.Pie(labels=labels, values=values)])
    
    pie_chart = pie_chart.to_html()
    #####################################
    
     ## 지도에 표시하기 국가 배경, 도시대기###
    
    stations = STATION_LOCATION.objects.all()
    
    # create a Folium map 
    m = folium.Map(location=[36, 127], zoom_start=6, zoom_control=False, width=800, height=500)
    
    with open(f"{settings.BASE_DIR / 'data' / 'skorea-provinces-2018-geo.json'}", "r", encoding="cp949") as gfile:
        jsondata = json.load(gfile)
        folium.GeoJson(jsondata, name="대한민국 경계").add_to(m)
    
    # add a marker to the map for each station 
    for station in stations:
        coordinates = (station.latitude, station.longitude)
        folium.Marker(coordinates, popup=station.station_name, icon=folium.Icon(color='red')).add_to(m)
    # latitudes = [station.latitude for station in  stations]
    # longitudes = [station.longitude for station in  stations]
    
    # FastMarkerCluster(data=list(zip(latitudes, longitudes)), name=[station.station_name for station in stations]).add_to(m)
    
    stations_city = STATION_LOCATION2.objects.all()
    m2 = folium.Map(location=[36, 127], zoom_start=6, zoom_control=False,  width=800, height=500)
    
    with open(f"{settings.BASE_DIR / 'data' / 'skorea-provinces-2018-geo.json'}", "r", encoding="cp949") as gfile:
        jsondata = json.load(gfile)
        folium.GeoJson(jsondata, name="대한민국 경계").add_to(m2)
        
  
    
    marker_cluster = MarkerCluster().add_to(m2)

    for station in stations_city:
        lat, lon = station.latitude, station.longitude
        label = station.station_name

        marker = folium.Marker([lat,lon], popup=label)
        marker.add_to(marker_cluster)
    
    # 누락 장소 테이블 
    
    
    nuraks = NURAK.objects.all()
    
    nurak_table = go.Figure(data=[go.Table(
        columnorder=[1, 2],
        columnwidth=[300, 700],
        header=dict(values=['측정소', "위치"],
                    align='left'),
        cells=dict(values=[[nurak.name for nurak in nuraks], [nurak.addr for nurak in nuraks]],
                   align='left'))
    ])
    
    nurak_table.update_layout(
                       margin=dict.fromkeys(list('ltrb'), 0)
                       )
    
    nurak_table = nurak_table.to_html()
    
    
    ######################################################
    # 미세먼지 관련 뉴스 연도별 추이(2015~2022)
    
    ### 테이블 ###
    num_news = NUM_NEWS.objects.all()
    
    num_news_table = go.Figure(data=[go.Table(
        columnorder=[1, 2],
        columnwidth=[300, 700],
        header=dict(values=['연도별', "뉴스기사 개수"],
                    align='left'),
                    cells=dict(values=[[news.date for news in num_news], [news.num_news for news in num_news]], align='left')
                                    )])
    
  
    
    num_news_table.update_layout(
                       width=800,
                       margin=dict.fromkeys(list('ltrb'), 0)
                       )
    
    num_news_table = num_news_table.to_html()
    
    ##### 선 그래프 #####
    
    num_news_line = px.line(
        x=[news.date for news in num_news],
        y=[news.num_news for news in num_news],
        labels={"x": "연도", "y":"뉴스기사 개수"}
    )
    
    num_news_line.update_layout(
                        width=800,
                        margin=dict.fromkeys(list('ltrb'), 0)
    )
    
    num_news_line = num_news_line.to_html()
    
    
    
    
    context = {'chart': chart,
               'chart2': chart2,
               'map1': m._repr_html_(),
               'map2': m2._repr_html_(),
               'nurak': nurak_table,
               'pie_chart': pie_chart,
               'num_news_table': num_news_table,
               'num_news_line': num_news_line
               }
    
    return render(request, "core/index.html", context=context)




def update_chart(request):
    
    year = CITY_FINEDUST.objects.values_list('date', flat=True)
    city = CITY_FINEDUST.objects.values_list('seoul', flat=True)
    search_city = request.GET.get('search_city')
    print(search_city)
    if search_city:
        city = CITY_FINEDUST.objects.values_list(f"{search_city}", flat=True)
    
    city_x = year
    city_y = city
    
    fig2 = px.bar(x=city_x,
                 y=city_y,
                 labels={"x": "연도", "y": "미세먼지 농도(㎍/㎡)"}
                 )
    
    city_dict = {"seoul": "서울",
                 "busan": "부산",
                 "daegu": "대구",
                 "incheon": "인천",
                 "gwangju": "광주",
                 "daejeon": "대전",
                 "ulsan": "울산",
                 "sejong": "세종",
                 "gyeonggi": "경기",
                 "gangwon": "강원",
                 "chungbuk": "충북",
                 "chungnam": "충남",
                 "jeonbuk": "전북",
                 "jeonnam": "전남",
                 "gyeongbuk": "경북",
                 "gyeongnam": "경남",
                 "jeju": "제주"
                }
    
    if search_city is None:
        fig2.update_layout(title_text=f"도시별 미세먼지 농도 (서울) (2015~2022)")
    else:
        print('hello')
        fig2.update_layout(title_text=f"도시별 미세먼지 농도 ({city_dict[search_city]}) (2015~2022)")
    
    fig2.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5},
         width=1100)
    
    chart3 = fig2.to_html()
    
    
    return HttpResponse(chart3)
