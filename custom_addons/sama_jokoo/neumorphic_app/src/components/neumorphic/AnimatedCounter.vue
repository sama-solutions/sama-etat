<template>
  <span class="animated-counter">{{ displayValue }}</span>
</template>

<script>
import { ref, watch, onMounted } from 'vue'

export default {
  name: 'AnimatedCounter',
  props: {
    value: {
      type: Number,
      default: 0
    },
    duration: {
      type: Number,
      default: 1000
    },
    formatNumber: {
      type: Boolean,
      default: true
    }
  },
  setup(props) {
    const displayValue = ref(0)
    
    const formatNum = (num) => {
      if (!props.formatNumber) return num.toString()
      
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K'
      }
      return num.toString()
    }
    
    const animateToValue = (targetValue) => {
      const startValue = displayValue.value
      const difference = targetValue - startValue
      const startTime = Date.now()
      
      const animate = () => {
        const elapsed = Date.now() - startTime
        const progress = Math.min(elapsed / props.duration, 1)
        
        // Fonction d'easing (ease-out)
        const easeOut = 1 - Math.pow(1 - progress, 3)
        
        const currentValue = Math.round(startValue + (difference * easeOut))
        displayValue.value = formatNum(currentValue)
        
        if (progress < 1) {
          requestAnimationFrame(animate)
        } else {
          displayValue.value = formatNum(targetValue)
        }
      }
      
      requestAnimationFrame(animate)
    }
    
    watch(() => props.value, (newValue) => {
      animateToValue(newValue)
    })
    
    onMounted(() => {
      animateToValue(props.value)
    })
    
    return {
      displayValue
    }
  }
}
</script>

<style scoped>
.animated-counter {
  font-variant-numeric: tabular-nums;
  transition: color var(--transition-normal);
}
</style>