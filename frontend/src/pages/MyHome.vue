<template>
  <div id="app" class="bg-[#b1ddf1] min-h-screen text-black px-6 py-10">
    <!-- Header -->
    <!-- Fixed, black header -->
<header class="fixed top-0 left-0 w-full z-50 flex items-center justify-between px-6 py-4 bg-gray-900 shadow-md">
  <!-- Logo and title -->
  <div class="flex items-center gap-3 text-white">
    <img src="http://pspl.com:8000/files/precimeet_logo.png" class="w-6.5 h-6.5 bg-black" alt="logo" />
    <span class="text-xl font-bold text-green-300">PreciMeet</span>
  </div>

  <!-- Navigation buttons -->
  <nav class="flex items-center gap-4">
    <button class="px-4 py-1 border border-yellow-600 text-green-300 rounded hover:bg-[#eecc43] hover:text-black transition">
      <router-link to="/AllBooking">
      My Bookings</router-link>
    </button>
    <button class="px-4 py-1 border border-yellow-600 text-green-300 rounded hover:bg-[#eecc43] hover:text-black transition">
      Meeting Rooms
    </button>
    <button class="px-4 py-1 border border-yellow-600 text-green-300 rounded hover:bg-[#eecc43] hover:text-black transition">
      Book Now
    </button>
    <img
    src="https://i.pravatar.cc/100"
    class="w-8 h-8 rounded-full border border-white cursor-pointer"
    @click="toggleLogout"
  />

  <!-- Logout Dropdown -->
  <div v-if="showLogout" class="absolute right-0 mt-16 bg-white border border-gray-300 rounded shadow-lg z-50 w-32"  >
    <button @click="logout" class="block w-full text-left px-4 py-2 text-sm text-black hover:bg-gray-100">
      Logout
    </button>
  </div>
  </nav>
</header>

    <!-- Main Section (Swapped) -->
    <!-- Main Section (Swapped, aligned horizontally) -->
<section class="flex flex-col md:flex-row gap-10 items-start pt-[72px]">
  <!-- Left: Upcoming Meetings Sidebar -->
  <div class="rounded-2xl shadow-xl p-6 w-full md:w-1/2 max-h-[720px] flex flex-col">
    <h2 class="text-2xl font-semibold mb-4">Upcoming Meetings</h2>
    <div class="overflow-y-auto flex-1 custom-scrollbar">
      <template v-if="bookings.length">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div
            v-for="booking in bookings"
            :key="booking.name"
            class="bg-[#f9f9f9] p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between"
          >
            <div class="flex justify-between items-start mb-2">
              <h3 class="text-black font-semibold text-lg truncate">
                {{ booking.subject }}
              </h3>
              <div class="flex gap-2">
                <button title="Edit" class="text-[#295a50] hover:text-green-700">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536M9 11l-2 6 6-2 7.071-7.071a2 2 0 10-2.828-2.828L9 11z" />
                  </svg>
                </button>
                <button title="Delete" class="text-red-500 hover:text-red-700">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
            <div class="text-sm text-gray-700 space-y-1 mb-2">
              <div class="flex items-center gap-1">
                <span>📍</span>
                <span>{{ booking.room }}</span>
              </div>
              <div class="flex items-center gap-1">
                <span>🕒</span>
                <span>{{ booking.from_time }} - {{ booking.to_time }}</span>
              </div>
              <div class="flex items-center gap-1">
                <span>📅</span>
                <span>{{ booking.date }}</span>
              </div>
            </div>
            <div class="flex items-center justify-between mt-2">
              <div class="text-sm text-black font-semibold">
                Organizer: {{ booking.organizer || 'N/A' }}
              </div>
              <div class="flex -space-x-2">
                <img
                  v-for="(person, index) in booking.participants || []"
                  :key="index"
                  :src="person"
                  class="w-8 h-8 rounded-full border border-white shadow"
                />
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

  <!-- Right: Book Room Form -->
  <div class="bg-white rounded-2xl shadow-xl p-8 w-full md:w-1/2 min-h-[720px]">
    <h2 class="text-2xl font-semibold mb-6">Book a Meeting</h2>
    <BookRoom />
  </div>
</section>
</div>
</template>

<script setup>
import { ref, onMounted,computed } from 'vue'
import BookRoom from './BookRoom.vue'
import { api,frappe } from '@/api'
import { useRouter } from 'vue-router'

const bookings = ref([])

const fetchBookings = async () => {
  try {
    const res = await api.get('/Room Reservation', {
      params: {
        fields: JSON.stringify(['subject', 'date', 'from_time', 'to_time', 'room']),
        limit_page_length: 100,
        order_by: 'date asc, from_time asc'
      }
    })
    bookings.value = res.data.data
  } catch (err) {
    console.error('Failed to fetch bookings:', err)
  }
}

onMounted(() => {
  fetchBookings()
})
// ✅ Computed: Only future meetings
const upcomingMeetings = computed(() => {
  const now = new Date()
  return bookings.value.filter(booking => {
    try {
      const fullDateTimeStr = `${booking.date}T${booking.from_time}`
      const meetingDate = new Date(fullDateTimeStr)
      return meetingDate >= now
    } catch (err) {
      console.warn('Invalid meeting date:', booking)
      return false
    }
  })
})

const router = useRouter()
const showLogout = ref(false)

const toggleLogout = () => {
  showLogout.value = !showLogout.value
}

const logout = async () => {
  try {
    // OPTIONAL: try calling Frappe's logout API (may not do much in token mode)
    await frappe.post('/logout', {}, { withCredentials: true })

    // Clear token headers (important for token-based auth)
    api.defaults.headers['Authorization'] = ''
    frappe.defaults.headers['Authorization'] = ''

    // Clear session storage
    localStorage.clear()
    sessionStorage.clear()

    // Redirect to login using Vue Router
    router.push({ name: 'Login' })
  } catch (err) {
    console.error('Logout failed:', err)
    alert('Logout failed. Check console for details.')
  }
}

const selectedBooking = ref(null)
const onBookingSubmitted = () => {
  selectedBooking.value = null
  // fetchBookings()
}

</script>

<style>
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #cccccc;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #999999;
}
</style>
