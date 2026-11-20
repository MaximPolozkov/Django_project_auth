from django.contrib.auth.decorators import login_required
from django.urls import path

from catalog.views import (
    ContactsView,
    HomeView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductUpdateView,
)

app_name = "catalog"

# Список товаров открыт всем; просмотр, создание, изменение и удаление
# товара — только для вошедших пользователей (login_required)
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path(
        "products/create/",
        login_required(ProductCreateView.as_view()),
        name="product_create",
    ),
    path(
        "products/<int:pk>/",
        login_required(ProductDetailView.as_view()),
        name="product_detail",
    ),
    path(
        "products/<int:pk>/update/",
        login_required(ProductUpdateView.as_view()),
        name="product_update",
    ),
    path(
        "products/<int:pk>/delete/",
        login_required(ProductDeleteView.as_view()),
        name="product_delete",
    ),
]
