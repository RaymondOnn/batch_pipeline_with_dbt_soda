terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.21.0"
    }
  }
}

provider "google" {
  project     = var.project_id
  credentials = file("../airflow/dags/online_retail/gcp/service_account.json")
}

resource "google_storage_bucket" "gcp_bucket" {
  name                        = var.storage_bucket_name
  location                    = var.region
  storage_class               = var.storage_class
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  versioning {
    enabled = true
  }
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 10 //days
    }
  }
  force_destroy = true
}

resource "google_bigquery_dataset" "bq_dataset" {
  project    = var.project_id
  dataset_id = var.bq_dataset_name
  location   = var.region
}
