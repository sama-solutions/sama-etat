<template>
  <NeuCard class="comment-card" :class="{ 'new': comment.isNew }" :hoverable="true">
    <!-- En-tête du commentaire -->
    <div class="comment-header">
      <div class="comment-author">
        <div class="author-avatar">
          {{ authorInitial }}
        </div>
        <div class="author-info">
          <h5 class="author-name">{{ authorName }}</h5>
          <p class="comment-date">{{ formattedDate }}</p>
        </div>
      </div>
      <div class="comment-menu">
        <NeuButton
          variant="ghost"
          size="small"
          @click="toggleMenu"
          class="menu-button"
        >
          ⋮
        </NeuButton>
        <div v-if="showMenu" class="menu-dropdown">
          <button @click="handleReply" class="menu-item">
            💬 Répondre
          </button>
          <button v-if="canDelete" @click="handleDelete" class="menu-item delete">
            🗑️ Supprimer
          </button>
        </div>
      </div>
    </div>

    <!-- Contenu du commentaire -->
    <div class="comment-content">
      <p class="comment-text">{{ comment.content }}</p>
    </div>

    <!-- Actions du commentaire -->
    <div class="comment-actions">
      <NeuButton
        variant="ghost"
        size="small"
        :class="{ 'action-liked': isLiked }"
        @click="handleLike"
      >
        <span class="action-icon">{{ isLiked ? '❤️' : '🤍' }}</span>
        <span class="action-text">{{ comment.like_count || 0 }}</span>
      </NeuButton>

      <NeuButton
        variant="ghost"
        size="small"
        @click="handleReply"
      >
        <span class="action-icon">💬</span>
        <span class="action-text">Répondre</span>
      </NeuButton>

      <NeuButton
        variant="ghost"
        size="small"
        @click="handleShare"
      >
        <span class="action-icon">🔗</span>
        <span class="action-text">Partager</span>
      </NeuButton>
    </div>

    <!-- Zone de réponse (si activée) -->
    <div v-if="showReplyBox" class="reply-section">
      <div class="reply-input-container">
        <div class="user-avatar-small">
          A
        </div>
        <NeuInput
          v-model="replyText"
          placeholder="Écrivez une réponse..."
          class="reply-input"
          @keypress.enter="submitReply"
        />
      </div>
      <div class="reply-actions">
        <NeuButton
          variant="default"
          size="small"
          @click="cancelReply"
        >
          Annuler
        </NeuButton>
        <NeuButton
          variant="primary"
          size="small"
          :disabled="!replyText.trim()"
          @click="submitReply"
        >
          Répondre
        </NeuButton>
      </div>
    </div>
  </NeuCard>
</template>

<script>
import { computed, ref } from 'vue'
import NeuCard from './neumorphic/NeuCard.vue'
import NeuButton from './neumorphic/NeuButton.vue'
import NeuInput from './neumorphic/NeuInput.vue'

