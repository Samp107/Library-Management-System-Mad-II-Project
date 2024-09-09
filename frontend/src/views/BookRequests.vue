<template>
    <div class="container">
      <h2 class="my-4">Book Requests</h2>
      <div v-if="!cartItems || cartItems.length === 0" class="alert alert-info">
        No book requests found.
      </div>
      <div v-else>

        <div class="container mt-4">
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">User</th>
                    <th scope="col">Book ID</th>
                    <th scope="col">Book Name</th>
                    <th scope="col">date_issued</th>
                    <th scope="col">date_return</th>
                    <th scope="col">Action</th>

                </tr>
            </thead>
            <tbody>
                <tr v-for="item in cartItems" :key="item.cart_id">
                    <td>{{item.user}}</td>
                    <td>{{item.book_id}}</td>
                    <td>{{item.book_name}}</td>
                    <td>{{item.date_issued}}</td>
                    <td>{{item.date_return}}</td>
                    <td class="btn-group">
                        <button @click="deleteItem(item.cart_id)" class="btn btn-danger">Delete</button>
                        <div v-if="item.status == 1">
                            <button class="btn btn-success">Approved</button>
                        </div>
                        <div v-else>
                            <button @click="approvebook(item.cart_id)" class="btn btn-danger">Approve</button>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
        

    </div>


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
        fetch('http://127.0.0.1:5000/book-requests', {
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
        fetch(`http://127.0.0.1:5000/delete-from-bookrequests/${cartItemId}`, {
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
      approvebook(cartItemId) {
        fetch(`http://127.0.0.1:5000/admin-approve/${cartItemId}`, {
          
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
          }
        })
        .then(response => {
          if (response.ok) {
            console.log('Book approved successfully');
            this.fetchCartItems();
          } else {
            throw new Error('Failed to approve the book');
          }
        })
        .catch(error => console.error('Error in approve book:', error));
      }
  }
}
  </script>
  
  <style scoped>
  .card {
    width: 100%;
  }
  </style>
  