resource "openstack_compute_instance_v2" "pystebin_db" {
  name      = "pystebin-database"
  image_id  = data.openstack_images_image_v2.ubuntu_22_04.id
  flavor_id = data.openstack_compute_flavor_v2.m1_small.id

  key_pair = data.openstack_compute_keypair_v2.chramb_k1.name

  user_data = base64encode(
    templatefile(
      "${path.module}/templates/db-user-data.tpl", {
        database_name     = var.database_name,
        database_user     = var.database_user,
        database_password = var.database_password
      }
    )
  )

  network {
    name = openstack_networking_network_v2.pystebin_internal.name
  }
}

