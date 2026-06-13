import os
import tempfile
from git import Repo # type: ignore

SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", 
    ".java", ".cpp", ".c", ".h", ".md", ".txt"
}

# FIXED: Changed **pycache** to __pycache__
IGNORED_DIRS = {
    ".git", "node_modules", "dist", "build", "venv", "__pycache__"
}

def load_github_repo(repo_url):
    # FIXED: Removed the markdown code block backticks from here
    temp_dir = tempfile.mkdtemp()
    
    # Optional performance optimization: shallow clone (depth=1) to save time/bandwidth
    Repo.clone_from(repo_url, temp_dir, depth=1)
    
    files = []
    
    for root, dirs, filenames in os.walk(temp_dir):
        # In-place modification of dirs to skip ignored folders
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        
        for filename in filenames:
            extension = os.path.splitext(filename)[1].lower()
            
            if extension not in SUPPORTED_EXTENSIONS:
                continue
                
            file_path = os.path.join(root, filename)
            
            # IMPROVEMENT: Calculate the relative path from the repo root
            # This is essential metadata for your RAG source citations!
            relative_path = os.path.relpath(file_path, temp_dir)
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                files.append({
                    "filename": filename,
                    "relative_path": relative_path,  # Crucial for polaris.ME citations
                    "content": content
                })
            except Exception:
                # Silently skip binaries or unreadable corrupted files
                continue
                
    return files