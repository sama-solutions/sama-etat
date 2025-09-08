#!/bin/bash

# Script de démarrage pour le développement mobile Sama Jokoo
# ===========================================================

# Configuration
MOBILE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_URL="http://localhost:8070"  # Port de développement

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_info "=== Démarrage du développement mobile Sama Jokoo ==="

# Vérifier si Flutter est installé
if ! command -v flutter &> /dev/null; then
    log_error "Flutter n'est pas installé. Veuillez installer Flutter d'abord."
    log_info "Visitez: https://flutter.dev/docs/get-started/install"
    exit 1
fi

# Vérifier si le backend Odoo est accessible
log_info "Vérification de la connexion au backend..."
if curl -s "$BACKEND_URL" > /dev/null; then
    log_success "Backend Odoo accessible sur $BACKEND_URL"
else
    log_warning "Backend Odoo non accessible sur $BACKEND_URL"
    log_info "Assurez-vous que le backend est démarré avec: ../dev_scripts/start_dev.sh"
fi

# Créer la structure de base de l'application Flutter
create_flutter_structure() {
    log_info "Création de la structure Flutter..."
    
    if [ ! -f "$MOBILE_PATH/pubspec.yaml" ]; then
        log_info "Initialisation du projet Flutter..."
        
        cd "$MOBILE_PATH"
        flutter create . --project-name sama_jokoo_mobile --org com.samajokoo.app
        
        # Créer la structure personnalisée
        mkdir -p lib/{config,models,services,screens,widgets,utils}
        mkdir -p assets/{images,icons}
        
        log_success "Structure Flutter créée"
    else
        log_info "Projet Flutter déjà initialisé"
    fi
}

# Créer le fichier de configuration
create_config() {
    log_info "Création de la configuration..."
    
    cat > "$MOBILE_PATH/lib/config/app_config.dart" << EOF
class AppConfig {
  // Configuration du backend Odoo
  static const String baseUrl = '$BACKEND_URL';
  static const String apiPath = '/api/social';
  
  // Configuration de l'application
  static const String appName = 'Sama Jokoo';
  static const String appVersion = '1.0.0';
  
  // Endpoints API
  static const String authEndpoint = '\$apiPath/auth';
  static const String postsEndpoint = '\$apiPath/posts';
  static const String usersEndpoint = '\$apiPath/users';
  static const String notificationsEndpoint = '\$apiPath/notifications';
  
  // Configuration UI
  static const int postsPerPage = 20;
  static const int maxImageSize = 5 * 1024 * 1024; // 5MB
  
  // Thèmes
  static const bool enableDarkMode = true;
  static const bool enableAutoTheme = true;
}
EOF
    
    log_success "Configuration créée"
}

# Mettre à jour pubspec.yaml avec les dépendances nécessaires
update_pubspec() {
    log_info "Mise à jour des dépendances..."
    
    cat > "$MOBILE_PATH/pubspec.yaml" << EOF
name: sama_jokoo_mobile
description: Application mobile pour Sama Jokoo - Réseau social intégré à Odoo

publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'
  flutter: ">=3.10.0"

dependencies:
  flutter:
    sdk: flutter
  
  # UI & Navigation
  cupertino_icons: ^1.0.2
  flutter_bloc: ^8.1.3
  go_router: ^12.1.1
  
  # Networking
  http: ^1.1.0
  dio: ^5.3.2
  
  # State Management
  equatable: ^2.0.5
  
  # Storage
  shared_preferences: ^2.2.2
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  
  # Images & Media
  cached_network_image: ^3.3.0
  image_picker: ^1.0.4
  photo_view: ^0.14.0
  
  # Utils
  intl: ^0.18.1
  timeago: ^3.6.0
  url_launcher: ^6.2.1
  
  # Notifications
  flutter_local_notifications: ^16.3.0
  
  # Social Features
  share_plus: ^7.2.1
  
dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
  hive_generator: ^2.0.1
  build_runner: ^2.4.7

flutter:
  uses-material-design: true
  
  assets:
    - assets/images/
    - assets/icons/
  
  fonts:
    - family: SamaJokoo
      fonts:
        - asset: assets/fonts/Roboto-Regular.ttf
        - asset: assets/fonts/Roboto-Bold.ttf
          weight: 700
EOF
    
    log_success "Dépendances mises à jour"
}

# Créer l'application de base
create_main_app() {
    log_info "Création de l'application principale..."
    
    cat > "$MOBILE_PATH/lib/main.dart" << EOF
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'config/app_config.dart';

void main() {
  runApp(const SamaJokooApp());
}

class SamaJokooApp extends StatelessWidget {
  const SamaJokooApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: AppConfig.appName,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      darkTheme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blue,
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      themeMode: ThemeMode.system,
      home: const SplashScreen(),
    );
  }
}

class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.people,
              size: 100,
              color: Colors.blue,
            ),
            const SizedBox(height: 20),
            Text(
              AppConfig.appName,
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: 10),
            Text(
              'Version \${AppConfig.appVersion}',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: 40),
            const CircularProgressIndicator(),
            const SizedBox(height: 20),
            Text(
              'Connexion au backend...',
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const SizedBox(height: 10),
            Text(
              AppConfig.baseUrl,
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                color: Colors.grey,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
EOF
    
    log_success "Application principale créée"
}

# Installer les dépendances
install_dependencies() {
    log_info "Installation des dépendances Flutter..."
    
    cd "$MOBILE_PATH"
    flutter pub get
    
    if [ $? -eq 0 ]; then
        log_success "Dépendances installées avec succès"
    else
        log_error "Erreur lors de l'installation des dépendances"
        exit 1
    fi
}

# Démarrer l'application en mode développement
start_development() {
    log_info "Démarrage de l'application en mode développement..."
    
    cd "$MOBILE_PATH"
    
    # Vérifier les appareils disponibles
    flutter devices
    
    log_info "Démarrage de l'application..."
    log_info "Utilisez Ctrl+C pour arrêter"
    
    # Démarrer en mode hot reload
    flutter run --debug
}

# Exécution principale
log_info "Initialisation du développement mobile..."

create_flutter_structure
create_config
update_pubspec
create_main_app
install_dependencies

log_success "=== Environnement mobile prêt ==="
log_info "Backend: $BACKEND_URL"
log_info "Dossier: $MOBILE_PATH"

# Demander si on veut démarrer l'application
read -p "Voulez-vous démarrer l'application maintenant? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    start_development
else
    log_info "Pour démarrer l'application plus tard, utilisez:"
    log_info "cd $MOBILE_PATH && flutter run"
fi