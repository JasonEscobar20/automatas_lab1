from django.urls import path
from core.views import index_view, read_txt


app_name = 'core'

urlpatterns = [
    path('', index_view),
    path('result/',read_txt, name='read_result')
]
