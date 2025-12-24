function getCSRFToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function addToCart() {
  fetch('/products/cart/add/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCSRFToken(),
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
      variant_id: document.getElementById('variant').value,
      quantity: document.getElementById('qty').value
    })
  })
  .then(res => res.json())
  .then(data => alert(data.success ? 'Added to cart' : data.error));
}

function toggleWishlist(productId) {
  fetch('/products/wishlist/toggle/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCSRFToken(),
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({ product_id: productId })
  })
  .then(res => res.json())
  .then(data => alert(data.wishlisted ? 'Added to wishlist' : 'Removed from wishlist'));
}
