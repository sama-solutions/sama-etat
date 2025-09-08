# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime

from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError, AccessError

_logger = logging.getLogger(__name__)


class SocialNotificationAPI(http.Controller):

    def _get_success_response(self, data=None, message=None):
        """Format de réponse de succès standardisé"""
        response = {'success': True}
        if data is not None:
            response['data'] = data
        if message:
            response['message'] = message
        return response

    def _get_error_response(self, error, code=None):
        """Format de réponse d'erreur standardisé"""
        response = {
            'success': False,
            'error': error
        }
        if code:
            response['code'] = code
        return response

    @http.route('/api/social/notifications', type='json', auth='user', methods=['GET'], csrf=False)
    def get_notifications(self, **kwargs):
        """Récupérer les notifications de l'utilisateur"""
        try:
            limit = kwargs.get('limit', 50)
            unread_only = kwargs.get('unread_only', False)
            
            notifications_data = request.env['social.notification'].get_notifications(
                limit=limit,
                unread_only=unread_only
            )
            
            return self._get_success_response(notifications_data)
            
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des notifications: {e}")
            return self._get_error_response('Erreur lors de la récupération des notifications', 'FETCH_ERROR')

    @http.route('/api/social/notifications/count', type='json', auth='user', methods=['GET'], csrf=False)
    def get_unread_count(self, **kwargs):
        """Récupérer le nombre de notifications non lues"""
        try:
            count = request.env['social.notification'].get_unread_count()
            
            return self._get_success_response({'unread_count': count})
            
        except Exception as e:
            _logger.error(f"Erreur lors du comptage des notifications: {e}")
            return self._get_error_response('Erreur lors du comptage', 'COUNT_ERROR')

    @http.route('/api/social/notifications/<int:notification_id>/read', type='json', auth='user', methods=['POST'], csrf=False)
    def mark_notification_read(self, notification_id, **kwargs):
        """Marquer une notification comme lue"""
        try:
            notification = request.env['social.notification'].browse(notification_id)
            
            if not notification.exists():
                return self._get_error_response('Notification non trouvée', 'NOTIFICATION_NOT_FOUND')
            
            if notification.user_id != request.env.user:
                return self._get_error_response('Accès refusé', 'ACCESS_DENIED')
            
            notification.action_mark_read()
            
            return self._get_success_response({'message': 'Notification marquée comme lue'})
            
        except Exception as e:
            _logger.error(f"Erreur lors du marquage de la notification {notification_id}: {e}")
            return self._get_error_response('Erreur lors du marquage', 'MARK_ERROR')

    @http.route('/api/social/notifications/mark-all-read', type='json', auth='user', methods=['POST'], csrf=False)
    def mark_all_read(self, **kwargs):
        """Marquer toutes les notifications comme lues"""
        try:
            count = request.env['social.notification'].mark_all_read()
            
            return self._get_success_response({
                'message': f'{count} notifications marquées comme lues',
                'count': count
            })
            
        except Exception as e:
            _logger.error(f"Erreur lors du marquage global: {e}")
            return self._get_error_response('Erreur lors du marquage global', 'MARK_ALL_ERROR')

    @http.route('/api/social/notifications/stats', type='json', auth='user', methods=['GET'], csrf=False)
    def get_notification_stats(self, **kwargs):
        """Récupérer les statistiques de notifications"""
        try:
            stats = request.env['social.notification'].get_notification_stats()
            
            return self._get_success_response(stats)
            
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des statistiques: {e}")
            return self._get_error_response('Erreur lors de la récupération des statistiques', 'STATS_ERROR')

    @http.route('/api/social/notifications/preferences', type='json', auth='user', methods=['GET'], csrf=False)
    def get_notification_preferences(self, **kwargs):
        """Récupérer les préférences de notification de l'utilisateur"""
        try:
            preferences = request.env.user.get_notification_preferences()
            
            return self._get_success_response(preferences)
            
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des préférences: {e}")
            return self._get_error_response('Erreur lors de la récupération des préférences', 'PREFERENCES_ERROR')

    @http.route('/api/social/notifications/preferences', type='json', auth='user', methods=['PUT'], csrf=False)
    def update_notification_preferences(self, **kwargs):
        """Mettre à jour les préférences de notification"""
        try:
            preferences = {
                'likes': kwargs.get('likes'),
                'comments': kwargs.get('comments'),
                'mentions': kwargs.get('mentions'),
                'follows': kwargs.get('follows'),
                'push': kwargs.get('push'),
            }
            
            # Filtrer les valeurs None
            preferences = {k: v for k, v in preferences.items() if v is not None}
            
            if not preferences:
                return self._get_error_response('Aucune préférence fournie', 'NO_PREFERENCES')
            
            request.env.user.update_notification_preferences(preferences)
            
            return self._get_success_response({'message': 'Préférences mises à jour avec succès'})
            
        except ValidationError as e:
            return self._get_error_response(str(e), 'VALIDATION_ERROR')
        except Exception as e:
            _logger.error(f"Erreur lors de la mise à jour des préférences: {e}")
            return self._get_error_response('Erreur lors de la mise à jour', 'UPDATE_ERROR')

    @http.route('/api/social/notifications/test', type='json', auth='user', methods=['POST'], csrf=False)
    def send_test_notification(self, **kwargs):
        """Envoyer une notification de test"""
        try:
            notification_type = kwargs.get('type', 'system')
            title = kwargs.get('title', 'Notification de test')
            message = kwargs.get('message', 'Ceci est une notification de test depuis l\'API Sama Jokoo')
            
            notification = request.env['social.notification'].create_notification(
                user_id=request.env.user.id,
                notification_type=notification_type,
                title=title,
                message=message,
                author_id=request.env.user.id
            )
            
            return self._get_success_response({
                'notification_id': notification.id,
                'message': 'Notification de test envoyée'
            })
            
        except Exception as e:
            _logger.error(f"Erreur lors de l'envoi de la notification de test: {e}")
            return self._get_error_response('Erreur lors de l\'envoi', 'SEND_ERROR')

    @http.route('/api/social/notifications/<int:notification_id>', type='json', auth='user', methods=['DELETE'], csrf=False)
    def delete_notification(self, notification_id, **kwargs):
        """Supprimer une notification"""
        try:
            notification = request.env['social.notification'].browse(notification_id)
            
            if not notification.exists():
                return self._get_error_response('Notification non trouvée', 'NOTIFICATION_NOT_FOUND')
            
            if notification.user_id != request.env.user:
                return self._get_error_response('Accès refusé', 'ACCESS_DENIED')
            
            notification.unlink()
            
            return self._get_success_response({'message': 'Notification supprimée'})
            
        except Exception as e:
            _logger.error(f"Erreur lors de la suppression de la notification {notification_id}: {e}")
            return self._get_error_response('Erreur lors de la suppression', 'DELETE_ERROR')

    @http.route('/api/social/notifications/cleanup', type='json', auth='user', methods=['POST'], csrf=False)
    def cleanup_old_notifications(self, **kwargs):
        """Nettoyer les anciennes notifications"""
        try:
            days = kwargs.get('days', 30)
            
            # Seuls les admins peuvent nettoyer
            if not request.env.user.has_group('sama_jokoo.group_social_admin'):
                return self._get_error_response('Accès refusé - Admin requis', 'ACCESS_DENIED')
            
            count = request.env['social.notification'].cleanup_old_notifications(days)
            
            return self._get_success_response({
                'message': f'{count} notifications supprimées',
                'count': count
            })
            
        except Exception as e:
            _logger.error(f"Erreur lors du nettoyage: {e}")
            return self._get_error_response('Erreur lors du nettoyage', 'CLEANUP_ERROR')