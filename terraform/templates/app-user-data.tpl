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
    docker.list:
      source: deb [arch=amd64] https://download.docker.com/linux/ubuntu $RELEASE stable
      keyid: 9DC858229FC7DD38854AE2D88D81803C0EBFCD88

# Install packages
packages:
  - tmux
  - mosh
  - docker-ce
  - docker-ce-cli


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

write_files:
  - path: /etc/systemd/system/pystebin.service
    permissions: '0640'
    content: |
      [Unit]
      Description=pystebin container
      After=docker.service
      Wants=network-online.target docker.socket
      Requires=docker.socket

      [Service]
      Restart=always
      ExecStartPre=/bin/bash -c "/usr/bin/docker container inspect pystebin 2> /dev/null || /usr/bin/docker run -d --name pystebin --net host -v /etc/pystebin.toml:/etc/pystebin.toml:ro ghcr.io/pwr-pro/pystebin${container_tag}"
      ExecStart=/usr/bin/docker start -a pystebin
      ExecStop=/usr/bin/docker stop -t 10 pystebin

      [Install]
      WantedBy=multi-user.target

  - path: /etc/pystebin.toml
    permission: '0600'
    content: |
      [app]
      host = "${app_host}"
      port = ${app_port}

      [auth]
      secret = "${app_auth_secret}"
      algorithm = "${app_auth_algorithm}"

      [github]
      client_id = "${github_client_id}"
      client_secret = "${github_client_secret}"

      [database]
      host = "${database_host}"
      database = "${database_name}"
      user = "${database_user}"
      password = "${database_password}"
      port = 5432

runcmd:
  - mkdir /postgres
  - systemctl daemon-reload
  - systemctl enable --now pystebin.service