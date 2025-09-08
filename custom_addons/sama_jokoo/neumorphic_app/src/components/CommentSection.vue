<template>
  <div class="comment-section">
    <!-- En-tête des commentaires -->
    <div class="comments-header">
      <h3 class="comments-title">
        💬 Commentaires ({{ comments.length }})
      </h3>
      <NeuButton
        size="small"
        @click="toggleComments"
        :class="{ 'active': showComments }"
      >
        {{ showComments ? 'Masquer' : 'Afficher' }}
      </NeuButton>
    </div>

    <!-- Zone de création de commentaire -->
    <div v-if="showComments" class="comment-create">
      <NeuCard variant="inset" padding="normal">
        <div class="create-comment-header">
          <div class="user-avatar small">
            {{ currentUser?.name?.charAt(0) || 'U' }}
          </div>
          <div class="create-comment-input">
            <NeuInput
              v-model="newComment"
              placeholder="Écrivez un commentaire..."
              :disabled="loading"
              @keypress.enter="createComment"
            />
          </div>
        </div>
        <div class="create-comment-actions">
          <NeuButton
            variant="primary"
            size="small"
            :loading="loading"
            :disabled="!newComment.trim()"
            @click="createComment"
          >
            Commenter
          </NeuButton>
        </div>
      </NeuCard>
    </div>

    <!-- Liste des commentaires -->
    <div v-if="showComments" class="comments-list">
      <div v-if="loadingComments" class="loading-comments">
        <NeuCard class="loading-card">
          <div class="loading-content">
            <div class="loading-spinner"></div>
            <p>Chargement des commentaires...</p>
          </div>
        </NeuCard>
      </div>

      <div v-else-if="comments.length === 0" class="empty-comments">
        <NeuCard variant="flat" class="empty-card">
          <div class="empty-content">
            <span class="empty-icon">💭</span>
            <h4>Aucun commentaire</h4>
            <p>Soyez le premier à commenter ce post !</p>
          </div>
        </NeuCard>
      </div>

      <div v-else class="comments-container">
        <CommentCard
          v-for="comment in comments"
          :key="comment.id"
          :comment="comment"
          @like="handleLikeComment"
          @reply="handleReplyComment"
          @delete="handleDeleteComment"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import NeuCard from './neumorphic/NeuCard.vue'
import NeuInput from './neumorphic/NeuInput.vue'
import NeuButton from './neumorphic/NeuButton.vue'
import CommentCard from './CommentCard.vue'

export default {
  name: 'CommentSection',
  components: {
    NeuCard,
    NeuInput,
    NeuButton,
    CommentCard
  },
  props: {
    postId: {
      type: Number,
      required: true
    },
    initialCommentsCount: {
      type: Number,
      default: 0
    },
    apiService: {
      type: Object,
      required: true
    }
  },
  emits: ['comments-updated'],
  setup(props, { emit }) {
    const comments = ref([])
    const newComment = ref('')
    const loading = ref(false)
    const loadingComments = ref(false)
    const showComments = ref(false)
    
    const currentUser = ref({
      name: 'Admin',
      id: 2
    })
    
    const toggleComments = async () => {
      showComments.value = !showComments.value
      
      if (showComments.value && comments.value.length === 0) {
        await loadComments()
      }
    }
    
    const loadComments = async () => {
      loadingComments.value = true
      try {
        const fetchedComments = await props.apiService.getComments(props.postId, 10)
        comments.value = fetchedComments
      } catch (error) {
        console.error('Erreur lors du chargement des commentaires:', error)
      } finally {
        loadingComments.value = false
      }
    }
    
    const createComment = async () => {
      if (!newComment.value.trim()) return
      
      loading.value = true
      try {
        const comment = await props.apiService.createComment(
          props.postId,
          newComment.value.trim()
        )
        
        comments.value.unshift({
          id: comment.id || Date.now(),
          content: newComment.value.trim(),
          author_id: [currentUser.value.id, currentUser.value.name],
          create_date: new Date().toISOString(),
          like_count: 0
        })
        
        newComment.value = ''
        emit('comments-updated', comments.value.length)
        
      } catch (error) {
        console.error('Erreur lors de la création du commentaire:', error)
      } finally {
        loading.value = false
      }
    }
    
    const handleLikeComment = async (commentId) => {
      try {
        await props.apiService.toggleLikeComment(commentId)
        const comment = comments.value.find(c => c.id === commentId)
        if (comment) {
          comment.like_count = (comment.like_count || 0) + 1
        }
      } catch (error) {
        console.error('Erreur lors du like du commentaire:', error)
      }
    }
    
    const handleReplyComment = (commentId) => {
      console.log('Répondre au commentaire:', commentId)
    }
    
    const handleDeleteComment = async (commentId) => {
      try {
        await props.apiService.deleteComment(commentId)
        const index = comments.value.findIndex(c => c.id === commentId)
        if (index !== -1) {
          comments.value.splice(index, 1)
          emit('comments-updated', comments.value.length)
        }
      } catch (error) {
        console.error('Erreur lors de la suppression du commentaire:', error)
      }
    }
    
    return {
      comments,
      newComment,
      loading,
      loadingComments,
      showComments,
      currentUser,
      toggleComments,
      createComment,
      handleLikeComment,
      handleReplyComment,
      handleDeleteComment
    }
  }
}
</script>

<style scoped>
.comment-section {
  margin-top: var(--spacing-lg);
}

.comments-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.comments-title {
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
}

.comment-create {
  margin-bottom: var(--spacing-lg);
}

.create-comment-header {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.user-avatar.small {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  flex-shrink: 0;
  box-shadow: 
    3px 3px 6px var(--shadow-dark),
    -3px -3px 6px var(--shadow-light);
}

.create-comment-input {
  flex: 1;
}

.create-comment-actions {
  display: flex;
  justify-content: flex-end;
}

.loading-content,
.empty-content {
  padding: var(--spacing-lg);
  text-align: center;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--bg-secondary);
  border-top: 2px solid var(--accent-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto var(--spacing-md);
}

.empty-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: var(--spacing-md);
}

.comments-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.neu-button.active {
  background: var(--accent-primary);
  color: white;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>