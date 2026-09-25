<template>
  <div
    class="day-cell"
    :class="{
      'other-month': !day.isCurrentMonth,
      'is-today': day.isToday
    }"
    @dblclick="$emit('edit-day', day)"
  >
    <div class="day-header">
      <span class="day-number">{{ day.dayNumber }}</span>
    </div>
    <div class="day-content">
      <p v-if="day.content">{{ day.content }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  day: {
    type: Object,
    required: true
    // Expected shape: { date: '2026-09-24', dayNumber: 24, isCurrentMonth: true, isToday: true, content: '...' }
  }
})

defineEmits(['edit-day'])
</script>

<style scoped>
.day-cell {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  padding: 8px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: border-color 0.2s;
  min-height: 100px;
}

.day-cell:hover {
  border-color: #cbd5e1;
}

.other-month {
  background-color: #f8fafc;
  color: #94a3b8;
}

.is-today {
  border: 2px solid #3b82f6;
  background-color: #eff6ff;
}

.day-header {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 4px;
}

.day-number {
  font-size: 0.85rem;
  font-weight: 600;
  color: #334155;
}

.other-month .day-number {
  color: #94a3b8;
}

.day-content {
  font-size: 0.75rem;
  color: #475569;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}
</style>
