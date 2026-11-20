from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from catalog.forms import ContactForm, ProductForm
from catalog.models import Product


class HomeView(ListView):
    """Главная страница: список всех товаров."""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(DetailView):
    """Страница одного товара. Если товара с таким pk нет, вернётся 404."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Товар «{self.object.name}» добавлен.")
        return response

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.object.pk])


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Товар «{self.object.name}» сохранён.")
        return response

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.object.pk])


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        name = self.object.name
        response = super().form_valid(form)
        messages.success(self.request, f"Товар «{name}» удалён.")
        return response


class ContactsView(TemplateView):
    """Страница контактов с формой обратной связи."""

    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("form", ContactForm())
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(
                request, f"Спасибо, {contact.name}! Ваше сообщение отправлено."
            )
            # Перенаправление защищает от повторной отправки при обновлении страницы
            return redirect("catalog:contacts")
        # Форма с ошибками показывается снова
        return self.render_to_response(self.get_context_data(form=form))
