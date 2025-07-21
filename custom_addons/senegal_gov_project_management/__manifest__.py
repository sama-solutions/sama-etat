{
    'name': 'Senegal Government Project Management',
    'version': '1.0',
    'category': 'Project Management',
    'summary': 'Module for managing government projects, decisions, events, and budgets based on Plan Senegal 2050.',
    'description': """
        This module provides a comprehensive solution for managing various aspects of government operations
        in Senegal, aligning them with the strategic objectives of Plan Senegal 2050.
    """,
    'author': 'Your Name/Organization', # TODO: Replace with actual author
    'website': 'http://www.yourwebsite.com', # TODO: Replace with actual website
    'depends': ['base', 'project', 'mail', 'website', 'hr'],
    'data': [
        # Views defining actions and structures must be loaded first
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
        
        'views/public_templates.xml',
        'views/public_templates_extra.xml',
        # Wizard views
        'wizard/government_project_wizard_views.xml',
        # Menu views loaded after all actions
        'views/dashboard_views.xml',
        'views/menu_views.xml',
        # Security files loaded last to ensure models are registered
        'security/ir.model.access.csv',
        'security/security.xml',
        # Currency configuration
        'data/currency_xof_data.xml',
        # Demo data files
        'data/strategic_objectives_demo_data.xml',
        'data/ministries_demo_data.xml',
        'data/budgets_demo_data.xml',
        'data/government_projects_demo_data.xml',
        'data/employees_demo_data.xml',
        'data/project_tasks_demo_data.xml',
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'external_dependencies': {
        'python': ['qrcode', 'pillow']
    },
}
