# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime

from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError, AccessError

_logger = logging.getLogger(__name__)


class SocialMainController(http.Controller):

    @http.route('/social', type='http', auth='user', website=True)
    def social_main(self, **kwargs):
        """Page principale de l'application sociale"""
        return request.render('sama_jokoo.social_main_template', {
            'user': request.env.user,
            'posts': request.env['social.post'].get_feed(limit=10),
        })

    @http.route('/social/dashboard', type='http', auth='user', website=True)
    def social_dashboard(self, **kwargs):
        """Dashboard social"""
        user = request.env.user
        
        # Statistiques générales
        stats = {
            'total_posts': request.env['social.post'].search_count([('state', '=', 'published')]),
            'my_posts': request.env['social.post'].search_count([
                ('author_id', '=', user.id),
                ('state', '=', 'published')
            ]),
            'total_users': request.env['res.users'].search_count([('active', '=', True)]),
            'unread_notifications': request.env['social.notification'].get_unread_count(),
        }
        
        # Posts récents
        recent_posts = request.env['social.post'].search([
            ('state', '=', 'published')
        ], limit=5, order='create_date desc')
        
        # Hashtags populaires
        popular_hashtags = request.env['social.hashtag'].get_popular_hashtags(limit=10)
        
        # Utilisateurs actifs
        active_users = request.env['res.users'].search([
            ('social_is_online', '=', True)
        ], limit=10)
        
        return request.render('sama_jokoo.social_dashboard_template', {
            'stats': stats,
            'recent_posts': recent_posts,
            'popular_hashtags': popular_hashtags,
            'active_users': active_users,
        })

    @http.route('/social/post/<int:post_id>', type='http', auth='user', website=True)
    def social_post_detail(self, post_id, **kwargs):
        """Détail d'un post"""
        post = request.env['social.post'].browse(post_id)
        
        if not post.exists():
            return request.not_found()
        
        # Vérifier les permissions
        try:
            post.check_access_rights('read')
            post.check_access_rule('read')
        except AccessError:
            return request.render('website.403')
        
        # Commentaires
        comments = request.env['social.comment'].get_comments_tree(post_id)
        
        return request.render('sama_jokoo.social_post_detail_template', {
            'post': post,
            'comments': comments,
        })

    @http.route('/social/user/<int:user_id>', type='http', auth='user', website=True)
    def social_user_profile(self, user_id, **kwargs):
        """Profil d'un utilisateur"""
        user_profile = request.env['res.users'].browse(user_id)
        
        if not user_profile.exists():
            return request.not_found()
        
        # Récupérer le profil social
        profile_data = request.env['res.users'].get_user_profile(user_id)
        
        # Posts de l'utilisateur
        user_posts = request.env['social.post'].search([
            ('author_id', '=', user_id),
            ('state', '=', 'published')
        ], limit=20, order='create_date desc')
        
        return request.render('sama_jokoo.social_user_profile_template', {
            'user_profile': user_profile,
            'profile_data': profile_data,
            'user_posts': user_posts,
        })

    @http.route('/social/hashtag/<string:hashtag_name>', type='http', auth='user', website=True)
    def social_hashtag_posts(self, hashtag_name, **kwargs):
        """Posts d'un hashtag"""
        hashtag = request.env['social.hashtag'].search([
            ('name', '=', hashtag_name.lower())
        ], limit=1)
        
        if not hashtag:
            return request.not_found()
        
        # Posts du hashtag
        posts = request.env['social.hashtag'].get_hashtag_posts(
            hashtag.id, 
            limit=20
        )
        
        return request.render('sama_jokoo.social_hashtag_posts_template', {
            'hashtag': hashtag,
            'posts': posts,
        })

    @http.route('/social/api/status', type='json', auth='user', methods=['GET'], csrf=False)
    def api_status(self, **kwargs):
        """Statut de l'API"""
        return {
            'success': True,
            'status': 'active',
            'version': '1.0.0',
            'user': {
                'id': request.env.user.id,
                'name': request.env.user.name,
                'login': request.env.user.login,
            },
            'timestamp': datetime.now().isoformat(),
        }

    @http.route('/social/api/health', type='json', auth='none', methods=['GET'], csrf=False)
    def api_health(self, **kwargs):
        """Health check de l'API"""
        try:
            # Test de base de données
            request.env['social.post'].search([], limit=1)
            
            return {
                'success': True,
                'status': 'healthy',
                'database': 'connected',
                'timestamp': datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                'success': False,
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
            }

    @http.route('/social/widget/feed', type='json', auth='user', methods=['GET'], csrf=False)
    def widget_feed(self, **kwargs):
        """Widget de feed pour intégration"""
        try:
            limit = kwargs.get('limit', 5)
            posts = request.env['social.post'].get_feed(limit=limit)
            
            return {
                'success': True,
                'posts': posts,
            }
        except Exception as e:
            _logger.error(f"Erreur widget feed: {e}")
            return {
                'success': False,
                'error': str(e),
            }

    @http.route('/social/widget/notifications', type='json', auth='user', methods=['GET'], csrf=False)
    def widget_notifications(self, **kwargs):
        """Widget de notifications pour intégration"""
        try:
            limit = kwargs.get('limit', 5)
            notifications = request.env['social.notification'].get_notifications(
                limit=limit,
                unread_only=True
            )
            
            return {
                'success': True,
                'notifications': notifications,
                'unread_count': len(notifications),
            }
        except Exception as e:
            _logger.error(f"Erreur widget notifications: {e}")
            return {
                'success': False,
                'error': str(e),
            }

    @http.route('/social/embed/post/<int:post_id>', type='http', auth='public', website=True)
    def embed_post(self, post_id, **kwargs):
        """Embed d'un post pour partage externe"""
        post = request.env['social.post'].sudo().browse(post_id)
        
        if not post.exists() or post.visibility not in ['public', 'company']:
            return request.not_found()
        
        return request.render('sama_jokoo.social_post_embed_template', {
            'post': post,
            'embed': True,
        })

    @http.route('/social/qr/<int:post_id>', type='http', auth='user')
    def post_qr_code(self, post_id, **kwargs):
        """QR Code pour un post"""
        post = request.env['social.post'].browse(post_id)
        
        if not post.exists():
            return request.not_found()
        
        try:
            import qrcode
            from io import BytesIO
            import base64
            
            # URL du post
            post_url = f"{request.httprequest.host_url}social/post/{post_id}"
            
            # Générer le QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(post_url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convertir en base64
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return request.make_response(
                base64.b64decode(img_str),
                headers=[
                    ('Content-Type', 'image/png'),
                    ('Content-Disposition', f'inline; filename="post_{post_id}_qr.png"')
                ]
            )
            
        except ImportError:
            return request.render('website.404', {
                'message': 'QR Code non disponible (module qrcode manquant)'
            })
        except Exception as e:
            _logger.error(f"Erreur génération QR code: {e}")
            return request.render('website.500')

    @http.route('/social/export/posts', type='http', auth='user', methods=['GET'])
    def export_posts(self, **kwargs):
        """Export des posts de l'utilisateur"""
        try:
            user_posts = request.env['social.post'].search([
                ('author_id', '=', request.env.user.id)
            ])
            
            # Préparer les données d'export
            export_data = []
            for post in user_posts:
                export_data.append({
                    'id': post.id,
                    'content': post.content,
                    'create_date': post.create_date.isoformat() if post.create_date else None,
                    'visibility': post.visibility,
                    'like_count': post.like_count,
                    'comment_count': post.comment_count,
                    'hashtags': [h.name for h in post.hashtag_ids],
                })
            
            # Retourner en JSON
            response = request.make_response(
                json.dumps(export_data, indent=2, ensure_ascii=False),
                headers=[
                    ('Content-Type', 'application/json'),
                    ('Content-Disposition', f'attachment; filename="sama_jokoo_posts_{request.env.user.login}.json"')
                ]
            )
            
            return response
            
        except Exception as e:
            _logger.error(f"Erreur export posts: {e}")
            return request.render('website.500')