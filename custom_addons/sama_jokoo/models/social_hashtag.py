# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SocialHashtag(models.Model):
    _name = 'social.hashtag'
    _description = 'Hashtag Social'
    _order = 'usage_count desc, name'

    # Nom du hashtag
    name = fields.Char(
        string='Hashtag',
        required=True,
        index=True,
        help="Nom du hashtag sans le symbole #"
    )
    
    # Description
    description = fields.Text(string='Description')
    
    # Relations
    post_ids = fields.Many2many(
        'social.post',
        string='Posts'
    )
    
    # Statistiques
    usage_count = fields.Integer(
        string='Nombre d\'utilisations',
        compute='_compute_usage_count',
        store=True
    )
    
    # Métadonnées
    create_date = fields.Datetime(
        string='Date de création',
        default=fields.Datetime.now,
        readonly=True
    )
    last_used = fields.Datetime(
        string='Dernière utilisation',
        compute='_compute_last_used',
        store=True
    )
    
    # Statut
    is_trending = fields.Boolean(
        string='Tendance',
        compute='_compute_is_trending'
    )
    is_featured = fields.Boolean(
        string='Mis en avant',
        default=False
    )
    
    # Couleur pour l'affichage
    color = fields.Char(
        string='Couleur',
        default='#3498db',
        help="Couleur d'affichage du hashtag"
    )

    @api.depends('post_ids')
    def _compute_usage_count(self):
        for hashtag in self:
            hashtag.usage_count = len(hashtag.post_ids.filtered(lambda p: p.state == 'published'))

    @api.depends('post_ids.create_date')
    def _compute_last_used(self):
        for hashtag in self:
            if hashtag.post_ids:
                hashtag.last_used = max(hashtag.post_ids.mapped('create_date'))
            else:
                hashtag.last_used = False

    def _compute_is_trending(self):
        """Calculer si le hashtag est en tendance (utilisé récemment et fréquemment)"""
        from datetime import datetime, timedelta
        
        # Considérer comme tendance si utilisé dans les 7 derniers jours
        # et au moins 5 fois
        cutoff_date = datetime.now() - timedelta(days=7)
        
        for hashtag in self:
            recent_posts = hashtag.post_ids.filtered(
                lambda p: p.create_date >= cutoff_date and p.state == 'published'
            )
            hashtag.is_trending = len(recent_posts) >= 5

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Normaliser le nom (minuscules, sans #)
            if 'name' in vals:
                vals['name'] = vals['name'].lower().lstrip('#')
        
        return super().create(vals_list)

    def write(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].lower().lstrip('#')
        
        return super().write(vals)

    @api.model
    def get_trending_hashtags(self, limit=10):
        """Récupérer les hashtags en tendance"""
        hashtags = self.search([
            ('is_trending', '=', True)
        ], limit=limit, order='usage_count desc')
        
        return [{
            'id': hashtag.id,
            'name': hashtag.name,
            'usage_count': hashtag.usage_count,
            'color': hashtag.color,
            'is_featured': hashtag.is_featured,
        } for hashtag in hashtags]

    @api.model
    def get_popular_hashtags(self, limit=20):
        """Récupérer les hashtags populaires"""
        hashtags = self.search([], limit=limit, order='usage_count desc')
        
        return [{
            'id': hashtag.id,
            'name': hashtag.name,
            'usage_count': hashtag.usage_count,
            'color': hashtag.color,
            'is_trending': hashtag.is_trending,
            'is_featured': hashtag.is_featured,
        } for hashtag in hashtags]

    @api.model
    def search_hashtags(self, query, limit=10):
        """Rechercher des hashtags"""
        query = query.lower().lstrip('#')
        
        hashtags = self.search([
            ('name', 'ilike', query)
        ], limit=limit, order='usage_count desc')
        
        return [{
            'id': hashtag.id,
            'name': hashtag.name,
            'usage_count': hashtag.usage_count,
            'color': hashtag.color,
        } for hashtag in hashtags]

    @api.model
    def get_hashtag_posts(self, hashtag_id, limit=20, offset=0):
        """Récupérer les posts d'un hashtag"""
        hashtag = self.browse(hashtag_id)
        
        posts = hashtag.post_ids.filtered(
            lambda p: p.state == 'published'
        ).sorted('create_date', reverse=True)[offset:offset+limit]
        
        return posts.read([
            'id', 'content', 'content_preview', 'author_id', 'create_date',
            'like_count', 'comment_count', 'share_count', 'has_media'
        ])

    @api.model
    def get_or_create_hashtag(self, name):
        """Récupérer ou créer un hashtag"""
        name = name.lower().lstrip('#')
        
        hashtag = self.search([('name', '=', name)], limit=1)
        
        if not hashtag:
            hashtag = self.create({'name': name})
        
        return hashtag

    @api.model
    def get_hashtag_suggestions(self, partial_name, limit=5):
        """Récupérer des suggestions de hashtags"""
        partial_name = partial_name.lower().lstrip('#')
        
        if len(partial_name) < 2:
            return []
        
        hashtags = self.search([
            ('name', 'ilike', f'{partial_name}%')
        ], limit=limit, order='usage_count desc')
        
        return [hashtag.name for hashtag in hashtags]

    @api.model
    def get_hashtag_stats(self):
        """Récupérer les statistiques des hashtags"""
        total_hashtags = self.search_count([])
        trending_count = self.search_count([('is_trending', '=', True)])
        featured_count = self.search_count([('is_featured', '=', True)])
        
        # Top 5 hashtags
        top_hashtags = self.search([], limit=5, order='usage_count desc')
        
        return {
            'total_hashtags': total_hashtags,
            'trending_count': trending_count,
            'featured_count': featured_count,
            'top_hashtags': [{
                'name': h.name,
                'usage_count': h.usage_count,
            } for h in top_hashtags]
        }

    def action_feature(self):
        """Mettre en avant un hashtag"""
        self.is_featured = True

    def action_unfeature(self):
        """Retirer de la mise en avant"""
        self.is_featured = False

    def action_view_posts(self):
        """Voir les posts du hashtag"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Posts #{self.name}',
            'res_model': 'social.post',
            'view_mode': 'tree,form',
            'domain': [('hashtag_ids', 'in', self.id)],
            'context': {'default_hashtag_ids': [(6, 0, [self.id])]},
        }