/**
 * Service WebSocket pour la communication temps réel
 */

import { Server as SocketIOServer, Socket } from 'socket.io';
import { RedisService } from './RedisService.js';

interface ConnectedUser {
  id: string;
  socketId: string;
  experienceId?: string;
  joinedAt: Date;
}

export class SocketService {
  private io: SocketIOServer;
  private connectedUsers: Map<string, ConnectedUser> = new Map();

  constructor(io: SocketIOServer) {
    this.io = io;
    this.setupEventHandlers();
  }

  private setupEventHandlers(): void {
    this.io.on('connection', (socket: Socket) => {
      console.log(`Nouvelle connexion WebSocket: ${socket.id}`);

      // Événements de connexion
      socket.on('join', this.handleJoin.bind(this, socket));
      socket.on('leave', this.handleLeave.bind(this, socket));
      
      // Événements AR
      socket.on('ar:scan', this.handleARScan.bind(this, socket));
      socket.on('ar:interaction', this.handleARInteraction.bind(this, socket));
      socket.on('ar:session:start', this.handleARSessionStart.bind(this, socket));
      socket.on('ar:session:end', this.handleARSessionEnd.bind(this, socket));

      // Événements de déconnexion
      socket.on('disconnect', this.handleDisconnect.bind(this, socket));
    });
  }

  private async handleJoin(socket: Socket, data: { userId?: string; experienceId?: string }): Promise<void> {
    try {
      const user: ConnectedUser = {
        id: data.userId || `anonymous_${socket.id}`,
        socketId: socket.id,
        experienceId: data.experienceId,
        joinedAt: new Date()
      };

      this.connectedUsers.set(socket.id, user);

      // Rejoindre la room de l'expérience si spécifiée
      if (data.experienceId) {
        socket.join(`experience:${data.experienceId}`);
        
        // Notifier les autres utilisateurs de l'expérience
        socket.to(`experience:${data.experienceId}`).emit('user:joined', {
          userId: user.id,
          experienceId: data.experienceId
        });

        // Incrémenter le compteur d'utilisateurs actifs
        await RedisService.incr(`active_users:${data.experienceId}`);
      }

      socket.emit('joined', { success: true, userId: user.id });
      
      console.log(`Utilisateur ${user.id} rejoint l'expérience ${data.experienceId}`);
    } catch (error) {
      console.error('Erreur lors du join:', error);
      socket.emit('error', { message: 'Erreur lors de la connexion' });
    }
  }

  private async handleLeave(socket: Socket, data: { experienceId?: string }): Promise<void> {
    try {
      const user = this.connectedUsers.get(socket.id);
      if (!user) return;

      const experienceId = data.experienceId || user.experienceId;
      
      if (experienceId) {
        socket.leave(`experience:${experienceId}`);
        
        // Notifier les autres utilisateurs
        socket.to(`experience:${experienceId}`).emit('user:left', {
          userId: user.id,
          experienceId
        });

        // Décrémenter le compteur d'utilisateurs actifs
        const activeUsers = await RedisService.get(`active_users:${experienceId}`) || 0;
        if (activeUsers > 0) {
          await RedisService.set(`active_users:${experienceId}`, activeUsers - 1);
        }
      }

      socket.emit('left', { success: true });
      
      console.log(`Utilisateur ${user.id} a quitté l'expérience ${experienceId}`);
    } catch (error) {
      console.error('Erreur lors du leave:', error);
    }
  }

  private async handleARScan(socket: Socket, data: { experienceId: string; qrData: any }): Promise<void> {
    try {
      const user = this.connectedUsers.get(socket.id);
      if (!user) return;

      // Diffuser l'événement de scan aux autres utilisateurs de l'expérience
      socket.to(`experience:${data.experienceId}`).emit('ar:scan:detected', {
        userId: user.id,
        experienceId: data.experienceId,
        qrData: data.qrData,
        timestamp: new Date()
      });

      // Mettre à jour les statistiques en temps réel
      await RedisService.incr(`realtime:scans:${data.experienceId}`);

      console.log(`Scan AR détecté par ${user.id} pour l'expérience ${data.experienceId}`);
    } catch (error) {
      console.error('Erreur lors du scan AR:', error);
    }
  }

