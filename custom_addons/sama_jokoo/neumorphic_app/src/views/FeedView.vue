<template>
  <div class="feed-view">
    <div class="feed-container">
      <!-- En-tête -->
      <header class="feed-header">
        <div class="header-content">
          <h1 class="app-title">Sama Jokoo</h1>
          <NeuButton 
            variant="primary" 
            size="small" 
            @click="handleLogout"
          >
            Déconnexion
          </NeuButton>
        </div>
      </header>

      <!-- Indicateur de mode -->
      <div v-if="isDemoMode" class="demo-banner">
        <div class="demo-content">
          <span class="demo-icon">🎭</span>
          <span class="demo-text">Mode Démo - Données de test</span>
        </div>
      </div>

      <!-- Création de post -->
      <NeuCard class="create-post-card">
        <div class="create-post-header">
          <div class="user-avatar">
            {{ currentUser?.name?.charAt(0) || 'A' }}
          </div>
          <div class="create-post-input">
            <NeuInput
              v-model="newPostContent"
              placeholder="Quoi de neuf ?"
              :disabled="loading"
            />
          </div>
        </div>
        <div class="create-post-actions">
          <NeuButton
            variant="primary"
            :loading="loading"
            :disabled="!newPostContent.trim()"
            @click="createPost"
          >
            Publier
          </NeuButton>
        </div>
      </NeuCard>

      <!-- Liste des posts -->
      <div class="posts-list">
        <div v-if="loadingPosts" class="loading-posts">
          <NeuCard class="loading-card">
            <div class="loading-content">
              <div class="loading-spinner"></div>
              <p>Chargement des posts...</p>
            </div>
          </NeuCard>
        </div>

        <div v-else-if="posts.length === 0" class="empty-posts">
          <NeuCard class="empty-card">
            <div class="empty-content">
              <span class="empty-icon">📝</span>
              <h3>Aucun post pour le moment</h3>
              <p>Soyez le premier à publier quelque chose !</p>
            </div>
          </NeuCard>
        </div>

        <div v-else>
          <PostCard
            v-for="post in posts"
            :key="post.id"
            :post="post"
            @like="handleLike"
            @comment="handleComment"
          />
        </div>
      </div>

      <!-- Bouton de rechargement -->
      <div class="refresh-section">
        <NeuButton
          variant="success"
          :loading="loadingPosts"
          @click="loadPosts"
        >
          Actualiser
        </NeuButton>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import NeuCard from '../components/neumorphic/NeuCard.vue'
import NeuInput from '../components/neumorphic/NeuInput.vue'
import NeuButton from '../components/neumorphic/NeuButton.vue'
import PostCard from '../components/PostCard.vue'
import odooApi from '../services/odooApi.js'
import demoApi from '../services/demoApi.js'

export default {
  name: 'FeedView',
  components: {
    NeuCard,
    NeuInput,
    NeuButton,
    PostCard
  },
  setup() {
    const router = useRouter()
    
    const posts = ref([])
    const newPostContent = ref('')
    const loading = ref(false)
    const loadingPosts = ref(false)
    const currentUser = ref(null)
    const isDemoMode = ref(false)
    
    // Déterminer quelle API utiliser
    const getApi = () => {
      // Vérifier si on est en mode démo
      if (demoApi.isAuthenticated()) {
        isDemoMode.value = true
        return demoApi
      } else if (odooApi.isAuthenticated()) {
        isDemoMode.value = false
        return odooApi
      } else {
        // Rediriger vers login si pas authentifié
        router.push('/login')
        return null
      }
    }
    
    const loadPosts = async () => {
      const api = getApi()
      if (!api) return
      
      loadingPosts.value = true
      try {
        const fetchedPosts = await api.getPosts(20, 0)
        posts.value = fetchedPosts
      } catch (error) {
        console.error('Erreur lors du chargement des posts:', error)
      } finally {
        loadingPosts.value = false
      }
    }
    
    const loadCurrentUser = async () => {
      const api = getApi()
      if (!api) return
      
      try {
        const user = await api.getCurrentUser()
        currentUser.value = user
      } catch (error) {
        console.error('Erreur lors du chargement de l\'utilisateur:', error)
      }
    }
    
    const createPost = async () => {
      const api = getApi()
      if (!api || !newPostContent.value.trim()) return
      
      loading.value = true
      try {
        const newPost = await api.createPost(newPostContent.value.trim())
        posts.value.unshift(newPost)
        newPostContent.value = ''
      } catch (error) {
        console.error('Erreur lors de la création du post:', error)
      } finally {
        loading.value = false
      }
    }
    
    const handleLike = async (postId) => {
      const api = getApi()
      if (!api) return
      
      try {
        const result = await api.toggleLike(postId)
        // Mettre à jour le post localement
        const post = posts.value.find(p => p.id === postId)
        if (post) {
          if (result.liked) {
            post.like_count++
          } else {
            post.like_count = Math.max(0, post.like_count - 1)
          }
        }
      } catch (error) {
        console.error('Erreur lors du like:', error)
      }
    }
    
    const handleComment = (postId) => {
      // TODO: Implémenter l'interface de commentaires
      console.log('Commentaire sur le post:', postId)
    }
    
    const handleLogout = () => {
      const api = getApi()
      if (api) {
        api.logout()
      }
      router.push('/login')
    }
    
    onMounted(async () => {
      await loadCurrentUser()
      await loadPosts()
    })
    
    return {
      posts,
      newPostContent,
      loading,
      loadingPosts,
      currentUser,
      isDemoMode,
      createPost,
      loadPosts,
      handleLike,
      handleComment,
      handleLogout
    }
  }
}
</script>

<style scoped>
.feed-view {
  min-height: 100vh;
  background: var(--bg-primary);
}

.feed-container {
  max-width: 600px;
  margin: 0 auto;
  padding: var(--spacing-md);
}

.feed-header {
  margin-bottom: var(--spacing-lg);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) 0;
}

.app-title {
  font-size: 1.75rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.demo-banner {
  margin-bottom: var(--spacing-lg);
}

.demo-content {
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: var(--text-white);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  box-shadow: 
    4px 4px 8px var(--shadow-dark),
    -4px -4px 8px var(--shadow-light);
}

.demo-icon {
  font-size: 1.25rem;
}

.demo-text {
  font-weight: 600;
}

.create-post-card {
  margin-bottom: var(--spacing-lg);
}

.create-post-header {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: var(--text-white);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.25rem;
  flex-shrink: 0;
  box-shadow: 
    4px 4px 8px var(--shadow-dark),
    -4px -4px 8px var(--shadow-light);
}

.create-post-input {
  flex: 1;
}

.create-post-actions {
  display: flex;
  justify-content: flex-end;
}

.posts-list {
  margin-bottom: var(--spacing-lg);
}

.loading-posts,
.empty-posts {
  margin-bottom: var(--spacing-lg);
}

.loading-card,
.empty-card {
  text-align: center;
}

.loading-content,
.empty-content {
  padding: var(--spacing-lg);
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--bg-secondary);
  border-top: 3px solid var(--accent-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto var(--spacing-md);
}

.empty-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: var(--spacing-md);
}

.empty-content h3 {
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.empty-content p {
  color: var(--text-secondary);
}

.refresh-section {
  text-align: center;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .feed-container {
    padding: var(--spacing-sm);
  }
  
  .header-content {
    flex-direction: column;
    gap: var(--spacing-md);
    text-align: center;
  }
  
  .app-title {
    font-size: 1.5rem;
  }
}
</style>