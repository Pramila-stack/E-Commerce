from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,TemplateView,View,FormView,CreateView

from ministore.forms import CheckoutForm, SignupForm
from ministore.models import Product
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
    



class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = Product.objects.all().order_by("-created_at")

        query = self.request.GET.get("q")

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)|
                Q(category__name__icontains=query)
            )
        return queryset


class ProductDetailView(LoginRequiredMixin,DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(pk=self.kwargs['pk'])
    
class CartView(LoginRequiredMixin,TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = self.request.session.get("cart",{})
        products = Product.objects.filter(id__in=[int(pk) for pk in cart.keys()])

        cart_items = []
        total = 0

        for product in products:
            quantity = cart[str(product.id)]
            subtotal = product.price * quantity
            total += subtotal

            cart_items.append({
                "product":product,
                "quantity":quantity,
                "subtotal":subtotal
            })

        context['cart_items'] = cart_items
        context['total'] = total

        return context
    
class AddToCartView(LoginRequiredMixin,View):
    def get(self,request,pk):
        cart = self.request.session.get("cart",{})
        cart[str(pk)] = cart.get(str(pk),0) + 1
        request.session['cart'] = cart
        return redirect("cart")
    
class RemoveFromCartView(LoginRequiredMixin,View):
    def get(self,request,pk):
        cart = self.request.session.get("cart",{})

        if str(pk) in cart:
            del cart[str(pk)]

        request.session['cart'] = cart
        return redirect("cart")


class CheckoutView(LoginRequiredMixin, FormView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("success")

    def form_valid(self, form):
        request = self.request
        cart = request.session.get("cart", {})
        products = Product.objects.filter(id__in=[int(pk) for pk in cart.keys()])

        cart_items = []
        total = 0

        for product in products:
            quantity = cart[str(product.id)]
            subtotal = product.price * quantity
            total += subtotal

            cart_items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            })

        # ✅ Email context
        context = {
            "cart_items": cart_items,
            "total": total,
            "user": form.cleaned_data
        }

        subject = "Order Confirmation - Pramms Mini Store"
        from_email = "pramilatmg.np@gmail.com"
        to_email = [form.cleaned_data["email"]]

        html_content = render_to_string("order_email.html", context)

        email = EmailMultiAlternatives(subject, "", from_email, to_email)
        email.attach_alternative(html_content, "text/html")

        # ✅ Attach images (IMPORTANT PART)
        for item in cart_items:
            product = item["product"]
            if product.image:
                try:
                    with open(product.image.path, 'rb') as f:
                        img = MIMEImage(f.read())
                        img.add_header('Content-ID', f'<image_{product.id}>')
                        img.add_header('Content-Disposition', 'inline', filename=product.name)
                        email.attach(img)
                except Exception as e:
                    print("Image attach error:", e)

        email.send()

        # ✅ Clear cart
        request.session["cart"] = {}

        return super().form_valid(form)
    
class CheckoutSuccessView(LoginRequiredMixin,TemplateView):
    template_name = "success_page.html"


class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("login")


class WishlistView(LoginRequiredMixin, TemplateView):
    template_name = "wishlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        wishlist = self.request.session.get("wishlist", [])
        products = Product.objects.filter(id__in=wishlist)

        context["products"] = products
        return context
    
class AddToWishlistView(LoginRequiredMixin, View):
    def get(self, request, pk):
        wishlist = request.session.get("wishlist", [])

        if pk not in wishlist:
            wishlist.append(pk)

        request.session["wishlist"] = wishlist
        return redirect("wishlist")
    
class RemoveFromWishlistView(LoginRequiredMixin, View):
    def get(self, request, pk):
        wishlist = request.session.get("wishlist", [])

        if pk in wishlist:
            wishlist.remove(pk)

        request.session["wishlist"] = wishlist
        return redirect("wishlist")