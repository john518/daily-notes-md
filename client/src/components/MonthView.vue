<template>
  <div class="month-container">
    <!-- Header Navigation -->
    <div class="calendar-header">
      <button class="nav-btn" @click="prevMonth">&lt;</button>
      <h2>September 2026</h2>
      <button class="nav-btn" @click="nextMonth">&gt;</button>
    </div>

    <!-- Weekday Labels -->
    <div class="weekdays-grid">
      <div v-for="day in weekdays" :key="day" class="weekday-label">{{ day }}</div>
    </div>

    <!-- Days Grid (5 weeks = 35 cells) -->
    <div class="days-grid">
      <DayCell
        v-for="(day, index) in days"
        :key="index"
        :day="day"
        @edit-day="handleEditDay"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DayCell from './DayCell.vue'

const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

// Hardcoded initial data matching the September 2026 mockup layout
const days = ref([
  // Week 1
  { date: '2026-08-30', dayNumber: 30, isCurrentMonth: false, isToday: false, content: '' },
  { date: '2026-08-31', dayNumber: 31, isCurrentMonth: false, isToday: false, content: '' },
  { date: '2026-09-01', dayNumber: 1, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-02', dayNumber: 2, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-03', dayNumber: 3, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-04', dayNumber: 4, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-05', dayNumber: 5, isCurrentMonth: true, isToday: false, content: '' },
  // Week 2
  { date: '2026-09-06', dayNumber: 6, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-07', dayNumber: 7, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-08', dayNumber: 8, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-09', dayNumber: 9, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-10', dayNumber: 10, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-11', dayNumber: 11, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-12', dayNumber: 12, isCurrentMonth: true, isToday: false, content: '' },
  // Week 3
  { date: '2026-09-13', dayNumber: 13, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-14', dayNumber: 14, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-15', dayNumber: 15, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-16', dayNumber: 16, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-17', dayNumber: 17, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-18', dayNumber: 18, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-19', dayNumber: 19, isCurrentMonth: true, isToday: false, content: '' },
  // Week 4
  { date: '2026-09-20', dayNumber: 20, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-21', dayNumber: 21, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-22', dayNumber: 22, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-23', dayNumber: 23, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-24', dayNumber: 24, isCurrentMonth: true, isToday: true, content: "a rat in Tom's house may eat Tom's ice cream" }, // Mockup sample entry[cite: 1]
  { date: '2026-09-25', dayNumber: 25, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-26', dayNumber: 26, isCurrentMonth: true, isToday: false, content: '' },
  // Week 5
  { date: '2026-09-27', dayNumber: 27, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-28', dayNumber: 28, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-29', dayNumber: 29, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-09-30', dayNumber: 30, isCurrentMonth: true, isToday: false, content: '' },
  { date: '2026-10-01', dayNumber: 1, isCurrentMonth: false, isToday: false, content: '' },
  { date: '2026-10-02', dayNumber: 2, isCurrentMonth: false, isToday: false, content: '' },
  { date: '2026-10-03', dayNumber: 3, isCurrentMonth: false, isToday: false, content: '' }
])

const prevMonth = () => {
  console.log('Navigate to previous month')
}

const nextMonth = () => {
  console.log('Navigate to next month')
}

const handleEditDay = (day) => {
  console.log('Double clicked day:', day.date)
  // This is where you'll trigger opening the editor view later
}
</script>

<style scoped>
.month-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem;
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
  grid-template-rows: repeat(5, minmax(110px, 1fr));
  border: 1px solid #cbd5e1;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  background-color: #cbd5e1; /* acts as gap lines */
  gap: 1px;
}
</style>
