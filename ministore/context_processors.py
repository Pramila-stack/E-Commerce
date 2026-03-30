# ministore/context_processors.py
def cart_item_count(request):
    cart = request.session.get("cart", {})  # get the cart from session
    total_quantity = sum(cart.values())     # sum all quantities
    return {"cart_count": total_quantity}   # send this to templates