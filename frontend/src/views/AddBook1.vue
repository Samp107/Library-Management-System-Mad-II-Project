<template>
    <div class="container mt-5">
      <div class="card">
        <div class="card-header">
          <h2>Add Product</h2>
        </div>
        <div class="card-body">
          <form @submit.prevent="addBook" class="row g-3">
            <div class="col-md-6">
              <label for="title" class="form-label">Book Title:</label>
              <input v-model="title" type="text" class="form-control" id="title" required />
            </div>
            <div class="col-md-6">
              <label for="author" class="form-label">Author:</label>
              <input v-model="author" type="text" class="form-control" id="author" required />
            </div>
            <div class="col-md-6">
              <label for="price" class="form-label">Price:</label>
              <input v-model="price" type="number" class="form-control" id="price" required />
            </div>
            <div class="col-md-6">
              <label for="content" class="form-label">Content:</label>
              <input v-model="content" type="text" class="form-control" id="content" required />
            </div>
            <div class="col-md-6">
                <label for="sectionDropdown" class="form-label">Section:</label>
                <select v-model="selectedSection" class="form-select" id="sectionDropdown" required>
                <option disabled value="">Select Section</option>
                <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
                </select>
            </div>
            <div class="col-12 mt-3">
              <button type="submit" class="btn btn-primary">Add Book</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
export default {
  data() {
    return {
      title: '',
      author: '',
      price: null,
      content: '',
      selectedSection: '',
      sections: [],
    };
  },
  created() {
    this.fetchSections();
    const sectionIdFromRoute = this.$route.params.id;
    console.log(sectionIdFromRoute)
    if (sectionIdFromRoute) {
      this.selectedSection = sectionIdFromRoute;
      console.log(this.selectedSection);
    }

  },
  methods: {
    fetchSections() {
      fetch('http://127.0.0.1:5000/sections', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
        .then(response => response.json())
        .then(data => {
          this.sections = data;
          console.log('datafetch')
        })
        .catch(error => {
          console.error('Error fetching sections:', error);
        });
    },
    addBook() {
      fetch(`http://127.0.0.1:5000/section/${this.selectedSection}/add-book`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        },
        body: JSON.stringify({
          title: this.title,
          author: this.author,
          price: this.price,
          content: this.content,
        }),
      })
        .then(response => response.json())
        .then(data => {
          alert(data.message);
          this.$router.push('/');
          // Optionally, you can redirect or perform other actions after adding the product
        })
        .catch(error => {
          console.error('Error adding book:', error);
        });
    },
  },
};
</script>

  

  