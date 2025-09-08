#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test de l'API Odoo pour Sama Jokoo
==================================

Script de validation de la base technique :
- Connexion à Odoo
- Vérification des modèles
- Test des APIs de base
"""

import requests
import json
import sys

class OdooAPITester:
    def __init__(self, url='http://localhost:8070', db='sama_jokoo_dev'):
        self.url = url
        self.db = db
        self.session = requests.Session()
        self.uid = None
        
    def print_step(self, step, message):
        """Afficher une étape de test"""
        print(f"🔍 {step}: {message}")
        
    def print_success(self, message):
        """Afficher un succès"""
        print(f"✅ {message}")
        
    def print_error(self, message):
        """Afficher une erreur"""
        print(f"❌ {message}")
        
    def test_server_connection(self):
        """Tester la connexion au serveur Odoo"""
        self.print_step("1", "Test de connexion au serveur Odoo")
        
        try:
            response = self.session.get(f"{self.url}/web/database/selector")
            if response.status_code == 200:
                self.print_success("Serveur Odoo accessible")
                return True
            else:
                self.print_error(f"Serveur non accessible (code: {response.status_code})")
                return False
        except Exception as e:
            self.print_error(f"Erreur de connexion: {e}")
            return False
    
    def test_authentication(self, username='admin', password='admin'):
        """Tester l'authentification"""
        self.print_step("2", f"Test d'authentification (user: {username})")
        
        try:
            data = {
                'jsonrpc': '2.0',
                'method': 'call',
                'params': {
                    'service': 'common',
                    'method': 'authenticate',
                    'args': [self.db, username, password, {}]
                },
                'id': 1
            }
            
            response = self.session.post(
                f"{self.url}/jsonrpc",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(data)
            )
            
            result = response.json()
            if result.get('result'):
                self.uid = result['result']
                self.print_success(f"Authentification réussie (UID: {self.uid})")
                return True
            else:
                self.print_error(f"Échec authentification: {result.get('error', 'Erreur inconnue')}")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur authentification: {e}")
            return False
    
    def test_model_exists(self, model_name):
        """Tester l'existence d'un modèle"""
        try:
            data = {
                'jsonrpc': '2.0',
                'method': 'call',
                'params': {
                    'service': 'object',
                    'method': 'execute_kw',
                    'args': [
                        self.db, self.uid, 'admin',
                        'ir.model', 'search',
                        [[['model', '=', model_name]]]
                    ]
                },
                'id': 1
            }
            
            response = self.session.post(
                f"{self.url}/jsonrpc",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(data)
            )
            
            result = response.json()
            if result.get('result') and len(result['result']) > 0:
                self.print_success(f"Modèle '{model_name}' existe")
                return True
            else:
                self.print_error(f"Modèle '{model_name}' introuvable")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur test modèle {model_name}: {e}")
            return False
    
    def test_model_access(self, model_name):
        """Tester l'accès en lecture à un modèle"""
        try:
            data = {
                'jsonrpc': '2.0',
                'method': 'call',
                'params': {
                    'service': 'object',
                    'method': 'execute_kw',
                    'args': [
                        self.db, self.uid, 'admin',
                        model_name, 'search_read',
                        [[], ['id']]
                    ]
                },
                'id': 1
            }
            
            response = self.session.post(
                f"{self.url}/jsonrpc",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(data)
            )
            
            result = response.json()
            if 'result' in result:
                count = len(result['result']) if result['result'] else 0
                self.print_success(f"Accès lecture '{model_name}' OK ({count} enregistrements)")
                return True
            else:
                self.print_error(f"Erreur accès '{model_name}': {result.get('error', 'Erreur inconnue')}")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur accès modèle {model_name}: {e}")
            return False
    
    def test_create_post(self):
        """Tester la création d'un post"""
        self.print_step("6", "Test de création d'un post")
        
        try:
            data = {
                'jsonrpc': '2.0',
                'method': 'call',
                'params': {
                    'service': 'object',
                    'method': 'execute_kw',
                    'args': [
                        self.db, self.uid, 'admin',
                        'social.post', 'create',
                        [{
                            'content': 'Test post depuis l\'API - ' + str(self.uid),
                            'state': 'published'
                        }]
                    ]
                },
                'id': 1
            }
            
            response = self.session.post(
                f"{self.url}/jsonrpc",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(data)
            )
            
            result = response.json()
            if result.get('result'):
                post_id = result['result']
                self.print_success(f"Post créé avec succès (ID: {post_id})")
                return post_id
            else:
                self.print_error(f"Erreur création post: {result.get('error', 'Erreur inconnue')}")
                return False
                
        except Exception as e:
            self.print_error(f"Erreur création post: {e}")
            return False
    
    def run_full_test(self):
        """Exécuter tous les tests"""
        print("🚀 Test complet de l'API Odoo - Sama Jokoo")
        print("=" * 50)
        
        # Test 1: Connexion serveur
        if not self.test_server_connection():
            return False
        
        # Test 2: Authentification
        if not self.test_authentication():
            return False
        
        # Test 3: Vérification des modèles
        self.print_step("3", "Vérification des modèles Sama Jokoo")
        models_to_test = [
            'social.post',
            'social.comment', 
            'social.like',
            'social.follow',
            'social.notification',
            'social.media',
            'social.hashtag'
        ]
        
        models_ok = 0
        for model in models_to_test:
            if self.test_model_exists(model):
                models_ok += 1
        
        print(f"📊 Modèles validés: {models_ok}/{len(models_to_test)}")
        
        # Test 4: Accès aux modèles
        self.print_step("4", "Test d'accès aux modèles")
        access_ok = 0
        for model in models_to_test:
            if self.test_model_access(model):
                access_ok += 1
        
        print(f"📊 Accès validés: {access_ok}/{len(models_to_test)}")
        
        # Test 5: Création de données
        post_id = self.test_create_post()
        
        # Résumé
        print("\n" + "=" * 50)
        if models_ok == len(models_to_test) and access_ok == len(models_to_test) and post_id:
            self.print_success("🎉 TOUS LES TESTS PASSÉS ! API Odoo fonctionnelle")
            print(f"📱 Prêt pour le développement de l'application neumorphique")
            return True
        else:
            self.print_error("❌ Certains tests ont échoué")
            return False

def main():
    """Fonction principale"""
    tester = OdooAPITester()
    success = tester.run_full_test()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()