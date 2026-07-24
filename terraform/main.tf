provider "google" {
  project = var.project_id
  region  = var.region
}

# GCS Buckets for the Pipeline
resource "google_storage_bucket" "raw_landing" {
  name     = "${var.project_id}-raw-landing"
  location = var.region
  storage_class = var.storage_class
}

resource "google_storage_bucket" "whisper_output" {
  name     = "${var.project_id}-whisper-output"
  location = var.region
  storage_class = var.storage_class
}

resource "google_storage_bucket" "processed_json" {
  name     = "${var.project_id}-processed-json"
  location = var.region
  storage_class = var.storage_class
}

resource "google_storage_bucket" "training_data" {
  name     = "${var.project_id}-training-data"
  location = var.region
  storage_class = var.storage_class
}

resource "google_storage_bucket" "results" {
  name     = "${var.project_id}-results"
  location = var.region
  storage_class = var.storage_class
}

# Artifact Registry for Whisper Container
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = "sutta-pipeline"
  format        = "DOCKER"
}
