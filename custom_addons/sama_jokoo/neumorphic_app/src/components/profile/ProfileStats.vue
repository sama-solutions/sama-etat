<template>
  <NeuCard class="profile-stats">
    <h3 class="stats-title">📊 Statistiques</h3>
    
    <div class="stats-grid">
      <!-- Statistique Posts -->
      <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-content">
          <div class="stat-number">
            <AnimatedCounter :value="stats.posts_count || 0" />
          </div>
          <div class="stat-label">Posts publiés</div>
          <div class="stat-trend positive">
            <span class="trend-icon">📈</span>
            <span class="trend-text">+12% ce mois</span>
          </div>
        </div>
      </div>

      <!-- Statistique Likes -->
      <div class="stat-card">
        <div class="stat-icon">❤️</div>
        <div class="stat-content">
          <div class="stat-number">
            <AnimatedCounter :value="stats.likes_received || 0" />
          </div>
          <div class="stat-label">Likes reçus</div>
          <div class="stat-trend positive">
            <span class="trend-icon">📈</span>
            <span class="trend-text">+8% ce mois</span>
          </div>
        </div>
      </div>

      <!-- Statistique Commentaires -->
      <div class="stat-card">
        <div class="stat-icon">💬</div>
        <div class="stat-content">
          <div class="stat-number">
            <AnimatedCounter :value="stats.comments_received || 0" />
          </div>
          <div class="stat-label">Commentaires</div>
          <div class="stat-trend positive">
            <span class="trend-icon">📈</span>
            <span class="trend-text">+15% ce mois</span>
          </div>
        </div>
      </div>

      <!-- Statistique Partages -->
      <div class="stat-card">
        <div class="stat-icon">🔗</div>
        <div class="stat-content">
          <div class="stat-number">
            <AnimatedCounter :value="stats.shares_received || 0" />
          </div>
          <div class="stat-label">Partages</div>
          <div class="stat-trend neutral">
            <span class="trend-icon">➡️</span>
            <span class="trend-text">Stable</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Graphiques d'activité -->
    <div class="activity-section">
      <h4 class="activity-title">📈 Activité récente</h4>
      
      <!-- Graphique en barres simple -->
      <div class="activity-chart">
        <div class="chart-bars">
          <div
            v-for="(day, index) in activityData"
            :key="index"
            class="chart-bar"
            :style="{ height: `${(day.value / maxActivity) * 100}%` }"
            :title="`${day.label}: ${day.value} interactions`"
          >
            <div class="bar-fill"></div>
          </div>
        </div>
        <div class="chart-labels">
          <span
            v-for="(day, index) in activityData"
            :key="index"
            class="chart-label"
          >
            {{ day.label }}
          </span>
        </div>
      </div>
    </div>

    <!-- Anneaux de progression -->
    <div class="progress-section">
      <h4 class="progress-title">🎯 Objectifs</h4>
      
      <div class="progress-rings">
        <!-- Objectif Posts -->
        <div class="progress-ring-container">
          <ProgressRing
            :progress="(stats.posts_count || 0) / 50 * 100"
            :size="80"
            :stroke-width="8"
            color="var(--accent-primary)"
          />
          <div class="ring-label">
            <div class="ring-number">{{ stats.posts_count || 0 }}/50</div>
            <div class="ring-text">Posts</div>
          </div>
        </div>

        <!-- Objectif Likes -->
        <div class="progress-ring-container">
          <ProgressRing
            :progress="(stats.likes_received || 0) / 500 * 100"
            :size="80"
            :stroke-width="8"
            color="var(--accent-error)"
          />
          <div class="ring-label">
            <div class="ring-number">{{ stats.likes_received || 0 }}/500</div>
            <div class="ring-text">Likes</div>
          </div>
        </div>

        <!-- Objectif Followers -->
        <div class="progress-ring-container">
          <ProgressRing
            :progress="(stats.followers_count || 0) / 100 * 100"
            :size="80"
            :stroke-width="8"
            color="var(--accent-success)"
          />
          <div class="ring-label">
            <div class="ring-number">{{ stats.followers_count || 0 }}/100</div>
            <div class="ring-text">Followers</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Badges de réalisation -->
    <div class="achievements-section">
      <h4 class="achievements-title">🏆 Réalisations</h4>
      
      <div class="achievements-grid">
        <div
          v-for="achievement in achievements"
          :key="achievement.id"
          class="achievement-badge"
          :class="{ 'unlocked': achievement.unlocked }"
        >
          <div class="badge-icon">{{ achievement.icon }}</div>
          <div class="badge-name">{{ achievement.name }}</div>
          <div class="badge-description">{{ achievement.description }}</div>
        </div>
      </div>
    </div>
  </NeuCard>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import NeuCard from '../neumorphic/NeuCard.vue'
import AnimatedCounter from '../neumorphic/AnimatedCounter.vue'
import ProgressRing from '../neumorphic/ProgressRing.vue'

