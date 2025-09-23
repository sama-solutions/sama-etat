# -*- coding: utf-8 -*-
{
    'name': 'SAMA SYNDICAT - Gestion Zéro Papier',
    'version': '1.0.0',
    'category': 'Human Resources',
    'summary': 'Gestion complète et zéro papier d\'un syndicat ou groupement professionnel',
    'description': """
SAMA SYNDICAT - Gestion Zéro Papier d'un Syndicat
==================================================

Ce module permet la gestion complète et zéro papier d'un syndicat ou groupement professionnel.

Fonctionnalités principales :
-----------------------------
* Gestion des adhérents et cotisations
* Organisation des assemblées générales et réunions
* Gestion des revendications et négociations
* Suivi des actions syndicales et manifestations
* Communication avec les adhérents
* Gestion des formations professionnelles
* Suivi des conventions collectives
* Gestion des conflits et médiations
* Tableau de bord et statistiques
* Interface publique pour les adhérents

Modules inclus :
----------------
* Gestion des adhérents
* Assemblées et réunions
* Revendications syndicales
* Actions collectives
* Communications
* Formations
* Conventions collectives
* Médiations et conflits
* Tableau de bord
* Interface publique

Auteur : POLITECH SÉNÉGAL
Licence : LGPL-3
    """,
    'author': 'POLITECH SÉNÉGAL',
    'website': 'https://www.politech.sn',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'portal',
        'website',
        'contacts'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'data/data.xml',
        'views/syndicat_adherent_views.xml',
        'views/syndicat_assemblee_views.xml',
        'views/syndicat_revendication_views.xml',
        'views/syndicat_action_views.xml',
        'views/syndicat_communication_views.xml',
        'views/syndicat_formation_views.xml',
        'views/syndicat_convention_views.xml',
        'views/syndicat_mediation_views.xml',
        'views/syndicat_dashboard_views.xml',
        'views/dashboard_actions.xml',
        'views/dashboard_v1_native_odoo.xml',
        'views/dashboard_v2_compact.xml',
        'views/dashboard_v3_graphiques.xml',
        'views/dashboard_v4_minimal.xml',
        'views/dashboard_modern_cards.xml',
        'views/dashboard_executive.xml',
        'views/dashboard_modern_menus.xml',
        'views/website/website_templates.xml',
        'views/menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sama_syndicat/static/src/css/dashboard.css',
            'sama_syndicat/static/src/css/dashboard_modern.css',
        ],
        'web.assets_frontend': [
            'sama_syndicat/static/src/css/website.css',
        ],
    },
    'demo': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 10,
}