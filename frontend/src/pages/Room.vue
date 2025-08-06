<template>
  <div class="min-h-screen bg-[#b1ddf1] flex flex-col">
    <!-- Header -->
    <header class="bg-gray-900 shadow-md px-6 py-4 flex justify-between items-center">
      <div class="flex items-center gap-3 text-white">
        <router-link to="/" class="flex items-center gap-3">
          <img src="http://pspl.com:8000/files/precimeet_logo.png" class="w-6 h-6 bg-black" alt="logo" />
          <span class="text-xl font-bold text-green-300">PreciMeet</span>
        </router-link>
      </div>

      <!-- FIX: Wrap avatar and dropdown inside `.dropdown` -->
        <div class="relative dropdown">
          <!-- Trigger -->
          <div class="flex items-center space-x-2 cursor-pointer" @click="toggleDropdown">
            <UserAvatar :full-name="loggedInUser" :image-url="userImageUrl" />
          </div>

          <!-- Dropdown -->
          <div v-if="showDropdown" class="absolute right-0 mt-2 w-48 bg-black shadow-lg rounded-md z-10">
            <button class="block w-full px-4 py-2 text-left text-gray-700 hover:text-white hover:bg-gray-700 hover:rounded" @click="handleLogout">
              Logout
            </button>
          </div>
        </div>

    </header>

    <div class="flex flex-1">
      <!-- Sidebar -->
      <aside class="w-64 bg-white p-4 shadow-md">
        <nav class="space-y-2 text-gray-700">
          <router-link :to="{ name: 'home' }"
            class="block w-full bg-black text-white py-2 rounded mt-4 text-center hover:bg-gray-800">
            Schedule Meeting
          </router-link>

          <button class="block w-full bg-black text-white py-2 rounded mt-4 text-center hover:bg-gray-800"
            @click="showMyMeetings = !showMyMeetings">
            {{ showMyMeetings ? 'Meeting Rooms' : 'My Meeting' }}
          </button>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 p-6">
        <!-- <h1 class="text-2xl font-semibold text-gray-700 mb-6">
          {{ showMyMeetings ? 'My Meetings' : 'Available Rooms' }}
        </h1> -->


        <!-- My Meetings Section -->
        <div v-if="showMyMeetings" class="w-full p-4">
          <h2 class="text-2xl font-bold text-gray-800 mb-4">My Meetings</h2>

          <div class="overflow-y-auto flex-1 custom-scrollbar">
            <template v-if="myMeetings.length">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div v-for="meeting in myMeetings" :key="meeting.name"
                  class="bg-[#f9f9f9] p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between">
                  <div class="flex justify-between items-start mb-2">
                    <h3 class="text-black text-xl font-extrabold truncate">
                      {{ meeting.subject }}
                    </h3>
                    <!-- Edit / Delete buttons inside My Meetings card -->
                    <div class="flex gap-2">
                      <button title="Edit" class="text-[#295a50] hover:text-green-700" @click="editBooking(meeting)">
                        <!-- Edit icon -->
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                          stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M15.232 5.232l3.536 3.536M9 11l-2 6 6-2 7.071-7.071a2 2 0 10-2.828-2.828L9 11z" />
                        </svg>
                      </button>
                      <button title="Delete" class="text-red-500 hover:text-red-700"
                        @click="cancelBooking(meeting.name)">
                        <!-- Delete icon -->
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                          stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>

                  </div>

                  <div class="font-semibold text-lg text-gray-700 space-y-1 mb-2">
                    <div class="flex items-center gap-1"><span>📍</span><span>{{ meeting.room }}</span></div>
                    <div class="flex items-center gap-1"><span>🕒</span><span>{{ meeting.from_time }} - {{
                        meeting.to_time }}</span></div>
                    <div class="flex items-center gap-1"><span>📅</span><span>{{ meeting.date }}</span></div>
                  </div>

                  <div class="flex items-center justify-between mt-2">
                    <!-- <div class="text-lg text-black font-semibold">
              Organizer: {{ meeting.booked_by || 'N/A' }}
            </div> -->
                    <div class="flex -space-x-2">
                      <img v-for="(person, index) in meeting.participants || []" :key="index" :src="person"
                        class="w-8 h-8 rounded-full border border-white shadow" />
                    </div>
                  </div>
                </div>
              </div>
            </template>
            <template v-else>
              <div class="text-gray-500 text-center italic">No upcoming meetings</div>
            </template>
          </div>
        </div>


        <!-- Room List View -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="r in rooms" :key="r.room"
            class="bg-white shadow-md border rounded-lg p-4 flex flex-col justify-between">
            <router-link :to="{ name: 'Home', params: { roomName: r.name } }">
              <img :src="getImageUrl(r.room_image)" alt="Room Image" class="w-full h-40 object-cover rounded mb-4" />

              <div class="text-sm space-y-1 text-gray-700">
                <p>
                  <strong>Room Name:</strong>
                  <span class="text-blue-600 underline cursor-pointer">{{ r.room }}</span>
                </p>
                <p><strong>Building/Floor:</strong> <span class="text-blue-600">{{ r.floor }}</span></p>
                <p><strong>No. of seats:</strong> {{ r.no_of_seat }}</p>
                <p><strong>Additional Facilities:</strong> —</p>
              </div>
            </router-link>

            <!-- Reserve Button -->
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
import { api, frappe } from '@/api'
import UserAvatar from './UserAvatar.vue'
import { useRouter } from 'vue-router'
import { session } from '../data/session'

