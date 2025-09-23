# -*- coding: utf-8 -*-

from odoo import http, fields, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict


class SyndicatPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        """Ajoute les compteurs syndicaux au portail"""
        values = super()._prepare_home_portal_values(counters)
        
        partner = request.env.user.partner_id
        if partner.is_adherent_syndicat and partner.adherent_syndicat_id:
            adherent = partner.adherent_syndicat_id
            
            if 'assemblee_count' in counters:
                values['assemblee_count'] = len(adherent.assemblee_ids)
            if 'action_count' in counters:
                values['action_count'] = len(adherent.action_ids)
            if 'formation_count' in counters:
                values['formation_count'] = len(adherent.formation_ids)
            if 'cotisation_count' in counters:
                values['cotisation_count'] = len(adherent.cotisation_ids)
        
        return values

    def _get_archive_groups(self, model, domain=None, fields=None, groupby="create_date", order="create_date desc"):
        """Groupement par archives pour les modèles syndicaux"""
        if not model:
            return []
        return super()._get_archive_groups(model, domain, fields, groupby, order)

    # === ASSEMBLÉES ===
    
    @http.route(['/my/assemblees', '/my/assemblees/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_assemblees(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        """Page des assemblées de l'adhérent"""
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        
        if not partner.is_adherent_syndicat or not partner.adherent_syndicat_id:
            return request.render('sama_syndicat.portal_not_adherent')
        
        adherent = partner.adherent_syndicat_id
        
        # Domaine de base
        domain = [('adherent_invites_ids', 'in', [adherent.id])]
        
        # Filtres par date
        if date_begin and date_end:
            domain += [('date_debut', '>=', date_begin), ('date_debut', '<=', date_end)]
        
        # Options de tri
        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'date_debut desc'},
            'name': {'label': _('Nom'), 'order': 'name'},
            'status': {'label': _('Statut'), 'order': 'statut'},
        }
        
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        
        # Compter les assemblées
        assemblee_count = request.env['syndicat.assemblee'].search_count(domain)
        
        # Pagination
        pager = portal_pager(
            url="/my/assemblees",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=assemblee_count,
            page=page,
            step=self._items_per_page
        )
        
        # Récupérer les assemblées
        assemblees = request.env['syndicat.assemblee'].search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'assemblees': assemblees,
            'page_name': 'assemblee',
            'archive_groups': self._get_archive_groups('syndicat.assemblee', domain),
            'default_url': '/my/assemblees',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        
        return request.render("sama_syndicat.portal_my_assemblees", values)

    @http.route(['/my/assemblee/<int:assemblee_id>'], type='http', auth="user", website=True)
    def portal_my_assemblee(self, assemblee_id=None, access_token=None, **kw):
        """Détail d'une assemblée"""
        try:
            assemblee_sudo = self._document_check_access('syndicat.assemblee', assemblee_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        values = {
            'assemblee': assemblee_sudo,
            'page_name': 'assemblee',
        }
        
        return request.render("sama_syndicat.portal_my_assemblee", values)

    # === ACTIONS ===
    
    @http.route(['/my/actions', '/my/actions/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_actions(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        """Page des actions de l'adhérent"""
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        
        if not partner.is_adherent_syndicat or not partner.adherent_syndicat_id:
            return request.render('sama_syndicat.portal_not_adherent')
        
        adherent = partner.adherent_syndicat_id
        
        # Domaine de base
        domain = [('adherents_participants_ids', 'in', [adherent.id])]
        
        # Filtres par date
        if date_begin and date_end:
            domain += [('date_debut', '>=', date_begin), ('date_debut', '<=', date_end)]
        
        # Options de tri
        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'date_debut desc'},
            'name': {'label': _('Nom'), 'order': 'name'},
            'status': {'label': _('Statut'), 'order': 'statut'},
        }
        
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        
        # Compter les actions
        action_count = request.env['syndicat.action'].search_count(domain)
        
        # Pagination
        pager = portal_pager(
            url="/my/actions",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=action_count,
            page=page,
            step=self._items_per_page
        )
        
        # Récupérer les actions
        actions = request.env['syndicat.action'].search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'actions': actions,
            'page_name': 'action',
            'archive_groups': self._get_archive_groups('syndicat.action', domain),
            'default_url': '/my/actions',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        
        return request.render("sama_syndicat.portal_my_actions", values)

    @http.route(['/my/action/<int:action_id>'], type='http', auth="user", website=True)
    def portal_my_action(self, action_id=None, access_token=None, **kw):
        """Détail d'une action"""
        try:
            action_sudo = self._document_check_access('syndicat.action', action_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        values = {
            'action': action_sudo,
            'page_name': 'action',
        }
        
        return request.render("sama_syndicat.portal_my_action", values)

    # === FORMATIONS ===
    
    @http.route(['/my/formations', '/my/formations/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_formations(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        """Page des formations de l'adhérent"""
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        
        if not partner.is_adherent_syndicat or not partner.adherent_syndicat_id:
            return request.render('sama_syndicat.portal_not_adherent')
        
        adherent = partner.adherent_syndicat_id
        
        # Domaine de base
        domain = [('participants_ids', 'in', [adherent.id])]
        
        # Filtres par date
        if date_begin and date_end:
            domain += [('date_debut', '>=', date_begin), ('date_debut', '<=', date_end)]
        
        # Options de tri
        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'date_debut desc'},
            'name': {'label': _('Nom'), 'order': 'name'},
            'status': {'label': _('Statut'), 'order': 'statut'},
        }
        
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        
        # Compter les formations
        formation_count = request.env['syndicat.formation'].search_count(domain)
        
        # Pagination
        pager = portal_pager(
            url="/my/formations",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=formation_count,
            page=page,
            step=self._items_per_page
        )
        
        # Récupérer les formations
        formations = request.env['syndicat.formation'].search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'formations': formations,
            'page_name': 'formation',
            'archive_groups': self._get_archive_groups('syndicat.formation', domain),
            'default_url': '/my/formations',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        
        return request.render("sama_syndicat.portal_my_formations", values)

    @http.route(['/my/formation/<int:formation_id>'], type='http', auth="user", website=True)
    def portal_my_formation(self, formation_id=None, access_token=None, **kw):
        """Détail d'une formation"""
        try:
            formation_sudo = self._document_check_access('syndicat.formation', formation_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        values = {
            'formation': formation_sudo,
            'page_name': 'formation',
        }
        
        return request.render("sama_syndicat.portal_my_formation", values)

    # === COTISATIONS ===
    
    @http.route(['/my/cotisations', '/my/cotisations/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_cotisations(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        """Page des cotisations de l'adhérent"""
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        
        if not partner.is_adherent_syndicat or not partner.adherent_syndicat_id:
            return request.render('sama_syndicat.portal_not_adherent')
        
        adherent = partner.adherent_syndicat_id
        
        # Domaine de base
        domain = [('adherent_id', '=', adherent.id)]
        
        # Filtres par date
        if date_begin and date_end:
            domain += [('date_echeance', '>=', date_begin), ('date_echeance', '<=', date_end)]
        
        # Options de tri
        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'annee desc, mois desc'},
            'status': {'label': _('Statut'), 'order': 'statut'},
            'amount': {'label': _('Montant'), 'order': 'montant desc'},
        }
        
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        
        # Compter les cotisations
        cotisation_count = request.env['syndicat.cotisation'].search_count(domain)
        
        # Pagination
        pager = portal_pager(
            url="/my/cotisations",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=cotisation_count,
            page=page,
            step=self._items_per_page
        )
        
        # Récupérer les cotisations
        cotisations = request.env['syndicat.cotisation'].search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'cotisations': cotisations,
            'page_name': 'cotisation',
            'archive_groups': self._get_archive_groups('syndicat.cotisation', domain),
            'default_url': '/my/cotisations',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'adherent': adherent,
        })
        
        return request.render("sama_syndicat.portal_my_cotisations", values)

    @http.route(['/my/cotisation/<int:cotisation_id>'], type='http', auth="user", website=True)
    def portal_my_cotisation(self, cotisation_id=None, access_token=None, **kw):
        """Détail d'une cotisation"""
        try:
            cotisation_sudo = self._document_check_access('syndicat.cotisation', cotisation_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        values = {
            'cotisation': cotisation_sudo,
            'page_name': 'cotisation',
        }
        
        return request.render("sama_syndicat.portal_my_cotisation", values)

    # === PROFIL ADHÉRENT ===
    
    @http.route(['/my/profil'], type='http', auth="user", website=True)
    def portal_my_profil(self, **kw):
        """Page de profil de l'adhérent"""
        partner = request.env.user.partner_id
        
        if not partner.is_adherent_syndicat or not partner.adherent_syndicat_id:
            return request.render('sama_syndicat.portal_not_adherent')
        
        adherent = partner.adherent_syndicat_id
        
        values = {
            'adherent': adherent,
            'partner': partner,
            'page_name': 'profil',
        }
        
        return request.render("sama_syndicat.portal_my_profil", values)

    @http.route(['/my/profil/update'], type='http', auth="user", website=True, methods=['POST'], csrf=False)
    def portal_my_profil_update(self, **post):
        """Mise à jour du profil adhérent"""
        partner = request.env.user.partner_id
        
        if not partner.is_adherent_syndicat or not partner.adherent_syndicat_id:
            return request.redirect('/my')
        
        adherent = partner.adherent_syndicat_id
        
        try:
            # Mise à jour des informations modifiables
            adherent_vals = {}
            partner_vals = {}
            
            if post.get('telephone'):
                adherent_vals['telephone'] = post.get('telephone')
                partner_vals['phone'] = post.get('telephone')
            
            if post.get('adresse'):
                adherent_vals['adresse'] = post.get('adresse')
                partner_vals['street'] = post.get('adresse')
            
            if post.get('ville'):
                adherent_vals['ville'] = post.get('ville')
                partner_vals['city'] = post.get('ville')
            
            if post.get('employeur'):
                adherent_vals['employeur'] = post.get('employeur')
            
            if post.get('poste_occupe'):
                adherent_vals['poste_occupe'] = post.get('poste_occupe')
                partner_vals['function'] = post.get('poste_occupe')
            
            # Mettre à jour
            if adherent_vals:
                adherent.sudo().write(adherent_vals)
            if partner_vals:
                partner.sudo().write(partner_vals)
            
            return request.redirect('/my/profil?message=success')
            
        except Exception as e:
            return request.redirect('/my/profil?message=error')

    # === COMMUNICATIONS ===
    
    @http.route(['/my/communications', '/my/communications/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_communications(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        """Page des communications pour l'adhérent"""
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        
        if not partner.is_adherent_syndicat or not partner.adherent_syndicat_id:
            return request.render('sama_syndicat.portal_not_adherent')
        
        adherent = partner.adherent_syndicat_id
        
        # Domaine de base - communications publiques ou destinées à l'adhérent
        domain = [
            ('statut', '=', 'publiee'),
            '|',
            ('canal_diffusion', 'in', ['public', 'mixte']),
            '|',
            ('destinataires_tous_adherents', '=', True),
            ('destinataires_adherents_ids', 'in', [adherent.id])
        ]
        
        # Filtres par date
        if date_begin and date_end:
            domain += [('date_publication', '>=', date_begin), ('date_publication', '<=', date_end)]
        
        # Options de tri
        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'date_publication desc'},
            'name': {'label': _('Titre'), 'order': 'name'},
            'type': {'label': _('Type'), 'order': 'type_communication'},
        }
        
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        
        # Compter les communications
        communication_count = request.env['syndicat.communication'].search_count(domain)
        
        # Pagination
        pager = portal_pager(
            url="/my/communications",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=communication_count,
            page=page,
            step=self._items_per_page
        )
        
        # Récupérer les communications
        communications = request.env['syndicat.communication'].search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'communications': communications,
            'page_name': 'communication',
            'archive_groups': self._get_archive_groups('syndicat.communication', domain),
            'default_url': '/my/communications',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        
        return request.render("sama_syndicat.portal_my_communications", values)

    @http.route(['/my/communication/<int:communication_id>'], type='http', auth="user", website=True)
    def portal_my_communication(self, communication_id=None, access_token=None, **kw):
        """Détail d'une communication"""
        try:
            communication_sudo = self._document_check_access('syndicat.communication', communication_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        # Incrémenter le nombre de lectures
        communication_sudo.action_incrementer_lectures()
        
        values = {
            'communication': communication_sudo,
            'page_name': 'communication',
        }
        
        return request.render("sama_syndicat.portal_my_communication", values)