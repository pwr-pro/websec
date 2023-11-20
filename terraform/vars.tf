variable "cloud" {
  type    = string
  default = "openstack"
}

variable "container_tag" {
  type    = string
  default = ":latest"

}

variable "app_host" {
    type = string
    default = "0.0.0.0"
}

variable "app_port" {
    type = number
    default = 8080
}

variable "app_auth_secret" {
    type = string
    sensitive = true
}

variable "app_auth_algorithm" {
    type = string
    sensitive = true
    default = "HS256" 
}

variable "github_client_id" {
    type = string
    sensitive = true
}

variable "github_client_secret" {
    type = string
    sensitive = true
}

variable "database_user" {
    type = string
    sensitive = true
    default = "postgres"
}

variable "database_name" {
    type = string
    default = "postgres"
}

variable "database_password" {
    type = string
    sensitive = true
  
}