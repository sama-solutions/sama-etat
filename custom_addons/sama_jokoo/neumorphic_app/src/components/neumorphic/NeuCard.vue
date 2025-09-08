<template>
  <div :class="cardClasses">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'NeuCard',
  props: {
    variant: {
      type: String,
      default: 'default',
      validator: (value) => ['default', 'inset', 'flat'].includes(value)
    },
    hoverable: {
      type: Boolean,
      default: true
    },
    padding: {
      type: String,
      default: 'normal',
      validator: (value) => ['none', 'small', 'normal', 'large'].includes(value)
    }
  },
  computed: {
    cardClasses() {
      return [
        'neu-card',
        `neu-card--${this.variant}`,
        `neu-card--padding-${this.padding}`,
        {
          'neu-card--hoverable': this.hoverable
        }
      ];
    }
  }
}
</script>

<style scoped>
.neu-card--hoverable:hover {
  transform: translateY(-2px);
  box-shadow: 
    12px 12px 24px var(--shadow-dark),
    -12px -12px 24px var(--shadow-light);
}

.neu-card--padding-none {
  padding: 0;
}

.neu-card--padding-small {
  padding: var(--spacing-sm);
}

.neu-card--padding-normal {
  padding: var(--spacing-md);
}

.neu-card--padding-large {
  padding: var(--spacing-lg);
}
</style>