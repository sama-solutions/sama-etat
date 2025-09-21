# Guide de Contribution | Contributing Guide

<div align="center">
  <img src="logo.png" alt="SAMA ÉTAT Logo" width="150"/>
  
  **Merci de votre intérêt pour contribuer à SAMA ÉTAT !**
  
  *Thank you for your interest in contributing to SAMA ÉTAT!*
</div>

---

## 🌍 Français

### 🤝 Comment Contribuer

Nous accueillons chaleureusement toutes les contributions qui peuvent améliorer SAMA ÉTAT. Voici comment vous pouvez participer :

#### 🐛 Signaler des Bugs
1. Vérifiez d'abord si le bug n'a pas déjà été signalé dans les [Issues](https://github.com/loi200812/sama-etat/issues)
2. Créez une nouvelle issue avec le template "Bug Report"
3. Décrivez le problème de manière détaillée
4. Incluez les étapes pour reproduire le bug
5. Ajoutez des captures d'écran si nécessaire

#### ✨ Proposer des Fonctionnalités
1. Consultez la [roadmap du projet](https://github.com/loi200812/sama-etat/projects)
2. Créez une issue avec le template "Feature Request"
3. Expliquez clairement la fonctionnalité proposée
4. Justifiez pourquoi cette fonctionnalité serait utile
5. Proposez une implémentation si possible

#### 🔧 Contribuer au Code
1. **Fork** le repository
2. **Clonez** votre fork localement
3. **Créez** une branche pour votre fonctionnalité
4. **Développez** en suivant nos standards
5. **Testez** vos modifications
6. **Commitez** avec des messages clairs
7. **Poussez** vers votre fork
8. **Créez** une Pull Request

### 📋 Standards de Code

#### Python
- Suivre les conventions **PEP 8**
- Utiliser des docstrings pour toutes les fonctions et classes
- Limiter les lignes à 88 caractères (Black formatter)
- Utiliser des noms de variables explicites

#### JavaScript
- Suivre les standards **ES6+**
- Utiliser **JSDoc** pour la documentation
- Préférer `const` et `let` à `var`
- Utiliser des noms de fonctions descriptifs

#### XML/HTML
- Indentation de 4 espaces
- Fermer toutes les balises
- Utiliser des attributs en minuscules
- Commenter les sections complexes

### 🧪 Tests

#### Tests Unitaires
```bash
# Lancer les tests Python
python -m pytest tests/

# Lancer les tests JavaScript
npm test
```

#### Tests d'Intégration
```bash
# Tests Odoo
odoo-bin -d test_db -i sama_etat --test-enable --stop-after-init
```

### 📝 Documentation

- Documenter toutes les nouvelles fonctionnalités
- Mettre à jour le README si nécessaire
- Ajouter des exemples d'utilisation
- Traduire en français et anglais

### 🔄 Processus de Review

1. **Vérification automatique** : CI/CD checks
2. **Review par les mainteneurs** : Code quality, architecture
3. **Tests** : Fonctionnalité et non-régression
4. **Approbation** : Merge après validation

---

## 🌍 English

### 🤝 How to Contribute

We warmly welcome all contributions that can improve SAMA ÉTAT. Here's how you can participate:

#### 🐛 Reporting Bugs
1. First check if the bug hasn't already been reported in [Issues](https://github.com/loi200812/sama-etat/issues)
2. Create a new issue with the "Bug Report" template
3. Describe the problem in detail
4. Include steps to reproduce the bug
5. Add screenshots if necessary

#### ✨ Proposing Features
1. Check the [project roadmap](https://github.com/loi200812/sama-etat/projects)
2. Create an issue with the "Feature Request" template
3. Clearly explain the proposed feature
4. Justify why this feature would be useful
5. Propose an implementation if possible

#### 🔧 Contributing Code
1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a branch for your feature
4. **Develop** following our standards
5. **Test** your changes
6. **Commit** with clear messages
7. **Push** to your fork
8. **Create** a Pull Request

### 📋 Code Standards

#### Python
- Follow **PEP 8** conventions
- Use docstrings for all functions and classes
- Limit lines to 88 characters (Black formatter)
- Use explicit variable names

#### JavaScript
- Follow **ES6+** standards
- Use **JSDoc** for documentation
- Prefer `const` and `let` over `var`
- Use descriptive function names

#### XML/HTML
- 4-space indentation
- Close all tags
- Use lowercase attributes
- Comment complex sections

### 🧪 Testing

#### Unit Tests
```bash
# Run Python tests
python -m pytest tests/

# Run JavaScript tests
npm test
```

#### Integration Tests
```bash
# Odoo tests
odoo-bin -d test_db -i sama_etat --test-enable --stop-after-init
```

### 📝 Documentation

- Document all new features
- Update README if necessary
- Add usage examples
- Translate to French and English

### 🔄 Review Process

1. **Automatic verification**: CI/CD checks
2. **Maintainer review**: Code quality, architecture
3. **Testing**: Functionality and non-regression
4. **Approval**: Merge after validation

---

## 🏷️ Types de Contributions | Contribution Types

### 🐛 Bug Fixes
- Correction de bugs critiques
- Amélioration de la stabilité
- Optimisation des performances

### ✨ Nouvelles Fonctionnalités | New Features
- Modules additionnels
- Intégrations externes
- Améliorations UX/UI

### 📚 Documentation
- Guides utilisateur
- Documentation technique
- Traductions

### 🧪 Tests
- Tests unitaires
- Tests d'intégration
- Tests de performance

---

## 🎯 Priorités de Développement | Development Priorities

### 🔥 Haute Priorité | High Priority
1. Sécurité et authentification
2. Performance et optimisation
3. Accessibilité et responsive design
4. Intégration API gouvernementales

### 📈 Moyenne Priorité | Medium Priority
1. Nouvelles fonctionnalités utilisateur
2. Améliorations UX/UI
3. Outils d'administration
4. Rapports et analytics

### 💡 Basse Priorité | Low Priority
1. Fonctionnalités expérimentales
2. Intégrations tierces
3. Optimisations mineures
4. Refactoring non-critique

---

## 👥 Équipe et Rôles | Team & Roles

### 🏗️ Core Maintainers
- **Mamadou Mbagnick DOGUE** - Architecte Principal
- **Rassol DOGUE** - Développeur Senior

### 🤝 Contributors
- Développeurs communautaires
- Testeurs et QA
- Rédacteurs de documentation
- Traducteurs

### 📞 Contact
- **GitHub Issues** : Questions techniques
- **Email** : contact@sama-etat.sn
- **Discussions** : [GitHub Discussions](https://github.com/loi200812/sama-etat/discussions)

---

## 📜 Code de Conduite | Code of Conduct

### 🤝 Notre Engagement | Our Pledge

Nous nous engageons à faire de la participation à notre projet une expérience sans harcèlement pour tous, quel que soit l'âge, la taille corporelle, le handicap visible ou invisible, l'origine ethnique, les caractéristiques sexuelles, l'identité et l'expression de genre, le niveau d'expérience, l'éducation, le statut socio-économique, la nationalité, l'apparence personnelle, la race, la religion ou l'identité et l'orientation sexuelles.

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### ✅ Comportements Encouragés | Encouraged Behaviors

- Utiliser un langage accueillant et inclusif
- Respecter les différents points de vue et expériences
- Accepter gracieusement les critiques constructives
- Se concentrer sur ce qui est le mieux pour la communauté
- Faire preuve d'empathie envers les autres membres

### ❌ Comportements Inacceptables | Unacceptable Behaviors

- Langage ou imagerie sexualisés et attention sexuelle non désirée
- Trolling, commentaires insultants/désobligeants et attaques personnelles
- Harcèlement public ou privé
- Publication d'informations privées sans permission explicite
- Autres conduites qui pourraient raisonnablement être considérées comme inappropriées

---

## 🏆 Reconnaissance | Recognition

### 🌟 Hall of Fame
Les contributeurs exceptionnels seront reconnus dans notre Hall of Fame avec :
- Mention dans le README principal
- Badge de contributeur spécial
- Invitation aux événements communautaires

### 🎁 Récompenses | Rewards
- Stickers et goodies SAMA ÉTAT
- Certificats de contribution
- Recommandations LinkedIn

---

<div align="center">
  
  **🇸🇳 Ensemble, construisons l'avenir numérique du Sénégal ! 🇸🇳**
  
  *Together, let's build Senegal's digital future!*
  
  ⭐ **Merci de contribuer à SAMA ÉTAT !** | **Thank you for contributing to SAMA ÉTAT!** ⭐
  
</div>