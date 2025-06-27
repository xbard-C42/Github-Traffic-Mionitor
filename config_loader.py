'''src/traffic_monitor/config.py

Configuration loader and validator for GitHub Traffic Monitor.
Supports YAML and INI files.
'''
import os
import sys
from pathlib import Path
import logging

def load_config(path: str):
    """
    Load configuration from YAML or INI file.
    Required fields:
      - token: GitHub Personal Access Token or environment variable GITHUB_TOKEN
    Optional fields:
      - organization: GitHub org to query (default: user account)
      - output_dir: directory for output files (default: cwd)
    """
    file = Path(path)
    if not file.exists():
        logging.error(f"Config file not found: {path}")
        sys.exit(1)

    # Determine by extension
    if file.suffix in ('.yml', '.yaml'):
        return _load_yaml(file)
    elif file.suffix in ('.ini', '.cfg'):
        return _load_ini(file)
    else:
        logging.error("Unsupported config format. Use YAML (.yml/.yaml) or INI (.ini/.cfg).")
        sys.exit(1)


def _load_yaml(file: Path):
    try:
        import yaml
    except ImportError:
        logging.error("PyYAML not installed. Install via `pip install pyyaml`.")
        sys.exit(1)
    with open(file, 'r') as f:
        data = yaml.safe_load(f)
    return _validate(data)


def _load_ini(file: Path):
    import configparser
    parser = configparser.ConfigParser()
    parser.read(file)
    data = {}
    if 'github' in parser.sections():
        cfg = parser['github']
        data['token'] = cfg.get('token', fallback=None)
        data['organization'] = cfg.get('organization', fallback=None)
        data['output_dir'] = cfg.get('output_dir', fallback=None)
    else:
        logging.error("INI file missing [github] section.")
        sys.exit(1)
    return _validate(data)


def _validate(data: dict):
    # Token: from config or env
    token = data.get('token') or os.getenv('GITHUB_TOKEN')
    if not token:
        logging.error("GitHub token missing. Provide in config or set GITHUB_TOKEN env var.")
        sys.exit(1)
    org = data.get('organization')
    out = data.get('output_dir') or os.getcwd()
    return Config(token=token, organization=org, output_dir=out)


class Config:
    """Simple config container"""
    def __init__(self, token: str, organization: str | None, output_dir: str):
        self.token: str = token
        self.organization: str | None = organization
        self.output_dir: Path = Path(output_dir).expanduser().resolve()
        if not self.output_dir.exists():
            logging.debug(f"Creating output directory at {self.output_dir}")
            self.output_dir.mkdir(parents=True, exist_ok=True)

    def __repr__(self):
        return (
            f"<Config token=***{'*'*5} org={self.organization or 'user'} out={self.output_dir}>"
        )