export default {
  name: 'ProfileStats',
  components: {
    NeuCard,
    AnimatedCounter,
    ProgressRing
  },
  props: {
    stats: {
      type: Object,
      default: () => ({})
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const activityData = ref([
      { label: 'Lun', value: 12 },
      { label: 'Mar', value: 8 },
      { label: 'Mer', value: 15 },
      { label: 'Jeu', value: 22 },
      { label: 'Ven', value: 18 },
      { label: 'Sam', value: 25 },
      { label: 'Dim', value: 10 }
    ])
    
    const achievements = ref([
      {
        id: 1,
        icon: '🎉',
        name: 'Premier Post',
        description: 'Publier votre premier post',
        unlocked: true
      },
      {
        id: 2,
        icon: '❤️',
        name: 'Populaire',
        description: 'Recevoir 100 likes',
        unlocked: (props.stats.likes_received || 0) >= 100
      },
      {
        id: 3,
        icon: '👥',
        name: 'Influenceur',
        description: 'Avoir 50 followers',
        unlocked: (props.stats.followers_count || 0) >= 50
      },
      {
        id: 4,
        icon: '💬',
        name: 'Conversationnel',
        description: 'Recevoir 50 commentaires',
        unlocked: (props.stats.comments_received || 0) >= 50
      },
      {
        id: 5,
        icon: '🔥',
        name: 'En Feu',
        description: 'Publier 30 posts',
        unlocked: (props.stats.posts_count || 0) >= 30
      },
      {
        id: 6,
        icon: '⭐',
        name: 'Superstar',
        description: 'Atteindre 1000 likes',
        unlocked: (props.stats.likes_received || 0) >= 1000
      }
    ])
    
    const maxActivity = computed(() => {
      return Math.max(...activityData.value.map(day => day.value))
    })
    
    return {
      activityData,
      achievements,
      maxActivity
    }
  }
}
</script>

<style scoped>
.profile-stats {
  margin-bottom: var(--spacing-lg);
}

.stats-title {
  color: var(--text-primary);
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: var(--spacing-lg);
  text-align: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.stat-card {
  background: var(--bg-primary);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  box-shadow: 
    inset 4px 4px 8px var(--shadow-dark),
    inset -4px -4px 8px var(--shadow-light);
  transition: all var(--transition-normal);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 
    4px 4px 8px var(--shadow-dark),
    -4px -4px 8px var(--shadow-light);
}

.stat-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-xs);
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: 0.75rem;
}

.stat-trend.positive {
  color: var(--accent-success);
}

.stat-trend.negative {
  color: var(--accent-error);
}

.stat-trend.neutral {
  color: var(--text-muted);
}

.activity-section {
  margin-bottom: var(--spacing-xl);
}

.activity-title {
  color: var(--text-primary);
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: var(--spacing-md);
}

.activity-chart {
  background: var(--bg-primary);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  box-shadow: 
    inset 4px 4px 8px var(--shadow-dark),
    inset -4px -4px 8px var(--shadow-light);
}

.chart-bars {
  display: flex;
  align-items: end;
  gap: var(--spacing-sm);
  height: 100px;
  margin-bottom: var(--spacing-md);
}

.chart-bar {
  flex: 1;
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
  position: relative;
  min-height: 10px;
  cursor: pointer;
  transition: all var(--transition-normal);
}

.chart-bar:hover {
  transform: translateY(-2px);
}

.bar-fill {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  border-radius: var(--radius-sm);
}

.chart-labels {
  display: flex;
  gap: var(--spacing-sm);
}

.chart-label {
  flex: 1;
  text-align: center;
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.progress-section {
  margin-bottom: var(--spacing-xl);
}

.progress-title {
  color: var(--text-primary);
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: var(--spacing-md);
}

.progress-rings {
  display: flex;
  justify-content: space-around;
  gap: var(--spacing-lg);
}

.progress-ring-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.ring-label {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.ring-number {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-primary);
}

.ring-text {
  font-size: 0.625rem;
  color: var(--text-secondary);
}

.achievements-section {
  margin-bottom: var(--spacing-lg);
}

.achievements-title {
  color: var(--text-primary);
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: var(--spacing-md);
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-md);
}

.achievement-badge {
  background: var(--bg-primary);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  text-align: center;
  transition: all var(--transition-normal);
  opacity: 0.5;
  box-shadow: 
    inset 2px 2px 4px var(--shadow-dark),
    inset -2px -2px 4px var(--shadow-light);
}

.achievement-badge.unlocked {
  opacity: 1;
  box-shadow: 
    4px 4px 8px var(--shadow-dark),
    -4px -4px 8px var(--shadow-light);
}

.achievement-badge:hover {
  transform: translateY(-2px);
}

.badge-icon {
  font-size: 2rem;
  margin-bottom: var(--spacing-sm);
}

.badge-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.badge-description {
  font-size: 0.75rem;
  color: var(--text-secondary);
  line-height: 1.3;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-card {
    padding: var(--spacing-md);
  }
  
  .progress-rings {
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-md);
  }
  
  .achievements-grid {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  }
}

@media (max-width: 480px) {
  .chart-bars {
    height: 80px;
  }
  
  .achievements-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .achievement-badge {
    padding: var(--spacing-sm);
  }
  
  .badge-icon {
    font-size: 1.5rem;
  }
}
</style>