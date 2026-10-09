# TRACE Edge v1.4 — Installer release project

**This archive is NOT a compiled Windows installer.** The current environment cannot produce or test Windows PE executables. The `.exe` must be built on Windows. The release workflow compiles the installer once; customers only receive `TRACE-Edge-Setup-v1.4.0.exe` and do not run scripts.

## Release engineering
- Push this project to a private repository and run **TRACE Edge Windows Installer** workflow on a Windows runner; or run `desktop/build-windows.ps1` on a Windows build computer, then compile `installer/TRACE-Edge.iss` with Inno Setup 6.
- Distribute only the compiled installer, not this project.
- Verify installer, uninstall, SmartScreen and application launch on a clean Windows VM.

## Scope
- Polished guided desktop configuration preview from v1.3, branded v1.4.
- Does **not** contain live OPC UA discovery, cloud enrollment, Windows Service, telemetry, credential storage, certificate validation or PLC communication.
- Read-only by design; no write controls or OPC UA operations.
- This is NOT production ready and must NOT be connected to production OT equipment.
- Future secure collector/service work requires independent engineering and OT security testing.

## Why no Windows Service?
A service that appears operational without authenticated OPC UA and safe certificate handling would mislead users and create risk. Service installation will be added when the collector is implemented and validated.
