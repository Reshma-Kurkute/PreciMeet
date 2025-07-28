<template>
  <div class="min-h-screen bg-[#b1ddf1] flex flex-col">
    <!-- Header -->
    <header class="bg-gray-900 shadow-md px-6 py-4 flex justify-between items-center">
  <!-- Left: Logo -->
  <div class="flex items-center gap-3 text-white">
    <router-link to="/" class="flex items-center gap-3">
      <img src="http://pspl.com:8000/files/precimeet_logo.png" class="w-6 h-6 bg-black" alt="logo" />
      <span class="text-xl font-bold text-green-300">PreciMeet</span>
    </router-link>
  </div>

  <!-- Right: User Avatar -->
  <div class="flex items-center space-x-2">
    <UserAvatar :full-name="loggedInUser" :image-url="userImageUrl" />
  </div>
</header>


    <div class="flex flex-1">
      <!-- Sidebar -->
      <aside class="w-64 bg-white p-4 shadow-md">
        <nav class="space-y-2 text-gray-700">
          <router-link  :to="{ name: 'home' }" 
            class="block w-full bg-black text-white py-2 rounded mt-4 text-center hover:bg-gray-800">
            Schedule Meeting</router-link>
          <router-link  :to="{ name: 'home' }"
            class="block w-full bg-black text-white py-2 rounded mt-4 text-center hover:bg-gray-800">
              My Meetings
        </router-link>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 p-6">
        <h1 class="text-2xl font-semibold text-gray-700 mb-6">Available Rooms</h1>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="r in rooms" :key="r.room" class="bg-white shadow-md border rounded-lg p-4 flex flex-col justify-between">
            <router-link :to="{ name: 'Home', params: { roomName: r.name } }">
              <img :src="getImageUrl(r.room_image)" alt="Room Image" class="w-full h-40 object-cover rounded mb-4"/>

              <div class="text-sm space-y-1 text-gray-700">
                <p><strong>Room Name:</strong> <span class="text-blue-600 underline cursor-pointer">{{ r.room }}</span></p>
                <p><strong>Building/Floor:</strong> <span class="text-blue-600">{{ r.floor }}</span></p>
                <p><strong>No. of seats:</strong> {{ r.no_of_seat }}</p>
                <p><strong>Additional Facilities:</strong> —</p>
              </div>
            </router-link>
            <button type="button" class="mt-4 w-full bg-black text-white py-2 rounded hover:bg-gray-800"
              @click="$router.push({ name: 'home', params: { roomName: r.name } })">
              Reserve
            </button>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import UserAvatar from './UserAvatar.vue' // Ensure path is correct

const rooms = ref([])
const loggedInUser = ref('')
const userImageUrl = ref('')

// Fetch rooms
const fetchRooms = async () => {
  try {
    const response = await api.get('/Room', {
      params: {
        fields: JSON.stringify(['name', 'room', 'floor', 'no_of_seat', 'room_image']),
        limit_page_length: 100
      }
    })
    rooms.value = response.data.data
  } catch (error) {
    console.error('Failed to fetch rooms:', error)
  }
}

// Fetch user info
const fetchUser = async () => {
  try {
    const res = await api.get('/User/me')
    loggedInUser.value = res.data.data.full_name
    userImageUrl.value = res.data.data.user_image
  } catch (error) {
    console.error('Failed to fetch user:', error)
  }
}

onMounted(() => {
  fetchRooms()
  fetchUser()
})

const getImageUrl = (path) => {
  if (!path) {
    return 'https://via.placeholder.com/300x150?text=No+Image'
  }
  const cleanedPath = path.replace(/^\/room\/files\//, '/files/')
  return `http://pspl.com:8000${cleanedPath}`
}
</script>
