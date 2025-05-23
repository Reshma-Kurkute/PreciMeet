<!-- components/UserAvatar.vue -->
<template>
  <div
    class="w-10 h-10 rounded-full bg-gray-200 text-gray-700 font-semibold flex items-center justify-center overflow-hidden"
  >
    <img
      v-if="image"
      :src="image"
      alt="Avatar"
      class="w-full h-full object-cover"
      @error="onImageError"
    />
    <span v-else>{{ initials }}</span>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  fullName: String,
  imageUrl: String
})

const showImage = ref(true)

const image = computed(() => (showImage.value ? props.imageUrl : ''))

const onImageError = () => {
  showImage.value = false
}

const initials = computed(() => {
  if (!props.fullName) return ''
  const parts = props.fullName.trim().split(' ')
  const first = parts[0]?.[0] || ''
  const last = parts.length > 1 ? parts[parts.length - 1][0] : ''
  return (first + last).toUpperCase()
})
</script>
