<template>
  <div class="user-profile">
    <!-- En-tête du profil -->
    <ProfileHeader
      :user="user"
      :is-own-profile="isOwnProfile"
      :is-following="isFollowing"
      @follow="handleFollow"
      @unfollow="handleUnfollow"
      @edit="showEditModal = true"
      @message="handleMessage"
    />

    <!-- Statistiques -->
    <ProfileStats
      :stats="user.stats"
      :loading="loadingStats"
    />

    <!-- Badges et réalisations -->
    <ProfileBadges
      v-if="user.badges && user.badges.length > 0"
      :badges="user.badges"
    />

    <!-- Navigation des onglets -->
    <div class="profile-tabs">
      <NeuButton
        v-for="tab in tabs"
        :key="tab.id"
        :class="{ 'active': activeTab === tab.id }"
        @click="activeTab = tab.id"
        size="small"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        <span class="tab-label">{{ tab.label }}</span>
      </NeuButton>
    </div>

    <!-- Contenu des onglets -->
    <div class="tab-content">
      <!-- Onglet Posts -->
      <ProfilePosts
        v-if="activeTab === 'posts'"
        :user-id="userId"
        :posts="userPosts"
        :loading="loadingPosts"
        @load-more="loadMorePosts"
      />

      <!-- Onglet Followers -->
      <ProfileFollowers
        v-if="activeTab === 'followers'"
        :user-id="userId"
        :followers="followers"
        :loading="loadingFollowers"
      />

      <!-- Onglet Following -->
      <ProfileFollowing
        v-if="activeTab === 'following'"
        :user-id="userId"
        :following="following"
        :loading="loadingFollowing"
      />

      <!-- Onglet Activité -->
      <ProfileActivity
        v-if="activeTab === 'activity'"
        :user-id="userId"
        :activities="activities"
        :loading="loadingActivity"
      />
    </div>

    <!-- Modal d'édition -->
    <ProfileEditModal
      v-if="showEditModal"
      :user="user"
      @close="showEditModal = false"
      @save="handleSaveProfile"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NeuButton from '../neumorphic/NeuButton.vue'
import ProfileHeader from './ProfileHeader.vue'
import ProfileStats from './ProfileStats.vue'
import ProfileBadges from './ProfileBadges.vue'
import ProfilePosts from './ProfilePosts.vue'
import ProfileFollowers from './ProfileFollowers.vue'
import ProfileFollowing from './ProfileFollowing.vue'
import ProfileActivity from './ProfileActivity.vue'
import ProfileEditModal from './ProfileEditModal.vue'

