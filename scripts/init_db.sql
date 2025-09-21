-- Script d'initialisation de la base de données pour SAMA ÉTAT
-- Auteurs: Mamadou Mbagnick DOGUE, Rassol DOGUE

-- Création de la base de données SAMA ÉTAT si elle n'existe pas
SELECT 'CREATE DATABASE sama_etat'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'sama_etat')\gexec

-- Connexion à la base de données SAMA ÉTAT
\c sama_etat;

-- Activation des extensions nécessaires
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "unaccent";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Extension pour la géolocalisation (si disponible)
CREATE EXTENSION IF NOT EXISTS "postgis";

-- Création d'un utilisateur spécifique pour SAMA ÉTAT (optionnel)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'sama_etat_user') THEN
        CREATE ROLE sama_etat_user WITH LOGIN PASSWORD 'sama_etat_2024';
    END IF;
END
$$;

-- Octroi des permissions
GRANT ALL PRIVILEGES ON DATABASE sama_etat TO sama_etat_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sama_etat_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO sama_etat_user;

-- Configuration des paramètres de performance
ALTER DATABASE sama_etat SET shared_preload_libraries = 'pg_stat_statements';
ALTER DATABASE sama_etat SET log_statement = 'all';
ALTER DATABASE sama_etat SET log_min_duration_statement = 1000;

-- Index pour améliorer les performances des recherches textuelles
-- Ces index seront créés automatiquement par Odoo, mais on peut les préparer

-- Commentaires pour la documentation
COMMENT ON DATABASE sama_etat IS 'Base de données pour SAMA ÉTAT - Plateforme citoyenne de gouvernance stratégique';

-- Affichage des informations
SELECT 'Base de données SAMA ÉTAT initialisée avec succès' AS status;