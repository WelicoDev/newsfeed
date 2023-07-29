from django.urls import path
from .views import LandingPage , DetailPage , Home , ContactPage , Views ,\
    ErrorPage , Uzbekistan , Jahon , Texnologiya , Iqtisodiyot , Sport , \
    NewsCreate , NewsDelete , NewsUpdate , AdminPage , SearchResult

urlpatterns = [
    path('' , Home.as_view() , name = 'home'),
    path('contact/' , ContactPage.as_view() , name ='contact'),
    path('news/<slug:news>/',Views , name = 'views'),
    path('search/' ,SearchResult.as_view() , name='search'),
    path('create/',NewsCreate.as_view() , name='create'),
    path('news/<slug>/update/',NewsUpdate.as_view() , name='update'),
    path('news/<slug>/delete/',NewsDelete.as_view() , name='delete'),
    path('404/' , ErrorPage , name = "error_404"),
    path('post/' , LandingPage , name = 'landing_page'),
    path('post/<int:pk>/' , DetailPage , name ='detail_page'),
    path('uzbekistan/' , Uzbekistan.as_view() , name = 'uzbekistan'),
    path('jahon/' , Jahon.as_view() , name = 'jahon'),
    path('sport/' , Sport.as_view() , name = 'sport'),
    path('texnologiya/' , Texnologiya.as_view() , name = 'texnologiya'),
    path('iqtisodiyot/' , Iqtisodiyot.as_view() , name = 'iqtisodiyot'),
    path('admin-page/' , AdminPage , name='admin_page'),
]