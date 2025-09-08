# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SocialComment(models.Model):
    _name = 'social.comment'
    _description = 'Commentaire Social'
    _order = 'create_date asc'
    _rec_name = 'content_preview'

    # Contenu
    content = fields.Html(
        string='Commentaire',
        required=True,
        help="Contenu du commentaire"
    )
    content_preview = fields.Char(
        string='Aperçu',
        compute='_compute_content_preview',
        store=True
    )
    
    # Relations
    post_id = fields.Many2one(
        'social.post',
        string='Post',
        required=True,
        ondelete='cascade'
    )
    author_id = fields.Many2one(
        'res.users',
        string='Auteur',
        required=True,
        default=lambda self: self.env.user
    )
    
    # Commentaires imbriqués (réponses)
    parent_id = fields.Many2one(
        'social.comment',
        string='Commentaire parent',
        ondelete='cascade'
    )
    child_ids = fields.One2many(
        'social.comment',
        'parent_id',
        string='Réponses'
    )
    
    # Interactions
    like_ids = fields.One2many(
        'social.like',
        'comment_id',
        string='Likes'
    )
    like_count = fields.Integer(
        string='Nombre de likes',
        compute='_compute_like_count',
        store=True
    )
    
    # Mentions
    mention_ids = fields.Many2many(
        'res.users',
        'social_comment_mention_rel',
        'comment_id',
        'user_id',
        string='Mentions'
    )
    
    # Statut
    state = fields.Selection([
        ('published', 'Publié'),
        ('moderated', 'En modération'),
        ('hidden', 'Masqué'),
    ], string='Statut', default='published')
    
    # Métadonnées
    is_edited = fields.Boolean(string='Modifié', default=False)
    edit_date = fields.Datetime(string='Date de modification')
    
    # Champs calculés pour l'utilisateur actuel
    user_liked = fields.Boolean(
        string='Aimé par moi',
        compute='_compute_user_liked'
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
        for comment in self:
            if comment.content:
                import re
                clean_content = re.sub('<[^<]+?>', '', comment.content or '')
                comment.content_preview = (clean_content[:50] + '...') if len(clean_content) > 50 else clean_content
            else:
                comment.content_preview = _('Commentaire vide')

    @api.depends('like_ids')
    def _compute_like_count(self):
        for comment in self:
            comment.like_count = len(comment.like_ids)

    def _compute_user_liked(self):
        for comment in self:
            comment.user_liked = bool(comment.like_ids.filtered(lambda l: l.user_id == self.env.user))

    def _compute_user_permissions(self):
        for comment in self:
            is_author = comment.author_id == self.env.user
            is_admin = self.env.user.has_group('sama_jokoo.group_social_admin')
            is_post_author = comment.post_id.author_id == self.env.user
            
            comment.user_can_edit = is_author
            comment.user_can_delete = is_author or is_admin or is_post_author

    @api.model_create_multi
    def create(self, vals_list):
        comments = super().create(vals_list)
        
        for comment in comments:
            # Extraire mentions
            comment._extract_mentions()
            
            # Notification pour l'auteur du post
            if comment.post_id.author_id != comment.author_id:
                self.env['social.notification'].create({
                    'user_id': comment.post_id.author_id.id,
                    'type': 'comment',
                    'title': _('Nouveau commentaire'),
                    'message': _('%s a commenté votre post') % comment.author_id.name,
                    'post_id': comment.post_id.id,
                    'comment_id': comment.id,
                    'author_id': comment.author_id.id,
                })
            
            # Notification pour le parent si c'est une réponse
            if comment.parent_id and comment.parent_id.author_id != comment.author_id:
                self.env['social.notification'].create({
                    'user_id': comment.parent_id.author_id.id,
                    'type': 'reply',
                    'title': _('Nouvelle réponse'),
                    'message': _('%s a répondu à votre commentaire') % comment.author_id.name,
                    'post_id': comment.post_id.id,
                    'comment_id': comment.id,
                    'author_id': comment.author_id.id,
                })
        
        return comments

    def write(self, vals):
        if 'content' in vals:
            vals['is_edited'] = True
            vals['edit_date'] = fields.Datetime.now()
        
        result = super().write(vals)
        
        if 'content' in vals:
            for comment in self:
                comment._extract_mentions()
        
        return result

    def _extract_mentions(self):
        """Extraire les mentions du contenu"""
        if not self.content:
            return
        
        import re
        mention_pattern = r'@(\w+)'
        mentions = re.findall(mention_pattern, self.content, re.IGNORECASE)
        
        mentioned_users = []
        for username in set(mentions):
            user = self.env['res.users'].search([
                '|',
                ('login', '=ilike', username),
                ('name', 'ilike', username)
            ], limit=1)
            if user and user != self.author_id:
                mentioned_users.append(user.id)
                
                # Notification pour la mention
                self.env['social.notification'].create({
                    'user_id': user.id,
                    'type': 'mention',
                    'title': _('Vous avez été mentionné'),
                    'message': _('%s vous a mentionné dans un commentaire') % self.author_id.name,
                    'post_id': self.post_id.id,
                    'comment_id': self.id,
                    'author_id': self.author_id.id,
                })
        
        self.mention_ids = [(6, 0, mentioned_users)]

    def action_like(self):
        """Liker/Unliker un commentaire"""
        existing_like = self.like_ids.filtered(lambda l: l.user_id == self.env.user)
        
        if existing_like:
            existing_like.unlink()
            return {'liked': False}
        else:
            self.env['social.like'].create({
                'comment_id': self.id,
                'user_id': self.env.user.id,
            })
            
            # Notification pour l'auteur du commentaire
            if self.author_id != self.env.user:
                self.env['social.notification'].create({
                    'user_id': self.author_id.id,
                    'type': 'like',
                    'title': _('Commentaire aimé'),
                    'message': _('%s a aimé votre commentaire') % self.env.user.name,
                    'post_id': self.post_id.id,
                    'comment_id': self.id,
                    'author_id': self.env.user.id,
                })
            
            return {'liked': True}

    def action_reply(self, content):
        """Répondre à un commentaire"""
        return self.create({
            'content': content,
            'post_id': self.post_id.id,
            'parent_id': self.id,
            'author_id': self.env.user.id,
        })

    def action_hide(self):
        """Masquer un commentaire"""
        self.write({'state': 'hidden'})

    def action_show(self):
        """Afficher un commentaire"""
        self.write({'state': 'published'})

    @api.model
    def get_comments_tree(self, post_id, limit=50):
        """Récupérer les commentaires d'un post avec leur hiérarchie"""
        comments = self.search([
            ('post_id', '=', post_id),
            ('state', '=', 'published'),
            ('parent_id', '=', False)
        ], limit=limit)
        
        def build_tree(comment):
            return {
                'id': comment.id,
                'content': comment.content,
                'author_id': comment.author_id.read(['id', 'name', 'image_128'])[0],
                'create_date': comment.create_date,
                'like_count': comment.like_count,
                'user_liked': comment.user_liked,
                'is_edited': comment.is_edited,
                'edit_date': comment.edit_date,
                'children': [build_tree(child) for child in comment.child_ids.filtered(lambda c: c.state == 'published')]
            }
        
        return [build_tree(comment) for comment in comments]