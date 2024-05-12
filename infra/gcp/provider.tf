terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file("key.json")

  project = "diploma-410022"
  region  = "europe-west"
  zone    = "europe-west1"
}
