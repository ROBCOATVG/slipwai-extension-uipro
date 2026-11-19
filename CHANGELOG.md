# Changelog

Release notes, newest first, one entry per released version; the entry being written is `changelog.d/`.

## 1.0.1 — PATCH

**CI proves this package against slipwai itself.** Its workflow installed the keel, called the shared release workflow and took the cloud target sources from `ROBCOATVG/slipwai_v2_Fork`, a fork archived on 2026-10-17 and 244 commits behind `ROBCOATVG/slipwai`. All of them now come from `ROBCOATVG/slipwai`; where a commit is pinned, it is the same commit, which both repositories hold. Nothing the package does in a project changes.

## 1.0.0

**uipro ships as an extension package: `slipwai extension install uipro`, elected in a project with
`./init --extension uipro`.** The UI review tooling a project elects, with the check that keeps what it
writes current, and a missing tool reported rather than fatal to `./init`.
