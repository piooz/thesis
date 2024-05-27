variable "cache_host" {
  type = string
}

variable "cache_pass" {
  type = string
}

resource "google_artifact_registry_repository" "imagerepo" {
  location      = "europe-central2"
  repository_id = "pzuchowski"
  format        = "DOCKER"
}

# google_cloud_run_v2_service.api:
resource "google_cloud_run_v2_service" "api" {
    annotations             = {}
    client                  = "cloud-console"
    conditions              = [
        {
            execution_reason     = ""
            last_transition_time = "2024-05-22T22:15:19.092227Z"
            message              = ""
            reason               = ""
            revision_reason      = ""
            severity             = ""
            state                = "CONDITION_SUCCEEDED"
            type                 = "RoutesReady"
        },
        {
            execution_reason     = ""
            last_transition_time = "2024-05-21T22:47:00.449784Z"
            message              = ""
            reason               = ""
            revision_reason      = ""
            severity             = ""
            state                = "CONDITION_SUCCEEDED"
            type                 = "ConfigurationsReady"
        },
    ]
    ingress                 = "INGRESS_TRAFFIC_ALL"
    location                = "us-central1"
    name                    = "algorithm-service"
    project                 = "diploma-410022"

    template {
        max_instance_request_concurrency = 80
        service_account                  = "626532301577-compute@developer.gserviceaccount.com"
        timeout                          = "300s"

        containers {
            args    = []
            command = []
            image   = "europe-central2-docker.pkg.dev/diploma-410022/pzuchowski/api:latest"
            name    = "api-1"

            env {
              name = "CACHE_HOST"
              value = var.cache_host
            }
            env {
              name = "CACHE_PORT"
              value = 6379
            }
            env {
              name = "CACHE_EXPIRATION_SECONDS"
              value = 86400
            }
            env {
              name = "CACHE_PASS"
              value = var.cache_pass
            }

            ports {
                container_port = 80
                name           = "http1"
            }

            resources {
                cpu_idle = true
                limits   = {
                    "cpu"    = "1000m"
                    "memory" = "512Mi"
                }
            }

            startup_probe {
                failure_threshold     = 1
                initial_delay_seconds = 0
                period_seconds        = 240
                timeout_seconds       = 240

                tcp_socket {
                    port = 80
                }
            }
        }

        vpc_access {
            egress = "PRIVATE_RANGES_ONLY"
        }
    }

    traffic {
        percent = 100
        type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    }
}


data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_compute_instance" "redis-db" {
  boot_disk {
    auto_delete = true
    device_name = "redis-db"

    initialize_params {
      image = "projects/debian-cloud/global/images/debian-12-bookworm-v20240515"
      size  = 10
      type  = "pd-balanced"
    }

    mode = "READ_WRITE"
  }

  can_ip_forward      = false
  deletion_protection = false
  enable_display      = false
  hostname            = var.cache_host


  labels = {
    goog-ec-src = "vm_add-tf"
  }

  machine_type = "e2-micro"

  metadata = {
    startup-script = <<-EOT
      apt-get -y install lsb-release curl gpg

      curl -fsSL https://packages.redis.io/gpg | gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

      echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/redis.list

      apt-get update
      apt-get -y install redis

      # Update the bind address
      sed -i "s/^bind .*/bind 0.0.0.0/" /etc/redis/redis.conf

      echo "requirepass ${var.cache_pass}" >> /etc/redis/redis.conf

      systemctl enable redis-server
      systemctl start redis-server
      systemctl restart redis-server
    EOT
  }

  name = "redis-db"

  network_interface {
    access_config {
      network_tier = "PREMIUM"
    }

    queue_count = 0
    stack_type  = "IPV4_ONLY"
    subnetwork  = "projects/diploma-410022/regions/us-central1/subnetworks/default"
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  service_account {
    email  = "626532301577-compute@developer.gserviceaccount.com"
    scopes = ["https://www.googleapis.com/auth/devstorage.read_only", "https://www.googleapis.com/auth/logging.write", "https://www.googleapis.com/auth/monitoring.write", "https://www.googleapis.com/auth/service.management.readonly", "https://www.googleapis.com/auth/servicecontrol", "https://www.googleapis.com/auth/trace.append"]
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }

  zone = "us-central1-a"
}

resource "google_cloud_run_v2_service_iam_policy" "policy" {
  project = google_cloud_run_v2_service.api.project
  location = google_cloud_run_v2_service.api.location
  name = google_cloud_run_v2_service.api.name
  policy_data = data.google_iam_policy.noauth.policy_data
}