export default {
  name: 'UserProfile',
  components: {
    NeuButton,
    ProfileHeader,
    ProfileStats,
    ProfileBadges,
    ProfilePosts,
    ProfileFollowers,
    ProfileFollowing,
    ProfileActivity,
    ProfileEditModal
  },
  props: {
    apiService: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const route = useRoute()
    const router = useRouter()
    
    // État réactif
    const user = ref({})
    const userPosts = ref([])
    const followers = ref([])
    const following = ref([])
    const activities = ref([])
    const activeTab = ref('posts')
    const showEditModal = ref(false)
    
    // États de chargement
    const loading = ref(true)
    const loadingStats = ref(false)
    const loadingPosts = ref(false)
    const loadingFollowers = ref(false)
    const loadingFollowing = ref(false)
    const loadingActivity = ref(false)
    
    // État social
    const isFollowing = ref(false)
    
    // Configuration des onglets
    const tabs = ref([
      { id: 'posts', label: 'Posts', icon: '📝' },
      { id: 'followers', label: 'Followers', icon: '👥' },
      { id: 'following', label: 'Following', icon: '👤' },
      { id: 'activity', label: 'Activité', icon: '📊' }
    ])
    
    // Propriétés calculées
    const userId = computed(() => {
      return route.params.id || 'current'
    })
    
    const isOwnProfile = computed(() => {
      return userId.value === 'current' || userId.value === props.apiService.getCurrentUserId?.()
    })
    
    // Méthodes
    const loadUserProfile = async () => {
      loading.value = true
      try {
        const profileData = await props.apiService.getUserProfile(userId.value)
        user.value = profileData
        
        // Charger les données de l'onglet actif
        await loadTabData(activeTab.value)
        
      } catch (error) {
        console.error('Erreur lors du chargement du profil:', error)
        // Rediriger vers 404 ou page d'erreur
        router.push('/404')
      } finally {
        loading.value = false
      }
    }
    
    const loadTabData = async (tabId) => {
      switch (tabId) {
        case 'posts':
          await loadUserPosts()
          break
        case 'followers':
          await loadFollowers()
          break
        case 'following':
          await loadFollowing()
          break
        case 'activity':
          await loadActivity()
          break
      }
    }
    
    const loadUserPosts = async () => {
      loadingPosts.value = true
      try {
        const posts = await props.apiService.getUserPosts(userId.value)
        userPosts.value = posts
      } catch (error) {
        console.error('Erreur lors du chargement des posts:', error)
      } finally {
        loadingPosts.value = false
      }
    }
    
    const loadMorePosts = async () => {
      try {
        const morePosts = await props.apiService.getUserPosts(
          userId.value, 
          10, 
          userPosts.value.length
        )
        userPosts.value.push(...morePosts)
      } catch (error) {
        console.error('Erreur lors du chargement de plus de posts:', error)
      }
    }
    
    const loadFollowers = async () => {
      loadingFollowers.value = true
      try {
        const followersList = await props.apiService.getFollowers(userId.value)
        followers.value = followersList
      } catch (error) {
        console.error('Erreur lors du chargement des followers:', error)
      } finally {
        loadingFollowers.value = false
      }
    }
    
    const loadFollowing = async () => {
      loadingFollowing.value = true
      try {
        const followingList = await props.apiService.getFollowing(userId.value)
        following.value = followingList
      } catch (error) {
        console.error('Erreur lors du chargement des following:', error)
      } finally {
        loadingFollowing.value = false
      }
    }
    
    const loadActivity = async () => {
      loadingActivity.value = true
      try {
        const activityData = await props.apiService.getUserActivity(userId.value)
        activities.value = activityData
      } catch (error) {
        console.error('Erreur lors du chargement de l\'activité:', error)
      } finally {
        loadingActivity.value = false
      }
    }
    
    const handleFollow = async () => {
      try {
        await props.apiService.followUser(userId.value)
        isFollowing.value = true
        user.value.stats.followers_count++
      } catch (error) {
        console.error('Erreur lors du follow:', error)
      }
    }
    
    const handleUnfollow = async () => {
      try {
        await props.apiService.unfollowUser(userId.value)
        isFollowing.value = false
        user.value.stats.followers_count--
      } catch (error) {
        console.error('Erreur lors de l\'unfollow:', error)
      }
    }
    
    const handleMessage = () => {
      // Rediriger vers la messagerie ou ouvrir une modal
      router.push(`/messages/new/${userId.value}`)
    }
    
    const handleSaveProfile = async (updatedData) => {
      try {
        const updatedUser = await props.apiService.updateProfile(updatedData)
        user.value = { ...user.value, ...updatedUser }
        showEditModal.value = false
      } catch (error) {
        console.error('Erreur lors de la sauvegarde du profil:', error)
      }
    }
    
    // Watchers
    watch(() => route.params.id, () => {
      if (route.name === 'UserProfile') {
        loadUserProfile()
      }
    })
    
    watch(activeTab, (newTab) => {
      loadTabData(newTab)
    })
    
    // Lifecycle
    onMounted(() => {
      loadUserProfile()
    })
    
    return {
      user,
      userPosts,
      followers,
      following,
      activities,
      activeTab,
      showEditModal,
      loading,
      loadingStats,
      loadingPosts,
      loadingFollowers,
      loadingFollowing,
      loadingActivity,
      isFollowing,
      tabs,
      userId,
      isOwnProfile,
      handleFollow,
      handleUnfollow,
      handleMessage,
      handleSaveProfile,
      loadMorePosts
    }
  }
}
</script>

<style scoped>
.user-profile {
  max-width: 800px;
  margin: 0 auto;
  padding: var(--spacing-md);
}

.profile-tabs {
  display: flex;
  gap: var(--spacing-sm);
  margin: var(--spacing-lg) 0;
  padding: var(--spacing-md);
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  box-shadow: 
    inset 4px 4px 8px var(--shadow-dark),
    inset -4px -4px 8px var(--shadow-light);
}

.profile-tabs .neu-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  margin: 0;
  transition: all var(--transition-normal);
}

.profile-tabs .neu-button.active {
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: white;
  transform: translateY(-2px);
}

.tab-icon {
  font-size: 1rem;
}

.tab-label {
  font-size: 0.875rem;
  font-weight: 600;
}

.tab-content {
  margin-top: var(--spacing-lg);
}

@media (max-width: 768px) {
  .user-profile {
    padding: var(--spacing-sm);
  }
  
  .profile-tabs {
    flex-direction: column;
    gap: var(--spacing-xs);
  }
  
  .profile-tabs .neu-button {
    justify-content: flex-start;
    padding: var(--spacing-md);
  }
  
  .tab-label {
    display: none;
  }
}

@media (max-width: 480px) {
  .profile-tabs {
    flex-direction: row;
    overflow-x: auto;
    gap: var(--spacing-xs);
  }
  
  .profile-tabs .neu-button {
    flex: none;
    min-width: 80px;
    flex-direction: column;
    gap: var(--spacing-xs);
    padding: var(--spacing-sm);
  }
  
  .tab-label {
    display: block;
    font-size: 0.75rem;
  }
}
</style>