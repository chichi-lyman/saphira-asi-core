# Saphira Core: Active Agent Rules
# Lead Architect: Chelsea Megan Woods | Woods Legacies

## Master Directives
- **Zero Drift**: No modification to files under `security/` may bypass `security/gatekeeper_enforcer.py`.
- **Pre-Flight Check**: Before modifying any codebase file, read this file and check if a child `AGENTS.md` exists in the subdirectory you are targeting.
- **Traceability**: Append a natural-language reason ("The Why") to your Git commits explaining your architectural intent.

## Sub-Agent Index
- **Agent-Zero-DevOps**: Handles full-stack orchestration, Docker runtimes, and Firebase setups.
- **Agent-2-RedHat**: Monitors logging structures, performs security audits, and ensures SELinux type compliance.
