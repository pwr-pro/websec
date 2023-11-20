data "openstack_networking_subnet_v2" "public_subnet" {
  subnet_id = "81736cc6-2f9e-438f-9e0f-2f0453ee16c5"
}
data "openstack_networking_network_v2" "public" {
  network_id = "0d6bf40d-dcb9-4f94-bf00-56ec4d6d3b9d"
}
data "openstack_networking_network_v2" "provider" {
  network_id = "c8b620a1-7b8a-43d1-83d6-813ac2a23369"
}

data "openstack_images_image_v2" "ubuntu_22_04" {
  name = "ubuntu-22.04"
}

data "openstack_compute_keypair_v2" "chramb_k1" {
  name = "key1"
}

data "openstack_compute_flavor_v2" "m1_medium" {
  name = "m1.medium"
}
data "openstack_compute_flavor_v2" "m1_small" {
  name = "m1.small"
}
data "openstack_compute_flavor_v2" "m1_tiny" {
  name = "m1.tiny"
}
