<template>
    <NavBar />
    <div class="container mt-5">
        <h2>Update Section</h2>
        <form @submit.prevent="updateSection">
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
import UserMixin from '../mixins/userMixin';
export default {
    components: {
        NavBar
    },
    mixins: [UserMixin],
    data() {
        return {
            name: ''
        }
    },
    mounted(){
        const sectionId = this.$route.params.id
        this.fetchSection(sectionId)
    },
    methods: {
        async updateSection() {
            const sectionId = this.$route.params.id
            try {
                const response = await fetch(`http://localhost:5000/section/${sectionId}`, {
                    method: 'PUT',
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
                    // PUSH TO ALL sections
                    this.$router.push('/all-sections');

                }
                else {
                    alert(data.error);
                }
            } catch (error) {
                console.log(error);
            }

        },
        async fetchSection(sectionId) {
            try{
                const response = await fetch(`http://localhost:5000/section/${sectionId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                const data = await response.json();
                console.log(data)
                if (response.ok) {
                    this.name = data.name
                }
                else {
                    alert(data.error);
                }
            }
            catch(error){
                console.log(error);
            }
        }
    }
}
</script>