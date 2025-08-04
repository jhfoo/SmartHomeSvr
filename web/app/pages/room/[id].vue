<template>
  <a href="/">Home</a>
  <div>{{ data }}</div>
  <template v-if="data && data.rooms">
    {{ data }}
  </template>
  <div>Rooms: {{  RoomCount }}</div>
  <div>Room: {{ room }}</div>
  <div>Pending: {{ pending }}</div>
  <div>Error: {{ error }}</div>
  <div>Debug: {{ debug }}</div>
  <button @click="onLoadRoom">Load</button>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const route = useRoute()
const menu = ref({})
const room = ref({})
const RoomCount = ref(0)
const debug = ref('')
const error = ref('')
const pending = ref(false)
const data = ref({})

const URL_MENU_BASE = 'http://192.168.108.18:3002/api'
try {
  onLoadRoom()
} catch (err) {
  console.error('Error fetching menu:', err)
}

async function onLoadRoom() {
  debug.value = ''
  RoomCount.value = 0

  try {
    const data = await $fetch(`${URL_MENU_BASE}/menu/all?id=room`)
    if ('rooms' in data) {
      RoomCount.value = data.rooms.length
      data.rooms.forEach((ThisRoom) => {
        if (ThisRoom.id === route.params.id) {
          room.value = ThisRoom
        }
        debug.value += JSON.stringify(ThisRoom, null, 2) + '\n'
      })
    } else {
      error.value = 'No rooms found in menu data'
    }
  } catch (err) {
    error.value = `Error fetching menu: ${err.message}`
    console.error(error.value)
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