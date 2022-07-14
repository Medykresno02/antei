"""AnteikuAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from webapi.views.user_page import dashboard, signup, userInfo, login, logOut, page_ip, ip_api, index, resetapikey, verified, dokumentasi, contacts
from webapi.views.api import testApi, saucenao, earthquake, sendF, tikvid, blackp, jodo, artinama, nohoki, lucky, mimpi, rmbg, cnbceh, cuaca, emo2img, p_rnhub, wtpd, twibon, otakudes, xnx, loli, ytaa, ytvv, ytss, twetS, twetP, twetT, twetTr, smule, htahta, webton, stline, igstalk, tikstalk, antra, suare, ttpp, attpp, visitor, b16enc, b32enc, b64enc, b85enc, b16dec, b32dec, b64dec, b85dec, hent, jav, burnf, lightn, sandw, estik, simih
handler404 = 'webapi.views.handler404'
handler500 = 'webapi.views.handler500'
urlpatterns = [
    path('', index),
    path('visitor', visitor),
    path('admin/', admin.site.urls),
    path('dashboard', dashboard),
    path('signup', signup),
    path('twibon', twibon),
    path('login', login),
    path('user', userInfo),
    path('ip', page_ip),
    path('api-ip', ip_api),
    path('logout', logOut),
    path('api-reset', resetapikey),
    path('contacts', contacts),
    path('dokumentasi/<str:path>', dokumentasi),
    path('favicon.ico', RedirectView.as_view(url='/static/assets/images/favicon.ico', permanent=True)),
    path('test-api', testApi),
    path('saucenao', saucenao),
    path('infogempa', earthquake),
    path('tiktok', tikvid),
    path('blackpink', blackp),
    path('jodoh', jodo),
    path('artinama', artinama),
    path('nohoki', nohoki),
    path('ceklucky', lucky),
    path('tafsirmimpi', mimpi),
    path('removebg', rmbg),
    path('cnbc', cnbceh),
    path('antaranews', antra),
    path('suara', suare),
    path('cuaca', cuaca),
    path('emoji2img', emo2img),
    path('phlogo', p_rnhub),
    path('wattpad', wtpd),
    path('otakudesu', otakudes),
    path('xnxx', xnx),
    path('loli', loli),
    path('yta', ytaa),
    path('ytv', ytvv),
    path('ytsearch', ytss),
    path('tweet_dl', twetS),
    path('tweet_stalk', twetP),
    path('trendingtweet', twetT),
    path('tweet_trending', twetTr),
    path('smule_dl', smule),
    path('htahta', htahta),
    path('webtoon', webton),
    path('stickerline', stline),
    path('igstalk', igstalk),
    path('tiktokstalk', tikstalk),
    path('ttp', ttpp),
    path('attp', attpp),
    path('base16enc', b16enc),
    path('base32enc', b32enc),
    path('base64enc', b64enc),
    path('base85enc', b85enc),
    path('base16dec', b16dec),
    path('base32dec', b32dec),
    path('base64dec', b64dec),
    path('base85dec', b85dec),
    path('nekopoi_hentai', hent),
    path('nekopoi_jav', jav),
    path('lightning', lightn),
    path('burning_fire', burnf),
    path('sand_writing', sandw),
    path('estetik', estik),
    path('simsimi', simih),
    path('result/<str:result>', sendF),
    path('verification/<str:token>', verified)
]
