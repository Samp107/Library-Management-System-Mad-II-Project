<template>
    <div class="container">
      <h2 class="my-4">Your Cart</h2>
      <div v-if="!cartItems || cartItems.length === 0" class="alert alert-info">
        Your cart is empty.
      </div>
      <div v-else>
        <div v-for="item in cartItems" :key="item.cart_id" class="card mb-3">
          <div class="card-body">
            <h4 class="card-title">{{ item.book_name }}</h4>
            <p class="card-text">Author: {{ item.author }} </p>
            <p>Price: {{ item.price }}</p>
            <div class="row">
              <div class="col-md-4 d-flex align-items-center justify-content-end">
                <button @click="deleteItem(item.cart_id)" class="btn btn-danger">Delete</button>
              </div>
            </div>
          </div>
        </div>
        <button @click="placeOrder" class="btn btn-primary">Place Order</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        cartItems: []
      };
    },
    mounted() {
      this.fetchCartItems();
    },
    methods: {
      fetchCartItems() {
        fetch('http://127.0.0.1:5000/view-cart', {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token') 
          }
        })
        .then(response => response.json())
        .then(data => {
          this.cartItems = data.cart;
        })
        .catch(error => console.error('Error fetching cart items:', error));
      },
      deleteItem(cartItemId) {
        fetch(`http://127.0.0.1:5000/delete-from-cart/${cartItemId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
          }
        })
        .then(response => {
          if (response.ok) {
            console.log('Item deleted successfully');
            this.fetchCartItems();
          } else {
            throw new Error('Failed to delete item');
          }
        })
        .catch(error => console.error('Error deleting item:', error));
      },
      placeOrder() {
        fetch(`http://127.0.0.1:5000/place-order`, {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
          }
        })
        .then(response => {
          if (response.ok) {
            console.log('Order Placed Successfully');
            this.fetchCartItems();
            // Push to myorders page
          } else {
            throw new Error('Failed to order');
          }
        })
        .catch(error => console.error('Error:', error));
      }
    }
  };
  </script>
  
  <style scoped>
  .card {
    width: 100%;
  }
  </style>
  