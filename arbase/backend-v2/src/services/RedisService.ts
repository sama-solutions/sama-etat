/**
 * Service Redis pour le cache et les sessions
 */

import { createClient, RedisClientType } from 'redis';

class RedisServiceClass {
  private client: RedisClientType | null = null;
  private isConnected = false;

  async connect(): Promise<void> {
    try {
      this.client = createClient({
        url: process.env.REDIS_URL || 'redis://localhost:6379',
        socket: {
          connectTimeout: 5000
        }
      });

      this.client.on('error', (err) => {
        console.error('Erreur Redis:', err);
        this.isConnected = false;
      });

      this.client.on('connect', () => {
        console.log('Connexion Redis établie');
        this.isConnected = true;
      });

      await this.client.connect();
    } catch (error) {
      console.error('Impossible de se connecter à Redis:', error);
      this.client = null;
      this.isConnected = false;
      throw error;
    }
  }

  async disconnect(): Promise<void> {
    if (this.client) {
      await this.client.quit();
      this.client = null;
      this.isConnected = false;
    }
  }

  isConnectedState(): boolean {
    return this.isConnected && this.client !== null;
  }

  isConnected(): boolean {
    return this.isConnectedState();
  }

  async get(key: string): Promise<any> {
    if (!this.isConnectedState()) return null;

    try {
      const value = await this.client!.get(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error('Erreur Redis GET:', error);
      return null;
    }
  }

  async set(key: string, value: any): Promise<boolean> {
    if (!this.isConnectedState()) return false;

    try {
      await this.client!.set(key, JSON.stringify(value));
      return true;
    } catch (error) {
      console.error('Erreur Redis SET:', error);
      return false;
    }
  }

  async setex(key: string, seconds: number, value: any): Promise<boolean> {
    if (!this.isConnectedState()) return false;

    try {
      await this.client!.setEx(key, seconds, JSON.stringify(value));
      return true;
    } catch (error) {
      console.error('Erreur Redis SETEX:', error);
      return false;
    }
  }

  async del(key: string): Promise<boolean> {
    if (!this.isConnectedState()) return false;

    try {
      await this.client!.del(key);
      return true;
    } catch (error) {
      console.error('Erreur Redis DEL:', error);
      return false;
    }
  }

  async keys(pattern: string): Promise<string[]> {
    if (!this.isConnectedState()) return [];

    try {
      return await this.client!.keys(pattern);
    } catch (error) {
      console.error('Erreur Redis KEYS:', error);
      return [];
    }
  }

  async invalidatePattern(pattern: string): Promise<number> {
    if (!this.isConnectedState()) return 0;

    try {
      const keys = await this.keys(pattern);
      if (keys.length === 0) return 0;

      await this.client!.del(keys);
      return keys.length;
    } catch (error) {
      console.error('Erreur Redis invalidatePattern:', error);
      return 0;
    }
  }

  async incr(key: string): Promise<number> {
    if (!this.isConnectedState()) return 0;

    try {
      return await this.client!.incr(key);
    } catch (error) {
      console.error('Erreur Redis INCR:', error);
      return 0;
    }
  }

  async rateLimitCheck(key: string, limit: number, window: number): Promise<{ allowed: boolean; remaining: number; resetTime: number }> {
    if (!this.isConnectedState()) {
      return { allowed: true, remaining: limit - 1, resetTime: Date.now() + window * 1000 };
    }

    try {
      const rateLimitKey = `ratelimit:${key}`;
      const current = await this.incr(rateLimitKey);
      
      if (current === 1) {
        await this.client!.expire(rateLimitKey, window);
      }

      const ttl = await this.client!.ttl(rateLimitKey);
      const resetTime = Date.now() + ttl * 1000;

      return {
        allowed: current <= limit,
        remaining: Math.max(0, limit - current),
        resetTime
      };
    } catch (error) {
      console.error('Erreur Redis rate limit:', error);
      return { allowed: true, remaining: limit - 1, resetTime: Date.now() + window * 1000 };
    }
  }
}

export const RedisService = new RedisServiceClass();