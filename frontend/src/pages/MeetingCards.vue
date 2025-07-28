<template>
  <div class="overflow-y-auto flex-1 custom-scrollbar">
    <template v-if="meetings.length">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div
          v-for="meeting in meetings"
          :key="meeting.name"
          class="bg-[#f9f9f9] p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between"
        >
          <div class="flex justify-between items-start mb-2">
            <h3 class="text-black text-xl font-extrabold truncate">
              {{ meeting.subject }}
            </h3>
            <slot name="actions" :meeting="meeting" />
          </div>
          <div class="font-semibold text-lg text-gray-700 space-y-1 mb-2">
            <div class="flex items-center gap-1"><span>📍</span><span>{{ meeting.room }}</span></div>
            <div class="flex items-center gap-1"><span>🕒</span><span>{{ meeting.from_time }} - {{ meeting.to_time }}</span></div>
            <div class="flex items-center gap-1"><span>📅</span><span>{{ meeting.date }}</span></div>
          </div>
          <div class="flex items-center justify-between mt-2">
            <div class="text-lg text-black font-semibold">
              Organizer: {{ meeting.booked_by || 'N/A' }}
            </div>
            <div class="flex -space-x-2">
              <img
                v-for="(person, index) in meeting.participants || []"
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
</template>

<script setup>
defineProps({
  meetings: Array
})
</script>
