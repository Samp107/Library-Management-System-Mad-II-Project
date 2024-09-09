<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <router-link class="navbar-brand" to="/">Library Management Application</router-link>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNavDropdown">
      <ul v-if="isloggedin" class="navbar-nav">
        <li class="nav-item">
          <router-link class="nav-link" to="/">Home</router-link>
        </li>
        <li class="nav-item">
            <a class="nav-link" @click="logout">Logout</a>
        </li>
        
        <li v-if="this.role==='admin'" class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="/" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Admin Actions
          </a>
          <ul class="dropdown-menu">
            <li><router-link class="nav-link"to="/add-section">Add Section</router-link></li>
            <li><router-link class="nav-link"to="/all-sections">All Sctions</router-link></li>
          </ul>
        </li>

      <ul v-if="this.role==='admin'">
        <div class="nav-item">
            <router-link class="nav-link" to="/book-requests">Book requests</router-link>
        </div>
      </ul>
      <ul v-if="this.role==='admin'">
        <div class="nav-item">
            <a href="http://localhost:5000/download-bookissue-csv" class="btn btn-success">Book Issued Reports</a>
        </div>
      </ul>
      <ul v-else class="navbar-nav">
        <li class="nav-item">
            <router-link class="nav-link" to="/view-cart">Cart</router-link>
        </li>
        <li class="nav-item">
            <router-link class="nav-link" to="/user-book">My Book</router-link>
        </li>
      </ul>
      
        </ul>
        
        <ul v-else class="navbar-nav">
        <li class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
        </li>
        <li class="nav-item">
            <router-link class="nav-link"to="/register">Register</router-link>
        </li>

      </ul>
    </div>
  </div>
</nav>
</template>

<script>
import UserMixin from '../mixins/userMixin';
export default {
    mixins: [UserMixin],

}
</script>

<style scoped>

</style>