const router = useRouter()
const rooms = ref([])
const myMeetings = ref([])
const loggedInUser = ref('')
const userImageUrl = ref('')
const showMyMeetings = ref(false)

// Fetch list of rooms
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

// Fetch logged-in user and then their meetings
const fetchUser = async () => {
  try {
    const res = await frappe.get('/frappe.auth.get_logged_user')
    loggedInUser.value = res.data.message

    const userDoc = await api.get(`/User/${loggedInUser.value}`)
    userImageUrl.value = userDoc.data.data.image || ''

    // Fetch meetings after user is fully loaded
    fetchMyMeetings()
  } catch (error) {
    console.error('Failed to fetch user:', error)
  }
}

// Fetch meetings for current user
const fetchMyMeetings = async () => {
  try {
    const res = await api.get('/Room Reservation', {
      params: {
        filters: JSON.stringify([['owner', '=', loggedInUser.value]]),
        fields: JSON.stringify([
          'name',
          'subject',
          'date',
          'from_time',
          'to_time',
          'room',
          'booked_by',
          'description',
          'invitees_emails',
          'attendees_emails',
          'docstatus'
        ]),
        order_by: 'date desc',
        limit_page_length: 50
      }
    })
    myMeetings.value = res.data.data
  } catch (error) {
    console.error('Failed to fetch meetings:', error)
  }
}

// Image fallback
const getImageUrl = (path) => {
  if (!path) {
    return 'https://via.placeholder.com/300x150?text=No+Image'
  }
  const cleanedPath = path.replace(/^\/room\/files\//, '/files/')
  return `http://pspl.com:8000${cleanedPath}`
}

// Edit booking
const editBooking = (meeting) => {
  router.push({
    name: 'home',
    query: {
      editBooking: encodeURIComponent(JSON.stringify(meeting))
    }
  })
}


// Cancel booking
const cancelBooking = async (name) => {
  if (!confirm('Are you sure you want to cancel this meeting?')) return
  try {
    await api.delete(`/Room Reservation/${name}`)
    fetchMyMeetings()
  } catch (err) {
    console.error('Failed to cancel booking:', err)
  }
}

//------------------For logout-------------------------

// function getCookie(name) {
//   const value = `; ${document.cookie}`;
//   const parts = value.split(`; ${name}=`);
//   if (parts.length === 2) return parts.pop().split(';').shift();
//   return null;
// }
const handleLogout = async () => {
  await session.logout.submit()
}
// const logoutUser = async () => {
//   try {
//     const csrfToken = getCookie('csrf_token');

//     if (!csrfToken) {
//       console.error('Missing CSRF token from cookies');
//       return;
//     }

//     const response = await frappe.post('/logout', {
//       method: 'POST',
//       headers: {
//          'Content-Type': 'application/json',
//         'X-Frappe-CSRF-Token': csrfToken
//       },
//       credentials: 'include',
//     });

//     if (response.ok) {
//       // Redirect to login page or home
//       window.location.href = '/login';
//     } else {
//       console.error('Logout failed:', response.data);
//     }
//   } catch (error) {
//     console.error('Logout error:', error.response?.data || error.message);
//   }
// };


const showDropdown = ref(false);

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};
onMounted(() => {
  fetchRooms()
  fetchUser()
})


</script>
