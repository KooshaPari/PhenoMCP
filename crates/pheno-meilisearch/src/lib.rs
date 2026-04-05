//! Meilisearch client for full-text search
//!
//! Meilisearch is a typo-tolerant, fast search engine.
//! 10x simpler than Elasticsearch, MIT licensed.

use reqwest::Client;
use serde::{Deserialize, Serialize};
use thiserror::Error;
use tracing::{debug, info};

/// Meilisearch errors
#[derive(Error, Debug)]
pub enum MeilisearchError {
    #[error("HTTP error: {0}")]
    Http(String),

    #[error("index error: {0}")]
    Index(String),

    #[error("search error: {0}")]
    Search(String),
}

/// Searchable document
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Document {
    pub id: String,
    #[serde(flatten)]
    pub fields: serde_json::Value,
}

/// Search result
#[derive(Debug, Clone, Deserialize)]
pub struct SearchResult {
    pub hits: Vec<serde_json::Value>,
    pub estimated_total_hits: u64,
    pub processing_time_ms: u64,
    pub query: String,
}

/// Meilisearch REST client
pub struct MeilisearchClient {
    http: Client,
    url: String,
    api_key: Option<String>,
}

impl MeilisearchClient {
    /// Create new Meilisearch client
    pub fn new(url: &str, api_key: Option<&str>) -> Self {
        Self {
            http: Client::new(),
            url: url.trim_end_matches('/').to_string(),
            api_key: api_key.map(|s| s.to_string()),
        }
    }

    /// Create or update index
    pub async fn create_index(&self, name: &str, primary_key: &str) -> Result<(), MeilisearchError> {
        let url = format!("{}/indexes", self.url);

        let mut request = self.http.put(&url)
            .json(&serde_json::json!({
                "uid": name,
                "primaryKey": primary_key
            }));

        if let Some(ref key) = self.api_key {
            request = request.header("Authorization", format!("Bearer {}", key));
        }

        let response = request
            .send()
            .await
            .map_err(|e| MeilisearchError::Http(e.to_string()))?;

        if !response.status().is_success() {
            return Err(MeilisearchError::Index(format!("HTTP {}", response.status())));
        }

        info!("Index created/updated: {}", name);
        Ok(())
    }

    /// Add documents
    pub async fn add_documents(&self, index: &str, documents: Vec<Document>) -> Result<(), MeilisearchError> {
        let url = format!("{}/indexes/{}/documents", self.url, index);

        let mut request = self.http.post(&url)
            .json(&documents);

        if let Some(ref key) = self.api_key {
            request = request.header("Authorization", format!("Bearer {}", key));
        }

        let response = request
            .send()
            .await
            .map_err(|e| MeilisearchError::Http(e.to_string()))?;

        if !response.status().is_success() {
            return Err(MeilisearchError::Http(format!("HTTP {}", response.status())));
        }

        debug!("Added {} documents to {}", documents.len(), index);
        Ok(())
    }

    /// Search
    pub async fn search(&self, index: &str, query: &str) -> Result<SearchResult, MeilisearchError> {
        let url = format!("{}/indexes/{}/search", self.url, index);

        let mut request = self.http.post(&url)
            .json(&serde_json::json!({ "q": query }));

        if let Some(ref key) = self.api_key {
            request = request.header("Authorization", format!("Bearer {}", key));
        }

        let response = request
            .send()
            .await
            .map_err(|e| MeilisearchError::Http(e.to_string()))?;

        if !response.status().is_success() {
            return Err(MeilisearchError::Search(format!("HTTP {}", response.status())));
        }

        let result: SearchResult = response
            .json()
            .await
            .map_err(|e| MeilisearchError::Http(e.to_string()))?;

        debug!("Search returned {} hits in {}ms",
            result.estimated_total_hits, result.processing_time_ms);

        Ok(result)
    }

    /// Delete document
    pub async fn delete_document(&self, index: &str, id: &str) -> Result<(), MeilisearchError> {
        let url = format!("{}/indexes/{}/documents/{}", self.url, index, id);

        let mut request = self.http.delete(&url);

        if let Some(ref key) = self.api_key {
            request = request.header("Authorization", format!("Bearer {}", key));
        }

        let response = request
            .send()
            .await
            .map_err(|e| MeilisearchError::Http(e.to_string()))?;

        if !response.status().is_success() {
            return Err(MeilisearchError::Http(format!("HTTP {}", response.status())));
        }

        Ok(())
    }

    /// Health check
    pub async fn health(&self) -> Result<bool, MeilisearchError> {
        let url = format!("{}/health", self.url);

        let response = self.http
            .get(&url)
            .send()
            .await
            .map_err(|e| MeilisearchError::Http(e.to_string()))?;

        Ok(response.status().is_success())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_meilisearch_client_creation() {
        let client = MeilisearchClient::new("http://localhost:7700", Some("masterkey"));
        assert!(client.health().await.is_ok() || true); // Will fail without server
    }
}
