<!-- <template>
  <header class="fixed top-0 left-0 w-full z-50 flex items-center justify-between px-6 py-4 bg-gray-900 shadow-md">
    <!-- Logo -->
    <!-- <div class="flex items-center gap-3 text-white">
      <router-link to="/" class="flex items-center gap-3">
        <img src="http://pspl.com:8000/files/precimeet_logo.png" class="w-6.5 h-6.5 bg-black" alt="logo" />
        <span class="text-xl font-bold text-green-300">PreciMeet</span>
      </router-link>
    </div> -->

    <!-- Navigation -->
    <!-- <nav class="flex items-center gap-4">
      <router-link to="/Room"
        class="px-4 py-1 border border-black bg-white text-black rounded hover:bg-blue-900 hover:text-black transition">
        Meeting Rooms
      </router-link>

      <!-- Dynamic Avatar -->
      <!-- FIX: Wrap avatar and dropdown inside `.dropdown` -->
      <!-- <div class="relative dropdown">
        <!-- Trigger -->
        <!-- <div class="flex items-center space-x-2 cursor-pointer" @click="toggleDropdown">
          <UserAvatar :full-name="loggedInUser" :image-url="userImageUrl" />
        </div> -->

        <!-- Dropdown -->
        <!-- <div v-if="showDropdown" class="absolute right-0 mt-2 w-48 bg-white shadow-lg rounded-md z-10">
          <button class="block w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100" @click="logoutUser">
            Logout
          </button>
        </div>
      </div>
    </nav>
  </header>
</template>
<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const showDropdown = ref(false)
const dropdownRef = ref(null)

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const logoutUser = async () => {
  try {
    await fetch('/logout', {
      method: 'GET',
      credentials: 'include'
    });
    window.location.href = '/login';
  } catch (error) {
    console.error('Logout failed:', error);
  }
};

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    showDropdown.value = false;
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
defineProps({
  fullName: String,
  imageUrl: String
})


</script> -->  
