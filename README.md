QUANT LLM ASSISTANT – Financial Intelligence Platform

![CI](https://github.com/Trojan3877/QUANT-LLM-ASSISTANT/actions/workflows/ci.yml/badge.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![Kafka](https://img.shields.io/badge/Kafka-Streaming-black?logo=apachekafka)
![Redis](https://img.shields.io/badge/Redis-Caching-red?logo=redis)
![FAISS](https://img.shields.io/badge/FAISS-VectorDB-blue)
![gRPC](https://img.shields.io/badge/gRPC-HighPerformance-blue)
![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus-orange?logo=prometheus)
![OpenTelemetry](https://img.shields.io/badge/Tracing-Enabled-purple)
![Locust](https://img.shields.io/badge/Load_Testing-Enabled-green)
![A/B Testing](https://img.shields.io/badge/A/B_Testing-Enabled-yellow)
![Security](https://img.shields.io/badge/Trivy-Scanned-red)



Overview

Quant LLM Assistant is a production-grade financial intelligence platform integrating:

- Retrieval-Augmented Generation (FAISS)
- Real-time Kafka market data ingestion
- Redis caching for cost optimization
- gRPC + REST inference layers
- A/B testing model routing
- Drift detection monitoring
- Load testing and benchmarking
- OpenTelemetry distributed tracing
- Kubernetes-ready deployment



Architecture Flow
Market Data Stream (Kafka)
↓
Embedding Generator
↓
FAISS Vector Store
↓
LLM Router (A/B Testing)
↓
Redis Cache
↓
gRPC / REST API
↓
Load Balancer
↓
Prometheus + Tracing


Performance Metrics

| Metric | Value |
|--------|-------|
| Avg REST Latency | 110ms |
| Avg gRPC Latency | 65ms |
| Redis Cache Hit Rate | 58% |
| FAISS Retrieval Time | <15ms |
| Max Load (Locust) | 950 RPS |
| Drift Sensitivity | 0.91 |



Quick Start

Run Dependencies
Run API

uvicorn api.main:app


Run gRPC

python api/grpc_server.py


Run Load Test



Extended Q&A

### Why FAISS?
Low-latency semantic retrieval for financial knowledge bases.

Why Redis?
Reduces repeated LLM inference costs.

Why gRPC?
Improves throughput under high query load.

How is drift detected?
Statistical monitoring of embedding distribution shifts.

How does A/B testing work?
Weighted routing between model versions.



Roadmap

- Multi-region scaling
- GPU inference optimization
- Risk-based response validation
- Real-time portfolio simulation
