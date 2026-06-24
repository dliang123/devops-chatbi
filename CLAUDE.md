# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository State

This repository currently contains project documentation only (`README.md`, `LICENSE`, and `.gitignore`). There is no application source tree, package manifest, test configuration, or build tooling checked in yet.

## Development Commands

No build, lint, test, or application run commands are currently defined in the repository. Before adding code, introduce the appropriate manifest and scripts for the chosen stack, then update this file with the exact commands.

## Project Overview

DevEfficiency-ChatBI is intended to be an intelligent assistant for R&D efficiency analytics. The README describes a system that uses a multi-agent architecture to answer natural-language questions against engineering tool data from systems such as Jira, GitHub, GitLab, SonarQube, and internal databases.

The planned architecture includes:

- LangChain/LangGraph for LLM workflow orchestration and multi-agent coordination.
- A FastAPI backend for asynchronous APIs and streaming responses.
- SQL generation and validation agents, including intent recognition, SQL generation, SQL safety checking, and analysis/reporting roles.
- Vector retrieval through ChromaDB or Pinecone for an R&D efficiency knowledge base.
- A future UI layer using Streamlit or Next.js for charts and conversational interaction.

## Current Roadmap from README

- v0.1: basic SQL generation and data querying.
- v0.2: multi-agent workflow support for complex intent decomposition.
- v0.3: custom R&D efficiency dashboard exports.
- v0.4: DingTalk/WeCom workplace integrations.

## Notes for Future Agents

Treat the README as the current source of truth until implementation files are added. Do not assume the FastAPI, LangGraph, Streamlit, or Next.js components already exist; verify files and manifests before running or editing code.
