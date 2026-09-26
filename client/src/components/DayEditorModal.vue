<template>
  <div class="modal-backdrop" @click.self="close">
    <div class="modal-card">
      <!-- Modal Header -->
      <div class="modal-header">
        <h3>Journal Entry — {{ formatDate(day.date) }}</h3>
        <button class="close-btn" @click="close">&times;</button>
      </div>

      <!-- Mode Tabs -->
      <div class="tab-bar">
        <button
          :class="{ active: currentTab === 'edit' }"
          @click="currentTab = 'edit'"
        >
          Edit
        </button>
        <button
          :class="{ active: currentTab === 'preview' }"
          @click="currentTab = 'preview'"
        >
          Preview
        </button>
      </div>

      <!-- Modal Body -->
      <div class="modal-body">
        <textarea
          v-show="currentTab === 'edit'"
          v-model="editableContent"
          placeholder="Write your journal entry in markdown... (e.g., # Today's Notes)"
          ref="textareaRef"
        ></textarea>

        <div
          v-show="currentTab === 'preview'"
          class="markdown-preview"
          v-html="renderedMarkdown"
        ></div>
      </div>

      <!-- Modal Footer -->
      <div class="modal-footer">
        <button class="btn secondary" @click="close">Cancel</button>
        <button class="btn primary" @click="save">Save Entry</button>
      </div>

      <!-- Custom visual resize indicator (optional, makes it obvious) -->
      <div class="resize-handle"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'isomorphic-dompurify'

const props = defineProps({
  day: {
    type: Object,
    required: true
    // Expected shape: { date: '2026-09-24', fileKey: '260924', content: '...' }
  }
})

const emit = defineEmits(['close', 'save'])

const currentTab = ref('edit')
const editableContent = ref(props.day.content || '')
const textareaRef = ref(null)

// Safely parse and sanitize markdown for preview tab
const renderedMarkdown = computed(() => {
  const rawHtml = marked.parse(editableContent.value || '_Nothing to preview yet..._')
  return DOMPurify.sanitize(rawHtml)
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }
  // Fix timezone shift by splitting components manually if needed
  const [year, month, day] = dateStr.split('-')
  const d = new Date(year, month - 1, day)
  return d.toLocaleDateString(undefined, options)
}

const close = () => {
  emit('close')
}

const save = async () => {
  try {
    const response = await window.pywebview.api.save_entry(
      props.day.year,
      props.day.month,
      props.day.day,
      editableContent.value
    )
    if (response.status === 'success') {
      console.log(response.message)
      emit('close')
    }
  } catch (err) {
    console.error("Error saving entry across bridge:", err)
  }
}

onMounted(() => {
  // Auto-focus textarea on open
  if (textareaRef.value) {
    textareaRef.value.focus()
  }
})
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(15, 23, 42, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.modal-card {
  background: #ffffff;

  /* Use explicit initial dimensions instead of pure percentages */
  width: 650px;
  height: 550px;
  max-width: 95vw;
  max-height: 95vh;
  min-width: 450px;
  min-height: 350px;

  border-radius: 12px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);

  resize: both;
  overflow: auto;

  /* Ensures our absolute-positioned handle anchors correctly */
  position: relative;
}

.modal-header {
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e2e8f0;
  background-color: #f8fafc;
}

.modal-header h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #64748b;
}

.close-btn:hover {
  color: #0f172a;
}

.tab-bar {
  display: flex;
  background-color: #f1f5f9;
  padding: 0.5rem 1rem 0 1rem;
  gap: 0.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.tab-bar button {
  background: none;
  border: none;
  padding: 0.5rem 1rem;
  font-weight: 600;
  font-size: 0.85rem;
  color: #64748b;
  cursor: pointer;
  border-top-left-radius: 6px;
  border-top-right-radius: 6px;
  transition: all 0.2s;
}

.tab-bar button.active {
  background: #ffffff;
  color: #2563eb;
  border: 1px solid #e2e8f0;
  border-bottom: none;
}

.modal-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  overflow: hidden;
}

.modal-body textarea {
  width: 100%;
  height: 100%;
  resize: none;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 1rem;
  font-family: inherit;
  font-size: 0.95rem;
  color: #334155;
  outline: none;
  box-sizing: border-box;
}

.modal-body textarea:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.markdown-preview {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
  background-color: #ffffff;
  color: #334155;
  font-size: 0.95rem;
  box-sizing: border-box;
}

/* Basic styling for rendered markdown elements */
.markdown-preview :deep(h1),
.markdown-preview :deep(h2),
.markdown-preview :deep(h3) {
  margin-top: 0;
  color: #1e293b;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
  background-color: #f8fafc;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  border: 1px solid transparent;
}

.btn.secondary {
  background: transparent;
  border-color: #cbd5e1;
  color: #475569;
}

.btn.secondary:hover {
  background: #f1f5f9;
}

.btn.primary {
  background: #2563eb;
  color: white;
}

.btn.primary:hover {
  background: #1d4ed8;
}

/* Custom, easily-grabbable visual cue in the bottom right corner */
.resize-handle {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 16px;
  height: 16px;
  pointer-events: none; /* Let clicks pass through to the native resize zone */

  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'%3E%3Cpath d='M11 1L1 11M11 5L5 11M11 9L9 11' stroke='%23475569' stroke-width='1.5' stroke-linecap='round'/%3E%3C/svg%3E");
  opacity: 0.8;
}
</style>
