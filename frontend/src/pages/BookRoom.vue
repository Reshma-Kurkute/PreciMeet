<template>
  <!-- Booking Form -->
  <form @submit.prevent="submitForm" class="bg-white p-8 rounded-xl shadow-lg w-full space-y-6">
    <div class="flex flex-col md:flex-row gap-6">
      <!-- Left: Main Form Fields -->
      <div class="flex-1 space-y-4">
        <!-- Subject -->
        <div>
          <label class="block font-medium mb-1">Subject :</label>
          <input
            v-model="subject"
            type="text"
            class="w-full bg-[#FAF9EE] rounded px-2 py-1 border border-black focus:outline-none focus:ring-blue-900 " required>
        </div>

        <!-- Select Room -->
        <div>
          <label class="block font-medium mb-1">Select Room :</label>
          <select
            v-model="selectedRoom"
            class="w-full bg-[#FAF9EE] rounded px-2 py-1 border border-black focus:outline-none focus:ring-blue-900 " required>
            <option disabled value="">Select Room</option>
            <option v-for="room in availableRooms" :key="room.name" :value="room.name">{{ room.name }}</option>
          </select>
        </div>

        <!-- Attendees Emails -->
        <div class="relative">
          <label class="block font-medium mb-1">Attendees Emails:</label>
          <input
            type="text"
            v-model="attendeeInput"
            @input="onAttendeeInput"
            @keydown.down.prevent="highlightNext"
            @keydown.up.prevent="highlightPrev"
            @keydown.enter.prevent="selectCustomOrHighlighted"
            class="w-full bg-[#FAF9EE] rounded px-2 py-1 border border-black focus:outline-none focus:ring-blue-900 "
            placeholder="Type to search users..." 
          />
          <ul v-if="filteredUsers.length && showSuggestions" class="absolute bg-white shadow border w-full mt-1 rounded z-10 max-h-40 overflow-auto">
            <li
              v-for="(user, index) in filteredUsers"
              :key="user.email"
              :class="['px-4 py-2 cursor-pointer', index === highlightedIndex ? 'bg-[#FAF9EE] text-black' : 'hover:bg-[#dfece9]']"
              @click="addAttendee(user.email)"
            >
              {{ user.name }} ({{ user.email }})
            </li>
          </ul>
          <div class="mt-2 flex flex-wrap gap-2">
            <span
              v-for="(email, index) in attendeesEmails"
              :key="index"
              class="bg-[#295a50] text-white px-2 py-1 rounded-full text-sm flex items-center gap-1">
              {{ email }}
              <button type="button" @click="removeAttendee(index)" class="text-white hover:text-gray-300">&times;</button>
            </span>
          </div>
        </div>

        <!-- Invitees Emails -->
        <div>
          <label class="block font-medium mb-1">Invitees Emails :</label>
          <textarea
            v-model="invitees_emails"
            class="w-full bg-[#FAF9EE] rounded px-2 py-1 border border-black focus:ring-blue-900"/>
        </div>

        <!-- Date -->
        <div>
          <label class="block font-medium mb-1">Date :</label>
          <input
            type="date"
            v-model="date"
            class="w-full bg-[#FAF9EE] rounded px-2 py-1 border border-black focus:ring-blue-900 " required
          />
        </div>

        <!-- From/To Time -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block font-medium mb-1">From :</label>
            <input
              type="time"
              v-model="from_time"
              class="w-full bg-[#FAF9EE] rounded px-2 py-1 border border-black focus:ring-blue-900 " required
            />
          </div>
          <div>
            <label class="block font-medium mb-1">To :</label>
            <input
              type="time"
              v-model="to_time"
              class="w-full bg-[#FAF9EE] rounded px-2 py-1 border border-black focus:ring-blue-900 " required/>
          </div>
        </div>
      </div>

      <!-- Right: Description -->
      <div class="w-full md:w-[40%]">
        <label class="block font-medium mb-1">Description :</label>
        <textarea
          v-model="description"
          rows="11"
          class="w-full h-full bg-[#FAF9EE] rounded px-2 py-1 border border-black resize-none focus:ring-blue-900" required/>
      </div>
    </div>

    <!-- Submit Button -->
    <div class="pt-4 align-middle">
      <button
        type="submit"
        class="bg-black text-white px-6 py-2 rounded shadow hover:bg-blue-900 w-fit focus:ring-blue-900 focus:focus:bg-blue-900 align-middle">
        {{ name ? 'Update Booking' : 'Book Now' }}
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted, computed, watch, defineProps, defineEmits } from 'vue'
import { api } from '@/api'
import { useRoute } from 'vue-router';

const route = useRoute();


const emit = defineEmits(['bookingUpdated'])   //emits an event back to the parent when a booking is created/updated.
const props = defineProps({                     // gets the editBooking prop to handle update mode.
  editBooking: Object, 
  loggedInUser: String  
})

// These ref variables store form input values.
const subject = ref('')
const selectedRoom = ref('')
const invitees_emails = ref('')
const description = ref('')
const date = ref('')
const from_time = ref('')
const to_time = ref('')
const name = ref(null)
const booked_by=ref('')

// User search and suggestion are handled with:
// filteredUsers (computed)
// onAttendeeInput, highlightNext, highlightPrev, selectCustomOrHighlighted (keyboard navigation)
// addAttendee and removeAttendee manage the email list.

const attendeesEmails = ref([])
const attendeeInput = ref('')
const allUsers = ref([])
const showSuggestions = ref(false)
const highlightedIndex = ref(-1)

const onAttendeeInput = () => {
  showSuggestions.value = !!attendeeInput.value
  highlightedIndex.value = 0
}

