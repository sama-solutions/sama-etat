# Dockerfile pour SAMA ÉTAT
# Basé sur Odoo 18.0 officiel avec optimisations pour la production

FROM odoo:18.0

# Métadonnées du conteneur
LABEL maintainer="Mamadou Mbagnick DOGUE, Rassol DOGUE"
LABEL description="SAMA ÉTAT - Plateforme citoyenne de gouvernance stratégique"
LABEL version="1.0.0"
LABEL org.opencontainers.image.source="https://github.com/loi200812/sama-etat"

# Variables d'environnement
ENV ODOO_VERSION=18.0
ENV SAMA_ETAT_VERSION=1.0.0
ENV PYTHONPATH="${PYTHONPATH}:/mnt/extra-addons"

# Passer en mode root pour les installations
USER root

# Mise à jour du système et installation des dépendances
RUN apt-get update && apt-get install -y \
    # Outils système
    curl \
    wget \
    git \
    vim \
    htop \
    # Dépendances pour les bibliothèques Python
    build-essential \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    # Outils de géolocalisation
    gdal-bin \
    libgdal-dev \
    # Nettoyage
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python spécifiques à SAMA ÉTAT
RUN pip3 install --no-cache-dir \
    qrcode[pil]==7.4.2 \
    pillow==10.0.1 \
    geopy==2.3.0 \
    folium==0.14.0 \
    requests==2.31.0 \
    python-dateutil==2.8.2

# Création des répertoires nécessaires
RUN mkdir -p \
    /mnt/extra-addons/sama_etat \
    /var/lib/odoo/filestore \
    /var/lib/odoo/sessions \
    /var/log/odoo \
    /etc/odoo \
    /opt/sama_etat

# Copie du module SAMA ÉTAT
COPY . /mnt/extra-addons/sama_etat/

# Copie des fichiers de configuration
COPY config/odoo.conf /etc/odoo/odoo.conf
COPY scripts/ /opt/sama_etat/scripts/

# Configuration des permissions
RUN chown -R odoo:odoo \
    /mnt/extra-addons/sama_etat \
    /var/lib/odoo \
    /var/log/odoo \
    /etc/odoo \
    /opt/sama_etat

# Retour à l'utilisateur odoo
USER odoo

# Création du script d'entrée personnalisé
COPY --chown=odoo:odoo scripts/entrypoint.sh /opt/sama_etat/entrypoint.sh
RUN chmod +x /opt/sama_etat/entrypoint.sh

# Variables d'environnement pour Odoo
ENV ODOO_RC=/etc/odoo/odoo.conf
ENV ODOO_ADDONS_PATH=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons

# Exposition des ports
EXPOSE 8069 8071

# Volumes pour la persistance des données
VOLUME ["/var/lib/odoo", "/var/log/odoo"]

# Point de santé pour Docker
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8069/web/health || exit 1

# Script d'entrée
ENTRYPOINT ["/opt/sama_etat/entrypoint.sh"]

# Commande par défaut
CMD ["odoo"]