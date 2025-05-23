<template>
  <div id="app" class="bg-[#b1ddf1] min-h-screen text-black px-6 py-10">
    <!-- Header -->
    <!-- Fixed, black header -->
<header class="fixed top-0 left-0 w-full z-50 flex items-center justify-between px-6 py-4 bg-gray-900 shadow-md">
  <!-- Logo and title -->
  <div class="flex items-center gap-3 text-white">
  <router-link to="/" class="flex items-center gap-3">
    <img src="http://pspl.com:8000/files/precimeet_logo.png" class="w-6.5 h-6.5 bg-black" alt="logo" />
    <span class="text-xl font-bold text-green-300">PreciMeet</span>
  </router-link>
</div>

  <!-- Navigation buttons -->
  <nav class="flex items-center gap-4">
    <!-- <button class="px-4 py-1 border border-yellow-600 text-green-300 rounded hover:bg-blue-900 hover:text-black transition">
      <router-link to="/AllBooking">
      My Bookings</router-link>
    </button> -->
    
    <button class="px-4 py-1 border border-black bg-white text-black rounded hover:bg-blue-900 hover:text-black transition">
      <router-link to="/Room">
      Meeting Rooms
      </router-link>
    </button>
 
    <!-- <button class="px-4 py-1 border border-yellow-600 text-green-300 rounded hover:bg-blue-900 hover:text-black transition">
      Book Now
    </button> -->
    <div class="flex items-center space-x-2">
    <UserAvatar :full-name="loggedInUser" :image-url="userImageUrl" />
    <!-- <span>{{ loggedInUser }}</span> -->
  </div>
  <!-- Logout Dropdown -->
  
  </nav>
</header>

    <!-- Main Section (Swapped) -->
    <!-- Main Section (Swapped, aligned horizontally) -->
<section class="flex flex-col md:flex-row gap-10 items-start pt-[72px]">
  <!-- Left: Upcoming Meetings Sidebar -->
  <div class="rounded-2xl shadow-xl p-6 w-full md:w-1/2 max-h-[720px] flex flex-col">
    <div class="flex justify-between items-center mb-4">
  <h2 class="text-2xl font-semibold">Upcoming Meetings</h2>
  <button
    @click="showOnlyMine = !showOnlyMine"
    class="px-4 py-1 text-lg border border-black bg-black text-white rounded hover:bg-blue-900 transition"
  >
    {{ showOnlyMine ? 'Show All' : 'My Bookings' }}
  </button>
</div>
    <div class="overflow-y-auto flex-1 custom-scrollbar">
      <template v-if="bookings.length">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div
            v-for="booking in upcomingMeetings"
            :key="booking.name"
            class="bg-[#f9f9f9] p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between"
          >
            <div class="flex justify-between items-start mb-2">
              <h3 class="text-black text-xl font-extrabold truncate">
                {{ booking.subject }}
              </h3>
               <div class="flex gap-2" v-if="showOnlyMine">
                <button title="Edit" class="text-[#295a50] hover:text-green-700" @click="editBooking(booking)">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536M9 11l-2 6 6-2 7.071-7.071a2 2 0 10-2.828-2.828L9 11z" />
                  </svg>
                </button>
                <button title="Delete" class="text-red-500 hover:text-red-700" @click="cancelBooking(booking.name)">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div> 
            </div>
            <div class="font-semibold text-lg text-gray-700 space-y-1 mb-2">
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
              <div class="text-lg text-black font-semibold">
                Organizer: {{ booking.booked_by || 'N/A' }}
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
  <div class="bg-white rounded-2xl shadow-xl p-8 w-full md:w-1/2 min-h-[720px] ">
    <h2 class="text-2xl font-semibold mb-6">Book a Meeting</h2>
    <BookRoom :editBooking="selectedBooking" @bookingUpdated="fetchBookings" />
  </div>
</section>
</div>
</template>

<script setup>
import { ref, onMounted,computed } from 'vue'
import BookRoom from './BookRoom.vue'
import { api,frappe } from '@/api'
import UserAvatar from './UserAvatar.vue'

const bookings = ref([])

const fetchBookings = async () => {
  try {
    const res = await api.get('/Room Reservation', {
  params: {
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
    limit_page_length: 100,
    order_by: 'modified desc'
  }
})
    bookings.value = res.data.data
    
  } catch (err) {
    console.error('Failed to fetch bookings:', err)
  }
}
// to match frappe date time format
const parseBookingDateTime = (dateStr, timeStr) => {
  try {
    if (!dateStr || !timeStr) return new Date('invalid')

    // Ensure time has 2-digit hour
    const [h, m = '00', s = '00'] = timeStr.trim().split(':')
    const paddedTime = `${h.padStart(2, '0')}:${m.padStart(2, '0')}:${s.padStart(2, '0')}`

    const fullDateTime = `${dateStr}T${paddedTime}` // already yyyy-mm-dd
    const dt = new Date(fullDateTime)

    return isNaN(dt.getTime()) ? new Date('invalid') : dt
  } catch (err) {
    console.error('Date parsing error:', err)
    return new Date('invalid')
  }
}





// ✅ Computed: Only future meetings
const upcomingMeetings = computed(() => {
  const now = new Date()

  return bookings.value.filter(booking => {
   // console.log('Date by now function:', booking)
    // Skip if required fields are missing
    if (!booking.date || !booking.from_time) return false

    const meetingDate = parseBookingDateTime(booking.date, booking.from_time)
   // console.log('Parsed:', `${booking.date} ${booking.from_time} →`, meetingDate.toString())

    const isFuture = !isNaN(meetingDate) && meetingDate >= now
    const isActive = booking.docstatus !== 2

    if (showOnlyMine.value) {
      return isFuture && isActive && booking.booked_by === loggedInUser.value
    }

    return isFuture && isActive
  })
})

const emit = defineEmits(['bookingUpdated'])  //Ensure BookRoom.vue emits the correct event after booking

const showOnlyMine = ref(false)
const loggedInUser = ref('')

// Fetch logged in user
// const getUser = async () => {
//   try {
//     const res = await frappe.get('/frappe.auth.get_logged_user')
//     loggedInUser.value = res.data.message
//   } catch (err) {
//     console.error('Failed to get logged in user:', err)
//   }
// }



// for edit booking 
const selectedBooking = ref(null)

const editBooking = (booking) => {
  selectedBooking.value = booking
}

//for cancel booking
const cancelBooking = async (bookingName) => {
  if (!confirm('Are you sure you want to cancel this meeting?')) return

  try {
    await api.put(`/Room Reservation/${bookingName}`, {
      docstatus: 2  // this cancels the document
    })
    alert('Meeting cancelled successfully!')
    fetchBookings()
  } catch (err) {
    console.error('Cancel failed:', err)
    alert('Failed to cancel meeting. Check console for details.')
  }
}
onMounted(() => {
  getUser()
  fetchBookings()
})

//for profile picture

const userImageUrl = ref('')
const getUser = async () => {
  try {
    const res = await frappe.get('/frappe.auth.get_logged_user')
    loggedInUser.value = res.data.message

    // Fetch user's full info
    const userDoc = await api.get(`/User/${loggedInUser.value}`)
    userImageUrl.value = userDoc.data.data.image || ''
  } catch (err) {
    console.error('Failed to get logged in user:', err)
  }
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
