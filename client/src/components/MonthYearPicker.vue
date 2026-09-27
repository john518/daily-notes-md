<template>
  <div class="month-year-picker">
    <!-- Month Select -->
    <select v-model.number="draftMonth" class="picker-select">
      <option v-for="m in months" :value="m.value" :key="m.value">
        {{ m.name }}
      </option>
    </select>

    <!-- Year Select (2000 to Current Year) -->
    <select v-model.number="draftYear" class="picker-select">
      <option v-for="y in availableYears" :value="y" :key="y">
        {{ y }}
      </option>
    </select>

    <!-- Action Buttons -->
    <div class="picker-actions">
      <button class="btn-go" @click="handleGo" title="Jump to selected month">Go</button>
      <button class="btn-reset" @click="handleReset" title="Reset to current month">Today</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// Define props coming from the parent view so we stay in sync with next/prev arrows
const props = defineProps({
  year: {
    type: Number,
    required: true
  },
  month: {
    type: Number,
    required: true
  }
})

// Define events emitted back to the parent
const emit = defineEmits(['jump'])

// Local draft state so selection doesn't instantly fire on change
const draftYear = ref(props.year)
const draftMonth = ref(props.month)

// Watch for external changes (e.g. user clicking "Next" or "Previous" month arrows)
watch(() => props.year, (newVal) => { draftYear.value = newVal })
watch(() => props.month, (newVal) => { draftMonth.value = newVal })

// Month options list
const months = [
  { value: 1, name: 'January' },
  { value: 2, name: 'February' },
  { value: 3, name: 'March' },
  { value: 4, name: 'April' },
  { value: 5, name: 'May' },
  { value: 6, name: 'June' },
  { value: 7, name: 'July' },
  { value: 8, name: 'August' },
  { value: 9, name: 'September' },
  { value: 10, name: 'October' },
  { value: 11, name: 'November' },
  { value: 12, name: 'December' },
]

// Dynamically generate years from current year down to 2000
const availableYears = computed(() => {
  const currentYear = new Date().getFullYear()
  const years = []
  for (let y = currentYear; y >= 2000; y--) {
    years.push(y)
  }
  return years
})

// Triggered when user clicks "Go"
const handleGo = () => {
  emit('jump', { year: draftYear.value, month: draftMonth.value })
}

// Triggered when user clicks "Today" (snaps back to current system date)
const handleReset = () => {
  const now = new Date()
  draftYear.value = now.getFullYear()
  draftMonth.value = now.getMonth() + 1
  emit('jump', { year: draftYear.value, month: draftMonth.value })
}
</script>

<style scoped>
.month-year-picker {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: white;
  /* Reduced container padding */
  padding: 0.4rem 0.5rem;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.picker-select {
  /* Slimmed down vertical padding, tighter font */
  padding: 0.15rem 0.3rem;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  font-size: 0.85rem;
  background: #fff;
  color: #1e293b;
  cursor: pointer;
}

.picker-select:focus {
  outline: none;
  border-color: #3b82f6;
}

.picker-actions {
  display: flex;
  gap: 0.25rem;
  margin-left: 0.1rem;
}

button {
  /* Match the slim profile of the selects */
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid transparent;
}

.btn-go {
  background: #2563eb;
  color: white;
}

.btn-go:hover {
  background: #1d4ed8;
}

.btn-reset {
  background: #f1f5f9;
  color: #475569;
  border-color: #cbd5e1;
}

.btn-reset:hover {
  background: #e2e8f0;
}
</style>
