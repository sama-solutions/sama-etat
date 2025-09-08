<template>
  <div class="login-view">
    <div class="login-container">
      <!-- Logo et titre -->
      <div class="login-header">
        <div class="logo-container">
          <div class="logo">SJ</div>
        </div>
        <h1 class="login-title">Sama Jokoo</h1>
        <p class="login-subtitle">Connectez-vous à votre réseau social</p>
      </div>

      <!-- Formulaire de connexion -->
      <NeuCard class="login-form">
        <form @submit.prevent="handleLogin">
          <NeuInput
            v-model="credentials.username"
            label="Nom d'utilisateur"
            placeholder="Entrez votre nom d'utilisateur"
            :error="errors.username"
            :disabled="loading"
          >
            <template #icon>
              <UserIcon />
            </template>
          </NeuInput>

          <NeuInput
            v-model="credentials.password"
            type="password"
            label="Mot de passe"
            placeholder="Entrez votre mot de passe"
            :error="errors.password"
            :disabled="loading"
          >
            <template #icon>
              <LockIcon />
            </template>
          </NeuInput>

          <div v-if="errors.general" class="error-message">
            {{ errors.general }}
          </div>

          <NeuButton
            type="submit"
            variant="primary"
            size="large"
            :loading="loading"
            :disabled="!isFormValid"
            class="login-button"
          >
            Se connecter
          </NeuButton>
        </form>
      </NeuCard>

      <!-- Informations de test -->
      <NeuCard variant="flat" class="test-info">
        <h3>Compte de test</h3>
        <p><strong>Utilisateur :</strong> admin</p>
        <p><strong>Mot de passe :</strong> admin</p>
        <NeuButton
          variant="success"
          size="small"
          @click="fillTestCredentials"
          :disabled="loading"
        >
          Utiliser le compte de test
        </NeuButton>
      </NeuCard>

      <!-- Statut de connexion -->
      <div class="connection-status">
        <div :class="['status-indicator', connectionStatus]"></div>
        <span class="status-text">{{ connectionStatusText }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NeuCard from '../components/neumorphic/NeuCard.vue'
import NeuInput from '../components/neumorphic/NeuInput.vue'
import NeuButton from '../components/neumorphic/NeuButton.vue'
import odooApi from '../services/odooApi.js'
import demoApi from '../services/demoApi.js'

export default {
  name: 'LoginView',
  components: {
    NeuCard,
    NeuInput,
    NeuButton
  },
  setup() {
    const router = useRouter()
    
    const credentials = ref({
      username: '',
      password: ''
    })
    
    const errors = ref({
      username: '',
      password: '',
      general: ''
    })
    
    const loading = ref(false)
    const connectionStatus = ref('checking')
    
    const isFormValid = computed(() => {
      return credentials.value.username.length > 0 && 
             credentials.value.password.length > 0 && 
             !loading.value
    })
    
    const connectionStatusText = computed(() => {
      switch (connectionStatus.value) {
        case 'connected': return 'Serveur Odoo accessible'
        case 'disconnected': return 'Serveur Odoo non accessible'
        case 'demo': return 'Mode démo activé'
        case 'checking': return 'Vérification de la connexion...'
        default: return 'Statut inconnu'
      }
    })
    
    const checkConnection = async () => {
      connectionStatus.value = 'checking'
      try {
        const isConnected = await odooApi.testConnection()
        connectionStatus.value = isConnected ? 'connected' : 'disconnected'
      } catch (error) {
        // En cas d'erreur, utiliser le mode démo
        connectionStatus.value = 'demo'
      }
    }
    
    const validateForm = () => {
      errors.value = { username: '', password: '', general: '' }
      
      if (!credentials.value.username) {
        errors.value.username = 'Le nom d\'utilisateur est requis'
        return false
      }
      
      if (!credentials.value.password) {
        errors.value.password = 'Le mot de passe est requis'
        return false
      }
      
      return true
    }
    
    const handleLogin = async () => {
      if (!validateForm()) return
      
      loading.value = true
      errors.value.general = ''
      
      try {
        let result
        
        // Choisir l'API selon le statut de connexion
        if (connectionStatus.value === 'connected') {
          result = await odooApi.login(
            credentials.value.username,
            credentials.value.password
          )
        } else {
          // Utiliser l'API démo
          result = await demoApi.login(
            credentials.value.username,
            credentials.value.password
          )
        }
        
        if (result.success) {
          // Redirection vers le feed
          router.push('/feed')
        } else {
          errors.value.general = result.error || 'Erreur de connexion'
        }
      } catch (error) {
        errors.value.general = 'Erreur de connexion au serveur'
        console.error('Erreur de connexion:', error)
      } finally {
        loading.value = false
      }
    }
    
    const fillTestCredentials = () => {
      credentials.value.username = 'admin'
      credentials.value.password = 'admin'
    }
    
    // Vérifier la connexion au montage
    onMounted(async () => {
      await checkConnection()
      
      // Vérifier si déjà connecté
      if (connectionStatus.value === 'connected' && odooApi.isAuthenticated()) {
        const restored = await odooApi.restoreSession()
        if (restored) {
          router.push('/feed')
        }
      } else if (connectionStatus.value === 'demo' && demoApi.isAuthenticated()) {
        const restored = await demoApi.restoreSession()
        if (restored) {
          router.push('/feed')
        }
      }
    })
    
    return {
      credentials,
      errors,
      loading,
      connectionStatus,
      isFormValid,
      connectionStatusText,
      handleLogin,
      fillTestCredentials,
      checkConnection
    }
  }
}

// Composants d'icônes simples
const UserIcon = {
  template: `
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
    </svg>
  `
}

const LockIcon = {
  template: `
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
      <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/>
    </svg>
  `
}
</script>

<style scoped>
.login-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
  padding: var(--spacing-md);
}

