from django import template

register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False


@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0


@register.filter(name='price_total')
def price_total(product, cart):
    return product.Tickets_Price * cart_quantity(product, cart)


@register.filter(name='total_cart_price')
def total_cart_price(products, cart):
    sum = 0
    for p in products:
        sum += float(price_total(p, cart))

    return sum


@register.filter(name='delivery_charge')
def delivery_charge(products, cart):
    sum = float(total_cart_price(products, cart)) * float(0.13)
    return sum


@register.filter(name='total_bill')
def total_bill(products, cart):
    sum = float(total_cart_price(products, cart)) + float(delivery_charge(products, cart))
    return sum