# TRACE Edge v1.4 — GitHub upload package

Upload the **contents** of this package to the root of the existing `jmyall93/trace` repository, preserving `.github/workflows/windows-installer.yml` and `trace-edge/` paths. Do not upload the ZIP itself or nest everything inside another folder.

1. In GitHub, open the repository, select **Add file → Upload files**. GitHub browser uploads may not reliably preserve hidden `.github` directories; if necessary create `.github/workflows/windows-installer.yml` using **Add file → Create new file** and paste the file contents.
2. Commit the new files. Do not overwrite the existing TRACE Cloud files.
3. Open **Actions → TRACE Edge Preview Installer → Run workflow**.
4. When the workflow finishes, download the **artifact** `TRACE-Edge-Setup-v1.4.0-PREVIEW`. GitHub wraps artifacts in a ZIP containing the Windows `.exe`.
5. Test on a Windows test VM. This is a configuration UI preview, NOT a live OPC UA connector. Do not deploy to production OT.

The workflow deliberately does NOT publish a public GitHub Release or enable the TRACE Cloud download button. Only publish after functional/security validation, signing and release approval.
