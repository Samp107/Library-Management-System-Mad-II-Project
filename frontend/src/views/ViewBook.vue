<template>
    <div class="container mt-5">
      <div v-if="loading">
        <h2>Loading...</h2>
      </div>
      <div v-else>
        <div v-if="book">
          <div class="card">
            <div class="card-header">
              <h2>{{book.title }}</h2>
            </div>
            <div class="card-body">
              <dl class="row">
                <dt class="col-sm-3">Author:</dt>
                <dd class="col-sm-9">{{ book.author }}</dd>
  
                <dt class="col-sm-3">Section:</dt>
                <dd class="col-sm-9">{{ book.section_name }}</dd>

                <dt class="col-sm-3">Content:</dt>
                <dd class="col-sm-9">Rs.{{ book.content }}</dd>
              </dl>
             
            </div>
          </div>
        </div>
        <div v-else>
          <p>No book found.</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import userMixins from '../mixins/userMixin'
  
  export default {
    mixins: [userMixins],
    data() {
      return {
        book: null,
        loading: true,
      };
    },
    mounted() {
      this.fetchBookDetails();
    },
    methods: {
      fetchBookDetails() {
        const bookId = this.$route.params.bookId; 
        const token = localStorage.getItem('access_token');
  
        if (!token) {
          console.error('Access token is null');
          return;
        }
  
        fetch(`http://127.0.0.1:5000/read-book/${bookId}`, {
          method: 'GET',
          headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
          },
        })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
          })
          .then(data => {
            this.book_data = data.book;
          })
          .catch(error => {
            console.error('Error fetching book details:', error);
          })
          .finally(() => {
            this.loading = false;
          });
      },

    },
  };
  </script>
  
  <style scoped>
  .card {
    margin-top: 20px;
  }
  .btn {
    margin-right: 8px;
  }
  </style>
  