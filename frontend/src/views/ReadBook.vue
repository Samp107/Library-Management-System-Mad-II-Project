<template>
  <div class="container mt-5">
    <div v-if="loading">
      <h2>Loading...</h2>
    </div>
    <div v-else>
      <div v-if="book">
        <div class="card">
          <div class="card-header">
            <h2>{{ book.title }}</h2>
            <h3>Author : {{ book.author }}</h3>
            <h3>Section : {{ section_name }}</h3>
          </div>
          <div class="card-body">
            <h5>{{ book.content }}</h5>
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
import userMixin from '../mixins/userMixin'

export default {
  mixins: [userMixin],
  data() {
    return {
      book: null,
      section_name: null,
      loading: true,
    };
  },
  mounted() {
    this.fetchBookDetails();
  },
  methods: {
    fetchBookDetails() {
      const bookId = this.$route.params.id;
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
          this.book = data.book;
          this.section_name = data.section_name
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