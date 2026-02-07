import os
import json
import hashlib
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

INPUT_LIST = "pastas.txt"
OUTPUT_DIR = Path("ignorar/concatenados")
OUTPUT_FILE_MD = OUTPUT_DIR / "resultado_concatenado.md"
OUTPUT_FILE_JSON = OUTPUT_DIR / "resultado_concatenado.json"
OUTPUT_FILE_TXT = OUTPUT_DIR / "resultado_concatenado.txt"
LIMIT_VERSIONS = 20

def log(msg: str, level: str = "INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level:<5}] {msg}")

def get_vscode_history_root() -> Path:
    if sys.platform == "win32":
        return Path(os.path.expandvars(r'%APPDATA%\Code\User\History'))
    elif sys.platform == "darwin":
        return Path.home() / "Library/Application Support/Code/User/History"
    else:
        return Path.home() / ".config/Code/User/History"

class VSCodeForensicAnalyzer:
    def __init__(self):
        self.history_root = get_vscode_history_root()
        self.history_index = {}
        self.report_data = []
        
        if not self.history_root.exists():
            raise FileNotFoundError(f"VS Code history root not found: {self.history_root}")
        
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        log(f"Environment initialized. Root: {self.history_root}", "INIT")

    def _get_vscode_uri(self, file_path: Path) -> str:
        uri = file_path.resolve().as_uri().lower()
        if sys.platform == "win32" and uri.startswith("file:///"):
            if len(uri) > 9 and uri[9] == ':':
                uri = uri[:9] + "%3a" + uri[10:]
        return uri

    def build_global_index(self):
        log("Starting global history indexing...", "INDEX")
        count = 0
        for folder in self.history_root.iterdir():
            if folder.is_dir():
                entries_file = folder / "entries.json"
                if entries_file.exists():
                    try:
                        with open(entries_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            uri = data.get('resource', '').lower()
                            if uri: 
                                self.history_index[uri] = folder
                                count += 1
                    except Exception:
                        continue
        log(f"Global index built. Mapped {count} files.", "INDEX")

    def get_git_root(self, file_path: Path) -> Optional[Path]:
        try:
            cmd = ["git", "rev-parse", "--show-toplevel"]
            result = subprocess.run(
                cmd, 
                cwd=file_path.parent, 
                capture_output=True, 
                text=True, 
                encoding='utf-8',
                check=False
            )
            if result.returncode == 0:
                return Path(result.stdout.strip())
        except Exception:
            pass
        return None

    def run(self):
        if not Path(INPUT_LIST).exists():
            log(f"Input file {INPUT_LIST} not found.", "ERROR")
            return

        with open(INPUT_LIST, 'r', encoding='utf-8') as f:
            targets = [Path(line.strip()) for line in f if line.strip()]

        log(f"Loaded {len(targets)} targets from {INPUT_LIST}", "LOAD")

        for target in targets:
            self.process_single_file(target)

        self.generate_markdown()
        self.generate_txt()
        self.generate_json()

        log("Execution completed successfully.", "DONE")

    def process_single_file(self, path: Path):
        abs_path = path.resolve()
        log(f"Processing: {path.name}", "PROC")
        log(f"Absolute Path: {abs_path}", "DEBUG")
        
        vscode_versions = self.extract_vscode_history(abs_path)
        git_versions = self.extract_git_history(abs_path)
        
        all_versions = vscode_versions + git_versions
        
        if not all_versions:
            log(f"No versions found for {path.name}", "WARN")
            return

        unique_versions = []
        seen_hashes = set()
        
        try:
            sorted_versions = sorted(all_versions, key=lambda x: x['timestamp'])
        except TypeError:
            log("Timestamp sort failed, falling back to string sort.", "WARN")
            sorted_versions = sorted(all_versions, key=lambda x: str(x['timestamp']))

        for version in sorted_versions:
            content_hash = hashlib.sha256(version['content'].encode('utf-8')).hexdigest()
            if content_hash not in seen_hashes:
                version['hash'] = content_hash
                unique_versions.append(version)
                seen_hashes.add(content_hash)
        
        log(f"Stats | VSCode: {len(vscode_versions)} | Git: {len(git_versions)} | Unique: {len(unique_versions)}", "STATS")

        if len(unique_versions) <= (LIMIT_VERSIONS * 2):
            final_selection = unique_versions
            era_type = "FULL"
        else:
            final_selection = unique_versions[:LIMIT_VERSIONS] + unique_versions[-LIMIT_VERSIONS:]
            era_type = "PARTIAL"

        self.report_data.append({
            "file_path": str(abs_path),
            "file_name": path.name,
            "era_type": era_type,
            "total_versions_found": len(unique_versions),
            "versions": final_selection
        })

    def extract_vscode_history(self, path: Path) -> List[Dict]:
        uri = self._get_vscode_uri(path)
        log(f"Calculated URI: {uri}", "DEBUG")
        
        folder = self.history_index.get(uri)
        if not folder:
            log("URI not found in global index.", "DEBUG")
            return []

        entries_file = folder / "entries.json"
        if not entries_file.exists():
            return []

        versions = []
        try:
            with open(entries_file, 'r', encoding='utf-8') as f:
                entries = json.load(f).get('entries', [])
            
            for entry in entries:
                v_path = folder / entry['id']
                if v_path.exists():
                    dt = datetime.fromtimestamp(entry['timestamp'] / 1000.0)
                    versions.append({
                        "id": entry['id'],
                        "timestamp": dt,
                        "content": v_path.read_text(encoding='utf-8', errors='replace'),
                        "source": "VS Code Local"
                    })
        except Exception as e:
            log(f"Error reading VS Code entries: {e}", "ERROR")
            
        return versions

    def extract_git_history(self, path: Path) -> List[Dict]:
        versions = []
        repo_root = self.get_git_root(path)
        
        if not repo_root:
            log("Not a git repository.", "DEBUG")
            return []

        try:
            rel_path = path.relative_to(repo_root).as_posix()
            cmd = ["git", "log", "--follow", "--format=%H|%ai", "--", rel_path]
            
            result = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True, encoding='utf-8')
            if result.returncode != 0:
                return []

            lines = result.stdout.strip().split('\n')
            valid_lines = [l for l in lines if l]
            log(f"Git commits found: {len(valid_lines)}", "DEBUG")

            for line in valid_lines:
                parts = line.split('|')
                if len(parts) < 2: continue
                
                v_hash, v_time_str = parts[0], parts[1]
                
                content_res = subprocess.run(
                    ["git", "show", f"{v_hash}:{rel_path}"],
                    cwd=repo_root, capture_output=True, text=True, encoding='utf-8'
                )
                
                if content_res.returncode == 0:
                    dt_aware = datetime.fromisoformat(v_time_str.replace(" ", "T").split("\t")[0])
                    dt_naive = dt_aware.replace(tzinfo=None)
                    
                    versions.append({
                        "id": v_hash[:7],
                        "timestamp": dt_naive,
                        "content": content_res.stdout,
                        "source": "Git Commit"
                    })
        except Exception as e:
            log(f"Error extracting git history: {e}", "ERROR")
            
        return versions

    def _write_human_report(self, file_path: Path):
        try:
            with open(file_path, 'w', encoding='utf-8') as out:
                out.write(f"# UNIFIED FORENSIC REPORT (v12.10)\n")
                out.write(f"Generated at: {datetime.now().isoformat()}\n\n")
                
                for entry in self.report_data:
                    title = "FULL HISTORY" if entry['era_type'] == "FULL" else "PARTIAL HISTORY (Head/Tail)"
                    out.write(f"# {title}\n")
                    out.write(f"**File:** `{entry['file_path']}`\n")
                    out.write(f"**Total Versions:** {entry['total_versions_found']}\n\n")
                    
                    ext = Path(entry['file_name']).suffix.lstrip('.') or "txt"
                    
                    for i, v in enumerate(entry['versions'], 1):
                        dt = v['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                        out.write(f"## v{i:02d} | {v['source']} | {dt} | ID: {v['id']}\n")
                        out.write(f"SHA: `{v['hash'][:12]}`\n")
                        out.write(f"```{ext}\n{v['content']}\n```\n\n---\n\n")
        except Exception as e:
            log(f"Failed to write report {file_path}: {e}", "ERROR")

    def generate_markdown(self):
        log(f"Generating Markdown report: {OUTPUT_FILE_MD}", "WRITE")
        self._write_human_report(OUTPUT_FILE_MD)

    def generate_txt(self):
        log(f"Generating TXT report: {OUTPUT_FILE_TXT}", "WRITE")
        self._write_human_report(OUTPUT_FILE_TXT)

    def generate_json(self):
        log(f"Generating JSON report: {OUTPUT_FILE_JSON}", "WRITE")
        try:
            json_output = {
                "generated_at": datetime.now().isoformat(),
                "files": []
            }

            for entry in self.report_data:
                file_obj = {
                    "path": entry['file_path'],
                    "name": entry['file_name'],
                    "type": entry['era_type'],
                    "total_count": entry['total_versions_found'],
                    "versions": []
                }
                
                for v in entry['versions']:
                    file_obj["versions"].append({
                        "id": v['id'],
                        "source": v['source'],
                        "timestamp": v['timestamp'].isoformat(),
                        "hash": v['hash'],
                        "content": v['content']
                    })
                
                json_output["files"].append(file_obj)

            with open(OUTPUT_FILE_JSON, 'w', encoding='utf-8') as f:
                json.dump(json_output, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log(f"Failed to write JSON: {e}", "ERROR")

if __name__ == "__main__":
    try:
        analyzer = VSCodeForensicAnalyzer()
        analyzer.build_global_index()
        analyzer.run()
    except Exception as e:
        log(f"Critical failure: {e}", "CRITICAL")

