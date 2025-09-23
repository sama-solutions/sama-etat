#!/bin/bash

# Test de connectivité pour SAMA SYNDICAT

echo "🔍 SAMA SYNDICAT - TEST DE CONNECTIVITÉ"
echo "======================================"

# Configuration
ODOO_PATH="/var/odoo/odoo18"
VENV_PATH="/home/grand-as/odoo18-venv"
ADDONS_PATH="/home/grand-as/psagsn/custom_addons"
DB_USER="odoo"
DB_PASSWORD="odoo"

echo "🔧 Test 1: Environnement virtuel"
if [ -d "$VENV_PATH" ]; then
    echo "✅ Environnement virtuel trouvé: $VENV_PATH"
    source $VENV_PATH/bin/activate
    echo "✅ Environnement activé"
else
    echo "❌ Environnement virtuel non trouvé: $VENV_PATH"
fi

echo ""
echo "🔧 Test 2: Odoo"
if [ -d "$ODOO_PATH" ]; then
    echo "✅ Odoo trouvé: $ODOO_PATH"
    if [ -f "$ODOO_PATH/odoo-bin" ]; then
        echo "✅ odoo-bin trouvé"
    else
        echo "❌ odoo-bin non trouvé"
    fi
else
    echo "❌ Odoo non trouvé: $ODOO_PATH"
fi

echo ""
echo "🔧 Test 3: Addons"
if [ -d "$ADDONS_PATH" ]; then
    echo "✅ Répertoire addons trouvé: $ADDONS_PATH"
    if [ -d "$ADDONS_PATH/sama_syndicat" ]; then
        echo "✅ Module sama_syndicat trouvé"
    else
        echo "❌ Module sama_syndicat non trouvé"
    fi
else
    echo "❌ Répertoire addons non trouvé: $ADDONS_PATH"
fi

echo ""
echo "🔧 Test 4: PostgreSQL"
if command -v psql >/dev/null 2>&1; then
    echo "✅ psql trouvé"
    
    # Test de connexion avec PGPASSWORD
    export PGPASSWORD=$DB_PASSWORD
    
    if psql -U $DB_USER -d postgres -c "SELECT version();" >/dev/null 2>&1; then
        echo "✅ Connexion PostgreSQL réussie"
        
        # Lister les bases existantes
        echo "📊 Bases de données existantes:"
        psql -U $DB_USER -d postgres -c "SELECT datname FROM pg_database WHERE datname LIKE '%sama%';" 2>/dev/null
        
    else
        echo "❌ Échec de connexion PostgreSQL"
        echo "🔧 Tentative avec authentification locale..."
        
        # Essayer sans mot de passe (auth locale)
        if sudo -u postgres psql -c "SELECT version();" >/dev/null 2>&1; then
            echo "✅ Connexion PostgreSQL en tant que postgres"
            
            # Vérifier l'utilisateur odoo
            if sudo -u postgres psql -c "SELECT usename FROM pg_user WHERE usename='odoo';" | grep -q odoo; then
                echo "✅ Utilisateur odoo existe"
            else
                echo "❌ Utilisateur odoo n'existe pas"
                echo "🔧 Création de l'utilisateur odoo..."
                sudo -u postgres createuser -s odoo 2>/dev/null || echo "⚠️  Utilisateur existe déjà ou erreur"
                sudo -u postgres psql -c "ALTER USER odoo PASSWORD 'odoo';" 2>/dev/null
            fi
        else
            echo "❌ Impossible de se connecter à PostgreSQL"
        fi
    fi
    
    unset PGPASSWORD
else
    echo "❌ psql non trouvé"
fi

echo ""
echo "🔧 Test 5: Python et modules"
if command -v python3 >/dev/null 2>&1; then
    echo "✅ Python3 trouvé: $(python3 --version)"
    
    # Test des modules Python essentiels
    python3 -c "import psycopg2; print('✅ psycopg2 OK')" 2>/dev/null || echo "❌ psycopg2 manquant"
    python3 -c "import lxml; print('✅ lxml OK')" 2>/dev/null || echo "❌ lxml manquant"
    python3 -c "import werkzeug; print('✅ werkzeug OK')" 2>/dev/null || echo "❌ werkzeug manquant"
else
    echo "❌ Python3 non trouvé"
fi

echo ""
echo "🔧 Test 6: Ports"
if command -v netstat >/dev/null 2>&1; then
    echo "📊 Ports en écoute (80xx):"
    netstat -tlnp 2>/dev/null | grep ":80" | head -5
else
    echo "⚠️  netstat non disponible"
fi

echo ""
echo "📋 RÉSUMÉ DES TESTS"
echo "=================="
echo "✅ Tests réussis permettent l'installation"
echo "❌ Tests échoués nécessitent une correction"