export default {
  name: 'CommentCard',
  components: {
    NeuCard,
    NeuButton,
    NeuInput
  },
  props: {
    comment: {
      type: Object,
      required: true
    }
  },
  emits: ['like', 'reply', 'delete'],
  setup(props, { emit }) {
    const isLiked = ref(false)
    const showMenu = ref(false)
    const showReplyBox = ref(false)
    const replyText = ref('')
    
    const authorName = computed(() => {
      if (Array.isArray(props.comment.author_id)) {
        return props.comment.author_id[1] || 'Utilisateur'
      }
      return 'Utilisateur'
    })
    
    const authorInitial = computed(() => {
      return authorName.value.charAt(0).toUpperCase()
    })
    
    const formattedDate = computed(() => {
      if (!props.comment.create_date) return ''
      
      const date = new Date(props.comment.create_date)
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
    
    const canDelete = computed(() => {
      // L'utilisateur peut supprimer ses propres commentaires
      return props.comment.author_id && props.comment.author_id[0] === 2 // ID utilisateur actuel
    })
    
    const handleLike = () => {
      isLiked.value = !isLiked.value
      emit('like', props.comment.id)
    }
    
    const handleReply = () => {
      showReplyBox.value = !showReplyBox.value
      showMenu.value = false
    }
    
    const handleDelete = () => {
      if (confirm('Êtes-vous sûr de vouloir supprimer ce commentaire ?')) {
        emit('delete', props.comment.id)
      }
      showMenu.value = false
    }
    
    const handleShare = () => {
      // Copier le lien du commentaire
      const url = `${window.location.origin}/comment/${props.comment.id}`
      navigator.clipboard.writeText(url).then(() => {
        console.log('Lien du commentaire copié')
      }).catch(() => {
        console.log('Impossible de copier le lien')
      })
    }
    
    const toggleMenu = () => {
      showMenu.value = !showMenu.value
    }
    
    const submitReply = () => {
      if (replyText.value.trim()) {
        emit('reply', {
          commentId: props.comment.id,
          content: replyText.value.trim()
        })
        replyText.value = ''
        showReplyBox.value = false
      }
    }
    
    const cancelReply = () => {
      replyText.value = ''
      showReplyBox.value = false
    }
    
    // Fermer le menu si on clique ailleurs
    const handleClickOutside = (event) => {
      if (!event.target.closest('.comment-menu')) {
        showMenu.value = false
      }
    }
    
    // Ajouter l'écouteur d'événement
    if (typeof window !== 'undefined') {
      document.addEventListener('click', handleClickOutside)
    }
    
    return {
      isLiked,
      showMenu,
      showReplyBox,
      replyText,
      authorName,
      authorInitial,
      formattedDate,
      canDelete,
      handleLike,
      handleReply,
      handleDelete,
      handleShare,
      toggleMenu,
      submitReply,
      cancelReply
    }
  }
}
</script>

<style scoped>
.comment-card {
  transition: all var(--transition-normal);
  position: relative;
}

.comment-card.new {
  animation: slideInComment 0.5s ease-out;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-md);
}

.comment-author {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
}

.author-avatar {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.75rem;
  box-shadow: 
    2px 2px 4px var(--shadow-dark),
    -2px -2px 4px var(--shadow-light);
}

.author-info {
  flex: 1;
}

.author-name {
  color: var(--text-primary);
  font-size: 0.8125rem;
  font-weight: 600;
  margin: 0 0 var(--spacing-xs) 0;
}

.comment-date {
  color: var(--text-muted);
  font-size: 0.6875rem;
  margin: 0;
}

.comment-menu {
  position: relative;
}

.menu-button {
  padding: var(--spacing-xs);
  min-width: auto;
}

.menu-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: var(--bg-primary);
  border-radius: var(--radius-md);
  box-shadow: 
    6px 6px 12px var(--shadow-dark),
    -6px -6px 12px var(--shadow-light);
  z-index: 10;
  min-width: 120px;
  overflow: hidden;
}

.menu-item {
  display: block;
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  background: none;
  border: none;
  text-align: left;
  color: var(--text-primary);
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color var(--transition-normal);
}

.menu-item:hover {
  background: var(--bg-secondary);
}

.menu-item.delete {
  color: var(--accent-error);
}

.comment-content {
  margin-bottom: var(--spacing-md);
}

.comment-text {
  color: var(--text-primary);
  line-height: 1.5;
  font-size: 0.875rem;
  margin: 0;
}

.comment-actions {
  display: flex;
  gap: var(--spacing-sm);
  padding-top: var(--spacing-sm);
  border-top: 1px solid var(--bg-secondary);
}

.comment-actions .neu-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-xs) var(--spacing-sm);
  min-width: auto;
}

.action-icon {
  font-size: 0.875rem;
}

.action-text {
  font-size: 0.75rem;
  font-weight: 600;
}

.action-liked {
  color: var(--accent-error);
}

.action-liked .action-icon {
  animation: heartbeat 0.6s ease-in-out;
}

.reply-section {
  margin-top: var(--spacing-md);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--bg-secondary);
}

.reply-input-container {
  display: flex;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
}

.user-avatar-small {
  width: 24px;
  height: 24px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.625rem;
  flex-shrink: 0;
}

.reply-input {
  flex: 1;
}

.reply-actions {
  display: flex;
  gap: var(--spacing-sm);
  justify-content: flex-end;
}

@keyframes slideInComment {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes heartbeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

@media (max-width: 480px) {
  .comment-actions {
    flex-wrap: wrap;
    gap: var(--spacing-xs);
  }
  
  .comment-actions .neu-button {
    flex: 1;
    min-width: 0;
    justify-content: center;
  }
  
  .reply-input-container {
    flex-direction: column;
    gap: var(--spacing-xs);
  }
  
  .reply-actions {
    flex-direction: column;
  }
}
</style>