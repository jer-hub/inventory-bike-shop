from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier, Product
from .forms import SupplierForm, ProductForm
from django.db.models import Q
from django.core.paginator import Paginator
import django_filters # type: ignore
from django.http import JsonResponse

class SupplierFilter(django_filters.FilterSet):
    class Meta:
        model = Supplier
        fields = ['supplier_name', 'contact_name', 'phone', 'email', 'address', 'city', 'state', 'postal_code', 'country']

class ProductFilter(django_filters.FilterSet):
    quantity_in_stock__gt = django_filters.NumberFilter(field_name='quantity_in_stock', lookup_expr='gt')
    quantity_in_stock__lt = django_filters.NumberFilter(field_name='quantity_in_stock', lookup_expr='lt')
    unit_price__gt = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gt')
    unit_price__lt = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ['product_name', 'category', 'supplier__supplier_name', 'quantity_in_stock', 'reorder_level', 'unit_price']

def create_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier_name = form.cleaned_data['supplier_name']
            if Supplier.objects.filter(supplier_name=supplier_name).exists():
                return JsonResponse({'success': False, 'message': 'A supplier with this name already exists.'})
            else:
                form.save()
                return JsonResponse({'success': True, 'message': 'Supplier added successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            if Product.objects.filter(product_name=product_name).exists():
                return JsonResponse({'success': False, 'message': 'A product with this name already exists.'})
            else:
                form.save()
                return JsonResponse({'success': True, 'message': 'Product added successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def view_main(request):
    return render(request, "inventory/home.html")

def supplier_list(request):
    sort_by = request.GET.get('sort', 'supplier_name')
    order = request.GET.get('order', 'asc')
    query = request.GET.get('q', '')
    if sort_by not in ['supplier_name', 'contact_name', 'phone', 'email', 'address', 'city', 'state', 'postal_code', 'country']:
        sort_by = 'supplier_name'
    if order == 'desc':
        sort_by = '-' + sort_by
    suppliers = Supplier.objects.all()
    if query:
        suppliers = suppliers.filter(
            Q(supplier_name__icontains=query) |
            Q(contact_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query) |
            Q(address__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query) |
            Q(postal_code__icontains=query) |
            Q(country__icontains=query)
        )
    _filter = SupplierFilter(request.GET, queryset=suppliers.order_by(sort_by))
    paginator = Paginator(_filter.qs, 5)  # Show 5 suppliers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    form = SupplierForm()
    edit_forms = {supplier.pk: SupplierForm(instance=supplier) for supplier in page_obj}
    return render(request, 'inventory/supplier_list.html', {'page_obj': page_obj, 'form': form, 'edit_forms': edit_forms, 'filter': _filter, 'sort_by': sort_by.lstrip('-'), 'order': order, 'query': query})

def product_list(request):
    sort_by = request.GET.get('sort', 'product_name')
    order = request.GET.get('order', 'asc')
    query = request.GET.get('q', '')
    if sort_by not in ['product_name', 'category', 'supplier__supplier_name', 'quantity_in_stock', 'reorder_level', 'unit_price', 'date_added']:
        sort_by = 'product_name'
    if order == 'desc':
        sort_by = '-' + sort_by
    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(category__icontains=query) |
            Q(supplier__supplier_name__icontains=query) |
            Q(quantity_in_stock__icontains=query) |
            Q(reorder_level__icontains=query) |
            Q(unit_price__icontains=query) |
            Q(date_added__icontains=query)
        )
    _filter = ProductFilter(request.GET, queryset=products.order_by(sort_by))
    paginator = Paginator(_filter.qs, 5)  # Show 5 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    form = ProductForm()
    suppliers = Supplier.objects.all()
    edit_forms = {product.pk: ProductForm(instance=product) for product in page_obj}
    return render(request, 'inventory/product_list.html', {'page_obj': page_obj, 'form': form, 'suppliers': suppliers, 'edit_forms': edit_forms, 'filter': _filter, 'sort_by': sort_by.lstrip('-'), 'order': order, 'query': query})

def update_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('inventory:supplier_list')
    else:
        form = SupplierForm(instance=supplier, initial={
            'supplier_name': supplier.supplier_name,
            'contact_name': supplier.contact_name,
            'phone': supplier.phone,
            'email': supplier.email,
            'address': supplier.address,
            'city': supplier.city,
            'state': supplier.state,
            'postal_code': supplier.postal_code,
            'country': supplier.country,
        })
    return render(request, 'inventory/supplier_form.html', {'form': form})

def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('inventory:product_list')
    else:
        form = ProductForm(instance=product, initial={
            'product_name': product.product_name,
            'category': product.category,
            'supplier': product.supplier,
            'quantity_in_stock': product.quantity_in_stock,
            'reorder_level': product.reorder_level,
            'unit_price': product.unit_price,
        })
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/product_form.html', {'form': form, 'suppliers': suppliers})

def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('inventory:supplier_list')
    return render(request, 'inventory/supplier_confirm_delete.html', {'supplier': supplier})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('inventory:product_list')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})
