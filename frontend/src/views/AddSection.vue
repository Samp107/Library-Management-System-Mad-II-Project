<template>
    <NavBar />
    <div class="container mt-5">
        <h2>Add Section</h2>
        <form @submit.prevent="addSection">
            <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input v-model="name" type="text" class="form-control" id="name">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
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
            name: ''
        }
    },
    methods: {
        async addSection() {
            try {
                const response = await fetch('http://localhost:5000/add-section', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    },
                    body: JSON.stringify({
                        name: this.name
                    })
                });
                const data = await response.json();
                if (response.ok) {
                    alert(data.message);
                    // PUSH TO ALL SECTIONS
                    this.$router.push('/all-sections');
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