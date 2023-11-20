resource "openstack_networking_network_v2" "pystebin_internal" {
  name           = "pystebin-internal"
  admin_state_up = "true"

}

resource "openstack_networking_subnet_v2" "pystebin_internal_sub" {
  name        = "pystebin-internal-sub"
  network_id  = openstack_networking_network_v2.pystebin_internal.id
  cidr        = "192.168.199.0/24"
  enable_dhcp = true
  allocation_pool {
    start = "192.168.199.20"
    end   = "192.168.199.250"
  }
  gateway_ip = "192.168.199.1"
  ip_version = 4
}

resource "openstack_networking_router_v2" "pystebin_int_router" {
  name                = "pystebin-internal-router"
  external_network_id = data.openstack_networking_network_v2.public.id
  admin_state_up      = true
}

resource "openstack_networking_router_interface_v2" "ext_rt" {
  router_id = openstack_networking_router_v2.pystebin_int_router.id
  subnet_id = openstack_networking_subnet_v2.pystebin_internal_sub.id
}
