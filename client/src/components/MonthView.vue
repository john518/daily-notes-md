<template>
  <div class="month-container">
    <!-- Header Navigation -->
    <div class="calendar-header">
      <button class="nav-btn" @click="prevMonth">&lt;</button>
      <h2>{{ monthNames[currentMonth - 1] }} {{ currentYear }}</h2>
      <button class="nav-btn" @click="nextMonth">&gt;</button>
    </div>

    <!-- Weekday Labels -->
    <div class="weekdays-grid">
      <div v-for="day in weekdays" :key="day" class="weekday-label">{{ day }}</div>
    </div>

    <!-- Days Grid -->
    <div class="days-grid">
      <DayCell
        v-for="(day, index) in days"
        :key="index"
        :day="day"
        @edit-day="openEditor"
      />
    </div>

    <!-- Popup Editor Modal -->
    <DayEditorModal
      v-if="activeDay"
      :day="activeDay"
      @close="closeEditor"
      @save="saveEntry"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DayCell from './DayCell.vue'
import DayEditorModal from './DayEditorModal.vue' // <-- 1. Import the modal

const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const monthNames = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
]

const days = ref([])
const currentYear = ref(new Date().getFullYear())
const currentMonth = ref(new Date().getMonth() + 1)
const activeDay = ref(null)

// Used at startup to check that Python-Javascript bridge is instantiated
const waitForApi = async (timeoutMs = 3000) => {
  const startTime = Date.now()

  while (
    !window.pywebview ||
    !window.pywebview.api ||
    typeof window.pywebview.api.get_month_data !== 'function'
  ) {
    if (Date.now() - startTime > timeoutMs) {
      throw new Error("Timeout: Pywebview API failed to initialize.")
    }
    await new Promise(resolve => setTimeout(resolve, 50))
  }
}

const loadMonthData = async () => {
  try {
    const data = await window.pywebview.api.get_month_data(currentYear.value, currentMonth.value)
    days.value = data
  } catch (err) {
    console.error("Failed to fetch month data:", err)
  }
}

const prevMonth = () => {
  currentMonth.value -= 1
  if (currentMonth.value < 1) {
    currentMonth.value = 12
    currentYear.value -= 1
  }
  loadMonthData()
}

const nextMonth = () => {
  currentMonth.value += 1
  if (currentMonth.value > 12) {
    currentMonth.value = 1
    currentYear.value += 1
  }
  loadMonthData()
}

// 3. Modal open/close handlers
const openEditor = (day) => {
  activeDay.value = day
}

const closeEditor = () => {
  activeDay.value = null
}

// Handle saving the note back to Python
const saveEntry = async (payload) => {
  console.log('Saving entry for fileKey:', payload.fileKey, payload.content)

  if (window.pywebview && window.pywebview.api) {
    try {
      // We will define this save method in Python next!
      await window.pywebview.api.save_note(payload.fileKey, payload.content)

      // Update local state so the cell immediately shows snippet changes if needed
      const target = days.value.find(d => d.fileKey === payload.fileKey)
      if (target) {
        target.content = payload.content
      }
    } catch (err) {
      console.error("Failed to save note via Python API:", err)
    }
  }

  closeEditor()
}

onMounted(async () => {
  try {
    await waitForApi()
    // Extra safety buffer for the IPC pipe
    await new Promise(resolve => setTimeout(resolve, 100))
    await loadMonthData()
  } catch (err) {
    console.error("Initialization error:", err)
    // Optional: set a reactive error state to show a friendly banner in the UI
  }
})
</script>

<style scoped>
/* Keep your existing style rules here */
.month-container {
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  font-family: inherit;
}

.calendar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding: 0 1rem;
}

.calendar-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
}

.nav-btn {
  background: none;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-size: 1rem;
  color: #475569;
  transition: background-color 0.2s;
}

.nav-btn:hover {
  background-color: #f1f5f9;
}

.weekdays-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  background-color: #f1f5f9;
  border-top: 1px solid #cbd5e1;
  border-left: 1px solid #cbd5e1;
  border-right: 1px solid #cbd5e1;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}

.weekday-label {
  text-align: center;
  font-weight: 600;
  font-size: 0.85rem;
  color: #475569;
  padding: 0.75rem 0;
}

.days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  grid-auto-rows: minmax(0, 1fr);
  flex: 1;
  border: 1px solid #cbd5e1;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  background-color: #cbd5e1;
  gap: 1px;
  min-height: 0;
}
</style>
