# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    # Profil social
    social_bio = fields.Text(string='Biographie')
    social_website = fields.Char(string='Site web')
    social_location = fields.Char(string='Localisation')
    social_birth_date = fields.Date(string='Date de naissance')
    
    # Paramètres de confidentialité
    social_profile_private = fields.Boolean(
        string='Profil privé',
        default=False,
        help="Si activé, les autres utilisateurs doivent demander à vous suivre"
    )
    social_show_email = fields.Boolean(
        string='Afficher l\'email',
        default=False
    )
    social_show_phone = fields.Boolean(
        string='Afficher le téléphone',
        default=False
    )
    
    # Paramètres de notification
    social_notify_likes = fields.Boolean(
        string='Notifications pour les likes',
        default=True
    )
    social_notify_comments = fields.Boolean(
        string='Notifications pour les commentaires',
        default=True
    )
    social_notify_mentions = fields.Boolean(
        string='Notifications pour les mentions',
        default=True
    )
    social_notify_follows = fields.Boolean(
        string='Notifications pour les nouveaux abonnés',
        default=True
    )
    social_notify_push = fields.Boolean(
        string='Notifications push mobiles',
        default=True
    )
    
    # Statistiques sociales
    social_posts_count = fields.Integer(
        string='Nombre de posts',
        compute='_compute_social_stats'
    )
    social_followers_count = fields.Integer(
        string='Nombre d\'abonnés',
        compute='_compute_social_stats'
    )
    social_following_count = fields.Integer(
        string='Nombre d\'abonnements',
        compute='_compute_social_stats'
    )
    social_likes_received = fields.Integer(
        string='Likes reçus',
        compute='_compute_social_stats'
    )
    
    # Relations sociales
    social_posts = fields.One2many(
        'social.post',
        'author_id',
        string='Posts'
    )
    social_followers = fields.One2many(
        'social.follow',
        'followed_id',
        string='Abonnés'
    )
    social_following = fields.One2many(
        'social.follow',
        'follower_id',
        string='Abonnements'
    )
    social_notifications = fields.One2many(
        'social.notification',
        'user_id',
        string='Notifications'
    )
    
    # Statut en ligne
    social_last_seen = fields.Datetime(
        string='Dernière connexion',
        default=fields.Datetime.now
    )
    social_is_online = fields.Boolean(
        string='En ligne',
        compute='_compute_is_online'
    )
    
    # Badges et réalisations
    social_verified = fields.Boolean(
        string='Compte vérifié',
        default=False
    )
    social_badges = fields.Char(
        string='Badges',
        help="Badges séparés par des virgules"
    )
    
    # Thème préféré
    social_theme = fields.Selection([
        ('light', 'Clair'),
        ('dark', 'Sombre'),
        ('auto', 'Automatique'),
    ], string='Thème', default='auto')

    @api.depends('social_posts', 'social_followers', 'social_following')
    def _compute_social_stats(self):
        for user in self:
            # Compter les posts publiés
            user.social_posts_count = len(user.social_posts.filtered(lambda p: p.state == 'published'))
            
            # Compter les abonnés acceptés
            user.social_followers_count = len(user.social_followers.filtered(lambda f: f.state == 'accepted'))
            
            # Compter les abonnements acceptés
            user.social_following_count = len(user.social_following.filtered(lambda f: f.state == 'accepted'))
            
            # Compter les likes reçus sur tous les posts
            likes_received = 0
            for post in user.social_posts:
                likes_received += post.like_count
            user.social_likes_received = likes_received

    def _compute_is_online(self):
        """Calculer si l'utilisateur est en ligne (actif dans les 5 dernières minutes)"""
        from datetime import datetime, timedelta
        
        cutoff_time = datetime.now() - timedelta(minutes=5)
        
        for user in self:
            user.social_is_online = user.social_last_seen and user.social_last_seen >= cutoff_time

    def update_last_seen(self):
        """Mettre à jour la dernière connexion"""
        self.social_last_seen = fields.Datetime.now()

    @api.model
    def get_user_profile(self, user_id=None):
        """Récupérer le profil social d'un utilisateur"""
        if not user_id:
            user_id = self.env.user.id
        
        user = self.browse(user_id)
        current_user = self.env.user
        
        # Vérifier si l'utilisateur actuel suit cet utilisateur
        is_following = False
        follow_status = 'none'
        
        if user_id != current_user.id:
            follow = self.env['social.follow'].search([
                ('follower_id', '=', current_user.id),
                ('followed_id', '=', user_id)
            ], limit=1)
            
            if follow:
                is_following = follow.state == 'accepted'
                follow_status = follow.state
        
        # Vérifier les permissions de visibilité
        can_see_posts = True
        can_see_followers = True
        
        if user.social_profile_private and not is_following and user_id != current_user.id:
            can_see_posts = False
            can_see_followers = False
        
        return {
            'id': user.id,
            'name': user.name,
            'login': user.login,
            'email': user.email if user.social_show_email or user_id == current_user.id else None,
            'phone': user.phone if user.social_show_phone or user_id == current_user.id else None,
            'image_128': user.image_128,
            'bio': user.social_bio,
            'website': user.social_website,
            'location': user.social_location,
            'birth_date': user.social_birth_date,
            'verified': user.social_verified,
            'badges': user.social_badges.split(',') if user.social_badges else [],
            'theme': user.social_theme,
            'is_online': user.social_is_online,
            'last_seen': user.social_last_seen,
            'profile_private': user.social_profile_private,
            'stats': {
                'posts_count': user.social_posts_count,
                'followers_count': user.social_followers_count,
                'following_count': user.social_following_count,
                'likes_received': user.social_likes_received,
            },
            'permissions': {
                'can_see_posts': can_see_posts,
                'can_see_followers': can_see_followers,
                'is_following': is_following,
                'follow_status': follow_status,
                'is_own_profile': user_id == current_user.id,
            }
        }

    @api.model
    def search_users(self, query, limit=20):
        """Rechercher des utilisateurs"""
        users = self.search([
            '|', '|',
            ('name', 'ilike', query),
            ('login', 'ilike', query),
            ('email', 'ilike', query)
        ], limit=limit)
        
        return [{
            'id': user.id,
            'name': user.name,
            'login': user.login,
            'image_128': user.image_128,
            'verified': user.social_verified,
            'followers_count': user.social_followers_count,
            'is_online': user.social_is_online,
        } for user in users]

    @api.model
    def get_suggested_users(self, limit=10):
        """Récupérer des utilisateurs suggérés à suivre"""
        current_user = self.env.user
        
        # Utilisateurs que je ne suis pas encore
        already_following = current_user.social_following.filtered(
            lambda f: f.state in ['accepted', 'pending']
        ).mapped('followed_id.id')
        
        # Exclure moi-même et ceux que je suis déjà
        excluded_ids = [current_user.id] + already_following
        
        # Suggérer des utilisateurs populaires ou récemment actifs
        suggested = self.search([
            ('id', 'not in', excluded_ids),
            ('active', '=', True)
        ], limit=limit * 2, order='social_followers_count desc')
        
        # Mélanger et limiter
        import random
        suggested_list = list(suggested)
        random.shuffle(suggested_list)
        
        return [{
            'id': user.id,
            'name': user.name,
            'image_128': user.image_128,
            'bio': user.social_bio,
            'verified': user.social_verified,
            'followers_count': user.social_followers_count,
            'posts_count': user.social_posts_count,
        } for user in suggested_list[:limit]]

    def action_follow(self):
        """Suivre cet utilisateur"""
        return self.env['social.follow'].follow_user(self.id)

    def action_unfollow(self):
        """Ne plus suivre cet utilisateur"""
        return self.env['social.follow'].unfollow_user(self.id)

    @api.model
    def get_online_users(self, limit=50):
        """Récupérer les utilisateurs en ligne"""
        users = self.search([
            ('social_is_online', '=', True),
            ('active', '=', True)
        ], limit=limit, order='social_last_seen desc')
        
        return [{
            'id': user.id,
            'name': user.name,
            'image_128': user.image_128,
            'last_seen': user.social_last_seen,
        } for user in users]

    def get_notification_preferences(self):
        """Récupérer les préférences de notification"""
        return {
            'likes': self.social_notify_likes,
            'comments': self.social_notify_comments,
            'mentions': self.social_notify_mentions,
            'follows': self.social_notify_follows,
            'push': self.social_notify_push,
        }

    def update_notification_preferences(self, preferences):
        """Mettre à jour les préférences de notification"""
        vals = {}
        
        if 'likes' in preferences:
            vals['social_notify_likes'] = preferences['likes']
        if 'comments' in preferences:
            vals['social_notify_comments'] = preferences['comments']
        if 'mentions' in preferences:
            vals['social_notify_mentions'] = preferences['mentions']
        if 'follows' in preferences:
            vals['social_notify_follows'] = preferences['follows']
        if 'push' in preferences:
            vals['social_notify_push'] = preferences['push']
        
        if vals:
            self.write(vals)
        
        return True

    @api.model
    def get_user_activity_feed(self, user_id=None, limit=20):
        """Récupérer le feed d'activité d'un utilisateur"""
        if not user_id:
            user_id = self.env.user.id
        
        user = self.browse(user_id)
        
        activities = []
        
        # Posts récents
        recent_posts = user.social_posts.filtered(
            lambda p: p.state == 'published'
        ).sorted('create_date', reverse=True)[:limit//2]
        
        for post in recent_posts:
            activities.append({
                'type': 'post',
                'date': post.create_date,
                'data': {
                    'post_id': post.id,
                    'content_preview': post.content_preview,
                    'like_count': post.like_count,
                    'comment_count': post.comment_count,
                }
            })
        
        # Likes récents
        recent_likes = self.env['social.like'].search([
            ('user_id', '=', user_id),
            ('post_id', '!=', False)
        ], limit=limit//4, order='create_date desc')
        
        for like in recent_likes:
            activities.append({
                'type': 'like',
                'date': like.create_date,
                'data': {
                    'post_id': like.post_id.id,
                    'post_author': like.post_id.author_id.name,
                    'content_preview': like.post_id.content_preview,
                }
            })
        
        # Nouveaux abonnements
        recent_follows = user.social_following.filtered(
            lambda f: f.state == 'accepted'
        ).sorted('accept_date', reverse=True)[:limit//4]
        
        for follow in recent_follows:
            activities.append({
                'type': 'follow',
                'date': follow.accept_date or follow.create_date,
                'data': {
                    'user_id': follow.followed_id.id,
                    'user_name': follow.followed_id.name,
                    'user_avatar': follow.followed_id.image_128,
                }
            })
        
        # Trier par date
        activities.sort(key=lambda x: x['date'], reverse=True)
        
        return activities[:limit]