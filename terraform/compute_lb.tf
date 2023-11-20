resource "openstack_compute_instance_v2" "pystebin_lb" {
  name      = "pystebin-load-balancer"
  image_id  = data.openstack_images_image_v2.ubuntu_22_04.id
  flavor_id = data.openstack_compute_flavor_v2.m1_small.id

  key_pair = data.openstack_compute_keypair_v2.chramb_k1.name

  config_drive = true
  user_data = base64encode(
    templatefile(
      "${path.module}/templates/lb-user-data.tpl", {
        app_hosts = join(" ", [for i in range(0, length(openstack_compute_instance_v2.pystebin_app)) : "${openstack_compute_instance_v2.pystebin_app[i].access_ip_v4}:${var.app_port}"])
      }
    )
  )

  network {
    port = openstack_networking_port_v2.lb2provider.id
  }
  network {
    port = openstack_networking_port_v2.lb2int.id
  }

}

resource "openstack_networking_port_v2" "lb2provider" {
  name                  = "lb-provider"
  network_id            = data.openstack_networking_network_v2.public.id
  port_security_enabled = false
  fixed_ip {
    ip_address = "10.20.0.4"
    subnet_id  = data.openstack_networking_subnet_v2.public_subnet.id
  }
}

resource "openstack_networking_port_v2" "lb2int" {
  name       = "lb-internal"
  network_id = openstack_networking_network_v2.pystebin_internal.id
  fixed_ip {
    ip_address = "192.168.199.10"
    subnet_id  = openstack_networking_subnet_v2.pystebin_internal_sub.id
  }
}

