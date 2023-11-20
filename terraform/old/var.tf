variable "user_data" {
  type    = string
  default = <<EOT
      growpart:
    mode: auto
    devices: ['/']

  keyboard:
    layout: pl
    variant: pl

  # Update and upgrade (skip because takest too long during tests)
  package_update: true
  package_upgrade: true
  package_reboot_if_required: true

  # Install packages
  packages: ['tmux','mosh']


  # Configure user
  users:
    - name: chris
      passwd: '$6$pI83rW7KowwUSyh/$/DClOo5SWl3UfA3dW5cdBu2nsU66lFheJ6/ajyozFpLvXR7Yk2Nw/QvaI9iB/AePS5kbxYGROrc9QA6CpEOib/'
      lock_passwd: false
      gecos: Cool Guy
      groups: wheel, sudo
      sudo: ALL=(ALL) NOPASSWD:ALL
      shell: /bin/bash
      ssh_authorized_keys:
        - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICJj6XDn+eDD02i9wC/tQF3WsEMPf2nQsbPoKAFuWVJS kambrozy@mirantis.com
        - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFg0Uu76IkZwyU3sjOaxwo4dSPtFWPogEQYM+7ypLBkY chris@Gentoo

  write_files:
    - path: /etc/netplan/99-custom-networking.yaml
      permissions: '0640'
      content: |
        network:
          version: 2
          ethernets:
            ens3:
              dhcp4: true

    EOT
}
