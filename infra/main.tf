resource "google_artifact_registry_repository" "imagerepo" {
  location      = "europe-central2"
  repository_id = "pzuchowski"
  format        = "DOCKER"
}

resource "google_cloud_run_v2_service" "api" {
  name     = "algorithm-service"
  location = "europe-west1"
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "europe-central2-docker.pkg.dev/diploma-410022/pzuchowski/api:latest"
      ports {
        container_port = 80
      }
    }
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

resource "google_cloud_run_v2_service_iam_policy" "policy" {
  project = google_cloud_run_v2_service.api.project
  location = google_cloud_run_v2_service.api.location
  name = google_cloud_run_v2_service.api.name
  policy_data = data.google_iam_policy.noauth.policy_data
}
