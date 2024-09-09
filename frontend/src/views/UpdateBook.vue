<template>
    <NavBar />
    <div class="container mt-5">
        <h2>Update Book</h2>
        <form @submit.prevent="updateBook">
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
                <button type="submit" class="btn btn-primary">Update Book</button>
              </div>
        </form>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import UserMixin from '../mixins/userMixin';
export default {
    components: {
        NavBar
    },
    mixins: [UserMixin],
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
    mounted(){
        const bookId = this.$route.params.id
        this.fetchBook(bookId)
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
        async updateBook() {
            const bookId = this.$route.params.id
            try {
                const response = await fetch(`http://localhost:5000/update-book/${bookId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    },
                    body: JSON.stringify({
                        title: this.title,
                        author: this.author,
                        price: this.price,
                        content: this.content,
                    })
                });
                const data = await response.json();
                if (response.ok) {
                    alert(data.message);
                    // PUSH TO ALL sections
                    this.$router.push('/');

                }
                else {
                    alert(data.error);
                }
            } catch (error) {
                console.log(error);
            }

        },
        async fetchBook(bookId) {
            try{
                const response = await fetch(`http://localhost:5000/book/${bookId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                const data = await response.json();
                console.log(data)
                if (response.ok) {
                    this.title = data.title,
                    this.author = data.author,
                    this.price = data.price,
                    this.content = data.content
                }
                else {
                    alert(data.error);
                }
            }
            catch(error){
                console.log(error);
            }
        },
        
    }
}
</script>