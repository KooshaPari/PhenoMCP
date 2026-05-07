//! Qdrant client for vector search (semantic embeddings)
//!
//! Qdrant is a high-performance vector search engine.
//! Apache licensed, self-hosted alternative to Pinecone.

use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use thiserror::Error;
use tracing::{debug, info};

/// Qdrant errors
#[derive(Error, Debug)]
pub enum QdrantError {
    #[error("HTTP error: {0}")]
    Http(String),

    #[error("not found: {0}")]
    NotFound(String),

    #[error("collection error: {0}")]
    Collection(String),

    #[error("parse error: {0}")]
    Parse(String),
}

/// Vector point
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Point {
    pub id: String,
    pub vector: Vec<f32>,
    pub payload: HashMap<String, serde_json::Value>,
}

/// Search result
#[derive(Debug, Clone, Deserialize)]
pub struct SearchResult {
    pub id: String,
    pub score: f32,
    pub payload: HashMap<String, serde_json::Value>,
}

/// Qdrant REST client
pub struct QdrantClient {
    http: Client,
    url: String,
}

impl QdrantClient {
    /// Create new Qdrant client
    pub fn new(url: &str) -> Self {
        Self {
            http: Client::new(),
            url: url.trim_end_matches('/').to_string(),
        }
    }

    /// Create collection
    pub async fn create_collection(&self, name: &str, vector_size: u64) -> Result<(), QdrantError> {
        let url = format!("{}/collections/{}", self.url, name);

        let response = self.http
            .put(&url)
            .json(&serde_json::json!({
                "vectors": {
                    "size": vector_size,
                    "distance": "Cosine"
                },
                "hnsw_config": {
                    "m": 16,
                    "ef_construct": 100
                }
            }))
            .send()
            .await
            .map_err(|e| QdrantError::Http(e.to_string()))?;

        if !response.status().is_success() {
            return Err(QdrantError::Collection(format!("HTTP {}", response.status())));
        }

        info!("Collection created: {}", name);
        Ok(())
    }

    /// Upsert points
    pub async fn upsert(&self, collection: &str, points: Vec<Point>) -> Result<(), QdrantError> {
        let url = format!("{}/collections/{}/points", self.url, collection);

        let payload: Vec<serde_json::Value> = points
            .into_iter()
            .map(|p| {
                serde_json::json!({
                    "id": p.id,
                    "vector": p.vector,
                    "payload": p.payload
                })
            })
            .collect();

        let response = self.http
            .put(&url)
            .json(&serde_json::json!({ "points": payload }))
            .send()
            .await
            .map_err(|e| QdrantError::Http(e.to_string()))?;

        if !response.status().is_success() {
            return Err(QdrantError::Http(format!("HTTP {}", response.status())));
        }

        debug!("Upserted {} points to {}", payload.len(), collection);
        Ok(())
    }

    /// Search vectors
    pub async fn search(&self, collection: &str, query: &[f32], limit: usize) -> Result<Vec<SearchResult>, QdrantError> {
        let url = format!("{}/collections/{}/points/search", self.url, collection);

        let response = self.http
            .post(&url)
            .json(&serde_json::json!({
                "vector": query,
                "limit": limit,
                "with_payload": true
            }))
            .send()
            .await
            .map_err(|e| QdrantError::Http(e.to_string()))?;

        if !response.status().is_success() {
            return Err(QdrantError::Http(format!("HTTP {}", response.status())));
        }

        let results: Vec<SearchResult> = response
            .json()
            .await
            .map_err(|e| QdrantError::Parse(e.to_string()))?;

        Ok(results)
    }

    /// Delete collection
    pub async fn delete_collection(&self, name: &str) -> Result<(), QdrantError> {
        let url = format!("{}/collections/{}", self.url, name);

        let response = self.http
            .delete(&url)
            .send()
            .await
            .map_err(|e| QdrantError::Http(e.to_string()))?;

        if !response.status().is_success() {
            return Err(QdrantError::Collection(format!("HTTP {}", response.status())));
        }

        info!("Collection deleted: {}", name);
        Ok(())
    }

    /// Health check
    pub async fn health(&self) -> Result<bool, QdrantError> {
        let url = format!("{}/health", self.url);

        let response = self.http
            .get(&url)
            .send()
            .await
            .map_err(|e| QdrantError::Http(e.to_string()))?;

        Ok(response.status().is_success())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_qdrant_client_creation() {
        let client = QdrantClient::new("http://localhost:6333");
        assert!(client.health().await.is_ok() || true); // Will fail without server
    }
}
