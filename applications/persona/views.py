from django.db.models import query
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import(
    TemplateView, 
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
) 
from .models import Empleado, Habilidades
#importacion de forms
from .forms import EmpleadoForm
# Create your views here.


class InicioView(TemplateView):
    """ VISTA QUE CARGA LA PAGINA DE INICIO"""
    template_name = "inicio.html"


class ListAllEmpleados(ListView):
    template_name = 'persona/list_all.html'
    paginate_by = 4
    ordering = 'first_name'
    context_object_name = 'empleados'

    def get_queryset(self):
        print('****************')
        plabra_clave = self.request.GET.get("kword", '')
        lista = Empleado.objects.filter(
            full_name__icontains=plabra_clave
        )
        print('Lista resultado:', lista)
        return lista

class ListaEmpleadosAdmin(ListView):
    template_name = 'persona/lista_empleados.html'
    paginate_by = 10
    ordering = 'first_name'
    context_object_name = 'empleados'
    model = Empleado

class ListByAreaEmpleados(ListView):
    "lista empleados de una area"
    template_name = 'persona/list_by_area.html'
    context_object_name = 'empleados'
    
    def get_queryset(self):
        area = self.kwargs['shorname']
        lista = Empleado.objects.filter(
            departamento__shor_name= area
        )

        return lista

class ListEmpleadosByKword(ListView):
    " Lista empleado por palabra clave"
    template_name = 'persona/by_kword.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        print('****************')
        plabra_clave = self.request.GET.get("kword", '')
        lista = Empleado.objects.filter(
            first_name = plabra_clave
        )
        print('Lista resultado:', lista)
        return lista

class ListHabilidadesEmpleado(ListView):
    template_name = 'persona/habilidades.html'
    context_object_name = 'habilidades'

    def get_queryset(self):
        empleado = Empleado.objects.get(id=8)
        print(empleado.habilidades.all())
        return empleado.habilidades.all()

class ListHabilidadesEmpleadoBykword(ListView):
    template_name = 'persona/habilidades_by_kword.html'
    context_object_name = 'habilidades'
    
    def get_queryset(self):
        plabra_clave = self.request.GET.get("kword", '')
        lista = Empleado.objects.filter(
            first_name = plabra_clave
        )
        empleado = Empleado.objects.get(id=pk)
        print(lista)
        return []


class EmpleadoDetailView(DetailView):
    model = Empleado
    template_name = "persona/detail_empleado.html"

    def get_context_data(self, **kwargs):
        context = super(EmpleadoDetailView, self).get_context_data(**kwargs) 
        context['titulo'] = 'Empleado del mes'    
        return context
        

class SuccessView(TemplateView):
    template_name = "persona/success.html"


class EmpleadoCreateView(CreateView):
    template_name = "persona/add.html"
    model = Empleado
    form_class = EmpleadoForm
    success_url = reverse_lazy('persona_app:empleados_admin')

    def form_valid(self, form):
        empleado = form.save(commit=False)
        empleado.full_name = empleado.first_name + ' ' + empleado.last_name
        empleado.save()
        return super(EmpleadoCreateView, self).form_valid(form)
        

class EmpleadoUpdateView(UpdateView):
    template_name = "persona/update.html"
    model = Empleado
    fields =[
        'first_name',
        'last_name',
        'job',
        'departamento',
        'habilidades',
    ]
    success_url = reverse_lazy('persona_app:empleados_admin')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print('**************Metodo post*****************')
        print('======================================')
        print(request.POST)
        print(request.POST['last_name'])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print('**************Metodo form valid*****************')
        print('******************************************')
        return super(EmpleadoUpdateView, self).form_valid(form)


class EmpleadoDeleteView(DeleteView):
    template_name = "persona/delete.html"
    model = Empleado
    success_url = reverse_lazy('persona_app:empleados_admin')
