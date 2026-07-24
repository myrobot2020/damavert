provider "google" {
  project = var.project_id
  region  = var.region
}

# GCS Buckets
resource "google_storage_bucket" "raw_landing" {
  name     = "${var.project_id}-raw-landing"
  location = var.region
}
resource "google_storage_bucket" "whisper_output" {
  name     = "${var.project_id}-whisper-output"
  location = var.region
}
resource "google_storage_bucket" "processed_json" {
  name     = "${var.project_id}-processed-json"
  location = var.region
}
resource "google_storage_bucket" "manga_panels" {
  name     = "${var.project_id}-manga-panels"
  location = var.region
}

# Artifact Registry
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = "sutta-pipeline"
  format        = "DOCKER"
}

# Cloud Run Service for Ingestion
resource "google_cloud_run_v2_service" "ingestion" {
  name     = "sutta-ingestion"
  location = var.region
  template {
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/sutta-pipeline/ingestion:latest"
      env {
        name  = "RAW_BUCKET"
        value = google_storage_bucket.raw_landing.name
      }
    }
  }
}

# Pub/Sub for Human-in-the-Loop Audit
resource "google_pubsub_topic" "audit_topic" {
  name = "human-audit"
}

resource "google_pubsub_subscription" "audit_sub" {
  name  = "human-audit-sub"
  topic = google_pubsub_topic.audit_topic.name
}

# Cloud Workflow
resource "google_workflows_workflow" "sutta_workflow" {
  name            = "sutta-processing-pipeline"
  region          = var.region
  description     = "Orchestrates transcription, splitting, NLP, and Manga generation"
  service_account = google_service_account.pipeline_sa.id
  source_contents = file("${path.module}/../workflows/main.yaml")
}

# Service Account for Pipeline
resource "google_service_account" "pipeline_sa" {
  account_id   = "sutta-pipeline-sa"
  display_name = "Service Account for Dama Pipeline"
}

# IAM (Simplified for Boilerplate)
resource "google_project_iam_member" "pipeline_roles" {
  for_each = toset([
    "roles/aiplatform.user",
    "roles/storage.admin",
    "roles/dataproc.editor",
    "roles/pubsub.publisher",
    "roles/workflows.invoker"
  ])
  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

# Firestore / Vector Search
resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
}
