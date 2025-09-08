/**
 * Service API Demo pour Sama Jokoo
 * ================================
 * 
 * Version démo avec données mockées pour les tests
 */

class DemoAPI {
  constructor() {
    this.isDemo = true;
    this.uid = null;
    this.posts = [
      {
        id: 1,
        content: '<p>Bienvenue sur Sama Jokoo ! 🎉</p>',
        content_preview: 'Bienvenue sur Sama Jokoo ! 🎉',
        author_id: [2, 'Admin'],
        create_date: new Date().toISOString(),
        like_count: 5,
        comment_count: 2,
        state: 'published'
      },
      {
        id: 2,
        content: '<p>Découvrez notre design neumorphique moderne ! ✨</p>',
        content_preview: 'Découvrez notre design neumorphique moderne ! ✨',
        author_id: [2, 'Admin'],
        create_date: new Date(Date.now() - 3600000).toISOString(),
        like_count: 12,
        comment_count: 7,
        state: 'published'
      },
      {
        id: 3,
        content: '<p>Interface responsive et PWA ready ! 📱</p>',
        content_preview: 'Interface responsive et PWA ready ! 📱',
        author_id: [2, 'Admin'],
        create_date: new Date(Date.now() - 7200000).toISOString(),
        like_count: 8,
        comment_count: 3,
        state: 'published'
      }
    ];
  }

  /**
   * Authentification démo
   */
  async login(username, password) {
    // Simulation d'un délai réseau
    await new Promise(resolve => setTimeout(resolve, 500));
    
    if (username === 'admin' && password === 'admin') {
      this.uid = 2;
      
      // Stocker les informations de session
      localStorage.setItem('demo_uid', this.uid);
      localStorage.setItem('demo_username', username);
      
      return {
        success: true,
        uid: this.uid,
        username: username
      };
    } else {
      return {
        success: false,
        error: 'Identifiants incorrects (utilisez admin/admin)'
      };
    }
  }

  /**
   * Déconnexion
   */
  logout() {
    this.uid = null;
    localStorage.removeItem('demo_uid');
    localStorage.removeItem('demo_username');
  }

  /**
   * Vérifier si l'utilisateur est connecté
   */
  isAuthenticated() {
    return this.uid !== null || localStorage.getItem('demo_uid') !== null;
  }

  /**
   * Restaurer la session depuis le localStorage
   */
  async restoreSession() {
    const uid = localStorage.getItem('demo_uid');
    const username = localStorage.getItem('demo_username');

    if (uid && username) {
      this.uid = parseInt(uid);
      return true;
    }
    return false;
  }

  /**
   * Récupérer tous les posts
   */
  async getPosts(limit = 20, offset = 0) {
    // Simulation d'un délai réseau
    await new Promise(resolve => setTimeout(resolve, 300));
    
    if (!this.uid) {
      throw new Error('Non authentifié');
    }

    return this.posts.slice(offset, offset + limit);
  }

  /**
   * Créer un nouveau post
   */
  async createPost(content) {
    // Simulation d'un délai réseau
    await new Promise(resolve => setTimeout(resolve, 400));
    
    if (!this.uid) {
      throw new Error('Non authentifié');
    }

    const newPost = {
      id: this.posts.length + 1,
      content: `<p>${content}</p>`,
      content_preview: content.length > 50 ? content.substring(0, 50) + '...' : content,
      author_id: [this.uid, 'Admin'],
      create_date: new Date().toISOString(),
      like_count: 0,
      comment_count: 0,
      state: 'published'
    };

    this.posts.unshift(newPost);
    return newPost;
  }

  /**
   * Liker/Unliker un post
   */
  async toggleLike(postId) {
    // Simulation d'un délai réseau
    await new Promise(resolve => setTimeout(resolve, 200));
    
    const post = this.posts.find(p => p.id === postId);
    if (post) {
      // Simulation simple du toggle
      const isLiked = Math.random() > 0.5;
      if (isLiked) {
        post.like_count++;
      } else {
        post.like_count = Math.max(0, post.like_count - 1);
      }
      return { liked: isLiked };
    }
    throw new Error('Post non trouvé');
  }

  /**
   * Récupérer les commentaires d'un post
   */
  async getComments(postId, limit = 10) {
    // Simulation d'un délai réseau
    await new Promise(resolve => setTimeout(resolve, 250));
    
    // Commentaires de démonstration
    return [
      {
        id: 1,
        content: '<p>Super application ! 👍</p>',
        content_preview: 'Super application ! 👍',
        author_id: [3, 'Utilisateur Demo'],
        create_date: new Date(Date.now() - 1800000).toISOString(),
        like_count: 2
      },
      {
        id: 2,
        content: '<p>Le design neumorphique est magnifique ! ✨</p>',
        content_preview: 'Le design neumorphique est magnifique ! ✨',
        author_id: [4, 'Fan Design'],
        create_date: new Date(Date.now() - 900000).toISOString(),
        like_count: 5
      }
    ];
  }

  /**
   * Créer un commentaire
   */
  async createComment(postId, content) {
    // Simulation d'un délai réseau
    await new Promise(resolve => setTimeout(resolve, 300));
    
    return {
      id: Math.floor(Math.random() * 1000),
      content: `<p>${content}</p>`,
      content_preview: content,
      author_id: [this.uid, 'Admin'],
      create_date: new Date().toISOString(),
      like_count: 0
    };
  }

  /**
   * Récupérer les informations de l'utilisateur actuel
   */
  async getCurrentUser() {
    if (!this.uid) return null;
    
    return {
      id: this.uid,
      name: 'Administrateur Demo',
      login: 'admin',
      email: 'admin@samajokoo.demo',
      image_128: null
    };
  }

  /**
   * Test de connexion (toujours réussi en mode démo)
   */
  async testConnection() {
    return true;
  }
}

// Instance singleton
const demoApi = new DemoAPI();

export default demoApi;