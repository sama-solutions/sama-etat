<template>
  <NeuCard class="profile-header" :hoverable="false">
    <!-- Image de couverture -->
    <div class="cover-image" :style="coverImageStyle">
      <div class="cover-overlay"></div>
      <button v-if="isOwnProfile" class="edit-cover-btn neu-button-small">
        📷 Modifier la couverture
      </button>
    </div>

    <!-- Informations principales -->
    <div class="profile-main">
      <!-- Avatar -->
      <div class="avatar-section">
        <div class="avatar-container">
          <img
            v-if="user.avatar_url"
            :src="user.avatar_url"
            :alt="user.display_name"
            class="user-avatar-large"
          />
          <div v-else class="user-avatar-large default">
            {{ avatarInitial }}
          </div>
          
          <!-- Badge de statut -->
          <div v-if="user.is_online" class="status-badge online"></div>
          <div v-else class="status-badge offline"></div>
          
          <!-- Bouton d'édition avatar -->
          <button v-if="isOwnProfile" class="edit-avatar-btn" @click="$emit('edit-avatar')">
            📷
          </button>
        </div>
      </div>

      <!-- Informations utilisateur -->
      <div class="user-info">
        <div class="user-names">
          <h1 class="display-name">{{ user.display_name || user.username }}</h1>
          <p class="username">@{{ user.username }}</p>
        </div>

        <div class="user-meta">
          <div v-if="user.bio" class="bio">
            {{ user.bio }}
          </div>
          
          <div class="meta-items">
            <div v-if="user.location" class="meta-item">
              <span class="meta-icon">📍</span>
              <span class="meta-text">{{ user.location }}</span>
            </div>
            
            <div v-if="user.website" class="meta-item">
              <span class="meta-icon">🌐</span>
              <a :href="user.website" target="_blank" class="meta-link">
                {{ formatWebsite(user.website) }}
              </a>
            </div>
            
            <div class="meta-item">
              <span class="meta-icon">📅</span>
              <span class="meta-text">Membre depuis {{ formatJoinDate(user.join_date) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="profile-actions">
        <!-- Actions pour son propre profil -->
        <template v-if="isOwnProfile">
          <NeuButton variant="primary" @click="$emit('edit')">
            <span class="action-icon">✏️</span>
            <span class="action-text">Modifier le profil</span>
          </NeuButton>
          
          <NeuButton @click="shareProfile">
            <span class="action-icon">🔗</span>
            <span class="action-text">Partager</span>
          </NeuButton>
        </template>

        <!-- Actions pour les autres profils -->
        <template v-else>
          <NeuButton
            v-if="!isFollowing"
            variant="primary"
            @click="$emit('follow')"
            :loading="followLoading"
          >
            <span class="action-icon">➕</span>
            <span class="action-text">Suivre</span>
          </NeuButton>
          
          <NeuButton
            v-else
            variant="default"
            @click="$emit('unfollow')"
            :loading="followLoading"
          >
            <span class="action-icon">✅</span>
            <span class="action-text">Suivi</span>
          </NeuButton>
          
          <NeuButton @click="$emit('message')">
            <span class="action-icon">💬</span>
            <span class="action-text">Message</span>
          </NeuButton>
          
          <NeuButton @click="shareProfile">
            <span class="action-icon">🔗</span>
            <span class="action-text">Partager</span>
          </NeuButton>
          
          <!-- Menu plus d'options -->
          <div class="more-actions">
            <NeuButton @click="toggleMoreMenu" class="more-btn">
              <span class="action-icon">⋮</span>
            </NeuButton>
            
            <div v-if="showMoreMenu" class="more-menu">
              <button class="menu-item" @click="reportUser">
                🚨 Signaler
              </button>
              <button class="menu-item" @click="blockUser">
                🚫 Bloquer
              </button>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- Statistiques rapides -->
    <div class="quick-stats">
      <div class="stat-item" @click="$emit('show-followers')">
        <span class="stat-number">{{ formatNumber(user.stats?.followers_count || 0) }}</span>
        <span class="stat-label">Followers</span>
      </div>
      
      <div class="stat-item" @click="$emit('show-following')">
        <span class="stat-number">{{ formatNumber(user.stats?.following_count || 0) }}</span>
        <span class="stat-label">Following</span>
      </div>
      
      <div class="stat-item">
        <span class="stat-number">{{ formatNumber(user.stats?.posts_count || 0) }}</span>
        <span class="stat-label">Posts</span>
      </div>
      
      <div class="stat-item">
        <span class="stat-number">{{ formatNumber(user.stats?.likes_received || 0) }}</span>
        <span class="stat-label">Likes</span>
      </div>
    </div>
  </NeuCard>
</template>

<script>
import { ref, computed } from 'vue'
import NeuCard from '../neumorphic/NeuCard.vue'
import NeuButton from '../neumorphic/NeuButton.vue'

export default {
  name: 'ProfileHeader',
  components: {
    NeuCard,
    NeuButton
  },
  props: {
    user: {
      type: Object,
      required: true
    },
    isOwnProfile: {
      type: Boolean,
      default: false
    },
    isFollowing: {
      type: Boolean,
      default: false
    }
  },
  emits: ['follow', 'unfollow', 'edit', 'message', 'edit-avatar', 'show-followers', 'show-following'],
  setup(props) {
    const followLoading = ref(false)
    const showMoreMenu = ref(false)
    
    const avatarInitial = computed(() => {
      return (props.user.display_name || props.user.username || 'U').charAt(0).toUpperCase()
    })
    
    const coverImageStyle = computed(() => {
      if (props.user.cover_image) {
        return {
          backgroundImage: `url(${props.user.cover_image})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }
      }
      return {
        background: 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))'
      }
    })
    
    const formatNumber = (num) => {
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M'
      } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K'
      }
      return num.toString()
    }
    
    const formatWebsite = (url) => {
      return url.replace(/^https?:\/\//, '').replace(/\/$/, '')
    }
    
    const formatJoinDate = (date) => {
      if (!date) return ''
      const joinDate = new Date(date)
      return joinDate.toLocaleDateString('fr-FR', { 
        year: 'numeric', 
        month: 'long' 
      })
    }
    
    const shareProfile = () => {
      const url = `${window.location.origin}/profile/${props.user.username}`
      if (navigator.share) {
        navigator.share({
          title: `Profil de ${props.user.display_name}`,
          text: `Découvrez le profil de ${props.user.display_name} sur Sama Jokoo`,
          url: url
        })
      } else {
        navigator.clipboard.writeText(url)
        // Afficher une notification
        console.log('Lien copié dans le presse-papiers')
      }
    }
    
    const toggleMoreMenu = () => {
      showMoreMenu.value = !showMoreMenu.value
    }
    
    const reportUser = () => {
      // Implémenter le signalement
      console.log('Signaler utilisateur:', props.user.id)
      showMoreMenu.value = false
    }
    
    const blockUser = () => {
      // Implémenter le blocage
      console.log('Bloquer utilisateur:', props.user.id)
      showMoreMenu.value = false
    }
    
    return {
      followLoading,
      showMoreMenu,
      avatarInitial,
      coverImageStyle,
      formatNumber,
      formatWebsite,
      formatJoinDate,
      shareProfile,
      toggleMoreMenu,
      reportUser,
      blockUser
    }
  }
}
</script>

<style scoped>
.profile-header {
  position: relative;
  overflow: hidden;
  padding: 0;
  margin-bottom: var(--spacing-lg);
}

.cover-image {
  height: 200px;
  position: relative;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
}

.cover-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.1);
}

.edit-cover-btn {
  position: absolute;
  top: var(--spacing-md);
  right: var(--spacing-md);
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: var(--radius-md);
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all var(--transition-normal);
}

.profile-main {
  padding: var(--spacing-lg);
  position: relative;
}

.avatar-section {
  position: absolute;
  top: -60px;
  left: var(--spacing-lg);
}

.avatar-container {
  position: relative;
}

.user-avatar-large {
  width: 120px;
  height: 120px;
  border-radius: var(--radius-full);
  border: 4px solid var(--bg-primary);
  box-shadow: 
    8px 8px 16px var(--shadow-dark),
    -8px -8px 16px var(--shadow-light);
}

.user-avatar-large.default {
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: 700;
}

.status-badge {
  position: absolute;
  bottom: 8px;
  right: 8px;
  width: 20px;
  height: 20px;
  border-radius: var(--radius-full);
  border: 3px solid var(--bg-primary);
}

.status-badge.online {
  background: var(--accent-success);
  box-shadow: 0 0 8px rgba(78, 205, 196, 0.5);
}

.status-badge.offline {
  background: var(--text-muted);
}

.edit-avatar-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  background: var(--bg-primary);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  box-shadow: 
    4px 4px 8px var(--shadow-dark),
    -4px -4px 8px var(--shadow-light);
  transition: all var(--transition-normal);
}

.edit-avatar-btn:hover {
  transform: translateY(-2px);
}

.user-info {
  margin-left: 140px;
  margin-top: var(--spacing-md);
}

.user-names {
  margin-bottom: var(--spacing-md);
}

.display-name {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.username {
  font-size: 1rem;
  color: var(--text-secondary);
  margin: 0;
}

.bio {
  font-size: 1rem;
  color: var(--text-primary);
  line-height: 1.5;
  margin-bottom: var(--spacing-md);
}

.meta-items {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.meta-icon {
  font-size: 1rem;
}

.meta-link {
  color: var(--accent-primary);
  text-decoration: none;
}

.meta-link:hover {
  text-decoration: underline;
}

.profile-actions {
  display: flex;
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
  flex-wrap: wrap;
}

.profile-actions .neu-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.action-icon {
  font-size: 1rem;
}

.action-text {
  font-size: 0.875rem;
  font-weight: 600;
}

.more-actions {
  position: relative;
}

.more-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: var(--bg-primary);
  border-radius: var(--radius-md);
  box-shadow: 
    8px 8px 16px var(--shadow-dark),
    -8px -8px 16px var(--shadow-light);
  z-index: 10;
  min-width: 150px;
  overflow: hidden;
  margin-top: var(--spacing-sm);
}

.menu-item {
  display: block;
  width: 100%;
  padding: var(--spacing-md);
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

.quick-stats {
  display: flex;
  padding: var(--spacing-lg);
  border-top: 1px solid var(--bg-secondary);
  gap: var(--spacing-lg);
}

.stat-item {
  flex: 1;
  text-align: center;
  cursor: pointer;
  padding: var(--spacing-sm);
  border-radius: var(--radius-md);
  transition: all var(--transition-normal);
}

.stat-item:hover {
  background: var(--bg-secondary);
  transform: translateY(-2px);
}

.stat-number {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-label {
  display: block;
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: var(--spacing-xs);
}

@media (max-width: 768px) {
  .cover-image {
    height: 150px;
  }
  
  .user-avatar-large {
    width: 80px;
    height: 80px;
  }
  
  .user-avatar-large.default {
    font-size: 1.75rem;
  }
  
  .user-info {
    margin-left: 100px;
    margin-top: var(--spacing-sm);
  }
  
  .display-name {
    font-size: 1.5rem;
  }
  
  .profile-actions {
    flex-direction: column;
  }
  
  .quick-stats {
    gap: var(--spacing-md);
  }
  
  .stat-number {
    font-size: 1.25rem;
  }
}

@media (max-width: 480px) {
  .user-info {
    margin-left: 0;
    margin-top: 80px;
  }
  
  .avatar-section {
    left: 50%;
    transform: translateX(-50%);
  }
  
  .meta-items {
    flex-direction: column;
    gap: var(--spacing-sm);
  }
  
  .quick-stats {
    flex-wrap: wrap;
  }
  
  .stat-item {
    flex: 0 0 calc(50% - var(--spacing-sm));
  }
}
</style>