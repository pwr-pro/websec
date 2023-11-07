resource "openstack_networking_router_v2" "pystebin_db_router" {
  name                = "pystebin-db-router"
  external_network_id = data.openstack_networking_network_v2.public.id
  admin_state_up      = true
}

resource "openstack_networking_router_interface_v2" "int_db_rt" {
  router_id = openstack_networking_router_v2.pystebin_db_router.id
  subnet_id = openstack_networking_subnet_v2.pystebin_db_sub.id
}


resource "openstack_networking_network_v2" "pystebin_db" {
  name           = "pystebin-db"
  admin_state_up = "true"
}

resource "openstack_networking_subnet_v2" "pystebin_db_sub" {
  name        = "pystebin-db-sub"
  network_id  = openstack_networking_network_v2.pystebin_db.id
  cidr        = "192.168.200.0/24"
  enable_dhcp = false

  allocation_pool {
    start = "192.168.200.20"
    end   = "192.168.200.250"
  }

  gateway_ip = "192.168.200.1"
  ip_version = 4
}
