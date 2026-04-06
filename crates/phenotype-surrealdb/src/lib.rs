//! PhenotypeSurrealDB - SurrealDB fork with Pheno extensions
//!
//! Forked from surrealdb/surrealdb (29k stars)
//! 
//! Additions:
//! - MCP protocol adapter
//! - Skill storage schema
//! - WASM embedding support

use anyhow::Result;
use serde::{Deserialize, Serialize};
use surrealdb::engine::local::{Db, RocksDb};
use surrealdb::Surreal;

pub struct PhenoSurreal {
    db: Surreal<Db>,
}

impl PhenoSurreal {
    pub async fn new(path: impl Into<String>) -> Result<Self> {
        let db = Surreal::new::<RocksDb>(path.into()).await?;
        db.use_ns("pheno").use_db("main").await?;
        Ok(Self { db })
    }

    pub async fn store_skill(&self, skill: Skill) -> Result<SkillRecord> {
        let result: Option<SkillRecord> = self.db.create("skill").content(skill).await?;
        Ok(result.unwrap())
    }

    pub async fn query_skills(&self) -> Result<Vec<SkillRecord>> {
        let skills: Vec<SkillRecord> = self.db.select("skill").await?;
        Ok(skills)
    }

    pub async fn store_embedding(&self, embedding: Embedding) -> Result<EmbeddingRecord> {
        let result: Option<EmbeddingRecord> = self.db.create("embedding").content(embedding).await?;
        Ok(result.unwrap())
    }

    pub async fn search_similar(&self, query: &[f32], limit: usize) -> Result<Vec<SimilarResult>> {
        let results: Vec<SimilarResult> = self.db
            .query("SELECT *, vector::distance::cosine(embedding, $query) AS score FROM embedding ORDER BY score ASC LIMIT $limit")
            .bind(("query", query))
            .bind(("limit", limit))
            .await?
            .take(0)?;
        Ok(results)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Skill {
    pub id: Option<String>,
    pub name: String,
    pub version: String,
    pub code: String,
    pub runtime: String,
    pub metadata: serde_json::Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SkillRecord {
    pub id: surrealdb::sql::Thing,
    pub name: String,
    pub version: String,
    pub code: String,
    pub runtime: String,
    pub metadata: serde_json::Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Embedding {
    pub id: Option<String>,
    pub vector: Vec<f32>,
    pub metadata: serde_json::Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EmbeddingRecord {
    pub id: surrealdb::sql::Thing,
    pub vector: Vec<f32>,
    pub metadata: serde_json::Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SimilarResult {
    pub id: surrealdb::sql::Thing,
    pub score: f32,
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;

    #[tokio::test]
    async fn test_skill_storage() -> Result<()> {
        let dir = tempdir()?;
        let db = PhenoSurreal::new(dir.path().join("test.db")).await?;
        
        let skill = Skill {
            id: None,
            name: "test-skill".to_string(),
            version: "1.0.0".to_string(),
            code: "fn main() {}".to_string(),
            runtime: "wasm".to_string(),
            metadata: serde_json::json!({}),
        };
        
        let result = db.store_skill(skill).await?;
        assert_eq!(result.name, "test-skill");
        
        Ok(())
    }
}
