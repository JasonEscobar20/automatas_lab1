from django.urls import path
from core.views import index_view, read_txt, result_view


app_name = 'core'

urlpatterns = [
    path('', index_view),
    path('result/',result_view, name='read_result'),
    # path('result/afn', read_afn, name='read_afn')
]
