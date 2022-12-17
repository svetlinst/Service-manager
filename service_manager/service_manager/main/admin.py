from django.contrib import admin
from django.db.models import Count, Q, Sum
from django.urls import reverse_lazy
from django.utils.html import format_html

from service_manager.customers.models import CustomerAsset
from service_manager.main.models import ServiceOrderHeader, ServiceOrderDetail


@admin.register(ServiceOrderHeader)
class ServiceOrderHeaderAdmin(admin.ModelAdmin):
    """
    Admin features applied:
     - list display
     - list filter
     - search fields
     - custom ordering
     - custom calculated field
     - custom link field
    """
    list_display = ['customer', 'customer_asset', 'department', 'is_serviced', 'active', 'is_completed', 'total_amount_due',
                    'get_customer_asset_number_of_times_serviced', 'get_customer_asset_lifetime_revenue',
                    'open_service_order_details_page', ]
    list_filter = ['created_on', 'accepted_by', 'active', 'is_serviced', 'is_completed', ]
    search_fields = ['customer__name__icontains', ]
    ordering = ['-created_on',]

    def get_customer_asset_number_of_times_serviced(self, obj):
        """
        Calculate the number of times an order has been completed (serviced and finalized) for the given customer asset.
        Exclude soft deleted records (active must == True).
        """
        customer_asset = CustomerAsset.objects.get(pk=obj.customer_asset.pk)
        service_orders = ServiceOrderHeader.objects.filter(
            Q(customer_asset_id=customer_asset)
            & Q(is_completed=True)
            & Q(active=True)).aggregate(Count('pk'))

        if service_orders:
            return service_orders['pk__count']
        else:
            return 0

    def get_customer_asset_lifetime_revenue(self, obj):
        """
        Calculate total lifetime revenue for a given Customer asset.
        The Service order header must be completed (Serviced and Finalized), both Service order header and detail
        should be active (not soft deleted).
        """
        customer_asset = CustomerAsset.objects.get(pk=obj.customer_asset.pk)
        service_orders = ServiceOrderHeader.objects.prefetch_related('serviceorderdetail_set').filter(
            Q(customer_asset_id=customer_asset)
            & Q(is_completed=True)
            & Q(active=True)
            & Q(serviceorderdetail__active=True)
        )

        total_amount_due = sum(float(x.total_amount_due) for x in service_orders)
        return total_amount_due

    def open_service_order_details_page(self, obj):
        """
        Create a link to the Service order header details page to open in new browser window.
        """
        order_path = reverse_lazy('detail_service_order', kwargs={'pk': obj.id})
        return format_html('<a href="{}" target="blank">Details</a>', order_path)

    get_customer_asset_lifetime_revenue.short_description = 'Asset Lifetime Revenue'
    get_customer_asset_number_of_times_serviced.short_description = 'Times serviced'
    open_service_order_details_page.short_description = 'Order Details'


@admin.register(ServiceOrderDetail)
class ServiceOrderDetailAdmin(admin.ModelAdmin):
    list_display = ['service_order', 'material', 'quantity', 'discount']
