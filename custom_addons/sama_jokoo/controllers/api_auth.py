# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime, timedelta

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessDenied, ValidationError

_logger = logging.getLogger(__name__)


class SocialAuthAPI(http.Controller):

    @http.route('/api/social/auth/login', type='json', auth='none', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        """Authentification pour l'application mobile"""
        try:
            login = kwargs.get('login')
            password = kwargs.get('password')
            
            if not login or not password:
                return {
                    'success': False,
                    'error': 'Login et mot de passe requis',
                    'code': 'MISSING_CREDENTIALS'
                }
            
            # Authentification
            uid = request.session.authenticate(request.session.db, login, password)
            
            if not uid:
                return {
                    'success': False,
                    'error': 'Identifiants invalides',
                    'code': 'INVALID_CREDENTIALS'
                }
            
            # Récupérer les informations utilisateur
            user = request.env['res.users'].browse(uid)
            
            # Mettre à jour la dernière connexion
            user.update_last_seen()
            
            # Générer un token de session (simplifié pour la démo)
            session_token = request.session.sid
            
            return {
                'success': True,
                'data': {
                    'user_id': user.id,
                    'session_token': session_token,
                    'user_info': {
                        'id': user.id,
                        'name': user.name,
                        'login': user.login,
                        'email': user.email,
                        'image_128': user.image_128,
                        'social_theme': user.social_theme,
                        'social_verified': user.social_verified,
                        'company_id': user.company_id.id,
                        'company_name': user.company_id.name,
                    }
                }
            }
            
        except Exception as e:
            _logger.error(f"Erreur lors de l'authentification: {e}")
            return {
                'success': False,
                'error': 'Erreur interne du serveur',
                'code': 'INTERNAL_ERROR'
            }

    @http.route('/api/social/auth/logout', type='json', auth='user', methods=['POST'], csrf=False)
    def logout(self, **kwargs):
        """Déconnexion"""
        try:
            request.session.logout()
            return {
                'success': True,
                'message': 'Déconnexion réussie'
            }
        except Exception as e:
            _logger.error(f"Erreur lors de la déconnexion: {e}")
            return {
                'success': False,
                'error': 'Erreur lors de la déconnexion',
                'code': 'LOGOUT_ERROR'
            }

    @http.route('/api/social/auth/check', type='json', auth='user', methods=['GET'], csrf=False)
    def check_auth(self, **kwargs):
        """Vérifier l'authentification"""
        try:
            user = request.env.user
            
            # Mettre à jour la dernière connexion
            user.update_last_seen()
            
            return {
                'success': True,
                'data': {
                    'authenticated': True,
                    'user_id': user.id,
                    'user_info': {
                        'id': user.id,
                        'name': user.name,
                        'login': user.login,
                        'email': user.email,
                        'image_128': user.image_128,
                        'social_theme': user.social_theme,
                        'social_verified': user.social_verified,
                        'is_online': user.social_is_online,
                        'last_seen': user.social_last_seen,
                    }
                }
            }
        except Exception as e:
            _logger.error(f"Erreur lors de la vérification d'authentification: {e}")
            return {
                'success': False,
                'error': 'Non authentifié',
                'code': 'NOT_AUTHENTICATED'
            }

    @http.route('/api/social/auth/refresh', type='json', auth='user', methods=['POST'], csrf=False)
    def refresh_token(self, **kwargs):
        """Rafraîchir le token de session"""
        try:
            user = request.env.user
            user.update_last_seen()
            
            # Dans une implémentation réelle, on générerait un nouveau JWT token
            session_token = request.session.sid
            
            return {
                'success': True,
                'data': {
                    'session_token': session_token,
                    'expires_in': 3600,  # 1 heure
                }
            }
        except Exception as e:
            _logger.error(f"Erreur lors du rafraîchissement du token: {e}")
            return {
                'success': False,
                'error': 'Erreur lors du rafraîchissement',
                'code': 'REFRESH_ERROR'
            }

    @http.route('/api/social/auth/register', type='json', auth='none', methods=['POST'], csrf=False)
    def register(self, **kwargs):
        """Inscription (si autorisée)"""
        try:
            # Vérifier si l'inscription est autorisée
            allow_signup = request.env['ir.config_parameter'].sudo().get_param('auth_signup.allow_uninvited', 'False')
            
            if allow_signup != 'True':
                return {
                    'success': False,
                    'error': 'L\'inscription n\'est pas autorisée',
                    'code': 'SIGNUP_DISABLED'
                }
            
            name = kwargs.get('name')
            email = kwargs.get('email')
            password = kwargs.get('password')
            
            if not all([name, email, password]):
                return {
                    'success': False,
                    'error': 'Nom, email et mot de passe requis',
                    'code': 'MISSING_FIELDS'
                }
            
            # Vérifier si l'email existe déjà
            existing_user = request.env['res.users'].sudo().search([('email', '=', email)], limit=1)
            if existing_user:
                return {
                    'success': False,
                    'error': 'Un compte avec cet email existe déjà',
                    'code': 'EMAIL_EXISTS'
                }
            
            # Créer l'utilisateur
            user_vals = {
                'name': name,
                'login': email,
                'email': email,
                'password': password,
                'active': True,
                'groups_id': [(6, 0, [request.env.ref('base.group_user').id])],
            }
            
            user = request.env['res.users'].sudo().create(user_vals)
            
            return {
                'success': True,
                'message': 'Compte créé avec succès',
                'data': {
                    'user_id': user.id,
                    'name': user.name,
                    'email': user.email,
                }
            }
            
        except ValidationError as e:
            return {
                'success': False,
                'error': str(e),
                'code': 'VALIDATION_ERROR'
            }
        except Exception as e:
            _logger.error(f"Erreur lors de l'inscription: {e}")
            return {
                'success': False,
                'error': 'Erreur lors de la création du compte',
                'code': 'REGISTRATION_ERROR'
            }

    @http.route('/api/social/auth/reset-password', type='json', auth='none', methods=['POST'], csrf=False)
    def reset_password(self, **kwargs):
        """Demande de réinitialisation de mot de passe"""
        try:
            email = kwargs.get('email')
            
            if not email:
                return {
                    'success': False,
                    'error': 'Email requis',
                    'code': 'MISSING_EMAIL'
                }
            
            # Rechercher l'utilisateur
            user = request.env['res.users'].sudo().search([('email', '=', email)], limit=1)
            
            if not user:
                # Pour des raisons de sécurité, on ne révèle pas si l'email existe
                return {
                    'success': True,
                    'message': 'Si cet email existe, un lien de réinitialisation a été envoyé'
                }
            
            # Générer un token de réinitialisation
            user.action_reset_password()
            
            return {
                'success': True,
                'message': 'Un lien de réinitialisation a été envoyé à votre email'
            }
            
        except Exception as e:
            _logger.error(f"Erreur lors de la réinitialisation: {e}")
            return {
                'success': False,
                'error': 'Erreur lors de la réinitialisation',
                'code': 'RESET_ERROR'
            }

    @http.route('/api/social/auth/change-password', type='json', auth='user', methods=['POST'], csrf=False)
    def change_password(self, **kwargs):
        """Changer le mot de passe"""
        try:
            current_password = kwargs.get('current_password')
            new_password = kwargs.get('new_password')
            
            if not all([current_password, new_password]):
                return {
                    'success': False,
                    'error': 'Mot de passe actuel et nouveau mot de passe requis',
                    'code': 'MISSING_PASSWORDS'
                }
            
            user = request.env.user
            
            # Vérifier le mot de passe actuel
            try:
                user._check_credentials(current_password, {'interactive': True})
            except AccessDenied:
                return {
                    'success': False,
                    'error': 'Mot de passe actuel incorrect',
                    'code': 'INVALID_CURRENT_PASSWORD'
                }
            
            # Changer le mot de passe
            user.write({'password': new_password})
            
            return {
                'success': True,
                'message': 'Mot de passe changé avec succès'
            }
            
        except Exception as e:
            _logger.error(f"Erreur lors du changement de mot de passe: {e}")
            return {
                'success': False,
                'error': 'Erreur lors du changement de mot de passe',
                'code': 'PASSWORD_CHANGE_ERROR'
            }