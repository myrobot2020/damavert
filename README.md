# Damavert: Sutta Classification & Enrichment Pipeline

This repository contains the boilerplate for the automated Buddhist transcript processing pipeline.

## Structure
- `terraform/`: Infrastructure as Code for GCS buckets and Registry.
- `src/transcription/`: Whisper GPU transcription scripts.
- `src/processing/`: Dataproc/Spark logic for `x.y.z` splitting.
- `src/classification/`: Vertex AI Custom Training for sentence tagging.
- `src/enrichment/`: Gemini 1.5 Flash logic for Doctrinal Chains & MCQs.
- `src/localization/`: Translation and Voice Cloning logic.

## Setup
1. Initialize Terraform: `cd terraform && terraform init && terraform apply`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Configure your project ID in `terraform/variables.tf`.

## Usage
1. **Transcribe:** Run Whisper job on Vertex AI.
2. **Process:** Use `splitter.py` to segment into individual Sutta JSONs.
3. **Train:** Kick off the DistilBERT training job after labeling the first 10 suttas.
4. **Enrich:** Use the Gemini script to add doctrinal chains to each JSON.
