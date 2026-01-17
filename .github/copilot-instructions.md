# ImpactU Data Processing Pipeline

ImpactU is a data processing pipeline for Colombian academic research data that integrates multiple data sources (OpenAlex, Scienti, Google Scholar, DSpace repositories) using the Kahi ETL framework. The repository contains configuration files and workflow definitions rather than traditional software with build systems.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

**CRITICAL: Set timeouts of 60+ minutes for all data processing operations. NEVER CANCEL long-running commands.**

### Bootstrap and Dependencies
- Install Python 3.12+ and pip:
  - `sudo apt-get update && sudo apt-get install -y python3 python3-pip`
- Install Docker for database services:
  - `sudo apt-get install -y docker.io`
  - `sudo systemctl start docker`
- Install core Kahi framework:
  - `pip install kahi pymongo`
- Install required Kahi plugins:
  - `git clone https://github.com/colav/Kahi_sample.git /tmp/kahi_sample`
  - `pip install /tmp/kahi_sample/Kahi_scienti_sample/`
  - `pip install /tmp/kahi_sample/Kahi_minciencias_sample/`
  - `pip install /tmp/kahi_sample/Kahi_openalex_sample/`
  - `pip install /tmp/kahi_sample/Kahi_scholar_sample/`
- **TIMING**: Initial setup takes 5-10 minutes. Set timeout to 15+ minutes.

### Start Required Services
- Start MongoDB:
  - `docker run --name mongodb-impactu -p 27017:27017 -d mongo:latest`
  - **TIMING**: Container startup takes 30-60 seconds.
- Start Elasticsearch:
  - `docker run --name elasticsearch-impactu -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -d elasticsearch:8.11.0`
  - **TIMING**: Container startup takes 2-3 minutes. NEVER CANCEL.
- Verify services:
  - `docker ps` - Both containers should show "Up" status
  - `curl -X GET "localhost:9200/_cluster/health?pretty"` - Should return status "green"

### Run Data Processing Workflows
- Execute sample workflow:
  - `kahi_run --workflow workflows/samples/kahi_sample_vip.yml --verbose 5`
  - **TIMING**: Sample workflow with small dataset takes 5-10 minutes. Set timeout to 20+ minutes.
- Execute full production workflow:
  - `kahi_run --workflow workflows/impactu/kahi_impactu.yml --verbose 5`
  - **CRITICAL**: Full production workflow takes 45-90 minutes. NEVER CANCEL. Set timeout to 120+ minutes.

## Validation

**SCENARIO VALIDATION**: Always run through at least one complete end-to-end scenario after making changes.

### Test Sample Workflow
- **Complete scenario**: Run sample data processing workflow
  - Ensure MongoDB and Elasticsearch are running
  - Execute: `kahi_run --workflow workflows/samples/kahi_sample_vip.yml --verbose 5`
  - Verify: Check MongoDB collections are created with sample data
  - **TIMING**: Takes 5-10 minutes to complete. Set timeout to 20+ minutes.

### Manual Validation Scenarios  
**ALWAYS execute these scenarios after making any changes to ensure functionality:**

1. **Database Connectivity Test**:
   - Start services: `docker run --name mongodb-test -p 27017:27017 -d mongo:latest`
   - Verify connection: Configuration parsing should complete without timeout errors
   - Expected result: Kahi connects to MongoDB successfully

2. **Configuration Validation**:
   - Test all workflow files in `workflows/` directory
   - Verify YAML syntax is valid and Kahi can parse configurations
   - Expected result: No syntax errors, successful config loading

3. **Plugin Availability Test**:
   - Ensure all required Kahi plugins are installed and importable
   - Test with: `kahi_run --workflow workflows/samples/kahi_sample_vip.yml --verbose 5`
   - Expected result: All plugins load without ModuleNotFoundError

### Verify Database Integration
- Connect to MongoDB: `mongo localhost:27017`
- List databases: `show dbs`
- Check sample collections exist: `use scienti_sample; show collections`
- Verify Elasticsearch: `curl "localhost:9200/_cat/indices?v"`

### Test Configuration Changes
- Validate YAML syntax: `python3 -c "import yaml; yaml.safe_load(open('workflows/impactu/kahi_impactu.yml'))"`
  - **TIMING**: Syntax validation takes <1 second
- Test configuration loading: `kahi_run --workflow [your-config].yml --verbose 5` (will show config parsing)
  - **TIMING**: Configuration parsing and initial connection attempt takes ~30 seconds

## Common Tasks

The following are key commands and expected outputs. Reference them instead of running bash commands to save time.

