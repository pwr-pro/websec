data "openstack_images_image_v2" "ubuntu_22_04" {
  name = "ubuntu-22.04"
}

data "openstack_compute_keypair_v2" "chramb_k1" {
  name = "key1"
}

data "openstack_compute_flavor_v2" "m1_medium" {
  name = "m1.medium"
}


resource "openstack_compute_instance_v2" "pystebin_app" {
  count = 2

  name      = "pystebin-app-${count.index}"
  image_id  = data.openstack_images_image_v2.ubuntu_22_04.id
  flavor_id = data.openstack_compute_flavor_v2.m1_medium.id
  security_groups = [
    "default",
  ]
  key_pair  = data.openstack_compute_keypair_v2.chramb_k1.name
  user_data = var.user_data

  network {
    name = openstack_networking_network_v2.pystebin_internal.name
  }

  network {
    name = openstack_networking_network_v2.pystebin_db.name
  }

}


resource "openstack_compute_instance_v2" "pystebin_db" {
  name      = "pystebin-db"
  image_id  = data.openstack_images_image_v2.ubuntu_22_04.id
  flavor_id = data.openstack_compute_flavor_v2.m1_medium.id
  security_groups = [
    "default",
  ]
  key_pair  = data.openstack_compute_keypair_v2.chramb_k1.name
  user_data = var.user_data

  network {
    name = openstack_networking_network_v2.pystebin_db.name
  }
}
