<template>
    <NavBar />
    <div class="container mt-5">
        <h2>Add Book</h2>
        <form @submit.prevent="addBook">
            <div class="mb-3">
                <label for="title" class="form-label">Book title</label>
                <input v-model="title" type="text" class="form-control" id="title">
            </div>
            <div class="mb-3">
                <label for="author" class="form-label">Author name</label>
                <input v-model="author" type="text" class="form-control" id="author">
            </div>
            <div class="mb-3">
                <label for="price" class="form-label">Book price</label>
                <input v-model="prcie" type="number" class="form-control" id="price">
            </div>
            <div class="mb-3">
                <label for="content" class="form-label">Book content</label>
                <input v-model="content" type="text" class="form-control" id="content">
            </div>
            <button type="submit" class="btn btn-primary">Add Book</button>
        </form>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
export default {
    components: {
        NavBar
    },
    data() {
        return {
            title: '',
            author: '',
            price: '',
            content: ''
        }
    },
    methods: {
        async addBook() {
            try {
                const response = await fetch('http://localhost:5000/section/<int:id>/add-book', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    },
                    body: JSON.stringify({
                        title: this.title,
                        author: this.author,
                        price: this.price,
                        content: this.content
                    })
                });
                const data = await response.json();
                if (response.ok) {
                    alert(data.message);
                    // PUSH TO ALL SECTIONS
                    this.$router.push('/all-book');
                }
                else {
                    alert(data.error);
                }
            } catch (error) {
                console.log(error);
            }

        }
    }
}
</script>