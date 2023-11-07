variable "user_data" {
  type    = string
  default = <<EOT
    #cloud-config
    users:
      - name: chris
        passwd: "$6$t1xzt8V2GbYHY/Y4$tPbebuySTJYAuzAErmfo2i.RW2dY1S5MyIaMPkVSDQdVFTRhFCn.nb2vWZIfRoCHptGFxmB2nLg0VDgde3Fgs1"
        lock_passwd: false
        gecos: Cool Guy
        groups: wheel, sudo
        sudo: ALL=(ALL) NOPASSWD:ALL
        shell: /bin/bash
        ssh_authorized_keys:
          - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFg0Uu76IkZwyU3sjOaxwo4dSPtFWPogEQYM+7ypLBkY chris@Gentoo

    EOT
}
