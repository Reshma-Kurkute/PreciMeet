import { createRouter, createWebHistory } from 'vue-router'
import { session } from './data/session'
import { userResource } from '@/data/user'
import RoomDetail from '@/pages/BookRoom.vue'

const routes = [
  {
    name:'BookRoom',
    path: '/rooms/:roomName',
    component: RoomDetail,
  },
  {
    name:'Room',
    path: '/room',
    component:() => import('@/pages/Room.vue'),
  },
  {
    path:'/bookRoom',
    name: 'BookRoom',
    component: RoomDetail,
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
  },
  {
    name: 'Login',
    path: '/account/login',
    component: () => import('@/pages/Login.vue'),
  },
  {
  path: '/book-room/:roomName?', // For pass roomname via Room.vue on click of Reserve button
  name: 'home',
  component: () => import('@/pages/Home.vue'),
}
]

let router = createRouter({
  history: createWebHistory('/frontend'),
  routes,
})

router.beforeEach(async (to, from, next) => {
  let isLoggedIn = session.isLoggedIn
  try {
    await userResource.promise
  } catch (error) {
    isLoggedIn = false
  }

  if (to.name === 'Login' && isLoggedIn) {
    next({ name: 'Home' })
  } else if (to.name !== 'Login' && !isLoggedIn) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router
