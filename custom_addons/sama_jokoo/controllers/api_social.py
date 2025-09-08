# -*- coding: utf-8 -*-

import json
import logging
import base64
from datetime import datetime

from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError, AccessError

_logger = logging.getLogger(__name__)


class SocialAPI(http.Controller):

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

    # ==================== POSTS ====================

    @http.route('/api/social/posts', type='json', auth='user', methods=['GET'], csrf=False)
    def get_posts(self, **kwargs):
        """Récupérer le feed de posts"""
        try:
            limit = kwargs.get('limit', 20)
            offset = kwargs.get('offset', 0)
            filter_type = kwargs.get('filter', 'all')  # all, following, media
            
            posts_data = request.env['social.post'].get_feed(
                limit=limit, 
                offset=offset, 
                filter_type=filter_type
            )
            
            return self._get_success_response(posts_data)
            
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des posts: {e}")
            return self._get_error_response('Erreur lors de la récupération des posts', 'FETCH_ERROR')

    @http.route('/api/social/posts', type='json', auth='user', methods=['POST'], csrf=False)
    def create_post(self, **kwargs):
        """Créer un nouveau post"""
        try:
            content = kwargs.get('content')
            visibility = kwargs.get('visibility', 'public')
            media_files = kwargs.get('media_files', [])
            res_model = kwargs.get('res_model')
            res_id = kwargs.get('res_id')
            
            if not content:
                return self._get_error_response('Le contenu est requis', 'MISSING_CONTENT')
            
            # Créer le post
            post_vals = {
                'content': content,
                'visibility': visibility,
                'author_id': request.env.user.id,
                'state': 'published',
            }
            
            if res_model and res_id:
                post_vals.update({
                    'res_model': res_model,
                    'res_id': res_id,
                    'res_name': request.env[res_model].browse(res_id).display_name,
                })
            
            post = request.env['social.post'].create(post_vals)
            
            # Ajouter les médias si présents
            for media_data in media_files:
                request.env['social.media'].create({
                    'post_id': post.id,
                    'name': media_data.get('name'),
                    'file_data': media_data.get('data'),
                    'mimetype': media_data.get('mimetype'),
                })
            
            return self._get_success_response({
                'post_id': post.id,
                'message': 'Post créé avec succès'
            })
            
        except ValidationError as e:
            return self._get_error_response(str(e), 'VALIDATION_ERROR')
        except Exception as e:
            _logger.error(f"Erreur lors de la création du post: {e}")
            return self._get_error_response('Erreur lors de la création du post', 'CREATE_ERROR')

    @http.route('/api/social/posts/<int:post_id>', type='json', auth='user', methods=['GET'], csrf=False)
    def get_post(self, post_id, **kwargs):
        """Récupérer un post spécifique"""
        try:
            post = request.env['social.post'].browse(post_id)
            
            if not post.exists():
                return self._get_error_response('Post non trouvé', 'POST_NOT_FOUND')
            
            # Vérifier les permissions de lecture
            if not post.user_can_edit and post.visibility == 'private':
                return self._get_error_response('Accès refusé', 'ACCESS_DENIED')
            
            post_data = post.read([
                'id', 'content', 'author_id', 'create_date', 'write_date',
                'like_count', 'comment_count', 'share_count', 'user_liked',
                'has_media', 'is_shared', 'shared_post_id', 'hashtag_ids',
                'visibility', 'is_pinned', 'is_featured', 'state'
            ])[0]
            
            # Ajouter les médias
            media_data = post.media_ids.read(['id', 'name', 'media_type', 'public_url'])
            post_data['media'] = media_data
            
            # Ajouter les commentaires
            comments_data = request.env['social.comment'].get_comments_tree(post_id)
            post_data['comments'] = comments_data
            
            return self._get_success_response(post_data)
            
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération du post {post_id}: {e}")
            return self._get_error_response('Erreur lors de la récupération du post', 'FETCH_ERROR')

    @http.route('/api/social/posts/<int:post_id>/like', type='json', auth='user', methods=['POST'], csrf=False)
    def like_post(self, post_id, **kwargs):
        """Liker/Unliker un post"""
        try:
            post = request.env['social.post'].browse(post_id)
            
            if not post.exists():
                return self._get_error_response('Post non trouvé', 'POST_NOT_FOUND')
            
            result = post.action_like()
            
            return self._get_success_response({
                'liked': result['liked'],
                'like_count': post.like_count
            })
            
        except Exception as e:
            _logger.error(f"Erreur lors du like du post {post_id}: {e}")
            return self._get_error_response('Erreur lors du like', 'LIKE_ERROR')

    @http.route('/api/social/posts/<int:post_id>/share', type='json', auth='user', methods=['POST'], csrf=False)
    def share_post(self, post_id, **kwargs):
        """Partager un post"""
        try:
            post = request.env['social.post'].browse(post_id)
            
            if not post.exists():
                return self._get_error_response('Post non trouvé', 'POST_NOT_FOUND')
            
            content = kwargs.get('content', '')
            shared_post = post.action_share(content)
            
            return self._get_success_response({
                'shared_post_id': shared_post.id,
                'message': 'Post partagé avec succès'
            })
            
        except Exception as e:
            _logger.error(f"Erreur lors du partage du post {post_id}: {e}")
            return self._get_error_response('Erreur lors du partage', 'SHARE_ERROR')

    # ==================== COMMENTAIRES ====================

    @http.route('/api/social/posts/<int:post_id>/comments', type='json', auth='user', methods=['GET'], csrf=False)
    def get_comments(self, post_id, **kwargs):
        """Récupérer les commentaires d'un post"""
        try:
            limit = kwargs.get('limit', 50)
            comments_data = request.env['social.comment'].get_comments_tree(post_id, limit)
            
            return self._get_success_response(comments_data)
            
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des commentaires: {e}")
            return self._get_error_response('Erreur lors de la récupération des commentaires', 'FETCH_ERROR')

    @http.route('/api/social/posts/<int:post_id>/comments', type='json', auth='user', methods=['POST'], csrf=False)
    def create_comment(self, post_id, **kwargs):
        """Créer un commentaire"""
        try:
            content = kwargs.get('content')
            parent_id = kwargs.get('parent_id')
            
            if not content:
                return self._get_error_response('Le contenu est requis', 'MISSING_CONTENT')
            
            post = request.env['social.post'].browse(post_id)
            if not post.exists():
                return self._get_error_response('Post non trouvé', 'POST_NOT_FOUND')
            
            comment_vals = {
                'content': content,
                'post_id': post_id,
                'author_id': request.env.user.id,
            }
            
            if parent_id:
                comment_vals['parent_id'] = parent_id
            
            comment = request.env['social.comment'].create(comment_vals)
            
            return self._get_success_response({
                'comment_id': comment.id,
                'message': 'Commentaire créé avec succès'
            })
            
        except ValidationError as e:
            return self._get_error_response(str(e), 'VALIDATION_ERROR')
        except Exception as e:
            _logger.error(f"Erreur lors de la création du commentaire: {e}")
            return self._get_error_response('Erreur lors de la création du commentaire', 'CREATE_ERROR')

    @http.route('/api/social/comments/<int:comment_id>/like', type='json', auth='user', methods=['POST'], csrf=False)
    def like_comment(self, comment_id, **kwargs):
        """Liker/Unliker un commentaire"""
        try:
            comment = request.env['social.comment'].browse(comment_id)
            
            if not comment.exists():
                return self._get_error_response('Commentaire non trouvé', 'COMMENT_NOT_FOUND')
            
            result = comment.action_like()
            
            return self._get_success_response({
                'liked': result['liked'],
                'like_count': comment.like_count
            })
            
        except Exception as e:
            _logger.error(f"Erreur lors du like du commentaire {comment_id}: {e}")
            return self._get_error_response('Erreur lors du like', 'LIKE_ERROR')

    # ==================== UTILISATEURS ====================

    @http.route('/api/social/users/profile', type='json', auth='user', methods=['GET'], csrf=False)
    def get_user_profile(self, **kwargs):
        """Récupérer le profil de l'utilisateur actuel"""
        try:
            user_id = kwargs.get('user_id')
            profile_data = request.env['res.users'].get_user_profile(user_id)
            
            return self._get_success_response(profile_data)
            
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération du profil: {e}")
            return self._get_error_response('Erreur lors de la récupération du profil', 'FETCH_ERROR')

    @http.route('/api/social/users/profile', type='json', auth='user', methods=['PUT'], csrf=False)
    def update_user_profile(self, **kwargs):
        """Mettre à jour le profil utilisateur"""
        try:
            user = request.env.user
            
            allowed_fields = [
                'social_bio', 'social_website', 'social_location', 'social_birth_date',
                'social_profile_private', 'social_show_email', 'social_show_phone',
                'social_theme'
            ]
            
            vals = {}
            for field in allowed_fields:
                if field in kwargs:
                    vals[field] = kwargs[field]
            
            if vals:
                user.write(vals)
            
            return self._get_success_response({'message': 'Profil mis à jour avec succès'})
            
        except ValidationError as e:
            return self._get_error_response(str(e), 'VALIDATION_ERROR')
        except Exception as e:
            _logger.error(f"Erreur lors de la mise à jour du profil: {e}")
            return self._get_error_response('Erreur lors de la mise à jour', 'UPDATE_ERROR')

    @http.route('/api/social/users/search', type='json', auth='user', methods=['GET'], csrf=False)
    def search_users(self, **kwargs):
        """Rechercher des utilisateurs"""
        try:
            query = kwargs.get('query', '')
            limit = kwargs.get('limit', 20)
            
            if len(query) < 2:
                return self._get_error_response('La recherche doit contenir au moins 2 caractères', 'QUERY_TOO_SHORT')
            
            users_data = request.env['res.users'].search_users(query, limit)
            
            return self._get_success_response(users_data)
            
        except Exception as e:
            _logger.error(f"Erreur lors de la recherche d'utilisateurs: {e}")
            return self._get_error_response('Erreur lors de la recherche', 'SEARCH_ERROR')

    @http.route('/api/social/users/suggestions', type='json', auth='user', methods=['GET'], csrf=False)
    def get_user_suggestions(self, **kwargs):
        """Récupérer des suggestions d'utilisateurs à suivre"""
        try:
            limit = kwargs.get('limit', 10)
            suggestions = request.env['res.users'].get_suggested_users(limit)
            
            return self._get_success_response(suggestions)
            
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des suggestions: {e}")
            return self._get_error_response('Erreur lors de la récupération des suggestions', 'FETCH_ERROR')

    # ==================== SUIVI ====================

    @http.route('/api/social/users/<int:user_id>/follow', type='json', auth='user', methods=['POST'], csrf=False)
    def follow_user(self, user_id, **kwargs):
        """Suivre un utilisateur"""
        try:
            follow = request.env['social.follow'].follow_user(user_id)
            
            return self._get_success_response({
                'follow_id': follow.id,
                'status': follow.state,
                'message': 'Demande de suivi envoyée' if follow.state == 'pending' else 'Vous suivez maintenant cet utilisateur'
            })
            
        except ValidationError as e:
            return self._get_error_response(str(e), 'VALIDATION_ERROR')
        except Exception as e:
            _logger.error(f"Erreur lors du suivi de l'utilisateur {user_id}: {e}")
            return self._get_error_response('Erreur lors du suivi', 'FOLLOW_ERROR')

    @http.route('/api/social/users/<int:user_id>/unfollow', type='json', auth='user', methods=['POST'], csrf=False)
    def unfollow_user(self, user_id, **kwargs):
        """Ne plus suivre un utilisateur"""
        try:
            result = request.env['social.follow'].unfollow_user(user_id)
            
            message = 'Vous ne suivez plus cet utilisateur' if result else 'Vous ne suiviez pas cet utilisateur'
            
            return self._get_success_response({'message': message})
            
        except Exception as e:
            _logger.error(f"Erreur lors de l'arrêt du suivi de l'utilisateur {user_id}: {e}")
            return self._get_error_response('Erreur lors de l\'arrêt du suivi', 'UNFOLLOW_ERROR')

    @http.route('/api/social/users/followers', type='json', auth='user', methods=['GET'], csrf=False)
    def get_followers(self, **kwargs):
        """Récupérer les abonnés"""
        try:
            user_id = kwargs.get('user_id')
            limit = kwargs.get('limit', 50)
            
            followers = request.env['social.follow'].get_followers(user_id, limit)
            
            return self._get_success_response(followers)
            
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des abonnés: {e}")
            return self._get_error_response('Erreur lors de la récupération des abonnés', 'FETCH_ERROR')

    @http.route('/api/social/users/following', type='json', auth='user', methods=['GET'], csrf=False)
    def get_following(self, **kwargs):
        """Récupérer les abonnements"""
        try:
            user_id = kwargs.get('user_id')
            limit = kwargs.get('limit', 50)
            
            following = request.env['social.follow'].get_following(user_id, limit)
            
            return self._get_success_response(following)
            
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des abonnements: {e}")
            return self._get_error_response('Erreur lors de la récupération des abonnements', 'FETCH_ERROR')

    # ==================== HASHTAGS ====================

    @http.route('/api/social/hashtags/trending', type='json', auth='user', methods=['GET'], csrf=False)
    def get_trending_hashtags(self, **kwargs):
        """Récupérer les hashtags en tendance"""
        try:
            limit = kwargs.get('limit', 10)
            hashtags = request.env['social.hashtag'].get_trending_hashtags(limit)
            
            return self._get_success_response(hashtags)
            
        except Exception as e:
            _logger.error(f"Erreur lors de la récupération des hashtags tendance: {e}")
            return self._get_error_response('Erreur lors de la récupération', 'FETCH_ERROR')

    @http.route('/api/social/hashtags/search', type='json', auth='user', methods=['GET'], csrf=False)
    def search_hashtags(self, **kwargs):
        """Rechercher des hashtags"""
        try:
            query = kwargs.get('query', '')
            limit = kwargs.get('limit', 10)
            
            if len(query) < 1:
                return self._get_error_response('La recherche ne peut pas être vide', 'EMPTY_QUERY')
            
            hashtags = request.env['social.hashtag'].search_hashtags(query, limit)
            
            return self._get_success_response(hashtags)
            
        except Exception as e:
            _logger.error(f"Erreur lors de la recherche de hashtags: {e}")
            return self._get_error_response('Erreur lors de la recherche', 'SEARCH_ERROR')

    # ==================== UPLOAD MÉDIA ====================

    @http.route('/api/social/media/upload', type='json', auth='user', methods=['POST'], csrf=False)
    def upload_media(self, **kwargs):
        """Upload d'un fichier média"""
        try:
            file_data = kwargs.get('file_data')
            filename = kwargs.get('filename')
            post_id = kwargs.get('post_id')
            
            if not file_data or not filename:
                return self._get_error_response('Fichier et nom requis', 'MISSING_FILE_DATA')
            
            media = request.env['social.media'].upload_media(file_data, filename, post_id)
            
            return self._get_success_response({
                'media_id': media.id,
                'download_url': media.get_download_url(),
                'thumbnail_url': media.get_thumbnail_url(),
                'media_type': media.media_type,
            })
            
        except ValidationError as e:
            return self._get_error_response(str(e), 'VALIDATION_ERROR')
        except Exception as e:
            _logger.error(f"Erreur lors de l'upload: {e}")
            return self._get_error_response('Erreur lors de l\'upload', 'UPLOAD_ERROR')