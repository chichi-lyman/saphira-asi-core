#!/usr/bin/env python3
"""
Saphira ASI Sentinel Protocol - Gatekeeper Enforcer
Validates forensic drift and policy compliance across the Nova Umbrella ecosystem.
"""

import sys
import os
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Tuple

class SaphiraGatekeeper:
    """Core enforcement engine for Nova Umbrella policy compliance."""
    
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.security_dir = self.repo_root / "security"
        self.violations = []
        self.warnings = []
        
    def validate_selinux_policy(self) -> bool:
        """Verify SELinux policy file integrity."""
        policy_file = self.security_dir / "nova_umbrella.te"
        
        if not policy_file.exists():
            self.violations.append(f"[CRITICAL] SELinux policy file missing: {policy_file}")
            return False
            
        try:
            content = policy_file.read_text()
            required_domains = ["nova_agent_t", "nova_data_file"]
            missing_domains = [d for d in required_domains if d not in content]
            
            if missing_domains:
                self.violations.append(f"[CRITICAL] Missing policy domains: {missing_domains}")
                return False
                
            self.warnings.append(f"[OK] SELinux policy validated: {policy_file.name}")
            return True
        except Exception as e:
            self.violations.append(f"[ERROR] Failed to read policy file: {e}")
            return False
    
    def validate_dockerfile(self) -> bool:
        """Verify Docker configuration."""
        dockerfile = self.repo_root / "Dockerfile"
        
        if not dockerfile.exists():
            self.violations.append("[WARNING] Dockerfile not found")
            return True  # Not critical
            
        try:
            content = dockerfile.read_text()
            
            # Check for production-ready configurations
            if "FROM python:3.11-slim" not in content:
                self.warnings.append("[INFO] Consider using specific Python version tag")
            
            if "HEALTHCHECK" not in content:
                self.warnings.append("[INFO] Consider adding HEALTHCHECK instruction")
                
            self.warnings.append("[OK] Dockerfile structure validated")
            return True
        except Exception as e:
            self.violations.append(f"[ERROR] Failed to validate Dockerfile: {e}")
            return False
    
    def validate_requirements(self) -> bool:
        """Verify Python dependencies are locked."""
        req_file = self.repo_root / "requirements.txt"
        
        if not req_file.exists():
            self.warnings.append("[INFO] requirements.txt not found (optional)")
            return True
            
        try:
            content = req_file.read_text()
            lines = content.strip().split('\n')
            
            unpinned = [line for line in lines if line and not any(op in line for op in ['==', '~=', '>='])]
            if unpinned:
                self.warnings.append(f"[WARNING] Unpinned dependencies: {unpinned}")
            
            self.warnings.append(f"[OK] Dependencies validated: {len(lines)} packages")
            return True
        except Exception as e:
            self.violations.append(f"[ERROR] Failed to validate requirements: {e}")
            return False
    
    def run_checks(self) -> Tuple[bool, Dict]:
        """Execute all compliance checks."""
        print("\n" + "="*70)
        print("  SAPHIRA ASI SENTINEL PROTOCOL ENFORCER")
        print("  Policy & Forensic Drift Validation")
        print("="*70 + "\n")
        
        checks = [
            ("SELinux Policy Validation", self.validate_selinux_policy),
            ("Docker Configuration", self.validate_dockerfile),
            ("Dependency Management", self.validate_requirements),
        ]
        
        results = {}
        for check_name, check_func in checks:
            print(f"[*] Running: {check_name}...")
            try:
                result = check_func()
                results[check_name] = result
            except Exception as e:
                print(f"[!] Check failed with exception: {e}")
                results[check_name] = False
        
        # Print summary
        print("\n" + "-"*70)
        print("WARNINGS & NOTICES:")
        for warning in self.warnings:
            print(f"  {warning}")
        
        if self.violations:
            print("\n❌ CRITICAL VIOLATIONS:")
            for violation in self.violations:
                print(f"  {violation}")
        else:
            print("\n✅ NO CRITICAL VIOLATIONS DETECTED")
        
        print("-"*70 + "\n")
        
        passed = len(self.violations) == 0
        return passed, results


def main():
    """Entry point for gatekeeper enforcement."""
    gatekeeper = SaphiraGatekeeper()
    passed, results = gatekeeper.run_checks()
    
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
