# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re


class SocialPost(models.Model):
    _name = 'social.post'
    _description = 'Post Social'
    _order = 'create_date desc'
    _rec_name = 'content_preview'

    # Contenu du post
    content = fields.Html(
        string='Contenu',
        required=True,
        help="Contenu du post (supporte HTML et mentions)"
    )
    content_preview = fields.Char(
        string='Aperçu',
        compute='_compute_content_preview',
        store=True
    )
    
    # Auteur et visibilité
    author_id = fields.Many2one(
        'res.users',
        string='Auteur',
        required=True,
        default=lambda self: self.env.user
    )
    visibility = fields.Selection([
        ('public', 'Public'),
        ('followers', 'Abonnés seulement'),
        ('private', 'Privé'),
        ('company', 'Entreprise'),
    ], string='Visibilité', default='public', required=True)
    
    # Médias attachés
    media_ids = fields.One2many(
        'social.media',
        'post_id',
        string='Médias'
    )
    has_media = fields.Boolean(
        string='A des médias',
        compute='_compute_has_media'
    )
    
    # Interactions
    like_ids = fields.One2many(
        'social.like',
        'post_id',
        string='Likes'
    )
    comment_ids = fields.One2many(
        'social.comment',
        'post_id',
        string='Commentaires'
    )
    share_ids = fields.One2many(
        'social.post',
        'shared_post_id',
        string='Partages'
    )
    
    # Compteurs
    like_count = fields.Integer(
        string='Nombre de likes',
        compute='_compute_interaction_counts',
        store=True
    )
    comment_count = fields.Integer(
        string='Nombre de commentaires',
        compute='_compute_interaction_counts',
        store=True
    )
    share_count = fields.Integer(
        string='Nombre de partages',
        compute='_compute_interaction_counts',
        store=True
    )
    
    # Partage
    is_shared = fields.Boolean(string='Est un partage', default=False)
    shared_post_id = fields.Many2one(
        'social.post',
        string='Post partagé',
        ondelete='cascade'
    )
    shared_by_id = fields.Many2one(
        'res.users',
        string='Partagé par',
        default=lambda self: self.env.user
    )
    
    # Hashtags et mentions
    hashtag_ids = fields.Many2many(
        'social.hashtag',
        string='Hashtags'
    )
    mention_ids = fields.Many2many(
        'res.users',
        'social_post_mention_rel',
        'post_id',
        'user_id',
        string='Mentions'
    )
    
    # Lien avec les records Odoo
    res_model = fields.Char(string='Modèle lié')
    res_id = fields.Integer(string='ID du record lié')
    res_name = fields.Char(string='Nom du record lié')
    
    # Statut
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
        ('archived', 'Archivé'),
    ], string='Statut', default='draft')
    
    # Métadonnées
    is_pinned = fields.Boolean(string='Épinglé', default=False)
    is_featured = fields.Boolean(string='Mis en avant', default=False)
    
    # Champs calculés pour l'utilisateur actuel
    user_liked = fields.Boolean(
        string='Aimé par moi',
        compute='_compute_user_interactions'
    )
    user_can_edit = fields.Boolean(
        string='Peut modifier',
        compute='_compute_user_permissions'
    )
    user_can_delete = fields.Boolean(
        string='Peut supprimer',
        compute='_compute_user_permissions'
    )

    @api.depends('content')
    def _compute_content_preview(self):
        for post in self:
            if post.content:
                # Nettoyer le HTML et limiter à 100 caractères
                import re
                clean_content = re.sub('<[^<]+?>', '', post.content or '')
                post.content_preview = (clean_content[:100] + '...') if len(clean_content) > 100 else clean_content
            else:
                post.content_preview = _('Post sans contenu')

    @api.depends('media_ids')
    def _compute_has_media(self):
        for post in self:
            post.has_media = bool(post.media_ids)

    @api.depends('like_ids', 'comment_ids', 'share_ids')
    def _compute_interaction_counts(self):
        for post in self:
            post.like_count = len(post.like_ids)
            post.comment_count = len(post.comment_ids)
            post.share_count = len(post.share_ids)

    def _compute_user_interactions(self):
        for post in self:
            post.user_liked = bool(post.like_ids.filtered(lambda l: l.user_id == self.env.user))

    def _compute_user_permissions(self):
        for post in self:
            is_author = post.author_id == self.env.user
            is_admin = self.env.user.has_group('sama_jokoo.group_social_admin')
            
            post.user_can_edit = is_author or is_admin
            post.user_can_delete = is_author or is_admin

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Auto-publier si pas de statut spécifié
            if 'state' not in vals:
                vals['state'] = 'published'
        
        posts = super().create(vals_list)
        
        for post in posts:
            # Extraire hashtags et mentions
            post._extract_hashtags_and_mentions()
            
            # Créer notifications pour les mentions
            if post.mention_ids:
                post._create_mention_notifications()
        
        return posts

    def write(self, vals):
        result = super().write(vals)
        
        if 'content' in vals:
            for post in self:
                post._extract_hashtags_and_mentions()
        
        return result

    def _extract_hashtags_and_mentions(self):
        """Extraire les hashtags et mentions du contenu"""
        if not self.content:
            return
        
        # Extraire hashtags (#tag)
        hashtag_pattern = r'#(\w+)'
        hashtags = re.findall(hashtag_pattern, self.content, re.IGNORECASE)
        
        hashtag_records = []
        for tag in set(hashtags):
            hashtag = self.env['social.hashtag'].search([('name', '=ilike', tag)], limit=1)
            if not hashtag:
                hashtag = self.env['social.hashtag'].create({'name': tag.lower()})
            hashtag_records.append(hashtag.id)
        
        self.hashtag_ids = [(6, 0, hashtag_records)]
        
        # Extraire mentions (@user)
        mention_pattern = r'@(\w+)'
        mentions = re.findall(mention_pattern, self.content, re.IGNORECASE)
        
        mentioned_users = []
        for username in set(mentions):
            user = self.env['res.users'].search([
                '|',
                ('login', '=ilike', username),
                ('name', 'ilike', username)
            ], limit=1)
            if user:
                mentioned_users.append(user.id)
        
        self.mention_ids = [(6, 0, mentioned_users)]

    def _create_mention_notifications(self):
        """Créer des notifications pour les utilisateurs mentionnés"""
        for user in self.mention_ids:
            self.env['social.notification'].create({
                'user_id': user.id,
                'type': 'mention',
                'title': _('Vous avez été mentionné'),
                'message': _('%s vous a mentionné dans un post') % self.author_id.name,
                'post_id': self.id,
                'author_id': self.author_id.id,
            })

    def action_like(self):
        """Liker/Unliker un post"""
        existing_like = self.like_ids.filtered(lambda l: l.user_id == self.env.user)
        
        if existing_like:
            existing_like.unlink()
            return {'liked': False}
        else:
            self.env['social.like'].create({
                'post_id': self.id,
                'user_id': self.env.user.id,
            })
            
            # Notification pour l'auteur
            if self.author_id != self.env.user:
                self.env['social.notification'].create({
                    'user_id': self.author_id.id,
                    'type': 'like',
                    'title': _('Nouveau like'),
                    'message': _('%s a aimé votre post') % self.env.user.name,
                    'post_id': self.id,
                    'author_id': self.env.user.id,
                })
            
            return {'liked': True}

    def action_share(self, content=''):
        """Partager un post"""
        shared_post = self.create({
            'content': content or _('Post partagé'),
            'is_shared': True,
            'shared_post_id': self.id,
            'shared_by_id': self.env.user.id,
            'visibility': 'public',
            'state': 'published',
        })
        
        # Notification pour l'auteur original
        if self.author_id != self.env.user:
            self.env['social.notification'].create({
                'user_id': self.author_id.id,
                'type': 'share',
                'title': _('Post partagé'),
                'message': _('%s a partagé votre post') % self.env.user.name,
                'post_id': self.id,
                'author_id': self.env.user.id,
            })
        
        return shared_post

    def action_publish(self):
        """Publier un post"""
        self.write({'state': 'published'})

    def action_archive(self):
        """Archiver un post"""
        self.write({'state': 'archived'})

    def action_pin(self):
        """Épingler/Désépingler un post"""
        self.is_pinned = not self.is_pinned

    @api.model
    def get_feed(self, limit=20, offset=0, filter_type='all'):
        """Récupérer le feed social pour l'utilisateur actuel"""
        domain = [('state', '=', 'published')]
        
        # Filtres de visibilité
        user = self.env.user
        visibility_domain = [
            '|', ('visibility', '=', 'public'),
            '|', ('visibility', '=', 'company'),
            '|', ('author_id', '=', user.id),
            ('visibility', '=', 'followers')  # TODO: ajouter logique followers
        ]
        
        domain.extend(visibility_domain)
        
        # Filtres par type
        if filter_type == 'following':
            # TODO: implémenter logique de suivi
            pass
        elif filter_type == 'media':
            domain.append(('has_media', '=', True))
        
        posts = self.search(domain, limit=limit, offset=offset)
        
        return posts.read([
            'id', 'content', 'content_preview', 'author_id', 'create_date',
            'like_count', 'comment_count', 'share_count', 'user_liked',
            'has_media', 'is_shared', 'shared_post_id', 'hashtag_ids',
            'visibility', 'is_pinned', 'is_featured'
        ])

    @api.model
    def search_posts(self, query, limit=20):
        """Rechercher des posts"""
        domain = [
            ('state', '=', 'published'),
            '|',
            ('content', 'ilike', query),
            ('hashtag_ids.name', 'ilike', query)
        ]
        
        return self.search(domain, limit=limit)