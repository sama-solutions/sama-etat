/**
 * Middleware de gestion d'erreurs
 */

import { Request, Response, NextFunction } from 'express';

interface CustomError extends Error {
  statusCode?: number;
  code?: string | number;
}

export const errorHandler = (
  error: CustomError,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  let statusCode = error.statusCode || 500;
  let message = error.message || 'Erreur serveur interne';

  // Erreurs MongoDB
  if (error.name === 'ValidationError') {
    statusCode = 400;
    message = 'Données invalides';
  }

  if (error.name === 'CastError') {
    statusCode = 400;
    message = 'Format d\'ID invalide';
  }

  if (error.code === 11000) {
    statusCode = 409;
    message = 'Ressource déjà existante';
  }

  // Erreurs JWT
  if (error.name === 'JsonWebTokenError') {
    statusCode = 401;
    message = 'Token invalide';
  }

  if (error.name === 'TokenExpiredError') {
    statusCode = 401;
    message = 'Token expiré';
  }

  // Log de l'erreur
  console.error(`Erreur ${statusCode}: ${message}`, {
    error: error.message,
    stack: error.stack,
    url: req.url,
    method: req.method,
    ip: req.ip,
    userAgent: req.get('User-Agent')
  });

  // Réponse d'erreur
  res.status(statusCode).json({
    error: message,
    ...(process.env.NODE_ENV === 'development' && {
      stack: error.stack,
      details: error
    })
  });
};