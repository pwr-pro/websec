output "ip_0" {
  value = openstack_compute_instance_v2.pystebin_app[0].access_ip_v4
}

output "ip_1" {
  value = openstack_compute_instance_v2.pystebin_app[1].access_ip_v4
}
