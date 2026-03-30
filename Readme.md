<!-- Your cart views do not work directly with database models.
They work with sessions instead. -->


class AddToCartView(View):
    def get(self, request, pk):
        cart = request.session.get("cart", {})
        cart[str(pk)] = cart.get(str(pk), 0) + 1
        request.session["cart"] = cart
        return redirect("cart")

<!-- def get(self, request, pk): -->

This method runs when the user makes a GET request.
Example URL:/add/5/

<!-- cart = request.session.get("cart", {}) -->

This retrieves the cart stored in the user's session.
Session example:
{
    "cart": {
        "2": 1,
        "5": 2
    }
}
<!-- .get("cart", {}) means: -->
If "cart" exists → return it
If it doesn't exist → return {} (empty dictionary)
Example result:cart = {"2":1, "5":2}


<!-- Add Product to Cart
cart[str(pk)] = cart.get(str(pk), 0) + 1 -->

This is the most important line.
Let’s break it down.

<!-- Step 1: Convert product id to string
str(pk) -->

If:pk = 5 ,Then:"5"  #the pk comes from url in integer form so better convert into string.

<!-- Step 2: Check current quantity -->
cart.get(str(pk), 0)

Meaning:
Look for product "5" in cart
If not found → return 0
<!-- Example: -->
cart = {"2":1}
Then:
cart.get("5",0) = 0

<!-- Step 3: Increase quantity
cart.get(str(pk), 0) + 1 -->
Example:0 + 1 = 1

<!-- Save it in cart
cart[str(pk)] = 1 -->

Now cart becomes:{"2":1, "5":1}

If product already existed:{"5":2}

Then:2 + 1 = 3
Cart becomes:{"5":3}
So this line means:Increase the quantity of the product in the cart by 1.

<!-- Save Cart Back to Session
request.session["cart"] = cart -->

This updates the session.
Now the user's session stores the new cart.
<!-- Example stored session: -->
{
 "cart": {
   "2":1,
   "5":3
 }
}

So the cart persists across pages.

<!-- 8. Redirect to Cart Page
return redirect("cart") -->

After adding the product, the user is redirected to the cart page.
Equivalent URL:
/cart/

<!-- So the flow becomes: -->

User clicks "Add to Cart"
        ↓
AddToCartView runs
        ↓
Session cart updated
        ↓
User redirected to cart page
Complete Flow Example

User clicks:/add/3/

View runs:
1️⃣ Get cart
cart = {}

2️⃣ Add product
cart["3"] = 1

3️⃣ Save to session
request.session["cart"] = {"3":1}

4️⃣ Redirect
/cart/

Cart page now shows:
Product 3 → Quantity 1