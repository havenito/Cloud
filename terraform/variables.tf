variable "libvirt_uri" {
  description = "URI de connexion à l'hyperviseur KVM/libvirt"
  type        = string
  default     = "qemu:///system"
}

variable "pool_name" {
  description = "Nom du pool de stockage libvirt"
  type        = string
  default     = "cloud-pool"
}

variable "pool_path" {
  description = "Chemin disque du pool de stockage"
  type        = string
  default     = "/var/lib/libvirt/cloud-pool"
}

variable "base_image_url" {
  description = "Image cloud de base (Debian 12 generic cloud, qcow2)"
  type        = string
  default     = "https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-genericcloud-amd64.qcow2"
}

variable "ssh_public_key" {
  description = "Clé publique SSH injectée dans les VMs via cloud-init"
  type        = string
  # À renseigner dans terraform.tfvars, ex : file("~/.ssh/id_ed25519.pub")
}

variable "network_cidr" {
  description = "Réseau privé des VMs"
  type        = string
  default     = "10.10.0.0/24"
}

# Définition des 3 VMs : nom logique -> (ip, vcpu, ram en Mo)
variable "vms" {
  type = map(object({
    ip     = string
    vcpu   = number
    memory = number
  }))
  default = {
    reverse-proxy = { ip = "10.10.0.10", vcpu = 1, memory = 1024 }
    app           = { ip = "10.10.0.20", vcpu = 1, memory = 1536 }
    db            = { ip = "10.10.0.30", vcpu = 1, memory = 1536 }
  }
}
