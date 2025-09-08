#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test API rapide pour Sama Jokoo
===============================
"""

import requests
import json
import time

def quick_test():
    """Test rapide de l'API"""
    print("🚀 Test API rapide - Sama Jokoo")
    print("=" * 40)
    
    url = 'http://localhost:8070'
    
    try:
        # Test connexion
        print("🔍 Test connexion...")
        response = requests.get(f"{url}/web/database/selector", timeout=5)
        if response.status_code == 200:
            print("✅ Serveur accessible")
        else:
            print(f"❌ Serveur non accessible (code: {response.status_code})")
            return False
            
        # Test authentification
        print("🔍 Test authentification...")
        auth_data = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'service': 'common',
                'method': 'authenticate',
                'args': ['sama_jokoo_dev', 'admin', 'admin', {}]
            },
            'id': 1
        }
        
        response = requests.post(
            f"{url}/jsonrpc",
            headers={'Content-Type': 'application/json'},
            data=json.dumps(auth_data),
            timeout=5
        )
        
        result = response.json()
        if result.get('result'):
            uid = result['result']
            print(f"✅ Authentification OK (UID: {uid})")
        else:
            print("❌ Échec authentification")
            return False
            
        # Test modèle social.post
        print("🔍 Test modèle social.post...")
        model_data = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'service': 'object',
                'method': 'execute_kw',
                'args': [
                    'sama_jokoo_dev', uid, 'admin',
                    'social.post', 'search_read',
                    [[], ['id', 'content']]
                ]
            },
            'id': 1
        }
        
        response = requests.post(
            f"{url}/jsonrpc",
            headers={'Content-Type': 'application/json'},
            data=json.dumps(model_data),
            timeout=5
        )
        
        result = response.json()
        if 'result' in result:
            posts = result['result']
            print(f"✅ Modèle social.post accessible ({len(posts)} posts)")
            
            # Test création d'un post
            print("🔍 Test création post...")
            create_data = {
                'jsonrpc': '2.0',
                'method': 'call',
                'params': {
                    'service': 'object',
                    'method': 'execute_kw',
                    'args': [
                        'sama_jokoo_dev', uid, 'admin',
                        'social.post', 'create',
                        [{'content': f'Test post API - {int(time.time())}'}]
                    ]
                },
                'id': 1
            }
            
            response = requests.post(
                f"{url}/jsonrpc",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(create_data),
                timeout=5
            )
            
            result = response.json()
            if result.get('result'):
                post_id = result['result']
                print(f"✅ Post créé avec succès (ID: {post_id})")
                print("🎉 TOUS LES TESTS PASSÉS !")
                return True
            else:
                print(f"❌ Erreur création post: {result}")
                return False
        else:
            print(f"❌ Erreur accès modèle: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == '__main__':
    quick_test()