<script setup>
defineProps({
  fullName: String,
  imageUrl: String
})
</script setup>
<template>
  <header class="fixed top-0 left-0 w-full z-50 flex items-center justify-between px-6 py-4 bg-gray-900 shadow-md">
    <!-- Logo -->
    <div class="flex items-center gap-3 text-white">
      <router-link to="/" class="flex items-center gap-3">
        <img src="http://pspl.com:8000/files/precimeet_logo.png" class="w-6.5 h-6.5 bg-black" alt="logo" />
        <span class="text-xl font-bold text-green-300">PreciMeet</span>
      </router-link>
    </div>

    <!-- Navigation -->
    <nav class="flex items-center gap-4">
      <router-link to="/Room" class="px-4 py-1 border border-black bg-white text-black rounded hover:bg-blue-900 hover:text-black transition">
        Meeting Rooms
      </router-link>

      <!-- Dynamic Avatar -->
      <div class="flex items-center space-x-2">
        <UserAvatar :full-name="fullName" :image-url="imageUrl" />
      </div>
    </nav>
  </header>
</template>
