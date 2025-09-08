<template>
  <div class="neu-input-wrapper">
    <label v-if="label" :for="inputId" class="neu-input-label">
      {{ label }}
    </label>
    <div class="neu-input-container">
      <input
        :id="inputId"
        :type="type"
        :placeholder="placeholder"
        :value="modelValue"
        :disabled="disabled"
        :readonly="readonly"
        class="neu-input"
        @input="handleInput"
        @focus="handleFocus"
        @blur="handleBlur"
      />
      <div v-if="$slots.icon" class="neu-input-icon">
        <slot name="icon"></slot>
      </div>
    </div>
    <div v-if="error" class="neu-input-error">
      {{ error }}
    </div>
    <div v-else-if="hint" class="neu-input-hint">
      {{ hint }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'NeuInput',
  props: {
    modelValue: {
      type: [String, Number],
      default: ''
    },
    type: {
      type: String,
      default: 'text'
    },
    label: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    },
    readonly: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: ''
    },
    hint: {
      type: String,
      default: ''
    }
  },
  computed: {
    inputId() {
      return `neu-input-${Math.random().toString(36).substr(2, 9)}`;
    }
  },
  methods: {
    handleInput(event) {
      this.$emit('update:modelValue', event.target.value);
    },
    handleFocus(event) {
      this.$emit('focus', event);
    },
    handleBlur(event) {
      this.$emit('blur', event);
    }
  }
}
</script>

<style scoped>
.neu-input-wrapper {
  margin-bottom: var(--spacing-md);
}

.neu-input-label {
  display: block;
  margin-bottom: var(--spacing-sm);
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.875rem;
}

.neu-input-container {
  position: relative;
}

.neu-input-icon {
  position: absolute;
  right: var(--spacing-md);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
}

.neu-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.neu-input:readonly {
  background: var(--bg-secondary);
}

.neu-input-error {
  margin-top: var(--spacing-sm);
  color: var(--accent-error);
  font-size: 0.75rem;
}

.neu-input-hint {
  margin-top: var(--spacing-sm);
  color: var(--text-muted);
  font-size: 0.75rem;
}
</style>