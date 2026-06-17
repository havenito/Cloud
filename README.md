# Projet Cloud Computing – Déploiement automatisé d'une appli web conteneurisée
 
Module 3CLOU – École Hexagone. Déploiement d'une application web (Flask + PostgreSQL)
sur 3 VMs KVM/libvirt, provisionnées par Terraform et configurées par Ansible,
chaque service tournant dans un conteneur Docker derrière un reverse proxy NGINX.
 
## Architecture
 
| VM            | Rôle                | IP          |
|---------------|---------------------|-------------|
| reverse-proxy | NGINX (80/443)      | 10.10.0.10  |
| app           | Flask + Gunicorn    | 10.10.0.20  |
| db            | PostgreSQL 16       | 10.10.0.30  |
 
Schéma complet : `schema/architecture.png`
 
## Déploiement
 
```bash
# 1. Infrastructure
cd terraform/
cp terraform.tfvars.example terraform.tfvars   # mettre sa clé SSH publique
terraform init && terraform apply
 
# 2. Configuration + déploiement des conteneurs
cd ../ansible/
ansible-playbook site.yml
 
# 3. Accès : https://10.10.0.10/  (certificat auto-signé)
```
 
## Arborescence
 
- `terraform/` – IaC (VMs, réseau NAT, cloud-init)
- `ansible/`   – provisioning, 4 rôles (common, database, app, reverse_proxy)
- `local-test/`- Conf NGINX simplifiée pour le test local
- `app/`       – application Flask + Dockerfile
- `schema/`    – schéma d'architecture (SVG + PNG)
- `rapport/`   – rapport (source Markdown + PDF)