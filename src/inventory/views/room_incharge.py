from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView, CreateView
from inventory.models import Category, Room, Brand, Item
from inventory.forms.room_incharge import CategoryForm, BrandForm

class CategoryListView(ListView):
    template_name = 'room_incharge/category_list.html'
    model = Category
    context_object_name = 'categories'

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_slug'] = self.kwargs['room_slug']
        return context


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'room_incharge/category_update.html'
    form_class = CategoryForm
    success_url = reverse_lazy('room_incharge:category_list')
    slug_field = 'slug'
    slug_url_kwarg = 'category_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:category_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.profile.org
        category.room = Room.objects.get(slug=self.kwargs['room_slug'])
        category.save()
        return redirect(self.get_success_url())


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'room_incharge/category_delete_confirm.html'
    slug_field = 'slug'
    slug_url_kwarg = 'category_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:category_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'room_incharge/category_create.html'
    form_class = CategoryForm
    success_url = reverse_lazy('room_incharge:category_list')

    def get_success_url(self):
        return reverse_lazy('room_incharge:category_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.profile.org
        category.room = Room.objects.get(slug=self.kwargs['room_slug'])
        category.save()
        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['room'] = Room.objects.get(slug=self.kwargs['room_slug'])
        return kwargs


class RoomDashboardView(TemplateView):
    template_name = 'room_incharge/room_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_slug = self.kwargs['room_slug']
        context['room'] = Room.objects.get(slug=room_slug)
        return context


class BrandListView(ListView):
    template_name = 'room_incharge/brand_list.html'
    model = Brand
    context_object_name = 'brands'

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_slug'] = self.kwargs['room_slug']
        return context


class BrandCreateView(CreateView):
    model = Brand
    template_name = 'room_incharge/brand_create.html'
    form_class = BrandForm
    success_url = reverse_lazy('room_incharge:brand_list')

    def get_success_url(self):
        return reverse_lazy('room_incharge:brand_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        brand = form.save(commit=False)
        brand.organisation = self.request.user.profile.org
        brand.room = Room.objects.get(slug=self.kwargs['room_slug'])
        brand.save()
        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['room'] = Room.objects.get(slug=self.kwargs['room_slug'])
        return kwargs


class BrandUpdateView(UpdateView):
    model = Brand
    template_name = 'room_incharge/brand_update.html'
    form_class = BrandForm
    success_url = reverse_lazy('room_incharge:brand_list')
    slug_field = 'slug'
    slug_url_kwarg = 'brand_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:brand_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def form_valid(self, form):
        brand = form.save(commit=False)
        brand.organisation = self.request.user.profile.org
        brand.room = Room.objects.get(slug=self.kwargs['room_slug'])
        brand.save()
        return redirect(self.get_success_url())


class BrandDeleteView(DeleteView):
    model = Brand
    template_name = 'room_incharge/brand_delete_confirm.html'
    slug_field = 'slug'
    slug_url_kwarg = 'brand_slug'

    def get_success_url(self):
        return reverse_lazy('room_incharge:brand_list', kwargs={'room_slug': self.kwargs['room_slug']})

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)


class ItemListView(ListView):
    template_name = 'room_incharge/item_list.html'
    model = Item
    context_object_name = 'items'

    def get_queryset(self):
        room_slug = self.kwargs['room_slug']
        return super().get_queryset().filter(room__slug=room_slug, organisation=self.request.user.profile.org)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_slug'] = self.kwargs['room_slug']
        return context
