# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SocialFollow(models.Model):
    _name = 'social.follow'
    _description = 'Suivi Social'
    _rec_name = 'display_name'

    # Relations
    follower_id = fields.Many2one(
        'res.users',
        string='Abonné',
        required=True,
        ondelete='cascade'
    )
    followed_id = fields.Many2one(
        'res.users',
        string='Suivi',
        required=True,
        ondelete='cascade'
    )
    
    # Statut
    state = fields.Selection([
        ('pending', 'En attente'),
        ('accepted', 'Accepté'),
        ('blocked', 'Bloqué'),
    ], string='Statut', default='accepted')
    
    # Métadonnées
    create_date = fields.Datetime(
        string='Date de création',
        default=fields.Datetime.now,
        readonly=True
    )
    accept_date = fields.Datetime(string='Date d\'acceptation')
    
    # Champ calculé pour l'affichage
    display_name = fields.Char(
        string='Nom d\'affichage',
        compute='_compute_display_name'
    )

    @api.depends('follower_id', 'followed_id')
    def _compute_display_name(self):
        for follow in self:
            follow.display_name = _('%s suit %s') % (follow.follower_id.name, follow.followed_id.name)

    @api.constrains('follower_id', 'followed_id')
    def _check_self_follow(self):
        """Empêcher l'auto-suivi"""
        for follow in self:
            if follow.follower_id == follow.followed_id:
                raise ValidationError(_('Vous ne pouvez pas vous suivre vous-même.'))

    @api.constrains('follower_id', 'followed_id')
    def _check_unique_follow(self):
        """Vérifier l'unicité du suivi"""
        for follow in self:
            existing = self.search([
                ('follower_id', '=', follow.follower_id.id),
                ('followed_id', '=', follow.followed_id.id),
                ('id', '!=', follow.id)
            ])
            if existing:
                raise ValidationError(_('Vous suivez déjà cet utilisateur.'))

    def action_accept(self):
        """Accepter une demande de suivi"""
        self.write({
            'state': 'accepted',
            'accept_date': fields.Datetime.now()
        })
        
        # Notification
        self.env['social.notification'].create({
            'user_id': self.follower_id.id,
            'type': 'follow_accepted',
            'title': _('Demande acceptée'),
            'message': _('%s a accepté votre demande de suivi') % self.followed_id.name,
            'author_id': self.followed_id.id,
        })

    def action_reject(self):
        """Rejeter une demande de suivi"""
        self.unlink()

    def action_block(self):
        """Bloquer un utilisateur"""
        self.write({'state': 'blocked'})

    def action_unblock(self):
        """Débloquer un utilisateur"""
        self.write({'state': 'accepted'})

    @api.model
    def follow_user(self, user_id):
        """Suivre un utilisateur"""
        if user_id == self.env.user.id:
            raise ValidationError(_('Vous ne pouvez pas vous suivre vous-même.'))
        
        existing = self.search([
            ('follower_id', '=', self.env.user.id),
            ('followed_id', '=', user_id)
        ])
        
        if existing:
            if existing.state == 'blocked':
                raise ValidationError(_('Vous êtes bloqué par cet utilisateur.'))
            return existing
        
        followed_user = self.env['res.users'].browse(user_id)
        
        # Vérifier si l'utilisateur nécessite une approbation
        requires_approval = followed_user.social_profile_private
        
        follow = self.create({
            'follower_id': self.env.user.id,
            'followed_id': user_id,
            'state': 'pending' if requires_approval else 'accepted',
            'accept_date': fields.Datetime.now() if not requires_approval else False,
        })
        
        # Notification
        notification_type = 'follow_request' if requires_approval else 'new_follower'
        message = _('%s souhaite vous suivre') if requires_approval else _('%s vous suit maintenant')
        
        self.env['social.notification'].create({
            'user_id': user_id,
            'type': notification_type,
            'title': _('Nouveau suivi'),
            'message': message % self.env.user.name,
            'author_id': self.env.user.id,
        })
        
        return follow

    @api.model
    def unfollow_user(self, user_id):
        """Ne plus suivre un utilisateur"""
        follow = self.search([
            ('follower_id', '=', self.env.user.id),
            ('followed_id', '=', user_id)
        ])
        
        if follow:
            follow.unlink()
            return True
        
        return False

    @api.model
    def get_followers(self, user_id=None, limit=50):
        """Récupérer les abonnés d'un utilisateur"""
        if not user_id:
            user_id = self.env.user.id
        
        follows = self.search([
            ('followed_id', '=', user_id),
            ('state', '=', 'accepted')
        ], limit=limit, order='create_date desc')
        
        return [{
            'id': follow.id,
            'user_id': follow.follower_id.id,
            'user_name': follow.follower_id.name,
            'user_avatar': follow.follower_id.image_128,
            'follow_date': follow.accept_date or follow.create_date,
        } for follow in follows]

    @api.model
    def get_following(self, user_id=None, limit=50):
        """Récupérer les utilisateurs suivis"""
        if not user_id:
            user_id = self.env.user.id
        
        follows = self.search([
            ('follower_id', '=', user_id),
            ('state', '=', 'accepted')
        ], limit=limit, order='create_date desc')
        
        return [{
            'id': follow.id,
            'user_id': follow.followed_id.id,
            'user_name': follow.followed_id.name,
            'user_avatar': follow.followed_id.image_128,
            'follow_date': follow.accept_date or follow.create_date,
        } for follow in follows]

    @api.model
    def get_follow_requests(self, limit=20):
        """Récupérer les demandes de suivi en attente"""
        follows = self.search([
            ('followed_id', '=', self.env.user.id),
            ('state', '=', 'pending')
        ], limit=limit, order='create_date desc')
        
        return [{
            'id': follow.id,
            'user_id': follow.follower_id.id,
            'user_name': follow.follower_id.name,
            'user_avatar': follow.follower_id.image_128,
            'request_date': follow.create_date,
        } for follow in follows]

    @api.model
    def get_follow_stats(self, user_id=None):
        """Récupérer les statistiques de suivi"""
        if not user_id:
            user_id = self.env.user.id
        
        followers_count = self.search_count([
            ('followed_id', '=', user_id),
            ('state', '=', 'accepted')
        ])
        
        following_count = self.search_count([
            ('follower_id', '=', user_id),
            ('state', '=', 'accepted')
        ])
        
        pending_requests = self.search_count([
            ('followed_id', '=', user_id),
            ('state', '=', 'pending')
        ])
        
        return {
            'followers_count': followers_count,
            'following_count': following_count,
            'pending_requests': pending_requests,
        }

    @api.model
    def is_following(self, user_id):
        """Vérifier si l'utilisateur actuel suit un autre utilisateur"""
        return bool(self.search([
            ('follower_id', '=', self.env.user.id),
            ('followed_id', '=', user_id),
            ('state', '=', 'accepted')
        ], limit=1))

    @api.model
    def get_mutual_follows(self, user_id):
        """Récupérer les suivis mutuels avec un utilisateur"""
        # Utilisateurs que je suis et qui me suivent aussi
        my_following = self.search([
            ('follower_id', '=', self.env.user.id),
            ('state', '=', 'accepted')
        ]).mapped('followed_id.id')
        
        their_following = self.search([
            ('follower_id', '=', user_id),
            ('state', '=', 'accepted')
        ]).mapped('followed_id.id')
        
        mutual_ids = list(set(my_following) & set(their_following))
        
        if self.env.user.id in their_following and user_id in my_following:
            mutual_ids.append(user_id)
        
        return self.env['res.users'].browse(mutual_ids).read(['id', 'name', 'image_128'])