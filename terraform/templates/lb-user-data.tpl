#cloud-config

growpart:
  mode: auto
  devices: ['/']

keyboard:
  layout: pl
  variant: pl

# Update and upgrade (skip because takest too long during tests)
# package_update: true
# package_upgrade: true
# package_reboot_if_required: true

apt:
  sources:
    caddy-stable.list:
      source: deb https://dl.cloudsmith.io/public/caddy/stable/deb/debian any-version main
      keyid: 65760C51EDEA2017CEA2CA15155B6D79CA56EA34

# Install packages
packages: 
  - tmux
  - caddy


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
      - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICJj6XDn+eDD02i9wC/tQF3WsEMPf2nQsbPoKAFuWVJS
      - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFg0Uu76IkZwyU3sjOaxwo4dSPtFWPogEQYM+7ypLBkY chris@Gentoo

# Configure Netplan
write_files:
#  - path: /etc/cloud/cloud.cfg.d/99-custom-networking.cfg
#    permissions: '0644'
#    content: |
#      network: {config: disabled}
#
#  - path: /etc/netplan/60-config.yaml
#    permissions: '0644'
#    content: |
#      network:
#          version: 2
#          ethernets:
#              ens3:
#                dhcp4: true
#              ens4:
#                addresses: [192.168.199.10/24]
#                dhcp4: false
#

  - path: /etc/caddy/Caddyfile
    permission: '0600'
    content: |
      pystebin.duckdns.org {
        header { 
          # keep referrer data off of HTTP connections 
          Referrer-Policy no-referrer-when-downgrade 
          # Referrer-Policy "strict-origin-when-cross-origin" 
          #CSP - Allow content only from a trusted domain and all its subdomains; Block all scripts
          Content-Security-Policy "default-src 'self' pystebin.duckdns.org; script-src 'none'; style-src 'self' cdn.jsdelivr.net;"
          # enable HSTS 
          Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" 
          # Enable cross-site filter (XSS) and tell browser to block detected attacks 
          X-Xss-Protection "1; mode=block" 
          # disable clients from sniffing the media type 
          X-Content-Type-Options "nosniff" 
          # clickjacking protection 
          X-Frame-Options "DENY" Content-Security-Policy "upgrade-insecure-requests" 
        }
                  
        reverse_proxy ${app_hosts}
      }



runcmd:
#  - rm /etc/netplan/50-cloud-init.yaml
#  - netplan generate
#  - netplan apply
  - systemctl enable --now caddy