  private async handleARInteraction(socket: Socket, data: { 
    experienceId: string; 
    type: string; 
    target: string; 
    data?: any 
  }): Promise<void> {
    try {
      const user = this.connectedUsers.get(socket.id);
      if (!user) return;

      // Diffuser l'interaction aux autres utilisateurs
      socket.to(`experience:${data.experienceId}`).emit('ar:interaction:detected', {
        userId: user.id,
        experienceId: data.experienceId,
        type: data.type,
        target: data.target,
        data: data.data,
        timestamp: new Date()
      });

      // Mettre à jour les statistiques
      await RedisService.incr(`realtime:interactions:${data.experienceId}`);

      console.log(`Interaction AR de ${user.id}: ${data.type} sur ${data.target}`);
    } catch (error) {
      console.error('Erreur lors de l\'interaction AR:', error);
    }
  }

  private async handleARSessionStart(socket: Socket, data: { experienceId: string }): Promise<void> {
    try {
      const user = this.connectedUsers.get(socket.id);
      if (!user) return;

      // Enregistrer le début de session
      await RedisService.set(`session:${socket.id}:start`, Date.now());
      
      // Notifier les autres utilisateurs
      socket.to(`experience:${data.experienceId}`).emit('ar:session:started', {
        userId: user.id,
        experienceId: data.experienceId,
        timestamp: new Date()
      });

      console.log(`Session AR démarrée par ${user.id} pour l'expérience ${data.experienceId}`);
    } catch (error) {
      console.error('Erreur lors du démarrage de session AR:', error);
    }
  }

  private async handleARSessionEnd(socket: Socket, data: { 
    experienceId: string; 
    duration?: number; 
    interactions?: number 
  }): Promise<void> {
    try {
      const user = this.connectedUsers.get(socket.id);
      if (!user) return;

      // Calculer la durée si pas fournie
      let duration = data.duration;
      if (!duration) {
        const startTime = await RedisService.get(`session:${socket.id}:start`);
        if (startTime) {
          duration = Date.now() - startTime;
          await RedisService.del(`session:${socket.id}:start`);
        }
      }

      // Notifier les autres utilisateurs
      socket.to(`experience:${data.experienceId}`).emit('ar:session:ended', {
        userId: user.id,
        experienceId: data.experienceId,
        duration,
        interactions: data.interactions || 0,
        timestamp: new Date()
      });

      console.log(`Session AR terminée par ${user.id}: ${duration}ms, ${data.interactions || 0} interactions`);
    } catch (error) {
      console.error('Erreur lors de la fin de session AR:', error);
    }
  }

  private async handleDisconnect(socket: Socket): Promise<void> {
    try {
      const user = this.connectedUsers.get(socket.id);
      if (!user) return;

      // Nettoyer les données de session
      await RedisService.del(`session:${socket.id}:start`);

      // Notifier la déconnexion si l'utilisateur était dans une expérience
      if (user.experienceId) {
        socket.to(`experience:${user.experienceId}`).emit('user:disconnected', {
          userId: user.id,
          experienceId: user.experienceId
        });

        // Décrémenter le compteur d'utilisateurs actifs
        const activeUsers = await RedisService.get(`active_users:${user.experienceId}`) || 0;
        if (activeUsers > 0) {
          await RedisService.set(`active_users:${user.experienceId}`, activeUsers - 1);
        }
      }

      this.connectedUsers.delete(socket.id);
      
      console.log(`Utilisateur ${user.id} déconnecté`);
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error);
    }
  }

  // Méthodes publiques pour envoyer des événements
  async broadcastToExperience(experienceId: string, event: string, data: any): Promise<void> {
    this.io.to(`experience:${experienceId}`).emit(event, data);
  }

  async sendToUser(socketId: string, event: string, data: any): Promise<void> {
    this.io.to(socketId).emit(event, data);
  }

  async getActiveUsers(experienceId?: string): Promise<number> {
    if (experienceId) {
      return await RedisService.get(`active_users:${experienceId}`) || 0;
    }
    return this.connectedUsers.size;
  }

  async getConnectedUsers(): Promise<ConnectedUser[]> {
    return Array.from(this.connectedUsers.values());
  }

  async getRealTimeStats(experienceId: string): Promise<any> {
    const [scans, interactions, activeUsers] = await Promise.all([
      RedisService.get(`realtime:scans:${experienceId}`) || 0,
      RedisService.get(`realtime:interactions:${experienceId}`) || 0,
      RedisService.get(`active_users:${experienceId}`) || 0
    ]);

    return {
      scans,
      interactions,
      activeUsers,
      timestamp: new Date()
    };
  }
}