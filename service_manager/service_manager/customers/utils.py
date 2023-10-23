from service_manager.main.models import ServiceOrderHeader


def get_assets_currently_in_service(customer):
    customer_open_service_orders = ServiceOrderHeader.objects.filter(customer_id=customer.id, is_completed=False)
    assets_being_serviced = [x.customer_asset for x in customer_open_service_orders.all()]

    return assets_being_serviced
