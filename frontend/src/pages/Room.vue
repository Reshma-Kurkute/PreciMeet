<template>
  <div class="min-h-screen bg-gray-100 flex">
    <!-- Sidebar -->
     <aside class="w-64 bg-white p-4 shadow-md">
      <h2 class="text-xl font-bold mb-4">PreciMeet</h2>
      <nav class="space-y-2 text-gray-700">
        <!-- <a href="#" class="block hover:bg-gray-200 p-2 rounded">Admin View</a> -->
        <div>
          <p class="text-sm font-semibold text-gray-500">Booking</p>
          <a href="http://pspl.com:8080/pages/BookRoom.vue" class="block hover:bg-gray-200 p-2 rounded">Book a Room</a>
          <!-- <a href="#" class="block hover:bg-gray-200 p-2 rounded bg-gray-200">Available Rooms</a> -->
        </div>
        <a href="#" class="block hover:bg-gray-200 p-2 rounded">Meeting Room</a>
        <!-- <a href="#" class="block hover:bg-gray-200 p-2 rounded">Users</a> -->
        <a href="#" class="block hover:bg-gray-200 p-2 rounded">My View</a>
      </nav>
    </aside> 

    <!-- Main Content -->
    <main class="flex-1 p-6">
      <h1 class="text-2xl font-semibold text-gray-700 mb-6">Available Rooms</h1>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="r in rooms" :key="r.room" class="bg-white shadow-md border rounded-lg p-4 flex flex-col justify-between">
          <router-link :to="{ name: 'BookRoom', params: { roomName: r.name } }">
            <img :src="getImageUrl(r.room_image)" alt="Room Image" class="w-full h-40 object-cover rounded mb-4"/>

            <div class="text-sm space-y-1 text-gray-700">
              <p>
                <strong>Room Name:</strong>
                <span class="text-blue-600 underline cursor-pointer">{{ r.room }}</span>
              </p>
              <p>
                <strong>Building/Floor:</strong>
                <span class="text-blue-600">{{ r.floor }}</span>
              </p>
              <p><strong>No. of seats:</strong> {{ r.no_of_seat }}</p>
              <p><strong>Additional Facilities:</strong> —</p>
            </div>
          </router-link>
          <button class="mt-4 w-full bg-black text-white py-2 rounded hover:bg-gray-800">
            Reserve
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api, frappe } from '@/api'


const rooms = ref([])
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
onMounted(fetchRooms);

const getImageUrl = (path) => {
  if (!path) {
    return 'https://via.placeholder.com/300x150?text=No+Image';
  }

  // Remove /room prefix if it exists
  const cleanedPath = path.replace(/^\/room\/files\//, '/files/');
  console.log('Cleaned Path:', cleanedPath);
  return `http://pspl.com:8000${cleanedPath}`;
};

</script>
