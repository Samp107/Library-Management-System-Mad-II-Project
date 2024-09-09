<template>
  <NavBar />
  <div class="container mt-3">
    <h2>Library Management System</h2>
    <div class="form-group">
      <input 
        type="text" 
        v-model="searchQuery" 
        class="form-control" 
        placeholder="Search for books">
    </div>
    <div v-for="section in filteredSections" :key="section.id" class="mt-3">
      <div class="d-grid gap-2">
        <button class="btn btn-info" type="button" ><h4>Section: {{ section.name }}</h4></button>
      </div>
      &nbsp;&nbsp;
      
      <div class="row">
        <div v-for="book in section.books" :key="book.id" class="col-md-3 mb-3">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ book.title }}</h5>
              <p class="card-text">Author: {{ book.author }} </p>
              <p>Price: {{ book.price }}</p>
              <button v-if="this.role === 'user'" @click="addToCart(book.id)" class="btn btn-primary btn-block">
                Add to Cart
              </button>
              <div v-if="this.role === 'admin'" class="btn-group" role="group" aria-label="Basic mixed styles example">
                <button type="button" class="btn btn-success"><router-link class="nav-link" :to="`/read-book/${book.id}`">Read Book</router-link></button>
                <button type="button" class="btn btn-warning"><router-link class="nav-link" :to="`/update-book/${book.id}`">Update</router-link></button>
                <button type="button"  v-if="this.role === 'admin'" @click="deleteBook(book.id)" class="btn btn-danger">Delete</button>
              </div>
              <!-- <button v-if="this.role === 'admin'" class="btn btn-warning">
                <router-link class="nav-link" :to="`/read-book/${book.id}`">Read Book</router-link>
              </button>
      
              <button v-if="this.role === 'admin'" class="btn btn-primary btn-block">
                <router-link class="nav-link" :to="`/update-book/${book.id}`">Update</router-link>
              </button>
          
              <button v-if="this.role === 'admin'" @click="deleteBook(book.id)" class="btn btn-primary btn-block">
                Delete
              </button> -->

              
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import UserMixin from '../mixins/userMixin';

export default {
  components: {
    NavBar
  },
  mixins: [UserMixin],
  data() {
    return {
      sections: [],
      searchQuery: '',
    }
  },
  async created() {
    this.getdata()
  },
  computed: {
    filteredSections() {
      if (!this.searchQuery) {
        return this.sections.filter(section => section.books.length > 0);
      }
      const searchTerm = this.searchQuery.toLowerCase();
      return this.sections.map(section => {
        const filteredBooks = section.books.filter(book => 
          book.title.toLowerCase().includes(searchTerm)
        );
        return { ...section, books: filteredBooks };
      }).filter(section => section.books.length > 0);
    }
  },
  methods: {
    async getdata() {
      try {
        const response = await fetch('http://127.0.0.1:5000/getallbookinfo', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        const data = await response.json();
        if (response.ok) {
          this.sections = data;
          console.log("data fetched");
        } else {
          console.log("data not fetched");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    async getbook(bookId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/book/${bookId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        const book = await response.json();
        if (response.ok) {
          this.book = book;
          console.log("book fetched");
        } else {
          console.log("book not fetched");
        }
      } catch (error) {
        console.error("Error fetching book:", error);
      }
    },
    async addToCart(bookId) {
      try {
        const response = await fetch('http://127.0.0.1:5000/add-to-cart', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          },
          body: JSON.stringify({
            book_id: bookId,
          })
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.error("Error adding book to cart:", error);
      }
    },
    deleteBook(bookId) {
        fetch(`http://127.0.0.1:5000/deletebook/${bookId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
          }
        })
        .then(response => {
          if (response.ok) {
            console.log('Book deleted successfully');
            this.getbook(bookId);
          } else {
            throw new Error('Failed to delete Book');
          }
        })
        .catch(error => console.error('Error deleting book:', error));
      },
      updateBook(bookId) {
        fetch(`http://localhost:5000/update-book/${bookId}`, {
          method: 'PUT',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
          }
        })
        .then(response => {
          if (response.ok) {
            console.log('Book updated successfully');
            
          } else {
            throw new Error('Failed to update Book');
          }
        })
        .catch(error => console.error('Error updating book:', error));
      },
  }
}
</script>


<style scoped></style>