### Repository Structure
```
.
├── README.md
├── .gitignore
├── LICENSE
├── configs/
│   └── oxomoc/
│       └── colombia_config.py          # 105+ Colombian DSpace endpoints
├── doc/
│   ├── capture.md                      # Data source documentation
│   └── product types by source.md     # Product type mappings
├── releases/
│   ├── README_06_2025.md               # Latest release notes
│   └── README_12_08_2024_es.md         # Previous release notes
└── workflows/
    ├── impactu/
    │   ├── kahi_impactu.yml             # Main production workflow
    │   ├── kahi_impactu_dev.yml         # Development workflow
    │   └── kahi_impactu_dspace.yml      # DSpace-specific workflow
    └── samples/
        ├── README.md                    # Sample workflow documentation
        └── kahi_sample_vip.yml          # Sample VIP authors workflow
```

### Key Technologies and Data Sources
- **Primary Framework**: Kahi (Python-based ETL framework)
- **Databases**: MongoDB (document storage), Elasticsearch (search)
- **Data Sources**: 
  - OpenAlex (works, authors, institutions, sources)
  - Scienti (Colombian research products)
  - Google Scholar (author profiles and publications)
  - DSpace (105+ Colombian institutional repositories)
  - DOAJ (open access journals)
  - Minciencias (Colombian research ministry data)
  - ORCID (researcher identifiers)

### Common Workflow Patterns
- **Sample Creation**: Use `workflows/samples/kahi_sample_vip.yml` for testing with subset of data
- **Full ETL**: Use `workflows/impactu/kahi_impactu.yml` for complete data processing
- **Development**: Use `workflows/impactu/kahi_impactu_dev.yml` for incremental updates

### Timing Expectations
- **NEVER CANCEL**: All data processing operations require patience
- **YAML validation**: <1 second
- **Configuration parsing**: ~30 seconds
- **Kahi plugin installation**: 5-10 minutes. Set timeout to 15+ minutes.
- **Service startup (MongoDB/Elasticsearch)**: 2-3 minutes. Set timeout to 5+ minutes.
- **Sample workflow execution**: 5-10 minutes. Set timeout to 20+ minutes.
- **Full production workflow**: 45-90 minutes. Set timeout to 120+ minutes.
- **Large dataset processing**: Can take several hours. Set timeout to 240+ minutes.

### Data Processing Pipeline Overview
1. **Sources**: Extract data from multiple academic databases and repositories
2. **Transformation**: Standardize and deduplicate using DOI matching and similarity
3. **Loading**: Store in MongoDB with Elasticsearch indexing for search
4. **Post-processing**: Calculate impact metrics, co-authorship networks, institutional rankings

### Expected Database Collections After Workflow
MongoDB collections created by successful workflow execution:
- `works` - Academic publications and products
- `person` - Researchers and authors (deduplicated)
- `affiliations` - Institutions and organizations
- `sources` - Journals and publication venues
- Various staging collections for each data source

### Troubleshooting Common Issues
- **Module not found errors**: Install missing Kahi plugins from GitHub repositories
- **Database connection errors**: Ensure MongoDB container is running on port 27017
- **Elasticsearch errors**: Verify container started and health check returns "green"
- **Memory issues**: Large workflows require adequate RAM (8GB+ recommended)
- **Network timeouts**: Some pip installations may timeout - retry with longer timeouts

### Dependencies Installation Issues
If network issues prevent installing all dependencies:
- Essential: `kahi`, `pymongo` (core framework)
- Nice-to-have: Language detection libraries, specialized plugins
- **Docker alternative**: Use pre-built containers with all dependencies included

### Tested Installation Commands
The following commands have been validated to work:
```bash
# Core framework (validated)
pip install kahi pymongo

# Sample plugins (validated)
git clone https://github.com/colav/Kahi_sample.git /tmp/kahi_sample
pip install /tmp/kahi_sample/Kahi_scienti_sample/
pip install /tmp/kahi_sample/Kahi_minciencias_sample/
pip install /tmp/kahi_sample/Kahi_openalex_sample/
pip install /tmp/kahi_sample/Kahi_scholar_sample/

# Service containers (validated) 
docker run --name mongodb-impactu -p 27017:27017 -d mongo:latest
docker run --name elasticsearch-impactu -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -d elasticsearch:8.11.0

# Validation commands (validated)
python3 -c "import yaml; yaml.safe_load(open('workflows/impactu/kahi_impactu.yml'))"
kahi_run --help
docker ps
curl -X GET "localhost:9200/_cluster/health?pretty"
```

## Important Notes
- This is primarily a configuration and documentation repository for data processing workflows
- The actual data processing is handled by the Kahi framework and its plugins
- Always test workflows with sample data before running full production pipelines
- Monitor disk space - large datasets can require significant storage
- Backup important data before running workflows that drop/recreate databases