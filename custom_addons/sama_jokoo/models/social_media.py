# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import base64
import mimetypes
import os


class SocialMedia(models.Model):
    _name = 'social.media'
    _description = 'Média Social'
    _order = 'sequence, create_date'

    # Relations
    post_id = fields.Many2one(
        'social.post',
        string='Post',
        ondelete='cascade'
    )
    
    # Fichier
    name = fields.Char(string='Nom du fichier', required=True)
    file_data = fields.Binary(string='Fichier', required=True)
    file_size = fields.Integer(string='Taille du fichier')
    mimetype = fields.Char(string='Type MIME')
    
    # Type de média
    media_type = fields.Selection([
        ('image', 'Image'),
        ('video', 'Vidéo'),
        ('audio', 'Audio'),
        ('document', 'Document'),
    ], string='Type de média', compute='_compute_media_type', store=True)
    
    # Métadonnées pour images
    width = fields.Integer(string='Largeur')
    height = fields.Integer(string='Hauteur')
    
    # Métadonnées pour vidéos
    duration = fields.Float(string='Durée (secondes)')
    
    # Miniature (pour vidéos)
    thumbnail = fields.Binary(string='Miniature')
    
    # Description et alt text
    description = fields.Text(string='Description')
    alt_text = fields.Char(string='Texte alternatif')
    
    # Ordre d'affichage
    sequence = fields.Integer(string='Séquence', default=10)
    
    # URL publique (si stockage externe)
    public_url = fields.Char(string='URL publique')
    
    # Statut
    state = fields.Selection([
        ('uploading', 'En cours d\'upload'),
        ('processing', 'En traitement'),
        ('ready', 'Prêt'),
        ('error', 'Erreur'),
    ], string='Statut', default='ready')
    
    # Champs calculés
    file_extension = fields.Char(
        string='Extension',
        compute='_compute_file_extension'
    )
    is_image = fields.Boolean(
        string='Est une image',
        compute='_compute_media_flags'
    )
    is_video = fields.Boolean(
        string='Est une vidéo',
        compute='_compute_media_flags'
    )
    display_name = fields.Char(
        string='Nom d\'affichage',
        compute='_compute_display_name'
    )

    @api.depends('mimetype', 'name')
    def _compute_media_type(self):
        for media in self:
            if media.mimetype:
                if media.mimetype.startswith('image/'):
                    media.media_type = 'image'
                elif media.mimetype.startswith('video/'):
                    media.media_type = 'video'
                elif media.mimetype.startswith('audio/'):
                    media.media_type = 'audio'
                else:
                    media.media_type = 'document'
            else:
                # Fallback basé sur l'extension
                ext = os.path.splitext(media.name)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
                    media.media_type = 'image'
                elif ext in ['.mp4', '.avi', '.mov', '.webm', '.mkv']:
                    media.media_type = 'video'
                elif ext in ['.mp3', '.wav', '.ogg', '.m4a']:
                    media.media_type = 'audio'
                else:
                    media.media_type = 'document'

    @api.depends('name')
    def _compute_file_extension(self):
        for media in self:
            if media.name:
                media.file_extension = os.path.splitext(media.name)[1].lower()
            else:
                media.file_extension = ''

    @api.depends('media_type')
    def _compute_media_flags(self):
        for media in self:
            media.is_image = media.media_type == 'image'
            media.is_video = media.media_type == 'video'

    @api.depends('name', 'media_type')
    def _compute_display_name(self):
        for media in self:
            if media.name:
                media.display_name = f"{media.name} ({media.media_type})"
            else:
                media.display_name = f"Média {media.media_type}"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Détecter le type MIME si pas fourni
            if 'file_data' in vals and 'mimetype' not in vals:
                if 'name' in vals:
                    mimetype, _ = mimetypes.guess_type(vals['name'])
                    if mimetype:
                        vals['mimetype'] = mimetype
            
            # Calculer la taille du fichier
            if 'file_data' in vals and 'file_size' not in vals:
                try:
                    file_data = base64.b64decode(vals['file_data'])
                    vals['file_size'] = len(file_data)
                except:
                    pass
        
        medias = super().create(vals_list)
        
        # Post-traitement pour les images et vidéos
        for media in medias:
            if media.is_image:
                media._process_image()
            elif media.is_video:
                media._process_video()
        
        return medias

    def _process_image(self):
        """Traiter une image (redimensionner, extraire métadonnées)"""
        try:
            from PIL import Image
            import io
            
            # Décoder l'image
            image_data = base64.b64decode(self.file_data)
            image = Image.open(io.BytesIO(image_data))
            
            # Extraire les dimensions
            self.width, self.height = image.size
            
            # Redimensionner si trop grande (max 2048px)
            max_size = 2048
            if max(self.width, self.height) > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                # Sauvegarder l'image redimensionnée
                output = io.BytesIO()
                format = image.format or 'JPEG'
                image.save(output, format=format, quality=85, optimize=True)
                
                self.file_data = base64.b64encode(output.getvalue())
                self.width, self.height = image.size
                self.file_size = len(output.getvalue())
        
        except Exception as e:
            # Log l'erreur mais ne pas faire échouer la création
            import logging
            _logger = logging.getLogger(__name__)
            _logger.warning(f"Erreur lors du traitement de l'image {self.name}: {e}")

    def _process_video(self):
        """Traiter une vidéo (extraire métadonnées, créer miniature)"""
        # TODO: Implémenter avec ffmpeg ou autre outil
        # Pour l'instant, on laisse vide
        pass

    @api.constrains('file_size')
    def _check_file_size(self):
        """Vérifier la taille du fichier"""
        max_size = self.env['ir.config_parameter'].sudo().get_param(
            'sama_jokoo.max_file_size', '10485760'  # 10MB par défaut
        )
        max_size = int(max_size)
        
        for media in self:
            if media.file_size > max_size:
                raise ValidationError(
                    _('Le fichier est trop volumineux. Taille maximum autorisée: %s MB') 
                    % (max_size / 1024 / 1024)
                )

    @api.constrains('mimetype')
    def _check_allowed_types(self):
        """Vérifier les types de fichiers autorisés"""
        allowed_types = self.env['ir.config_parameter'].sudo().get_param(
            'sama_jokoo.allowed_mimetypes',
            'image/jpeg,image/png,image/gif,image/webp,video/mp4,video/webm,audio/mp3,audio/wav'
        ).split(',')
        
        for media in self:
            if media.mimetype and media.mimetype not in allowed_types:
                raise ValidationError(
                    _('Type de fichier non autorisé: %s') % media.mimetype
                )

    def get_download_url(self):
        """Récupérer l'URL de téléchargement"""
        return f'/web/content/social.media/{self.id}/file_data/{self.name}'

    def get_thumbnail_url(self):
        """Récupérer l'URL de la miniature"""
        if self.is_image:
            return self.get_download_url()
        elif self.is_video and self.thumbnail:
            return f'/web/content/social.media/{self.id}/thumbnail/thumbnail_{self.name}'
        else:
            # Retourner une icône par défaut selon le type
            icons = {
                'video': '/sama_jokoo/static/img/video-icon.png',
                'audio': '/sama_jokoo/static/img/audio-icon.png',
                'document': '/sama_jokoo/static/img/document-icon.png',
            }
            return icons.get(self.media_type, '/sama_jokoo/static/img/file-icon.png')

    @api.model
    def upload_media(self, file_data, filename, post_id=None):
        """Upload d'un média"""
        vals = {
            'name': filename,
            'file_data': file_data,
            'state': 'uploading',
        }
        
        if post_id:
            vals['post_id'] = post_id
        
        media = self.create(vals)
        
        # Marquer comme prêt après traitement
        media.write({'state': 'ready'})
        
        return media

    @api.model
    def get_media_stats(self):
        """Récupérer les statistiques des médias"""
        total_count = self.search_count([])
        total_size = sum(self.search([]).mapped('file_size'))
        
        stats_by_type = {}
        for media_type in ['image', 'video', 'audio', 'document']:
            count = self.search_count([('media_type', '=', media_type)])
            size = sum(self.search([('media_type', '=', media_type)]).mapped('file_size'))
            stats_by_type[media_type] = {
                'count': count,
                'size': size,
            }
        
        return {
            'total_count': total_count,
            'total_size': total_size,
            'by_type': stats_by_type,
        }