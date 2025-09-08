# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SocialNotification(models.Model):
    _name = 'social.notification'
    _description = 'Notification Sociale'
    _order = 'create_date desc'
    _rec_name = 'title'

    # Destinataire
    user_id = fields.Many2one(
        'res.users',
        string='Utilisateur',
        required=True,
        ondelete='cascade'
    )
    
    # Type de notification
    type = fields.Selection([
        ('like', 'Like'),
        ('comment', 'Commentaire'),
        ('reply', 'Réponse'),
        ('mention', 'Mention'),
        ('share', 'Partage'),
        ('follow_request', 'Demande de suivi'),
        ('follow_accepted', 'Suivi accepté'),
        ('new_follower', 'Nouvel abonné'),
        ('post_update', 'Mise à jour de post'),
        ('system', 'Système'),
        ('custom', 'Personnalisé'),
    ], string='Type', required=True)
    
    # Contenu
    title = fields.Char(string='Titre', required=True)
    message = fields.Text(string='Message')
    
    # Relations
    post_id = fields.Many2one(
        'social.post',
        string='Post lié',
        ondelete='cascade'
    )
    comment_id = fields.Many2one(
        'social.comment',
        string='Commentaire lié',
        ondelete='cascade'
    )
    author_id = fields.Many2one(
        'res.users',
        string='Auteur de l\'action',
        help="Utilisateur qui a déclenché la notification"
    )
    
    # Statut
    is_read = fields.Boolean(string='Lu', default=False)
    read_date = fields.Datetime(string='Date de lecture')
    
    # Métadonnées
    create_date = fields.Datetime(
        string='Date de création',
        default=fields.Datetime.now,
        readonly=True
    )
    
    # Données supplémentaires (JSON)
    data = fields.Json(string='Données supplémentaires')
    
    # Champs calculés
    icon = fields.Char(
        string='Icône',
        compute='_compute_icon'
    )
    color = fields.Char(
        string='Couleur',
        compute='_compute_color'
    )
    action_url = fields.Char(
        string='URL d\'action',
        compute='_compute_action_url'
    )

    @api.depends('type')
    def _compute_icon(self):
        icons = {
            'like': 'fa-heart',
            'comment': 'fa-comment',
            'reply': 'fa-reply',
            'mention': 'fa-at',
            'share': 'fa-share',
            'follow_request': 'fa-user-plus',
            'follow_accepted': 'fa-check',
            'new_follower': 'fa-users',
            'post_update': 'fa-edit',
            'system': 'fa-cog',
            'custom': 'fa-bell',
        }
        
        for notification in self:
            notification.icon = icons.get(notification.type, 'fa-bell')

    @api.depends('type')
    def _compute_color(self):
        colors = {
            'like': '#e74c3c',
            'comment': '#3498db',
            'reply': '#9b59b6',
            'mention': '#f39c12',
            'share': '#2ecc71',
            'follow_request': '#34495e',
            'follow_accepted': '#27ae60',
            'new_follower': '#16a085',
            'post_update': '#f1c40f',
            'system': '#95a5a6',
            'custom': '#8e44ad',
        }
        
        for notification in self:
            notification.color = colors.get(notification.type, '#95a5a6')

    @api.depends('type', 'post_id', 'comment_id')
    def _compute_action_url(self):
        for notification in self:
            if notification.post_id:
                notification.action_url = f'/social/post/{notification.post_id.id}'
            elif notification.comment_id:
                notification.action_url = f'/social/post/{notification.comment_id.post_id.id}#comment-{notification.comment_id.id}'
            elif notification.type in ['follow_request', 'new_follower']:
                notification.action_url = f'/social/profile/{notification.author_id.id}'
            else:
                notification.action_url = '/social/notifications'

    def action_mark_read(self):
        """Marquer comme lu"""
        self.write({
            'is_read': True,
            'read_date': fields.Datetime.now()
        })

    def action_mark_unread(self):
        """Marquer comme non lu"""
        self.write({
            'is_read': False,
            'read_date': False
        })

    @api.model
    def mark_all_read(self, user_id=None):
        """Marquer toutes les notifications comme lues"""
        if not user_id:
            user_id = self.env.user.id
        
        notifications = self.search([
            ('user_id', '=', user_id),
            ('is_read', '=', False)
        ])
        
        notifications.action_mark_read()
        return len(notifications)

    @api.model
    def get_notifications(self, user_id=None, limit=50, unread_only=False):
        """Récupérer les notifications d'un utilisateur"""
        if not user_id:
            user_id = self.env.user.id
        
        domain = [('user_id', '=', user_id)]
        
        if unread_only:
            domain.append(('is_read', '=', False))
        
        notifications = self.search(domain, limit=limit)
        
        return [{
            'id': notif.id,
            'type': notif.type,
            'title': notif.title,
            'message': notif.message,
            'icon': notif.icon,
            'color': notif.color,
            'action_url': notif.action_url,
            'is_read': notif.is_read,
            'create_date': notif.create_date,
            'author': {
                'id': notif.author_id.id,
                'name': notif.author_id.name,
                'avatar': notif.author_id.image_128,
            } if notif.author_id else None,
            'post_id': notif.post_id.id if notif.post_id else None,
            'comment_id': notif.comment_id.id if notif.comment_id else None,
            'data': notif.data,
        } for notif in notifications]

    @api.model
    def get_unread_count(self, user_id=None):
        """Récupérer le nombre de notifications non lues"""
        if not user_id:
            user_id = self.env.user.id
        
        return self.search_count([
            ('user_id', '=', user_id),
            ('is_read', '=', False)
        ])

    @api.model
    def create_notification(self, user_id, notification_type, title, message, **kwargs):
        """Créer une notification"""
        vals = {
            'user_id': user_id,
            'type': notification_type,
            'title': title,
            'message': message,
        }
        
        # Ajouter les champs optionnels
        for field in ['post_id', 'comment_id', 'author_id', 'data']:
            if field in kwargs:
                vals[field] = kwargs[field]
        
        notification = self.create(vals)
        
        # Envoyer notification push si configuré
        self._send_push_notification(notification)
        
        return notification

    def _send_push_notification(self, notification):
        """Envoyer une notification push (à implémenter selon le service choisi)"""
        # TODO: Intégrer avec Firebase Cloud Messaging ou autre service
        pass

    @api.model
    def cleanup_old_notifications(self, days=30):
        """Nettoyer les anciennes notifications"""
        cutoff_date = fields.Datetime.now() - timedelta(days=days)
        
        old_notifications = self.search([
            ('create_date', '<', cutoff_date),
            ('is_read', '=', True)
        ])
        
        count = len(old_notifications)
        old_notifications.unlink()
        
        return count

    @api.model
    def get_notification_stats(self, user_id=None):
        """Récupérer les statistiques de notifications"""
        if not user_id:
            user_id = self.env.user.id
        
        total = self.search_count([('user_id', '=', user_id)])
        unread = self.search_count([('user_id', '=', user_id), ('is_read', '=', False)])
        
        # Statistiques par type
        type_stats = {}
        for notif_type in dict(self._fields['type'].selection).keys():
            count = self.search_count([
                ('user_id', '=', user_id),
                ('type', '=', notif_type)
            ])
            if count > 0:
                type_stats[notif_type] = count
        
        return {
            'total': total,
            'unread': unread,
            'read': total - unread,
            'by_type': type_stats,
        }