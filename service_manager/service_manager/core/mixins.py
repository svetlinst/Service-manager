class PricingMixin:
    @property
    def discount_percentage(self):
        pct = 0
        if self.discount > 0:
            pct = self.discount / 100
        return pct

    @property
    def discounted_price(self):
        price = self.material.price
        if self.discount_percentage > 0:
            price = price * (1 - self.discount_percentage)
        return price

    @property
    def discounted_price_no_vat(self):
        price = self.material.price_no_vat
        if self.discount_percentage > 0:
            price = price * (1 - self.discount_percentage)
        return price

    @property
    def total_amount(self):
        return self.discounted_price * self.quantity

    @property
    def total_amount_no_vat(self):
        return self.discounted_price_no_vat * self.quantity


class MaterialFilteringMixin:
    def get_initial(self):
        category = self.request.GET.get('category' or None)
        if category:
            self.initial.update({
                'category': category,
            })
        elif 'category' in self.initial:
            self.initial.pop('category')

        search = self.request.GET.get('search' or None)
        if search:
            self.initial.update(
                {
                    'search': search,
                }
            )
        elif 'search' in self.initial:
            self.initial.pop('search')

        return super().get_initial()