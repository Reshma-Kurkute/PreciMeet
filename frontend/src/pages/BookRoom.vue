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
            class="w-full bg-blue-200 rounded px-2 py-1 border border-black focus:outline-none focus:ring-[#d1930d] focus:border-[#d1930d] "required>
        </div>

        <!-- Select Room -->
        <div>
          <label class="block font-medium mb-1">Select Room :</label>
          <select
            v-model="selectedRoom"
            class="w-full bg-blue-200 rounded px-2 py-1 border border-black focus:outline-none focus:ring-[#d1930d] focus:border-[#d1930d]" required
          >
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
            class="w-full bg-blue-200 rounded px-2 py-1 border border-black focus:outline-none focus:ring-[#d1930d] focus:border-[#d1930d]"
            placeholder="Type to search users..." 
          />

          <!-- Suggestion Dropdown -->
          <ul v-if="filteredUsers.length && showSuggestions" class="absolute bg-white shadow border w-full mt-1 rounded z-10 max-h-40 overflow-auto">
            <li
              v-for="(user, index) in filteredUsers"
              :key="user.email"
              :class="['px-4 py-2 cursor-pointer', index === highlightedIndex ? 'bg-blue-200 text-black' : 'hover:bg-[#dfece9]']"
              @click="addAttendee(user.email)"
            >
              {{ user.name }} ({{ user.email }})
            </li>
          </ul>

          <!-- Display Selected Emails -->
          <div class="mt-2 flex flex-wrap gap-2">
            <span
              v-for="(email, index) in attendeesEmails"
              :key="index"
              class="bg-[#295a50] text-white px-2 py-1 rounded-full text-sm flex items-center gap-1"
            >
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
            class="w-full bg-blue-200 rounded px-2 py-1 border border-black focus:ring-[#d1930d] focus:border-[#d1930d]"
          />
        </div>

        <!-- Date -->
        <div>
          <label class="block font-medium mb-1">Date :</label>
          <input
            type="date"
            v-model="date"
            class="w-full bg-blue-200 rounded px-2 py-1 border border-black focus:ring-[#d1930d] focus:border-[#d1930d]" required
          />
        </div>

        <!-- From/To Time -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block font-medium mb-1">From :</label>
            <input
              type="time"
              v-model="from_time"
              class="w-full bg-blue-200 rounded px-2 py-1 border border-black focus:ring-[#d1930d] focus:border-[#d1930d]" required
            />
          </div>
          <div>
            <label class="block font-medium mb-1">To :</label>
            <input
              type="time"
              v-model="to_time"
              class="w-full bg-blue-200 rounded px-2 py-1 border border-black focus:ring-[#d1930d] focus:border-[#d1930d]" required
            />
          </div>
        </div>
      </div>

      <!-- Right: Description -->
      <div class="w-full md:w-[40%]">
        <label class="block font-medium mb-1">Description :</label>
        <textarea
          v-model="description"
          rows="11"
          class="w-full h-full bg-blue-200 rounded px-2 py-1 border border-black resize-none focus:ring-[#d1930d] focus:border-[#d1930d]" required
        />
      </div>
    </div>

    <!-- Submit Button -->
    <div class="pt-4 align-middle">
      <button
        type="submit"
        class="bg-black text-white px-6 py-2 rounded shadow hover:bg-gray-800 w-fit focus:ring-[#d1930d] focus:border-[#d1930d]">
        Book Now
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { api } from '@/api'

const subject = ref('')
const selectedRoom = ref('')
const invitees_emails = ref('')
const description = ref('')
const date = ref('')
const from_time = ref('')
const to_time = ref('')
const availableRooms = ref([])

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
  return allUsers.value.filter(
    user => user.name.toLowerCase().includes(input) || user.email.toLowerCase().includes(input)
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

const fetchRooms = async () => {
  try {
    const response = await api.get('/Room', {
      params: {
        fields: JSON.stringify(['name', 'room']),
        limit_page_length: 100
      }
    })
    availableRooms.value = response.data.data
  } catch (error) {
    console.error('Error fetching rooms:', error)
  }
}

const fetchAttendees = async () => {
  try {
    const response = await api.get('/User', {
      params: {
        fields: JSON.stringify(['name', 'email']),
        filters: JSON.stringify([['enabled', '=', 1]]),
        limit_page_length: 100
      }
    })
    allUsers.value = response.data.data
  } catch (error) {
    console.error('Error fetching attendees:', error)
  }
}

const submitForm = async () => {
  const payload = {
    subject: subject.value,
    room: selectedRoom.value,
    attendees_emails: attendeesEmails.value.map(email => ({ email_ids: email })),
    invitees_emails: invitees_emails.value.split(/[\n,]+/).map(e => e.trim()).filter(Boolean).join(','),
    description: description.value,
    date: date.value,
    from_time: from_time.value,
    to_time: to_time.value
  }

  try {
    if (props.booking?.name) {
      // EDIT existing booking
      await api.put(`/api/resource/Room Reservation/${props.booking.name}`, payload)
      alert('Booking updated successfully!')
    } else {
      // CREATE new booking
      await api.post('/api/resource/Room Reservation', payload)
      alert('Booking created successfully!')
    }
    emit('submitted')
  } catch (error) {
    console.error('Booking failed:', error)
    alert('Booking failed. Check console for error details.')
  }
}
// emit('submitted')

onMounted(() => {
  fetchRooms()
  fetchAttendees()
})

// for reuse the form for edit booking
const props = defineProps({
  booking: {
    type: Object,
    default: null
  }
})
const emit = defineEmits(['submitted'])

//now reference declaration for load the fields
onMounted(() => {
  fetchRooms()
  fetchAttendees()

  if (props.booking) {
    subject.value = props.booking.subject
    selectedRoom.value = props.booking.room
    date.value = props.booking.date
    from_time.value = props.booking.from_time
    to_time.value = props.booking.to_time
    description.value = props.booking.description
    invitees_emails.value = props.booking.invitees_emails || ''
    attendeesEmails.value = (props.booking.attendees_emails || []).map(a => a.email_ids)
  }
})



</script>
