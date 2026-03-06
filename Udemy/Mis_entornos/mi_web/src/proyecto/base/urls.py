from django.urls import path
from .views import ListaPendientes, DetalleTarea, CreateTarea, EditarTarea


urlpatterns = [path('', ListaPendientes.as_view(), name='tareas'),
               path('tarea/<int:pk>', DetalleTarea.as_view(), name='tarea'),
               path('crear-tarea/', CreateTarea.as_view(), name='crear-tarea'),
               path('editar-tarea/<int:pk>', EditarTarea.as_view(), name='editar-tarea')]



