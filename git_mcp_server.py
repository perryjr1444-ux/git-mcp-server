#!/usr/bin/env python3
"""
Git MCP Server - Model Context Protocol server for Git operations
Streamlined repository management through MCP
"""

from fastmcp import FastMCP
import subprocess
import os
from typing import Dict, Any, List, Optional

mcp = FastMCP("Git MCP Server")

@mcp.tool()
async def git_clone(repository_url: str, destination: Optional[str] = None) -> Dict[str, Any]:
    """Clone a git repository"""
    try:
        cmd = ["git", "clone", repository_url]
        if destination:
            cmd.append(destination)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def git_commit(message: str, files: Optional[List[str]] = None) -> Dict[str, Any]:
    """Commit changes to git repository"""
    try:
        # Add files
        if files:
            for file in files:
                subprocess.run(["git", "add", file], check=True)
        else:
            subprocess.run(["git", "add", "."], check=True)
        
        # Commit
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True
        )
        
        return {
            "success": result.returncode == 0,
            "commit_message": message,
            "output": result.stdout
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def git_push(remote: str = "origin", branch: str = "main") -> Dict[str, Any]:
    """Push commits to remote repository"""
    try:
        result = subprocess.run(
            ["git", "push", remote, branch],
            capture_output=True,
            text=True
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def git_status() -> Dict[str, Any]:
    """Get git repository status"""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        
        return {
            "success": result.returncode == 0,
            "status": result.stdout,
            "clean": len(result.stdout.strip()) == 0
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def git_branch_list() -> Dict[str, Any]:
    """List all branches"""
    try:
        result = subprocess.run(
            ["git", "branch", "-a"],
            capture_output=True,
            text=True
        )
        
        branches = [b.strip().lstrip("* ") for b in result.stdout.split("\n") if b.strip()]
        
        return {
            "success": result.returncode == 0,
            "branches": branches
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def git_create_branch(branch_name: str, checkout: bool = True) -> Dict[str, Any]:
    """Create a new branch"""
    try:
        cmd = ["git", "branch", branch_name]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if checkout and result.returncode == 0:
            subprocess.run(["git", "checkout", branch_name], check=True)
        
        return {
            "success": result.returncode == 0,
            "branch": branch_name,
            "checked_out": checkout
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    mcp.run()
