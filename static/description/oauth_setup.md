# Configuration de l'authentification OAuth pour les fournisseurs d'IA

Ce document explique comment configurer l'authentification OAuth pour les fournisseurs d'IA (Google et Microsoft) dans le module Sama État.

## Prérequis

1. Module Sama État version 18.0.2.0.0 ou supérieure
2. Droits d'administration sur l'instance Odoo
3. Comptes développeur pour les fournisseurs d'IA (Google Cloud, Microsoft Azure)

## Configuration requise

### Paramètres système requis

Les paramètres système suivants doivent être configurés via **Paramètres techniques > Paramètres > Paramètres système** :

#### Pour Google (Gemini)
- `ai.google.client_id` : ID client OAuth 2.0 de Google Cloud
- `ai.google.client_secret` : Secret client OAuth 2.0 de Google Cloud

#### Pour Microsoft (Azure OpenAI)
- `ai.microsoft.client_id` : ID d'application (client) Azure AD
- `ai.microsoft.client_secret` : Clé secrète client Azure AD
- `ai.microsoft.tenant_id` : ID de locataire Azure AD (optionnel, utilise 'common' par défaut)

## Configuration des fournisseurs OAuth

### 1. Configuration de Google Cloud Platform

1. Allez sur la [Console Google Cloud](https://console.cloud.google.com/)
2. Créez un nouveau projet ou sélectionnez un projet existant
3. Activez l'API Google Gemini pour votre projet
4. Accédez à **APIs & Services > Identifiants**
5. Créez un nouvel **ID client OAuth 2.0**
   - Type d'application : Application Web
   - Nom : Sama État
   - URI de redirection autorisés : `https://votre-domaine.com/ai/oauth/google/callback`
6. Copiez l'ID client et le secret client dans les paramètres système Odoo

### 2. Configuration de Microsoft Azure AD

1. Connectez-vous au [Portail Azure](https://portal.azure.com/)
2. Allez dans **Azure Active Directory**
3. Sélectionnez **Inscriptions d'applications**
4. Cliquez sur **Nouvelle inscription**
   - Nom : Sama État
   - Types de comptes pris en charge : Comptes dans cet annuaire d'organisation uniquement
   - URI de redirection : Web, `https://votre-domaine.com/ai/oauth/microsoft/callback`
5. Une fois l'application créée, notez l'**ID d'application (client)**
6. Générez un nouveau secret client dans **Certificats & secrets**
7. Copiez l'ID client et le secret client dans les paramètres système Odoo
8. Allez dans **Autorisations des API** et ajoutez les autorisations nécessaires

## Configuration du module Sama État

1. Allez dans **Sama État > Configuration > Fournisseurs d'IA**
2. Créez un nouveau fournisseur ou modifiez un existant
3. Sélectionnez le type de fournisseur (Google ou Microsoft)
4. Choisissez "Authentification OAuth" comme méthode d'authentification
5. Enregistrez la configuration
6. Cliquez sur le bouton "Se connecter avec [Fournisseur]" pour lancer le flux OAuth

## Dépannage

### Erreurs courantes

1. **"Configuration manquante"** : Vérifiez que tous les paramètres système requis sont correctement configurés
2. **URI de redirection non autorisé** : Assurez-vous que l'URI de redirection dans la console du développeur correspond exactement à l'URL de votre instance Odoo
3. **Jetons expirés** : Les jetons d'accès expirent généralement après une heure. Le module tente de les rafraîchir automatiquement

### Journaux

Les erreurs OAuth sont enregistrées dans les journaux Odoo. Vous pouvez les consulter via **Paramètres techniques > Journalisation > Journaux du serveur**.

## Sécurité

- Les jetons OAuth sont stockés de manière sécurisée dans la base de données
- Les paramètres sensibles (clés secrètes) sont stockés sous forme chiffrée
- L'accès aux paramètres OAuth est restreint aux administrateurs système
