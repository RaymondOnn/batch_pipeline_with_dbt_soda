variable "project_id" {
  type = string
}

variable "region" {
  type        = string
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default     = "asia-southeast1"
}

variable "storage_class" {
  type        = string
  description = "The Storage Class of the new bucket. Ref: https://cloud.google.com/storage/docs/storage-classes"
  default     = "STANDARD"
}

variable "bq_dataset_name" {
  type        = string
  description = "Dataset in BigQuery where raw data (from Google Cloud Storage) will be loaded."
  default     = "some_dataset"
}

variable "storage_bucket_name" {
  type    = string
  default = "some_bucket"
}
