/**
 * Middleware de limitation de taux
 */

import { Request, Response, NextFunction } from 'express';
import { RedisService } from '../services/RedisService.js';

interface RateLimitOptions {
  windowMs: number;
  max: number;
  message?: string;
  keyGenerator?: (req: Request) => string;
}

const defaultOptions: RateLimitOptions = {
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requêtes par fenêtre
  message: 'Trop de requêtes, veuillez réessayer plus tard',
  keyGenerator: (req: Request) => req.ip
};

export const createRateLimiter = (options: Partial<RateLimitOptions> = {}) => {
  const opts = { ...defaultOptions, ...options };
  
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      const key = opts.keyGenerator!(req);
      const windowSeconds = Math.floor(opts.windowMs / 1000);
      
      const result = await RedisService.rateLimitCheck(key, opts.max, windowSeconds);
      
      // Ajouter les headers de rate limiting
      res.set({
        'X-RateLimit-Limit': opts.max.toString(),
        'X-RateLimit-Remaining': result.remaining.toString(),
        'X-RateLimit-Reset': new Date(result.resetTime).toISOString()
      });
      
      if (!result.allowed) {
        return res.status(429).json({
          error: opts.message,
          retryAfter: Math.ceil((result.resetTime - Date.now()) / 1000)
        });
      }
      
      next();
    } catch (error) {
      console.error('Erreur rate limiter:', error);
      // En cas d'erreur, laisser passer la requête
      next();
    }
  };
};

// Rate limiters prédéfinis
export const rateLimiter = createRateLimiter();

export const strictRateLimiter = createRateLimiter({
  windowMs: 5 * 60 * 1000, // 5 minutes
  max: 20, // 20 requêtes par fenêtre
  message: 'Limite stricte atteinte, veuillez réessayer dans quelques minutes'
});

export const apiRateLimiter = createRateLimiter({
  windowMs: 60 * 1000, // 1 minute
  max: 60, // 60 requêtes par minute
  keyGenerator: (req: Request) => {
    return `${req.ip}:${req.get('User-Agent') || 'unknown'}`;
  }
});