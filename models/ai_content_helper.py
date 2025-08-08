# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class AIContentHelper(models.TransientModel):
    """Helper model for AI content generation with WYSIWYG editor"""
    _name = 'ai.content.helper'
    _description = 'Assistant IA pour Génération de Contenu'
    
    # Input fields
    prompt = fields.Text(string="Prompt IA", required=True, 
                        help="Décrivez le contenu que vous souhaitez générer")
    context_info = fields.Text(string="Contexte Additionnel", 
                              help="Informations supplémentaires pour améliorer la génération")
    
    # Output field with WYSIWYG editor
    generated_content = fields.Html(string="Contenu Généré", readonly=True)
    
    # Configuration
    ai_model_id = fields.Many2one('ai.model.config', string="Modèle IA", 
                                 default=lambda self: self._get_default_model())
    
    # Status
    is_generated = fields.Boolean(string="Contenu Généré", default=False)
    
    @api.model
    def _get_default_model(self):
        """Get default AI model"""
        return self.env['ai.model.config'].get_default_model()
    
    def generate_content(self):
        """Generate AI content and display in WYSIWYG editor"""
        if not self.prompt:
            raise UserError("Veuillez saisir un prompt pour générer du contenu.")
        
        if not self.ai_model_id:
            raise UserError("Aucun modèle IA configuré. Veuillez configurer un modèle IA d'abord.")
        
        try:
            # Prepare context
            full_context = ""
            if self.context_info:
                full_context = f"Contexte: {self.context_info}\n\n"
            
            full_prompt = f"{full_context}Prompt: {self.prompt}"
            
            # Generate content using AI model
            content = self.ai_model_id.generate_content(full_prompt)
            
            # Format content as HTML for WYSIWYG display
            formatted_content = self._format_content_as_html(content)
            
            # Update fields
            self.write({
                'generated_content': formatted_content,
                'is_generated': True
            })
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Contenu généré avec succès!',
                    'message': 'Le contenu IA a été généré et est maintenant disponible dans l\'éditeur.',
                    'type': 'success',
                }
            }
            
        except Exception as e:
            _logger.error(f"Erreur lors de la génération de contenu IA: {e}")
            raise UserError(f"Erreur lors de la génération: {str(e)}")
    
    def _format_content_as_html(self, content):
        """Format plain text content as HTML for WYSIWYG editor"""
        if not content:
            return ""
        
        # Convert line breaks to HTML paragraphs
        paragraphs = content.split('\n\n')
        html_content = ""
        
        for paragraph in paragraphs:
            if paragraph.strip():
                # Handle bullet points
                if paragraph.strip().startswith('•') or paragraph.strip().startswith('-'):
                    lines = paragraph.split('\n')
                    html_content += "<ul>"
                    for line in lines:
                        if line.strip():
                            clean_line = line.strip().lstrip('•-').strip()
                            html_content += f"<li>{clean_line}</li>"
                    html_content += "</ul>"
                else:
                    # Regular paragraph
                    html_content += f"<p>{paragraph.strip()}</p>"
        
        return html_content
    
    def copy_to_clipboard(self):
        """Copy generated content to clipboard (client-side action)"""
        if not self.generated_content:
            raise UserError("Aucun contenu à copier.")
        
        return {
            'type': 'ir.actions.client',
            'tag': 'copy_to_clipboard',
            'params': {
                'content': self.generated_content,
                'title': 'Contenu copié!',
                'message': 'Le contenu a été copié dans le presse-papiers.',
            }
        }
    
    def clear_content(self):
        """Clear generated content"""
        self.write({
            'generated_content': '',
            'is_generated': False
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Contenu effacé',
                'message': 'Le contenu généré a été effacé.',
                'type': 'info',
            }
        }
