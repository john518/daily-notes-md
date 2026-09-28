<template>
  <div class="month-container">
    <!-- Header Navigation -->
    <div class="calendar-header">
      <button class="nav-btn" @click="prevMonth">&lt;</button>
      <h2>{{ monthNames[currentMonth - 1] }} {{ currentYear }}</h2>

      <!-- Right side of header container -->
      <div class="header-nav-right">

        <!-- Calendar Icon Toggle & Popover Wrapper -->
        <div class="date-picker-wrapper">
          <!-- The Popover Component -->
          <MonthYearPicker
          v-if="showDatePicker"
          :year="currentYear"
          :month="currentMonth"
          @jump="onJumpToDate"
          />

          <!-- The Calendar Button/Icon -->
          <button @click="toggleDatePicker" class="icon-trigger-btn" title="Select Month/Year">
            <!-- Clean inline SVG Calendar Icon -->
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
          </button>
        </div>

        <button class="nav-btn" @click="nextMonth">&gt;</button>
      </div>
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
      @closed="onEditorClosed"
      @saved="onDaySaved"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DayCell from './DayCell.vue'
import DayEditorModal from './DayEditorModal.vue' // <-- 1. Import the modal
import MonthYearPicker from './MonthYearPicker.vue'

const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const monthNames = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
]

const days = ref([])
const currentYear = ref(new Date().getFullYear())
const currentMonth = ref(new Date().getMonth() + 1)
const activeDay = ref(null)
const showDatePicker = ref(false)

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

const toggleDatePicker = () => {
  showDatePicker.value = !showDatePicker.value
}

const onJumpToDate = ({ year, month }) => {
  currentMonth.value = month
  currentYear.value = year
  loadMonthData()
  showDatePicker.value = false // close the popover
}

// Modal open/close handlers
const openEditor = (day) => {
  activeDay.value = day
}

const onEditorClosed = () => {
  activeDay.value = null
}

// Update after day entry saved
const onDaySaved = ({ fileKey, content }) => {
  // Map creates a new array reference, guaranteeing Vue triggers a re-render
  days.value = days.value.map(day => {
    if (day.fileKey === fileKey) {
      return { ...day, content: content } // Return a new object with updated content
    }
    return day
  })
}

onMounted(async () => {
  // NOTE: APPLICATION IS RESPONSIBLE FOR ENSURING PYTHON-JAVASCRIPT BRIDGE (API) IS READY
  await loadMonthData()
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
  margin: 0;
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


/* In MonthView.vue <style scoped> */
.header-nav-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.date-picker-wrapper {
  position: relative; /* Acts as the anchor point for the absolute dropdown */
  display: inline-block;
}

.icon-trigger-btn {
  background: transparent;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  padding: 0.35rem 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  color: #475569;
}

.icon-trigger-btn:hover {
  background: #f1f5f9;
  color: #1e293b;
}.date-picker-wrapper :deep(.month-year-picker) {
  position: absolute;
  right: 0;
  top: calc(100% + 6px);
  z-index: 100;
  white-space: nowrap;
}

/* Position the popover directly to the left of the icon button */
.date-picker-wrapper :deep(.month-year-picker) {
  position: absolute;
  right: calc(100% + 8px);   /* Push it to the left of the wrapper with an 8px gap */
  top: 50%;                  /* Center it vertically relative to the icon button */
  transform: translateY(-50%); /* Perfect vertical centering */
  z-index: 100;
  white-space: nowrap;
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
