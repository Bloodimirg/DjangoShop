from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from materials.forms import MaterialsForm
from materials.models import Materials


class MaterialsCreateView(CreateView):
    """Контроллер для создания материалов"""
    model = Materials
    form_class = MaterialsForm
    success_url = reverse_lazy('materials:list_materials')

    def form_valid(self, form):

        new_mat = form.save(commit=False)
        new_mat.slug = slugify(new_mat.title)
        new_mat.save()

        return super().form_valid(form)


class MaterialsListView(ListView):
    """Контроллер для просмотра списка материалов"""
    model = Materials

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class MaterialsDetailView(DetailView):
    """Контроллер для просмотра одного материала, добавлен счётчик просмотров"""
    model = Materials

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class MaterialsUpdateView(UpdateView):
    """Контроллер для изменения материала"""
    model = Materials
    form_class = MaterialsForm

    def get_success_url(self, *args, **kwargs):
        return reverse('materials:view_materials', args=[self.kwargs.get('pk')])


class MaterialsDeleteView(DeleteView):
    """Контроллер для удаления"""
    model = Materials
    success_url = reverse_lazy('materials:list_materials')
