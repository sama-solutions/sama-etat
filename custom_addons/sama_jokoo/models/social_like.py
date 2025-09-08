# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SocialLike(models.Model):
    _name = 'social.like'
    _description = 'Like Social'
    _rec_name = 'display_name'

    # Relations
    user_id = fields.Many2one(
        'res.users',
        string='Utilisateur',
        required=True,
        ondelete='cascade'
    )
    post_id = fields.Many2one(
        'social.post',
        string='Post',
        ondelete='cascade'
    )
    comment_id = fields.Many2one(
        'social.comment',
        string='Commentaire',
        ondelete='cascade'
    )
    
    # Métadonnées
    create_date = fields.Datetime(
        string='Date de création',
        default=fields.Datetime.now,
        readonly=True
    )
    
    # Champ calculé pour l'affichage
    display_name = fields.Char(
        string='Nom d\'affichage',
        compute='_compute_display_name'
    )

    @api.depends('user_id', 'post_id', 'comment_id')
    def _compute_display_name(self):
        for like in self:
            if like.post_id:
                like.display_name = _('%s aime le post') % like.user_id.name
            elif like.comment_id:
                like.display_name = _('%s aime le commentaire') % like.user_id.name
            else:
                like.display_name = _('Like de %s') % like.user_id.name

    @api.constrains('post_id', 'comment_id')
    def _check_target(self):
        """Vérifier qu'un like cible soit un post soit un commentaire"""
        for like in self:
            if not like.post_id and not like.comment_id:
                raise ValidationError(_('Un like doit cibler soit un post soit un commentaire.'))
            if like.post_id and like.comment_id:
                raise ValidationError(_('Un like ne peut pas cibler à la fois un post et un commentaire.'))

    @api.constrains('user_id', 'post_id', 'comment_id')
    def _check_unique_like(self):
        """Vérifier qu'un utilisateur ne peut liker qu'une fois le même contenu"""
        for like in self:
            domain = [('user_id', '=', like.user_id.id)]
            
            if like.post_id:
                domain.append(('post_id', '=', like.post_id.id))
                existing = self.search(domain)
                if len(existing) > 1:
                    raise ValidationError(_('Vous avez déjà aimé ce post.'))
            
            if like.comment_id:
                domain.append(('comment_id', '=', like.comment_id.id))
                existing = self.search(domain)
                if len(existing) > 1:
                    raise ValidationError(_('Vous avez déjà aimé ce commentaire.'))

    @api.model
    def get_post_likes(self, post_id, limit=20):
        """Récupérer les likes d'un post avec les infos utilisateurs"""
        likes = self.search([('post_id', '=', post_id)], limit=limit, order='create_date desc')
        
        return [{
            'id': like.id,
            'user_id': like.user_id.id,
            'user_name': like.user_id.name,
            'user_avatar': like.user_id.image_128,
            'create_date': like.create_date,
        } for like in likes]

    @api.model
    def get_comment_likes(self, comment_id, limit=20):
        """Récupérer les likes d'un commentaire avec les infos utilisateurs"""
        likes = self.search([('comment_id', '=', comment_id)], limit=limit, order='create_date desc')
        
        return [{
            'id': like.id,
            'user_id': like.user_id.id,
            'user_name': like.user_id.name,
            'user_avatar': like.user_id.image_128,
            'create_date': like.create_date,
        } for like in likes]

    @api.model
    def get_user_likes(self, user_id=None, limit=50):
        """Récupérer les likes d'un utilisateur"""
        if not user_id:
            user_id = self.env.user.id
        
        likes = self.search([('user_id', '=', user_id)], limit=limit, order='create_date desc')
        
        result = []
        for like in likes:
            if like.post_id:
                result.append({
                    'id': like.id,
                    'type': 'post',
                    'target_id': like.post_id.id,
                    'target_content': like.post_id.content_preview,
                    'target_author': like.post_id.author_id.name,
                    'create_date': like.create_date,
                })
            elif like.comment_id:
                result.append({
                    'id': like.id,
                    'type': 'comment',
                    'target_id': like.comment_id.id,
                    'target_content': like.comment_id.content_preview,
                    'target_author': like.comment_id.author_id.name,
                    'post_id': like.comment_id.post_id.id,
                    'create_date': like.create_date,
                })
        
        return result