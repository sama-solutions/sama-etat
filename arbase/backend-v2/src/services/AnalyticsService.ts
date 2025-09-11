/**
 * Service Analytics pour le suivi des métriques
 */

import { RedisService } from './RedisService.js';

interface AnalyticsEvent {
  type: 'view' | 'scan' | 'interaction';
  experienceId: string;
  timestamp: Date;
  ip?: string;
  userAgent?: string;
  data?: any;
}

class AnalyticsServiceClass {
  private events: AnalyticsEvent[] = [];
  private batchSize = 100;
  private flushInterval = 30000; // 30 secondes
  private flushTimer: NodeJS.Timeout | null = null;

  async initialize(): Promise<void> {
    // Démarrer le timer de flush périodique
    this.flushTimer = setInterval(() => {
      this.flushEvents().catch(console.error);
    }, this.flushInterval);

    console.log('Service Analytics initialisé');
  }

  async recordView(experienceId: string, ip?: string, userAgent?: string): Promise<void> {
    const event: AnalyticsEvent = {
      type: 'view',
      experienceId,
      timestamp: new Date(),
      ip,
      userAgent
    };

    this.events.push(event);

    // Incrémenter le compteur en temps réel
    await RedisService.incr(`analytics:views:${experienceId}:${this.getDateKey()}`);
    await RedisService.incr(`analytics:views:total:${this.getDateKey()}`);

    if (this.events.length >= this.batchSize) {
      await this.flushEvents();
    }
  }

  async recordScan(experienceId: string, ip?: string, userAgent?: string, location?: any): Promise<void> {
    const event: AnalyticsEvent = {
      type: 'scan',
      experienceId,
      timestamp: new Date(),
      ip,
      userAgent,
      data: { location }
    };

    this.events.push(event);

    // Incrémenter le compteur en temps réel
    await RedisService.incr(`analytics:scans:${experienceId}:${this.getDateKey()}`);
    await RedisService.incr(`analytics:scans:total:${this.getDateKey()}`);

    if (this.events.length >= this.batchSize) {
      await this.flushEvents();
    }
  }

  async recordInteraction(experienceId: string, type: string, data?: any): Promise<void> {
    const event: AnalyticsEvent = {
      type: 'interaction',
      experienceId,
      timestamp: new Date(),
      data: { interactionType: type, ...data }
    };

    this.events.push(event);

    // Incrémenter le compteur en temps réel
    await RedisService.incr(`analytics:interactions:${experienceId}:${this.getDateKey()}`);
    await RedisService.incr(`analytics:interactions:total:${this.getDateKey()}`);

    if (this.events.length >= this.batchSize) {
      await this.flushEvents();
    }
  }

  async getExperienceStats(experienceId: string, days: number = 7): Promise<any> {
    const stats = {
      views: [],
      scans: [],
      interactions: [],
      total: {
        views: 0,
        scans: 0,
        interactions: 0
      }
    };

    // Récupérer les stats des derniers jours
    for (let i = 0; i < days; i++) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      const dateKey = this.formatDateKey(date);

      const [views, scans, interactions] = await Promise.all([
        RedisService.get(`analytics:views:${experienceId}:${dateKey}`) || 0,
        RedisService.get(`analytics:scans:${experienceId}:${dateKey}`) || 0,
        RedisService.get(`analytics:interactions:${experienceId}:${dateKey}`) || 0
      ]);

      stats.views.unshift({ date: dateKey, count: views });
      stats.scans.unshift({ date: dateKey, count: scans });
      stats.interactions.unshift({ date: dateKey, count: interactions });

      stats.total.views += views;
      stats.total.scans += scans;
      stats.total.interactions += interactions;
    }

    return stats;
  }

  async getGlobalStats(days: number = 7): Promise<any> {
    const stats = {
      views: [],
      scans: [],
      interactions: [],
      total: {
        views: 0,
        scans: 0,
        interactions: 0
      }
    };

    // Récupérer les stats globales des derniers jours
    for (let i = 0; i < days; i++) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      const dateKey = this.formatDateKey(date);

      const [views, scans, interactions] = await Promise.all([
        RedisService.get(`analytics:views:total:${dateKey}`) || 0,
        RedisService.get(`analytics:scans:total:${dateKey}`) || 0,
        RedisService.get(`analytics:interactions:total:${dateKey}`) || 0
      ]);

      stats.views.unshift({ date: dateKey, count: views });
      stats.scans.unshift({ date: dateKey, count: scans });
      stats.interactions.unshift({ date: dateKey, count: interactions });

      stats.total.views += views;
      stats.total.scans += scans;
      stats.total.interactions += interactions;
    }

    return stats;
  }

  async getTopExperiences(limit: number = 10): Promise<any[]> {
    // Cette méthode nécessiterait une implémentation plus complexe
    // avec une base de données pour être vraiment efficace
    // Pour l'instant, on retourne un placeholder
    return [];
  }

  private async flushEvents(): Promise<void> {
    if (this.events.length === 0) return;

    try {
      // Dans une vraie implémentation, on sauvegarderait les événements
      // dans une base de données pour analyse détaillée
      console.log(`Flush de ${this.events.length} événements analytics`);
      
      // Vider le buffer
      this.events = [];
    } catch (error) {
      console.error('Erreur lors du flush des événements analytics:', error);
    }
  }

  private getDateKey(): string {
    return this.formatDateKey(new Date());
  }

  private formatDateKey(date: Date): string {
    return date.toISOString().split('T')[0]; // YYYY-MM-DD
  }

  async shutdown(): Promise<void> {
    if (this.flushTimer) {
      clearInterval(this.flushTimer);
      this.flushTimer = null;
    }

    // Flush final des événements
    await this.flushEvents();
  }
}

export const AnalyticsService = new AnalyticsServiceClass();