.login-container {
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.logo-container {
  margin-bottom: var(--spacing-lg);
}

.logo {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: var(--text-white);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  margin: 0 auto;
  box-shadow: 
    8px 8px 16px var(--shadow-dark),
    -8px -8px 16px var(--shadow-light);
}

.login-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.login-subtitle {
  color: var(--text-secondary);
  font-size: 1rem;
}

.login-form {
  margin-bottom: var(--spacing-lg);
}

.login-button {
  width: 100%;
  margin-top: var(--spacing-md);
}

.error-message {
  color: var(--accent-error);
  text-align: center;
  margin-bottom: var(--spacing-md);
  padding: var(--spacing-sm);
  background: rgba(255, 107, 107, 0.1);
  border-radius: var(--radius-sm);
}

.test-info {
  margin-bottom: var(--spacing-lg);
  text-align: center;
}

.test-info h3 {
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.test-info p {
  color: var(--text-secondary);
  margin-bottom: var(--spacing-xs);
  font-size: 0.875rem;
}

.connection-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: var(--radius-full);
  transition: all var(--transition-normal);
}

.status-indicator.connected {
  background: var(--accent-success);
  box-shadow: 0 0 8px rgba(78, 205, 196, 0.5);
}

.status-indicator.disconnected {
  background: var(--accent-error);
  box-shadow: 0 0 8px rgba(255, 107, 107, 0.5);
}

.status-indicator.checking {
  background: var(--accent-warning);
  animation: neu-pulse 1.5s infinite;
}

.status-indicator.demo {
  background: linear-gradient(45deg, var(--accent-primary), var(--accent-secondary));
  box-shadow: 0 0 8px rgba(102, 126, 234, 0.5);
}

.status-text {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

@media (max-width: 480px) {
  .login-view {
    padding: var(--spacing-sm);
  }
  
  .login-title {
    font-size: 2rem;
  }
  
  .logo {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }
}
</style>