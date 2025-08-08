{
    'name': 'SAMA ÉTAT',
    'version': '2.0',
    'category': 'Project Management',
    'summary': 'Governance platform for strategic plans: projects, budgets, decisions, events (Plan Sénégal 2050 ready).',
    'description': """
        SAMA ÉTAT est une plateforme Odoo pour exécuter un plan stratégique (État, municipalités, agences,
        entreprises publiques). Elle structure, pilote et rend visible l’action publique: projets, budgets,
        décisions, événements et suivi-évaluation, avec transparence par design.

        SAMA ÉTAT is an Odoo-based platform to operationalize strategic plans for governments, municipalities,
        and public entities. It structures, drives, and makes public action visible: projects, budgets,
        decisions, events, and M&E — transparency by design.
    """,
    'author': 'Mamadou Mbagnick DOGUE, Rassol DOGUE',
    'website': 'https://github.com/loi200812/sama-etat',
    'depends': ['base', 'project', 'mail', 'website', 'hr', 'calendar', 'website_event'],
    'data': [
        # Security files loaded first to ensure groups are defined
        'security/security.xml',
        'security/ir.model.access.csv',
        # Views defining actions and structures must be loaded after security
        'views/views.xml',
        'views/strategic_plan_views.xml',
        'views/strategic_pillar_views.xml',
        'views/strategic_axis_views.xml',
        'views/strategic_objective_views.xml',
        'views/strategic_kpi_views.xml',
        'views/government_project_views.xml',
        'views/government_decision_views.xml',
        'views/government_event_views.xml',
        'views/government_budget_views.xml',
        'views/government_ministry_views.xml',
        'views/ai_views_clean.xml',  # Clean AI implementation
        'views/ai_content_helper_views.xml',  # WYSIWYG AI content helper
        # 'views/ai_provider_config_views.xml',  # Moved later to ensure load order before menus
        # 'views/menu_views.xml',  # Moved to the end

        'views/public_templates.xml',
        'views/public_templates_extra.xml',
        'views/public_templates_modern.xml',
        'views/modern_dashboard.xml',
        'views/public_decision_page.xml',
        'views/public_event_page.xml',
        'views/public_objective_page.xml',
        'views/public_axis_page.xml',
        'views/public_pillar_page.xml',
        'views/calendar_event_views.xml',
        # Wizard views
        'wizard/government_project_wizard_views.xml',
        # Menu views loaded after all actions
        'views/dashboard_views.xml',
        'views/public_map.xml',
        'views/fullscreen_map.xml',
        'views/website_homepage.xml',
        'views/website_about.xml',
        # Dashboard default data
        'data/dashboard_data.xml',
        # AI default data
        # 'data/ai_default_data.xml',  # Temporairement désactivé pour éviter les conflits
        # Currency configuration - disabled to avoid conflicts with existing journal entries
        # 'data/currency_xof_data.xml',
        # Demo data for legal compliance (temporairement désactivées)
        # 'data/demo_legal_compliance.xml',
        # 'data/demo_cost_breakdown.xml',
        # 'data/demo_funding_sources.xml',
        # 'data/demo_legal_texts.xml',
        # Demo data files
        'data/strategic_objectives_demo_data.xml',
        'data/ministries_demo_data.xml',
        'data/budgets_demo_data.xml',
        'data/government_projects_demo_data.xml',
        'data/employees_demo_data.xml',
        'data/project_tasks_demo_data.xml',
        'data/government_events_demo_data.xml',
        'data/government_decisions_demo_data.xml',
        'data/cleanup_old_ai_menus.xml',
        'data/ai_menu_cleanup.xml',
        'data/force_clean_ai_implementation.xml',
        'data/final_ai_model_cleanup.xml',
        'data/ai_data_clean.xml',
        'data/ai_provider_config_data.xml',
        # Ensure action is defined right before menus
        'views/ai_provider_config_views.xml',
        'views/menu_views.xml',
        # OAuth controllers
        'controllers/oauth.py',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'external_dependencies': {
        'python': ['qrcode', 'pillow', 'requests', 'cryptography']
    },
}
