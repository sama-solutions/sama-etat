<template>
  <NeuCard class="post-card" :hoverable="true">
    <!-- En-tête du post -->
    <div class="post-header">
      <div class="post-author">
        <div class="author-avatar">
          {{ authorInitial }}
        </div>
        <div class="author-info">
          <h4 class="author-name">{{ authorName }}</h4>
          <p class="post-date">{{ formattedDate }}</p>
        </div>
      </div>
      <div class="post-status">
        <span :class="['status-badge', `status-${post.state}`]">
          {{ statusText }}
        </span>
      </div>
    </div>

    <!-- Contenu du post -->
    <div class="post-content">
      <div v-html="post.content" class="post-text"></div>
    </div>

    <!-- Actions du post -->
    <div class="post-actions">
      <NeuButton
        variant="default"
        size="small"
        :class="{ 'action-liked': isLiked }"
        @click="handleLike"
      >
        <span class="action-icon">{{ isLiked ? '❤️' : '🤍' }}</span>
        <span class="action-text">{{ post.like_count || 0 }}</span>
      </NeuButton>

      <NeuButton
        variant="default"
        size="small"
        @click="handleComment"
      >
        <span class="action-icon">💬</span>
        <span class="action-text">{{ post.comment_count || 0 }}</span>
      </NeuButton>

      <NeuButton
        variant="default"
        size="small"
        @click="handleShare"
      >
        <span class="action-icon">🔗</span>
        <span class="action-text">Partager</span>
      </NeuButton>
    </div>
  </NeuCard>
</template>

<script>
import { computed, ref } from 'vue'
import NeuCard from './neumorphic/NeuCard.vue'
import NeuButton from './neumorphic/NeuButton.vue'

export default {
  name: 'PostCard',
  components: {
    NeuCard,
    NeuButton
  },
  props: {
    post: {
      type: Object,
      required: true
    }
  },
  emits: ['like', 'comment', 'share'],
  setup(props, { emit }) {
    const isLiked = ref(false)
    
    const authorName = computed(() => {
      if (Array.isArray(props.post.author_id)) {
        return props.post.author_id[1] || 'Utilisateur'
      }
      return 'Utilisateur'
    })
    
    const authorInitial = computed(() => {
      return authorName.value.charAt(0).toUpperCase()
    })
    
    const formattedDate = computed(() => {
      if (!props.post.create_date) return ''
      
      const date = new Date(props.post.create_date)
      const now = new Date()
      const diffInMinutes = Math.floor((now - date) / (1000 * 60))
      
      if (diffInMinutes < 1) {
        return 'À l\'instant'
      } else if (diffInMinutes < 60) {
        return `Il y a ${diffInMinutes} min`
      } else if (diffInMinutes < 1440) {
        const hours = Math.floor(diffInMinutes / 60)
        return `Il y a ${hours}h`
      } else {
        const days = Math.floor(diffInMinutes / 1440)
        return `Il y a ${days}j`
      }
    })
    
    const statusText = computed(() => {
      switch (props.post.state) {
        case 'published': return 'Publié'
        case 'draft': return 'Brouillon'
        case 'moderated': return 'En modération'
        default: return 'Inconnu'
      }
    })
    
    const handleLike = () => {
      isLiked.value = !isLiked.value
      emit('like', props.post.id)
    }
    
    const handleComment = () => {
      emit('comment', props.post.id)
    }
    
    const handleShare = () => {
      // Copier le lien dans le presse-papiers
      const url = `${window.location.origin}/post/${props.post.id}`
      navigator.clipboard.writeText(url).then(() => {
        // TODO: Afficher une notification de succès
        console.log('Lien copié dans le presse-papiers')
      }).catch(() => {
        console.log('Impossible de copier le lien')
      })
      
      emit('share', props.post.id)
    }
    
    return {
      isLiked,
      authorName,
      authorInitial,
      formattedDate,
      statusText,
      handleLike,
      handleComment,
      handleShare
    }
  }
}
</script>

<style scoped>
.post-card {
  margin-bottom: var(--spacing-lg);
  transition: all var(--transition-normal);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-md);
}

.post-author {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: var(--text-white);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1rem;
  box-shadow: 
    3px 3px 6px var(--shadow-dark),
    -3px -3px 6px var(--shadow-light);
}

.author-info {
  flex: 1;
}

.author-name {
  color: var(--text-primary);
  font-size: 0.875rem;
  font-weight: 600;
  margin: 0 0 var(--spacing-xs) 0;
}

.post-date {
  color: var(--text-muted);
  font-size: 0.75rem;
  margin: 0;
}

.post-status {
  flex-shrink: 0;
}

.status-badge {
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-published {
  background: rgba(78, 205, 196, 0.1);
  color: var(--accent-success);
}

.status-draft {
  background: rgba(255, 230, 109, 0.1);
  color: var(--accent-warning);
}

.status-moderated {
  background: rgba(255, 107, 107, 0.1);
  color: var(--accent-error);
}

.post-content {
  margin-bottom: var(--spacing-lg);
}

.post-text {
  color: var(--text-primary);
  line-height: 1.6;
  font-size: 0.95rem;
}

.post-text p {
  margin: 0 0 var(--spacing-sm) 0;
}

.post-text p:last-child {
  margin-bottom: 0;
}

.post-actions {
  display: flex;
  gap: var(--spacing-md);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--bg-secondary);
}

.post-actions .neu-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  flex: 1;
  justify-content: center;
  padding: var(--spacing-sm) var(--spacing-md);
  transition: all var(--transition-normal);
}

.action-icon {
  font-size: 1rem;
}

.action-text {
  font-size: 0.875rem;
  font-weight: 600;
}

.action-liked {
  background: rgba(255, 107, 107, 0.1);
  color: var(--accent-error);
}

.action-liked .action-icon {
  animation: heartbeat 0.6s ease-in-out;
}

@keyframes heartbeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

@media (max-width: 480px) {
  .post-actions {
    flex-direction: column;
    gap: var(--spacing-sm);
  }
  
  .post-actions .neu-button {
    flex: none;
  }
  
  .author-avatar {
    width: 36px;
    height: 36px;
    font-size: 0.875rem;
  }
  
  .author-name {
    font-size: 0.8125rem;
  }
  
  .post-date {
    font-size: 0.6875rem;
  }
}
</style>