const filteredUsers = computed(() => {
  const input = attendeeInput.value.toLowerCase()
  return allUsers.value.filter(user =>
    user.name.toLowerCase().includes(input) || user.email.toLowerCase().includes(input)
  )
})

const addAttendee = (email) => {
  if (email && !attendeesEmails.value.includes(email)) {
    attendeesEmails.value.push(email)
  }
  attendeeInput.value = ''
  showSuggestions.value = false
}

const removeAttendee = (index) => {
  attendeesEmails.value.splice(index, 1)
}

const highlightNext = () => {
  if (highlightedIndex.value < filteredUsers.value.length - 1) highlightedIndex.value++
}

const highlightPrev = () => {
  if (highlightedIndex.value > 0) highlightedIndex.value--
}

const selectCustomOrHighlighted = () => {
  const selected = filteredUsers.value[highlightedIndex.value]
  if (selected) {
    addAttendee(selected.email)
  } else if (attendeeInput.value.includes('@')) {
    addAttendee(attendeeInput.value.trim())
  }
}

// Makes a GET request to the Frappe endpoint to get room names.
const availableRooms = ref([])

const fetchRooms = async () => {
  try {
    const res = await api.get('/Room', {
      params: {
        fields: JSON.stringify(['name', 'room']),
        limit_page_length: 100
      }
    })
    availableRooms.value = res.data.data
  } catch (error) {
    console.error('Error fetching rooms:', error)
  }
}

// Makes a GET request to the Frappe endpoint to get user names and emails.
// The response is stored in allUsers ref variable.
// The data is used for the attendee input field and suggestions.

const fetchAttendees = async () => {
  try {
    const res = await api.get('/User', {
      params: {
        fields: JSON.stringify(['name', 'email']),
        filters: JSON.stringify([['enabled', '=', 1]]),
        limit_page_length: 100
      }
    })
    allUsers.value = res.data.data
  } catch (error) {
    console.error('Error fetching attendees:', error)
  }
}


//When editing, this block populates form fields with data from editBooking.Watch for editBooking prop change

watch(() => props.editBooking, (newVal) => {
  if (newVal) {
    name.value = newVal.name
    subject.value = newVal.subject
    selectedRoom.value = newVal.room
    date.value = newVal.date
    from_time.value = newVal.from_time
    to_time.value = newVal.to_time
    description.value = newVal.description || ''
    // Safe handling for invitees_emails
    if (Array.isArray(newVal.invitees_emails)) {
      invitees_emails.value = newVal.invitees_emails.join(', ')
    } else {
      invitees_emails.value = newVal.invitees_emails || ''
    }
    // Set attendees emails
    //console.log('Attendees Emails:', newVal.attendees_emails)
    attendeesEmails.value = (newVal.attendees_emails || []).map(a => a.email_ids)
    name.value = newVal.name    
  }
}, { immediate: true })

// Create: Uses POST /api/resource/Room Reservation.
// Update: Uses PUT /api/resource/Room Reservation/[name].
// Payload includes subject, room, date, time, attendees, invitees, and description.


const submitForm = async () => {
// console.log('Submitting form with:', {
//     subject: subject.value,
//     room: selectedRoom.value,
//     attendees_emails: attendeesEmails.value.map(email => ({ email_ids: email })),
//     invitees_emails: invitees_emails.value,
//     description: description.value,
//     date: date.value,
//     from_time: from_time.value,
//     to_time: to_time.value
//   })
   if (!validateTimes()) {
    alert(timeError.value)
    return
  }
  const payload = {    
  subject: subject.value,
  room: selectedRoom.value,
  attendees_emails: attendeesEmails.value.map(email => ({ email_ids: email })),
  // Convert invitees_emails to a comma-separated string    
  invitees_emails: invitees_emails.value.split(/[\n,]+/).map(e => e.trim()).filter(Boolean).join(','),
  description: description.value,
  date: date.value,
  from_time: from_time.value,
  to_time: to_time.value,
  booked_by: props.loggedInUser
}


  try {
    if (name.value) {
      await api.put(`/Room Reservation/${name.value}`, payload)
      alert('Booking updated successfully!')
    } else {
      await api.post('/Room Reservation', payload)
      alert('Booking created successfully!')
    }

    emit('bookingUpdated')
    resetForm()
  } catch (error) {
    // console.error('Booking failed:', error)
    const message=error.response?.data?.message || 'Booking Failed'
    alert(`Slot not Available:${message}`)
  }
}

// Clears all form fields after submission.
const resetForm = () => {
  subject.value = ''
  selectedRoom.value = ''
  invitees_emails.value = ''
  description.value = ''
  date.value = ''
  from_time.value = ''
  to_time.value = ''
  attendeesEmails.value = []
  name.value = null
}

// On mount before update the room resevation routing from 
// onMounted(() => {
//   fetchRooms()
//   fetchAttendees()
// })

// Auto-select room if passed via route of Room.vue on click of Reserve button.
onMounted(() => {
  if (route.params.roomName) {
    selectedRoom.value = route.params.roomName;
  }
  fetchRooms();
  fetchAttendees();
});

//Ensures from_time is earlier than to_time.
const timeError = ref('')

const validateTimes = () => {
  if (from_time.value && to_time.value) {
    const [fromH, fromM] = from_time.value.split(':').map(Number)
    const [toH, toM] = to_time.value.split(':').map(Number)
    const fromMinutes = fromH * 60 + fromM
    const toMinutes = toH * 60 + toM

    if (fromMinutes >= toMinutes) {
      timeError.value = "'From' time must be earlier than 'To' time."
      return false
    } else {
      timeError.value = ''
      return true
    }
  }
  timeError.value = ''
  return true
}
</script>
