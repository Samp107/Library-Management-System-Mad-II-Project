<template>
    <NavBar />
    <div class="container mt-4">
        <h2>All Sections</h2>
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for= "section in sections" :key="section.id">
                    <th scope="row">{{section.id}}</th>
                    <td>{{section.name}}</td>
                    <td class="btn-group">
                        <router-link v-if="this.role === 'admin'" :to="`/update-section/${section.id}`" class="btn btn-light">Update</router-link>
                        <button v-if="this.role === 'admin'" class="btn btn-light" @click="deleteSection(section.id)">Delete</button>
                        <router-link v-if="this.role === 'admin'" :to="`/add-book/${section.id}`" class="btn btn-light">Add Book</router-link>
                    </td>
                </tr>
            </tbody>
        </table>
        <router-link to="/add-section" class="btn btn-dark">Add Section</router-link>

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
            sections: []
        }
    },
    created() {
        this.getSections();
    },
    methods: {
        async getSections() {
            try {
                const response = await fetch('http://localhost:5000/sections',{
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    }
                });

                const data = await response.json();
                if(response.ok){
                    this.sections = data;
                } else {
                    alert("Something went wrong");
                }
            } catch (error) {
                console.log(error);
            }
        },

        async deleteSection(id) {
            try {
                const response = await fetch(`http://localhost:5000/section/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    }
                });
                const data = await response.json();
                if(response.ok){
                    alert(data.message);
                    this.getSections();
                } else {
                    alert(data.error);
                }
            } catch (error) {
                console.log(error);
            }
        },
        viewSection(id) {
            console.log('Viewing section: ', id);
        }
    }
}
</script>
