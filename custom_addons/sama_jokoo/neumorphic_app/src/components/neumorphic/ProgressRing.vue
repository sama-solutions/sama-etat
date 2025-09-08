<template>
  <div class="progress-ring" :style="{ width: size + 'px', height: size + 'px' }">
    <svg
      :width="size"
      :height="size"
      class="progress-ring-svg"
    >
      <!-- Cercle de fond -->
      <circle
        :cx="center"
        :cy="center"
        :r="radius"
        :stroke-width="strokeWidth"
        class="progress-ring-background"
      />
      
      <!-- Cercle de progression -->
      <circle
        :cx="center"
        :cy="center"
        :r="radius"
        :stroke-width="strokeWidth"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="strokeDashoffset"
        :stroke="color"
        class="progress-ring-progress"
        :style="{ 
          transition: `stroke-dashoffset ${animationDuration}ms ease-out`,
          filter: glowEffect ? `drop-shadow(0 0 8px ${color}40)` : 'none'
        }"
      />
    </svg>
    
    <!-- Contenu au centre -->
    <div class="progress-ring-content">
      <slot>
        <span class="progress-percentage">{{ Math.round(progress) }}%</span>
      </slot>
    </div>
  </div>
</template>

<script>
import { computed, ref, watch, onMounted } from 'vue'

export default {
  name: 'ProgressRing',
  props: {
    progress: {
      type: Number,
      default: 0,
      validator: (value) => value >= 0 && value <= 100
    },
    size: {
      type: Number,
      default: 100
    },
    strokeWidth: {
      type: Number,
      default: 8
    },
    color: {
      type: String,
      default: 'var(--accent-primary)'
    },
    backgroundColor: {
      type: String,
      default: 'var(--bg-secondary)'
    },
    animationDuration: {
      type: Number,
      default: 1000
    },
    glowEffect: {
      type: Boolean,
      default: true
    }
  },
  setup(props) {
    const animatedProgress = ref(0)
    
    const center = computed(() => props.size / 2)
    const radius = computed(() => (props.size - props.strokeWidth) / 2)
    const circumference = computed(() => 2 * Math.PI * radius.value)
    
    const strokeDashoffset = computed(() => {
      const progressValue = Math.max(0, Math.min(100, animatedProgress.value))
      return circumference.value - (progressValue / 100) * circumference.value
    })
    
    const animateProgress = (targetProgress) => {
      const startProgress = animatedProgress.value
      const difference = targetProgress - startProgress
      const startTime = Date.now()
      
      const animate = () => {
        const elapsed = Date.now() - startTime
        const progress = Math.min(elapsed / props.animationDuration, 1)
        
        // Fonction d'easing (ease-out-cubic)
        const easeOut = 1 - Math.pow(1 - progress, 3)
        
        animatedProgress.value = startProgress + (difference * easeOut)
        
        if (progress < 1) {
          requestAnimationFrame(animate)
        } else {
          animatedProgress.value = targetProgress
        }
      }
      
      requestAnimationFrame(animate)
    }
    
    watch(() => props.progress, (newProgress) => {
      animateProgress(newProgress)
    })
    
    onMounted(() => {
      // Petit délai pour l'animation d'entrée
      setTimeout(() => {
        animateProgress(props.progress)
      }, 100)
    })
    
    return {
      center,
      radius,
      circumference,
      strokeDashoffset,
      animatedProgress
    }
  }
}
</script>

<style scoped>
.progress-ring {
  position: relative;
  display: inline-block;
}

.progress-ring-svg {
  transform: rotate(-90deg);
  overflow: visible;
}

.progress-ring-background {
  fill: none;
  stroke: var(--bg-secondary);
  opacity: 0.3;
}

.progress-ring-progress {
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.progress-ring-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  pointer-events: none;
}

.progress-percentage {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
}

/* Animation d'entrée */
@keyframes progressRingEntry {
  from {
    stroke-dashoffset: var(--circumference);
    opacity: 0;
  }
  to {
    stroke-dashoffset: var(--stroke-dashoffset);
    opacity: 1;
  }
}

/* Variantes de couleur */
.progress-ring.success .progress-ring-progress {
  stroke: var(--accent-success);
}

.progress-ring.warning .progress-ring-progress {
  stroke: var(--accent-warning);
}

.progress-ring.error .progress-ring-progress {
  stroke: var(--accent-error);
}

/* Effet de pulsation pour les valeurs élevées */
.progress-ring.pulse .progress-ring-progress {
  animation: progressPulse 2s ease-in-out infinite;
}

@keyframes progressPulse {
  0%, 100% {
    opacity: 1;
    filter: drop-shadow(0 0 8px currentColor);
  }
  50% {
    opacity: 0.8;
    filter: drop-shadow(0 0 16px currentColor);
  }
}

/* Responsive */
@media (max-width: 480px) {
  .progress-percentage {
    font-size: 0.75rem;
  }
}
</style>