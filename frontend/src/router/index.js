import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterPage from '../views/RegisterPage.vue'
import LoginPage from '../views/LoginPage.vue'
import AddSection from '../views/AddSection.vue'
import UpdateSection from '../views/UpdateSection.vue'
import AllSections from '../views/AllSections.vue'
import AddBook from '../views/AddBook1.vue'
// import ViewBook from '@/views/ViewBook.vue'
import BookRequests from '../views/BookRequests.vue'
import UserBook1 from '../views/UserBook1.vue'
import ReadBook from '../views/ReadBook.vue'
import UpdateBook from '../views/UpdateBook.vue'



const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage
  },
  {
    path: '/book-requests',
    name: 'book-requests',
    component: BookRequests
  },
  {
    path: '/user-book',
    name: 'user-book',
    component: UserBook1
  },
  {
    path: '/read-book/:id',
    name: 'read-book',
    component: ReadBook
  },
  {
    path: '/view-cart',
    name: 'view-cart',
    component: () => import('../views/ViewCart.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path:'/add-section',
    name: 'add-section',
    component: AddSection
  },
  { 
    path: '/all-sections',
    name: 'all-sections',
    component: AllSections
  },
  {
    path: '/update-section/:id',
    name: 'update-section',
    component: UpdateSection
  },
  {
    path:'/add-book/:id',
    name: 'add-book',
    component: AddBook
  },
  {
    path: '/update-book/:id',
    name: 'update-book',
    component: UpdateBook
  },

  {
    path: '/all-books',
    name: 'all-books',
    component: AllSections
  },
  // {
  //   path: '/book/:id',
  //   name: 'view-book',
  //   component: ViewBook
  // },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
