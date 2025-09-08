/**
 * Service API Odoo pour Sama Jokoo
 * ================================
 * 
 * Gestion de la connexion et des appels API vers Odoo
 */

class OdooAPI {
  constructor(baseURL = 'http://localhost:8070') {
    this.baseURL = baseURL;
    this.sessionId = null;
    this.uid = null;
    this.database = 'sama_jokoo_dev';
  }

  /**
   * Authentification utilisateur
   */
  async login(username, password) {
    try {
      const response = await fetch(`${this.baseURL}/jsonrpc`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          jsonrpc: '2.0',
          method: 'call',
          params: {
            service: 'common',
            method: 'authenticate',
            args: [this.database, username, password, {}]
          },
          id: 1
        })
      });

      const data = await response.json();
      
      if (data.result && data.result !== false) {
        this.uid = data.result;
        this.sessionId = response.headers.get('Set-Cookie');
        
        // Stocker les informations de session
        localStorage.setItem('odoo_uid', this.uid);
        localStorage.setItem('odoo_username', username);
        localStorage.setItem('odoo_password', password);
        
        return {
          success: true,
          uid: this.uid,
          username: username
        };
      } else {
        throw new Error('Identifiants incorrects');
      }
    } catch (error) {
      console.error('Erreur de connexion:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Déconnexion
   */
  logout() {
    this.uid = null;
    this.sessionId = null;
    localStorage.removeItem('odoo_uid');
    localStorage.removeItem('odoo_username');
    localStorage.removeItem('odoo_password');
  }

  /**
   * Vérifier si l'utilisateur est connecté
   */
  isAuthenticated() {
    return this.uid !== null || localStorage.getItem('odoo_uid') !== null;
  }

  /**
   * Restaurer la session depuis le localStorage
   */
  async restoreSession() {
    const uid = localStorage.getItem('odoo_uid');
    const username = localStorage.getItem('odoo_username');
    const password = localStorage.getItem('odoo_password');

    if (uid && username && password) {
      const result = await this.login(username, password);
      return result.success;
    }
    return false;
  }

  /**
   * Appel générique à l'API Odoo
   */
  async call(model, method, args = [], kwargs = {}) {
    if (!this.uid) {
      throw new Error('Non authentifié');
    }

    try {
      const response = await fetch(`${this.baseURL}/jsonrpc`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          jsonrpc: '2.0',
          method: 'call',
          params: {
            service: 'object',
            method: 'execute_kw',
            args: [
              this.database,
              this.uid,
              localStorage.getItem('odoo_password'),
              model,
              method,
              args,
              kwargs
            ]
          },
          id: Math.floor(Math.random() * 1000)
        })
      });

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error.data.message || 'Erreur API');
      }
      
      return data.result;
    } catch (error) {
      console.error(`Erreur API ${model}.${method}:`, error);
      throw error;
    }
  }

  /**
   * Récupérer tous les posts
   */
  async getPosts(limit = 20, offset = 0) {
    return await this.call('social.post', 'search_read', [
      [], // domain (tous les posts)
      ['id', 'content', 'content_preview', 'author_id', 'create_date', 'like_count', 'comment_count', 'state']
    ], {
      limit: limit,
      offset: offset,
      order: 'create_date desc'
    });
  }

  /**
   * Créer un nouveau post
   */
  async createPost(content) {
    const postId = await this.call('social.post', 'create', [{
      content: content
    }]);
    
    // Récupérer le post créé avec toutes ses données
    const posts = await this.call('social.post', 'read', [postId], {
      fields: ['id', 'content', 'content_preview', 'author_id', 'create_date', 'like_count', 'comment_count', 'state']
    });
    
    return posts[0];
  }

  /**
   * Liker/Unliker un post
   */
  async toggleLike(postId) {
    return await this.call('social.post', 'action_like', [postId]);
  }

  /**
   * Récupérer les commentaires d'un post
   */
  async getComments(postId, limit = 10) {
    return await this.call('social.comment', 'search_read', [
      [['post_id', '=', postId], ['state', '=', 'published']],
      ['id', 'content', 'content_preview', 'author_id', 'create_date', 'like_count']
    ], {
      limit: limit,
      order: 'create_date asc'
    });
  }

  /**
   * Créer un commentaire
   */
  async createComment(postId, content) {
    return await this.call('social.comment', 'create', [{
      post_id: postId,
      content: content
    }]);
  }

  /**
   * Récupérer les informations de l'utilisateur actuel
   */
  async getCurrentUser() {
    if (!this.uid) return null;
    
    const users = await this.call('res.users', 'read', [this.uid], {
      fields: ['id', 'name', 'login', 'email', 'image_128']
    });
    
    return users[0];
  }

  /**
   * Test de connexion rapide
   */
  async testConnection() {
    try {
      const response = await fetch(`${this.baseURL}/web/database/selector`, {
        method: 'GET',
        timeout: 5000
      });
      return response.ok;
    } catch (error) {
      return false;
    }
  }
}

// Instance singleton
const odooApi = new OdooAPI();

export default odooApi;