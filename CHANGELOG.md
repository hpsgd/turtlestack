# Changelog

## [3.4.0](https://github.com/hpsgd/turtlestack/compare/v3.3.1...v3.4.0) (2026-06-14)


### Features

* add agile-coach, delivery-manager, and product-team agents ([#38](https://github.com/hpsgd/turtlestack/issues/38)) ([230f57d](https://github.com/hpsgd/turtlestack/commit/230f57d628b28d6cb9fcbb395ba006bca84b54a8))
* add security baseline pattern hook and session change notices ([#40](https://github.com/hpsgd/turtlestack/issues/40)) ([a5a3c07](https://github.com/hpsgd/turtlestack/commit/a5a3c074f54fdffd44e9998925fc20e5e6290c70))
* multi-instance agent dispatch, hook-test harness, PO boundary fix ([#42](https://github.com/hpsgd/turtlestack/issues/42)) ([186be6b](https://github.com/hpsgd/turtlestack/commit/186be6b1e5a175bd6054543f4f8de49890060c15))

## [3.3.1](https://github.com/hpsgd/turtlestack/compare/v3.3.0...v3.3.1) (2026-05-31)


### Performance Improvements

* **writing-style:** trim tone-and-voice rule under 40k char threshold ([#36](https://github.com/hpsgd/turtlestack/issues/36)) ([6647592](https://github.com/hpsgd/turtlestack/commit/66475924f6dee61be0a4a2f91d7db801eec1cf1c))

## [3.3.0](https://github.com/hpsgd/turtlestack/compare/v3.2.0...v3.3.0) (2026-05-31)


### Features

* expand AI tell coverage + grant producer agents Write/Edit ([#34](https://github.com/hpsgd/turtlestack/issues/34)) ([88600b9](https://github.com/hpsgd/turtlestack/commit/88600b9233bea11e65854fb6b972a22c6e457836))

## [3.2.0](https://github.com/hpsgd/turtlestack/compare/v3.1.0...v3.2.0) (2026-05-29)


### Features

* **plugins:** dockerize runtime deps for publishing, coordinator, web-tools ([#26](https://github.com/hpsgd/turtlestack/issues/26)) ([ee26ce2](https://github.com/hpsgd/turtlestack/commit/ee26ce29035fd8e725035f69723f3634bc417fa2))
* **plugins:** publish runtime images to GHCR with build fallback ([#33](https://github.com/hpsgd/turtlestack/issues/33)) ([1fd9635](https://github.com/hpsgd/turtlestack/commit/1fd9635f8d0574d4b9c4e028668c0a95f200f581))


### Bug Fixes

* **billing-engineer:** strengthen output-skeleton enforcement; preserve no-code constraint ([#31](https://github.com/hpsgd/turtlestack/issues/31)) ([3552ed4](https://github.com/hpsgd/turtlestack/commit/3552ed490eef20eec9903ac45781184abcec512d))
* **dossier:** require dispatch plan in agent's final visible message ([#32](https://github.com/hpsgd/turtlestack/issues/32)) ([85ae7ab](https://github.com/hpsgd/turtlestack/commit/85ae7abadb5498675219d2d0d4d2cbf24c60d3da))
* **investigator:** require positive scope in refusals; re-grade definition-text criteria ([#30](https://github.com/hpsgd/turtlestack/issues/30)) ([d407de3](https://github.com/hpsgd/turtlestack/commit/d407de3449d95abcd1397a311820248bbd6d225b))

## [3.1.0](https://github.com/hpsgd/turtlestack/compare/v3.0.1...v3.1.0) (2026-05-23)


### Features

* **php-developer:** add framework-agnostic PHP plugin ([#24](https://github.com/hpsgd/turtlestack/issues/24)) ([a789bbe](https://github.com/hpsgd/turtlestack/commit/a789bbe0e59fb1187bc8878198968cde402daa72))


### Bug Fixes

* **thinking:** point plugin drift message at the per-marketplace files ([#22](https://github.com/hpsgd/turtlestack/issues/22)) ([9fad01a](https://github.com/hpsgd/turtlestack/commit/9fad01aea65cc4d074e3e36c9839d926fff5962e))

## [3.0.1](https://github.com/hpsgd/turtlestack/compare/v3.0.0...v3.0.1) (2026-05-20)


### Bug Fixes

* **thinking:** derive marketplace name from cache or source path ([#18](https://github.com/hpsgd/turtlestack/issues/18)) ([418ac10](https://github.com/hpsgd/turtlestack/commit/418ac10f761cc6a6038acbbaf0c92a93ea8ffc36))
* **thinking:** sweep orphan marketplace rule files at user level ([#20](https://github.com/hpsgd/turtlestack/issues/20)) ([34cd918](https://github.com/hpsgd/turtlestack/commit/34cd9182769de54c7af2dd083a0c08ef15afe44a))

## [3.0.0](https://github.com/hpsgd/turtlestack/compare/v2.6.2...v3.0.0) (2026-05-20)


### ⚠ BREAKING CHANGES

* **web-tools:** slash commands change from `/workflow-tools:*` to `/web-tools:*`. Consumers must update references — the old commands are no longer available. The skill body of content-retrieval is unchanged.

### Features

* **web-tools:** rename workflow-tools and add web-snapshot skill ([#15](https://github.com/hpsgd/turtlestack/issues/15)) ([46b9801](https://github.com/hpsgd/turtlestack/commit/46b98013f48c2d883831fe428fbb91385393df13))

## [2.6.2](https://github.com/hpsgd/turtlestack/compare/v2.6.1...v2.6.2) (2026-05-18)


### Miscellaneous Chores

* force test release of release-please pipeline ([#13](https://github.com/hpsgd/turtlestack/issues/13)) ([709c995](https://github.com/hpsgd/turtlestack/commit/709c99511f3bc025389abc4e693b9378da0f0b68))
