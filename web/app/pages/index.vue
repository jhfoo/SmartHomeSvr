<template>
  Index
  <template v-if="rooms">
    <div v-for="room in rooms" :key="room.id">
      <router-link :to="`/room/${room.id}`">{{ room.id }}</router-link>
      <a :href="`/room/${room.id}`">{{ room.id }}</a>
    </div>
  </template>
  <div>{{ pending }}</div>
  <div>{{ error }}</div>
  <button @click="onLoadRooms">fetch</button>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const menu = ref({})
const rooms = ref([])
const error = ref('')
const pending = ref(false)
const URL_MENU_BASE = 'http://192.168.108.18:3002/api'

try {
  onLoadRooms()
} catch (err) {
  console.error('Error fetching menu:', err)
}
async function onLoadRooms() {
  rooms.value = []

  console.log('Loading rooms...')
  const data = await $fetch(`${URL_MENU_BASE}/menu/all?id=home`)
  if (data && 'rooms' in data) {
    rooms.value = data.rooms
  } else {
    console.error('No rooms found in the response')
  }
}
// try {
//   const response = await fetch(`${URL_MENU_BASE}/menu/all`)
//   const data = await response.json()
//   console.log(data)
// } catch (error) {
//   console.error('Error fetching menu:', error)
// }
</script>