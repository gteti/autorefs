# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [0.3.1](https://github.com/mkdocstrings/autorefs/releases/tag/0.3.1) - 2021-12-27

<small>[Compare with 0.3.0](https://github.com/mkdocstrings/autorefs/compare/0.3.0...0.3.1)</small>

### Code Refactoring
- Support fallback method returning multiple identifiers ([0d2b411](https://github.com/mkdocstrings/autorefs/commit/0d2b411030d23cf65c834c6a881ec8d0efddee8c) by Timothée Mazzucotelli). [Issue #11](https://github.com/mkdocstrings/autorefs/issues/11), [PR #12](https://github.com/mkdocstrings/autorefs/pull/12) and [mkdocstrings#350](https://github.com/mkdocstrings/mkdocstrings/pull/350)


## [0.3.0](https://github.com/mkdocstrings/autorefs/releases/tag/0.3.0) - 2021-07-24

<small>[Compare with 0.2.1](https://github.com/mkdocstrings/autorefs/compare/0.2.1...0.3.0)</small>

### Features
- Add optional-hover ref type ([0288bdd](https://github.com/mkdocstrings/autorefs/commit/0288bdd34f779d73d3da19cfe2a89254fd3c4942) by Brian Koropoff). [PR #10](https://github.com/mkdocstrings/autorefs/pull/10)


## [0.2.1](https://github.com/mkdocstrings/autorefs/releases/tag/0.2.1) - 2021-05-07

<small>[Compare with 0.2.0](https://github.com/mkdocstrings/autorefs/compare/0.2.0...0.2.1)</small>

### Bug Fixes
- Prevent error during parallel installations ([c90e399](https://github.com/mkdocstrings/autorefs/commit/c90e399213dec3435bf5dd0a0e5035ba586076fd) by Timothée Mazzucotelli). [PR #9](https://github.com/mkdocstrings/autorefs/pull/9)


## [0.2.0](https://github.com/mkdocstrings/autorefs/releases/tag/0.2.0) - 2021-05-03

<small>[Compare with 0.1.1](https://github.com/mkdocstrings/autorefs/compare/0.1.1...0.2.0)</small>

### Features
- Allow registering absolute URLs for autorefs ([621686b](https://github.com/mkdocstrings/autorefs/commit/621686b4b36b8d24df80035095700f6a4f96567c) by Oleh Prypin). [PR #8](https://github.com/mkdocstrings/autorefs/pull/8)
- Allow external tools to insert references that are OK to skip ([7619c28](https://github.com/mkdocstrings/autorefs/commit/7619c2835a63b54b1f5e9e11c5f320c04e3579ac) by Oleh Prypin). [PR #7](https://github.com/mkdocstrings/autorefs/pull/7)
- Allow `[``identifier``][]`, understood as `[``identifier``][identifier]` ([2d3182d](https://github.com/mkdocstrings/autorefs/commit/2d3182db54dc33e75914e9c509bbf849842eb70a) by Oleh Prypin). [PR #5](https://github.com/mkdocstrings/autorefs/pull/5)


## [0.1.1](https://github.com/mkdocstrings/autorefs/releases/tag/0.1.1) - 2021-02-28

<small>[Compare with 0.1.0](https://github.com/mkdocstrings/autorefs/compare/0.1.0...0.1.1)</small>

### Packaging

- Remove unused dependencies ([9c6a8e6](https://github.com/mkdocstrings/autorefs/commit/9c6a8e610f52d471fefa02baa4aef2773bdb59c0) by Oleh Prypin).


## [0.1.0](https://github.com/mkdocstrings/autorefs/releases/tag/0.1.0) - 2021-02-17

<small>[Compare with first commit](https://github.com/mkdocstrings/autorefs/compare/fe6faa5d5a7a901605ec8ab98df09dc95067f6a8...0.1.0)</small>

### Features
- Split out "mkdocs-autorefs" plugin from "mkdocstrings" ([fe6faa5](https://github.com/mkdocstrings/autorefs/commit/fe6faa5d5a7a901605ec8ab98df09dc95067f6a8) by Oleh Prypin).
