from django.urls import path
from materials.apps import MaterialsConfig
from materials.views import MaterialsCreateView, MaterialsListView, MaterialsDetailView, MaterialsUpdateView, \
    MaterialsDeleteView

app_name = MaterialsConfig.name

urlpatterns = [
    path('', MaterialsListView.as_view(), name='list_materials'),
    path('create/', MaterialsCreateView.as_view(), name='create_materials'),
    path('view/<int:pk>/', MaterialsDetailView.as_view(), name='view_materials'),
    path('update/<int:pk>/', MaterialsUpdateView.as_view(), name='update_materials'),
    path('delete/<int:pk>/', MaterialsDeleteView.as_view(), name='delete_material'),

]

