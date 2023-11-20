resource "openstack_compute_instance_v2" "pystebin_app" {
  count = 1

  name      = "pystebin-app-${count.index}"
  image_id  = data.openstack_images_image_v2.ubuntu_22_04.id
  flavor_id = data.openstack_compute_flavor_v2.m1_small.id
  security_groups = [
    "default",
  ]
  key_pair = data.openstack_compute_keypair_v2.chramb_k1.name
  user_data = base64encode(
    templatefile(
      "${path.module}/templates/app-user-data.tpl", {

        container_tag = var.container_tag,

        app_host           = var.app_host,
        app_port           = var.app_port,
        app_auth_secret    = var.app_auth_secret,
        app_auth_algorithm = var.app_auth_algorithm,

        github_client_id     = var.github_client_id,
        github_client_secret = var.github_client_secret,

        database_host     = openstack_compute_instance_v2.pystebin_db.access_ip_v4,
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

