# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0](https://github.com/bamr87/it-journey/compare/v0.1.0...v0.2.0) (2026-10-27)


### Added

* **agents:** implement the GH-600 disciplines this repo teaches, and map them ([#407](https://github.com/bamr87/it-journey/issues/407)) ([3bb07b6](https://github.com/bamr87/it-journey/commit/3bb07b6c9b33a2807a8c136d6af71527744104e7))
* **ai:** adopt the shared ai-runner kit byte-identically from lifehacker.dev ([23b2157](https://github.com/bamr87/it-journey/commit/23b2157ed5050fc02d4c99e138400dd17a14ee98))
* **ai:** adopt the shared ai-runner kit; hub agent-context + prose kits; fleet manifest ([400a92b](https://github.com/bamr87/it-journey/commit/400a92b90f8913b63bf900490ddf9978de116fb1))
* **ai:** Claude-Code-OAuth content fleet for continuous on-brand improvement ([#378](https://github.com/bamr87/it-journey/issues/378)) ([8f124d8](https://github.com/bamr87/it-journey/commit/8f124d8dcc05cd58df55a857e3340999806b2b60))
* **analytics:** enable client-side PostHog on it-journey.dev ([#518](https://github.com/bamr87/it-journey/issues/518)) ([9bb0af6](https://github.com/bamr87/it-journey/commit/9bb0af60bf60661d89ace12e21fdaf156643875f))
* **automation:** autonomous issue-triage→PR autopilot (off by default) ([#383](https://github.com/bamr87/it-journey/issues/383)) ([565a81b](https://github.com/bamr87/it-journey/commit/565a81b7f2e07275d2955d7727ea6dcbaf098745))
* **cms:** add zer0.json console config for zer0-CMS ([2c0bb2a](https://github.com/bamr87/it-journey/commit/2c0bb2ad3637b945f774e7ff5001b156cda4672d))
* **navigation:** add /tags/ and /categories/ index pages ([888ddd7](https://github.com/bamr87/it-journey/commit/888ddd74a74ac33c84ca5643d1f95ecb643cd393))
* **navigation:** add /tags/ and /categories/ index pages ([1a941d3](https://github.com/bamr87/it-journey/commit/1a941d339d64a8a20b77fd2ff46f89b98fd36659))
* **notes:** turn /notes/ into an interactive workbench ([#634](https://github.com/bamr87/it-journey/issues/634)) ([74de6bc](https://github.com/bamr87/it-journey/commit/74de6bc62b4a73b8a0b9f9efaa0865c2e3eab550))
* **quests:** autonomous quest-perfection loop (gated, staged, safety-gated) ([#394](https://github.com/bamr87/it-journey/issues/394)) ([3332133](https://github.com/bamr87/it-journey/commit/3332133ae00609e8fbc8ddfc04a95a0462bed90f))
* **quests:** capture session screenshots as walkthrough artifacts ([#393](https://github.com/bamr87/it-journey/issues/393)) ([e0f2003](https://github.com/bamr87/it-journey/commit/e0f20038824eeeab78d6a9b86bb9acac7186515b))
* **quests:** daily end-to-end quest walkthrough routine + report ([#390](https://github.com/bamr87/it-journey/issues/390)) ([ab467ee](https://github.com/bamr87/it-journey/commit/ab467eec6f6de01047163159cd69f513a83b8f31))
* **quest:** serve the quest system over MCP so an agent can execute a campaign ([8772216](https://github.com/bamr87/it-journey/commit/877221660ebbf5c8794dfadd2aac29e1d6270047))
* **quest:** serve the quest system over MCP so an agent can execute a campaign ([e7a3939](https://github.com/bamr87/it-journey/commit/e7a3939339098a48dd79a3b6e5a2bbb6979b24c9))
* **quests:** forge the Quest Idea Forge — AI-assisted idea submission portal + gated intake lane ([#417](https://github.com/bamr87/it-journey/issues/417)) ([e4e3763](https://github.com/bamr87/it-journey/commit/e4e3763396ff05a3edec5ab5194f27a969faa607))
* **quests:** harden quest-perfection loop + surface walkthroughs/ledger on the site ([#471](https://github.com/bamr87/it-journey/issues/471)) ([1ee23de](https://github.com/bamr87/it-journey/commit/1ee23dec27910b48e3e7bfe47a46e773687cb186))
* **quests:** per-character skills for the perfection loop's walk + fix lanes ([#668](https://github.com/bamr87/it-journey/issues/668)) ([1235551](https://github.com/bamr87/it-journey/commit/1235551c2b3fcd68632cf4167e5e17adc4ecdb46))
* **quests:** quest-forge issue→epic-quest fleet + The Self-Operating Website campaign ([#365](https://github.com/bamr87/it-journey/issues/365)) ([#384](https://github.com/bamr87/it-journey/issues/384)) ([26c3f1a](https://github.com/bamr87/it-journey/commit/26c3f1ac2d8921a30e81a6977c8ad78b1368d768))
* **theme-scout:** frontend canary that files theme bugs upstream (off by default) ([#385](https://github.com/bamr87/it-journey/issues/385)) ([a7d99d5](https://github.com/bamr87/it-journey/commit/a7d99d5efd0ff4b904cee536a118973ea23d08a0))


### Fixed

* **a11y:** quest skip link lands on the quest body; hero clears the cookie banner ([#831](https://github.com/bamr87/it-journey/issues/831)) ([19876e5](https://github.com/bamr87/it-journey/commit/19876e5532d166d1274e46a9e73f8f8056a2c579))
* **ai:** hash usage-record ids with SHA-256 (CodeQL rb/weak-sensitive-data-hashing) ([63c9c2f](https://github.com/bamr87/it-journey/commit/63c9c2f7744eae0fb4bb7150994dd28b3f4466d0))
* **ci:** only run PR gates on PRs targeting main ([#670](https://github.com/bamr87/it-journey/issues/670)) ([d6454c7](https://github.com/bamr87/it-journey/commit/d6454c705a61d16e86d004e35df7a778c7900eaf))
* **ci:** persist-credentials:false on the remaining create-pull-request lanes ([#416](https://github.com/bamr87/it-journey/issues/416)) ([aee8653](https://github.com/bamr87/it-journey/commit/aee86539ca74673236412d5be65f5237f2734159))
* **ci:** repair invalid quest-perfection workflow + guard workflow validity ([#402](https://github.com/bamr87/it-journey/issues/402)) ([0ccf283](https://github.com/bamr87/it-journey/commit/0ccf2839305d39a1a7af542e8f0e199bf30a63ab))
* **ci:** repair the fleet's daily failures — CMS duplicate auth header + empty plan artifact ([#411](https://github.com/bamr87/it-journey/issues/411)) ([aafd4a1](https://github.com/bamr87/it-journey/commit/aafd4a1be754cda5ad5948286899b669b6e228b9))
* **ci:** scope content review to PRs into main ([#687](https://github.com/bamr87/it-journey/issues/687)) ([3c3a6e8](https://github.com/bamr87/it-journey/commit/3c3a6e8b5a04838310ecd519bd3fd181d50e5416))
* **ci:** skip the brand gate on the gh-pages deploy PR ([#662](https://github.com/bamr87/it-journey/issues/662)) ([1f296ee](https://github.com/bamr87/it-journey/commit/1f296eef3b0a1e9e78b42803844b2725b077f7ac))
* **ci:** stop dependency-checker false-positive spam + retire its auto-update job ([#377](https://github.com/bamr87/it-journey/issues/377)) ([f604454](https://github.com/bamr87/it-journey/commit/f60445453a7646c1c1c7a2854c97a3cb36b96eae))
* **ci:** stop the agentic quest review cancelling itself, skip the deploy PR ([#663](https://github.com/bamr87/it-journey/issues/663)) ([573d0bb](https://github.com/bamr87/it-journey/commit/573d0bb45978866a002c1ecb9e48a2dffc41ebe8))
* **ci:** stop the automated PR lanes manufacturing conflicts and missing merges ([#580](https://github.com/bamr87/it-journey/issues/580)) ([bc3d42a](https://github.com/bamr87/it-journey/commit/bc3d42a6ca30bf899d4a2e99dc4ebd37521a4110))
* **ci:** sync-gh-pages no longer blocks on its own in-progress check ([#408](https://github.com/bamr87/it-journey/issues/408)) ([e9cacd4](https://github.com/bamr87/it-journey/commit/e9cacd46f1c4efea58f528450f00ddbcfddb78ee))
* **ci:** unbreak Link Health Guardian's lychee step and drop its 12-min fetch ([#586](https://github.com/bamr87/it-journey/issues/586)) ([a7f83b6](https://github.com/bamr87/it-journey/commit/a7f83b6c7d0a350a52fb418718418dea0b1953d0))
* **ci:** unbreak the auto-merge lanes — stop watching our own check ([#441](https://github.com/bamr87/it-journey/issues/441)) ([d8313a9](https://github.com/bamr87/it-journey/commit/d8313a9932e030089fedb300bca9e69f39742092))
* **ci:** unbreak the quest-perfection loop's startup failure ([#422](https://github.com/bamr87/it-journey/issues/422)) ([cfeb5e3](https://github.com/bamr87/it-journey/commit/cfeb5e3aa81d7105c9c62069a09c8bc31a1ac864))
* **ci:** unbreak the quest-perfection report job on single-slice sweeps ([#596](https://github.com/bamr87/it-journey/issues/596)) ([c5a00cc](https://github.com/bamr87/it-journey/commit/c5a00ccf1bff8344c3e113b5a00ee3e28780294f))
* **ci:** workflow-minted sealed quest evidence, one consolidated report PR, dispatch-only standalone walkthrough ([#433](https://github.com/bamr87/it-journey/issues/433)) ([fd933c1](https://github.com/bamr87/it-journey/commit/fd933c18b26c2b146edfdb6f7373c90d117a70d1))
* **config:** repair broken image paths + dead sidebar nav mode ([#543](https://github.com/bamr87/it-journey/issues/543)) ([5ab3372](https://github.com/bamr87/it-journey/commit/5ab3372a5f3195ccdea526b1b8db2157cae7ea3c))
* **content:** add the leading slash to 164 quest preview paths ([aaee338](https://github.com/bamr87/it-journey/commit/aaee3380f3a9115bf73d82381c7b62ddf37556fb))
* **content:** add the leading slash to 164 quest preview paths ([e868f3e](https://github.com/bamr87/it-journey/commit/e868f3e8275a7b6f5367c0813958d518c9900f80))
* **deps:** add darwin and windows platforms to Gemfile.lock ([#497](https://github.com/bamr87/it-journey/issues/497)) ([c76fbc2](https://github.com/bamr87/it-journey/commit/c76fbc2a4b11a923baab6792279d71428d9837cd))
* **deps:** floor github-pages at &gt;= 232 so Bundler cannot walk it back ([c964728](https://github.com/bamr87/it-journey/commit/c9647284bce3f10e825246b54537189b4d77f4fa))
* **deps:** stop committing Gemfile.lock (fleet never-commit policy) ([e267acc](https://github.com/bamr87/it-journey/commit/e267accca18f53bcda6817a3f5d695a674d448ed))
* **home:** render real stats server-side and use the existing webp previews ([6dc53eb](https://github.com/bamr87/it-journey/commit/6dc53eb3bc3720e7cab8e7049a8d20b6e3dd977a))
* **home:** render real stats server-side and use the existing webp previews ([741fea7](https://github.com/bamr87/it-journey/commit/741fea725d9c9f3ba1c85870ebd5a35555667fce))
* **links:** repair sister-site link rot — BASH domain, lifehacker deep links, blog redirects ([#582](https://github.com/bamr87/it-journey/issues/582)) ([504a92d](https://github.com/bamr87/it-journey/commit/504a92dbc8a127db16631725755c86276a5097b0))
* **mobile:** main-nav menu, horizontal overflow, uncloseable sidebar ([#380](https://github.com/bamr87/it-journey/issues/380)) ([442d163](https://github.com/bamr87/it-journey/commit/442d16341181ba23cd1c6ffb5acad53b44e5464c))
* **notes:** resolve wiki links against the index's actual field name ([#636](https://github.com/bamr87/it-journey/issues/636)) ([df453ef](https://github.com/bamr87/it-journey/commit/df453ef0b0c8cd77f647cd25bb6fb0b1eabede58))
* **pages:** unbreak the site build; split the quest loop into walk + fix lanes ([#572](https://github.com/bamr87/it-journey/issues/572)) ([43daaf6](https://github.com/bamr87/it-journey/commit/43daaf6e6762df01f1b2419471304e7522ef0b87))
* **privacy:** require analytics consent before GA and PostHog load ([#828](https://github.com/bamr87/it-journey/issues/828)) ([d2b6631](https://github.com/bamr87/it-journey/commit/d2b6631207f9b90aacadb8c4262514d8ff2fe7b0))
* **quest-perfection:** diagnose auth vs rate-limit, stop red runs from withholding deploys ([#641](https://github.com/bamr87/it-journey/issues/641)) ([817e751](https://github.com/bamr87/it-journey/commit/817e7510dd2cf9f00b318aa68a179dd18f832b58))
* **quest-perfection:** keep genuinely-unexpected wipeouts loud, not silently green ([#643](https://github.com/bamr87/it-journey/issues/643)) ([b94fff3](https://github.com/bamr87/it-journey/commit/b94fff3643a83dd252b5e74700d3792233bfee97))
* **quest:** clarify the empty prerequisite slot and give /search/ an h1 ([7940070](https://github.com/bamr87/it-journey/commit/7940070e6b552c7368ff546cae1ccce40acb2c00))
* **quest:** clarify the empty prerequisite slot and give /search/ an h1 ([a343d71](https://github.com/bamr87/it-journey/commit/a343d716ef74d4fac45346c8f580ffa81658c331))
* **quest:** name missing arguments, and let a harness prove the quest was read ([ada376a](https://github.com/bamr87/it-journey/commit/ada376af7f275f478a1efd4af6841486ebfe3fcf))
* **quests:** Agentic Codex hub + Learn weight ranges (P0) ([c55c804](https://github.com/bamr87/it-journey/commit/c55c804216c830e83ee8ec6247b3215a1a9a3b6b))
* **quests:** capstone seals/rubric use Learn ranges; drop fake /100 scoring ([0bd1a69](https://github.com/bamr87/it-journey/commit/0bd1a6985582b0bb186079a84c0f8b3e558abd4b))
* **quests:** Ch I cite Learn D1 15–20% range, not fixed 18% ([6037f7e](https://github.com/bamr87/it-journey/commit/6037f7e9ac49fa75fea978195fd77294ce12a9e0))
* **quests:** Ch III cite Learn D3 10–15% range, not fixed 19% ([b96c682](https://github.com/bamr87/it-journey/commit/b96c68215fc18713f606344a8b5dc4545a0de419))
* **quests:** Ch VI cite Learn D6 10–15% range, not fixed 9% ([f6b0a38](https://github.com/bamr87/it-journey/commit/f6b0a387038ab694af953dcb9f13c07a09805259))
* **quests:** count quests and render start-here XP from one source ([#829](https://github.com/bamr87/it-journey/issues/829)) ([8347a7a](https://github.com/bamr87/it-journey/commit/8347a7a8a968a282b53135dafc87e6d3e7575d64))
* **quests:** give level pages a linked Obsidian-style quest graph ([#524](https://github.com/bamr87/it-journey/issues/524)) ([66c6bc7](https://github.com/bamr87/it-journey/commit/66c6bc73faaf2664a31789fc955efbc579e0f435))
* **quests:** hello-noob shows prerequisites once and unlocks begin-your-it-journey ([#830](https://github.com/bamr87/it-journey/issues/830)) ([f7e33b9](https://github.com/bamr87/it-journey/commit/f7e33b9b33d3f94dae700940f2a878116907d521))
* **quests:** repair bashcrawl quests — headers, navigation bugs, accuracy & clarity ([#392](https://github.com/bamr87/it-journey/issues/392)) ([1634892](https://github.com/bamr87/it-journey/commit/1634892aeb417d7954d2c7c9dea392b02f8595ae))
* **quests:** repair Liquid raw nesting that broke the production Pages build ([#387](https://github.com/bamr87/it-journey/issues/387)) ([158e1d7](https://github.com/bamr87/it-journey/commit/158e1d7a4993847906b44b1cf91d5f9eb8d70fa8))
* **quests:** repair verified walkthrough issues [developer/0001] ([#533](https://github.com/bamr87/it-journey/issues/533)) ([1b073f4](https://github.com/bamr87/it-journey/commit/1b073f495786d518a2e938c677f826caf3748f4c))
* **quests:** repair verified walkthrough issues [developer/0001] ([#547](https://github.com/bamr87/it-journey/issues/547)) ([11016ef](https://github.com/bamr87/it-journey/commit/11016ef4253b203125bd0894654c60e1f4fe0492))
* **quests:** repair verified walkthrough issues [developer/0001] ([#564](https://github.com/bamr87/it-journey/issues/564)) ([1bfc2e9](https://github.com/bamr87/it-journey/commit/1bfc2e99b120d96e6da44ed42c4492a46f9b8cbf))
* **quests:** repair verified walkthrough issues [developer/0001] ([#706](https://github.com/bamr87/it-journey/issues/706)) ([160aad6](https://github.com/bamr87/it-journey/commit/160aad6b69507eb31097eff36af457e6c71adeb9))
* **quests:** repair verified walkthrough issues [developer/0001] ([#714](https://github.com/bamr87/it-journey/issues/714)) ([662c643](https://github.com/bamr87/it-journey/commit/662c64317c937d8e9efe127b5788d25b06e27d02))
* **quests:** repair verified walkthrough issues [developer/0100] ([#465](https://github.com/bamr87/it-journey/issues/465)) ([c660607](https://github.com/bamr87/it-journey/commit/c6606071b737c1a650bfa975d3366b6840118f0a))
* **quests:** repair verified walkthrough issues [developer/0100] ([#501](https://github.com/bamr87/it-journey/issues/501)) ([8be9f34](https://github.com/bamr87/it-journey/commit/8be9f34f3358c78d8d58a0f8104409087008d2f7))
* **quests:** repair verified walkthrough issues [developer/0110] ([#476](https://github.com/bamr87/it-journey/issues/476)) ([514279e](https://github.com/bamr87/it-journey/commit/514279e2cba851e17a3396a396f8cd3ba93108c6))
* **quests:** repair verified walkthrough issues [developer/0111] ([#484](https://github.com/bamr87/it-journey/issues/484)) ([85ee9ef](https://github.com/bamr87/it-journey/commit/85ee9ef7a1e2cd8ae14a7c4c4a195c24003cd794))
* **quests:** repair verified walkthrough issues [developer/1110] ([#492](https://github.com/bamr87/it-journey/issues/492)) ([221a223](https://github.com/bamr87/it-journey/commit/221a223c8cfb6ac57877a065bb1e9fe6595c03d3))
* **quests:** repair verified walkthrough issues [digital-artist/0001] ([#667](https://github.com/bamr87/it-journey/issues/667)) ([995b6eb](https://github.com/bamr87/it-journey/commit/995b6eb7a68dcceb9fe10e49caa66b3445cf8ec4))
* **quests:** repair verified walkthrough issues [digital-artist/0001] ([#679](https://github.com/bamr87/it-journey/issues/679)) ([b500b16](https://github.com/bamr87/it-journey/commit/b500b16c21f6d5e5aa6a36e178e251d90904cee8))
* **quests:** repair verified walkthrough issues [digital-artist/0001] ([#685](https://github.com/bamr87/it-journey/issues/685)) ([5ca4510](https://github.com/bamr87/it-journey/commit/5ca451072d614310cf34bce5404cdb58ad7e9524))
* **quests:** repair verified walkthrough issues [digital-artist/0001] ([#696](https://github.com/bamr87/it-journey/issues/696)) ([06e456f](https://github.com/bamr87/it-journey/commit/06e456f6129459151dace3dd64c30e700e861ea7))
* **quests:** repair verified walkthrough issues [digital-artist/0001] ([#705](https://github.com/bamr87/it-journey/issues/705)) ([8198405](https://github.com/bamr87/it-journey/commit/8198405be70083f6328f40a771ed3790403e29b3))
* **quests:** repair verified walkthrough issues [digital-artist/0001] ([#713](https://github.com/bamr87/it-journey/issues/713)) ([64a138c](https://github.com/bamr87/it-journey/commit/64a138c453fbfee96372db637d7c8d2099efbafb))
* **quests:** repair verified walkthrough issues [digital-artist/0001] ([#727](https://github.com/bamr87/it-journey/issues/727)) ([062251d](https://github.com/bamr87/it-journey/commit/062251d5f798b0d1f5c38f3ff331efbd174b0c8a))
* **quests:** repair verified walkthrough issues [digital-artist/0111] ([#726](https://github.com/bamr87/it-journey/issues/726)) ([f641240](https://github.com/bamr87/it-journey/commit/f6412406e8783cbed45b91f42845634cc661c908))
* **quests:** repair verified walkthrough issues [game-developer/0001] ([#648](https://github.com/bamr87/it-journey/issues/648)) ([cb0803c](https://github.com/bamr87/it-journey/commit/cb0803c426a6b309df0751b5cce77a45a7341022))
* **quests:** repair verified walkthrough issues [game-developer/0001] ([#657](https://github.com/bamr87/it-journey/issues/657)) ([5041fac](https://github.com/bamr87/it-journey/commit/5041fac33925ec8325aaf4d0d6103b94523023f3))
* **quests:** repair verified walkthrough issues [security-specialist/0010] ([#445](https://github.com/bamr87/it-journey/issues/445)) ([08ca5d1](https://github.com/bamr87/it-journey/commit/08ca5d1cc26104794d39429740acaaa4ba55703e))
* **quests:** repair verified walkthrough issues [security-specialist/1000] ([#453](https://github.com/bamr87/it-journey/issues/453)) ([96d8e03](https://github.com/bamr87/it-journey/commit/96d8e039fe6faade29c30e69c693385ffbc859b0))
* **quests:** repair verified walkthrough issues [security-specialist/1011] ([#478](https://github.com/bamr87/it-journey/issues/478)) ([ea37abb](https://github.com/bamr87/it-journey/commit/ea37abbbf1fcb3725b091b15b5ad16a1b180ef04))
* **quests:** repair verified walkthrough issues [security-specialist/1011] ([#494](https://github.com/bamr87/it-journey/issues/494)) ([0c4d11f](https://github.com/bamr87/it-journey/commit/0c4d11fa75aee98ef474ae55a52ba6717fbebcd5))
* **quests:** repair verified walkthrough issues [security-specialist/1011] ([#503](https://github.com/bamr87/it-journey/issues/503)) ([36b3bfb](https://github.com/bamr87/it-journey/commit/36b3bfbbc63158021353a7c02aed467becc3c27b))
* **quests:** repair verified walkthrough issues [security-specialist/1011] ([#535](https://github.com/bamr87/it-journey/issues/535)) ([ee68151](https://github.com/bamr87/it-journey/commit/ee681518142114fe5a4dcc09eeb5a8d4f8153797))
* **quests:** repair verified walkthrough issues [security-specialist/1011] ([#541](https://github.com/bamr87/it-journey/issues/541)) ([281bf39](https://github.com/bamr87/it-journey/commit/281bf39c1cc91432e382e022ce4ceaed50fd6118))
* **quests:** repair verified walkthrough issues [security-specialist/1011] ([#558](https://github.com/bamr87/it-journey/issues/558)) ([112b5cf](https://github.com/bamr87/it-journey/commit/112b5cf331a72474689e35a456a15eadba1b084f))
* **quests:** repair verified walkthrough issues [security-specialist/1011] ([#565](https://github.com/bamr87/it-journey/issues/565)) ([5c65dbf](https://github.com/bamr87/it-journey/commit/5c65dbf992c80428da8d04252101e28cb65a1c41))
* **quests:** repair verified walkthrough issues [security-specialist/1011] ([#570](https://github.com/bamr87/it-journey/issues/570)) ([ed1b1f4](https://github.com/bamr87/it-journey/commit/ed1b1f4c69a364f3e3ff8067ecd5bd1bf7e96132))
* **quests:** repair verified walkthrough issues [security-specialist/1110] ([#486](https://github.com/bamr87/it-journey/issues/486)) ([5432c53](https://github.com/bamr87/it-journey/commit/5432c53ae0cfb28c5278d8051da61a6f4f4ff400))
* **quests:** repair verified walkthrough issues [system-engineer/0101] ([#502](https://github.com/bamr87/it-journey/issues/502)) ([c881734](https://github.com/bamr87/it-journey/commit/c881734a8c495e5d9a9a3d60ec976703a75be462))
* **quests:** repair verified walkthrough issues [system-engineer/0101] ([#569](https://github.com/bamr87/it-journey/issues/569)) ([c64f2c8](https://github.com/bamr87/it-journey/commit/c64f2c8e49f91b504f931b811d6dd09ec8ae52c5))
* **quests:** repair verified walkthrough issues [system-engineer/1001] ([#477](https://github.com/bamr87/it-journey/issues/477)) ([4ff179c](https://github.com/bamr87/it-journey/commit/4ff179c0e8e05f5bf962d2bf223db1f95178255a))
* **quests:** repair verified walkthrough issues [system-engineer/1001] ([#516](https://github.com/bamr87/it-journey/issues/516)) ([2446cd9](https://github.com/bamr87/it-journey/commit/2446cd9b8e251604c93a483ddf230ffb998b1351))
* **quests:** repair verified walkthrough issues [system-engineer/1001] ([#540](https://github.com/bamr87/it-journey/issues/540)) ([c8948ec](https://github.com/bamr87/it-journey/commit/c8948ec170eb4b94364c7a82fce092d0b7b1bec5))
* **quests:** repair verified walkthrough issues [system-engineer/1001] ([#557](https://github.com/bamr87/it-journey/issues/557)) ([236e828](https://github.com/bamr87/it-journey/commit/236e82820d4fa9ca4f8bd5ddbda16cbfd6537668))
* **quests:** repair verified walkthrough issues [system-engineer/1010] ([#485](https://github.com/bamr87/it-journey/issues/485)) ([f2a62d6](https://github.com/bamr87/it-journey/commit/f2a62d67fbfcc18256ca92438f5a8584e5a4f278))
* **quests:** rotate a bounded quest window per run + accumulate coverage across days ([#438](https://github.com/bamr87/it-journey/issues/438)) ([dca2714](https://github.com/bamr87/it-journey/commit/dca27143392d73fa1a75173ed0045300be808918))
* **quests:** thin Agentic Codex hub; Learn weight ranges only ([df002c5](https://github.com/bamr87/it-journey/commit/df002c5446cbd858865142acfbf36449c57c6d20))
* unbreak Pages deploy — orphan endraw in 0010 quest + the two CI holes that let it merge ([#449](https://github.com/bamr87/it-journey/issues/449)) ([aab6c5b](https://github.com/bamr87/it-journey/commit/aab6c5b1edf8c0affe5814f684082cb5f0a4a739))


### Changed

* **agents:** streamline and update AI agents guide for clarity and relevance ([a8576c2](https://github.com/bamr87/it-journey/commit/a8576c2a566eea75d34e1917d502e894d2bbe0a0))
* **assets:** compress site images to WebP and install zer0-image-generator ([#598](https://github.com/bamr87/it-journey/issues/598)) ([e9a8f0b](https://github.com/bamr87/it-journey/commit/e9a8f0baf0171d99bafcc5f54fb1209900cd99ce))
* bump posthog-ruby from 3.19.0 to 3.21.0 in the ruby group ([#549](https://github.com/bamr87/it-journey/issues/549)) ([f481b24](https://github.com/bamr87/it-journey/commit/f481b24cd3b81a6f0eae37e98334c74c779a82e6))
* **quest-loop:** pin Sonnet-class models per stage, adaptive turn budgets, budget-overrun becomes a scored fail ([#644](https://github.com/bamr87/it-journey/issues/644)) ([4decfcc](https://github.com/bamr87/it-journey/commit/4decfcc0a1d5f98cc2d5acc4c258e629b69bb4ed))
* **quests:** start the quest graph (data, cytoscape, layout) only when it nears the viewport ([#832](https://github.com/bamr87/it-journey/issues/832)) ([c1249d9](https://github.com/bamr87/it-journey/commit/c1249d978f265e501ea2ae072bbded6c79798c8a))


### Documentation

* add DailyDebian chmod calculator to Armoury resources ([#818](https://github.com/bamr87/it-journey/issues/818)) ([f03658d](https://github.com/bamr87/it-journey/commit/f03658d4e24f5009bfa91b06019e86fa5f859cef))
* add feature catalog, constitution and amendments; link PRD ([#846](https://github.com/bamr87/it-journey/issues/846)) ([a1c0c60](https://github.com/bamr87/it-journey/commit/a1c0c606820f38c32404843483c18d9f57ba8104))
* **agents:** seed the hub agent-context kit v0.4.0 and the fleet manifest ([dbb8873](https://github.com/bamr87/it-journey/commit/dbb88733b12362272f4b832cb68b46e8bf090273))
* **changelog:** merge duplicate Unreleased headings into one section ([#824](https://github.com/bamr87/it-journey/issues/824)) ([f435444](https://github.com/bamr87/it-journey/commit/f4354440a3fe50b971c4f874bd795ae430b1c445))
* **claude:** document the zer0 stack consumer layout ([d723bd5](https://github.com/bamr87/it-journey/commit/d723bd5fe113213a8f5f08975d7e4c63de350416))
* harmonize documentation to the fleet docs framework ([#847](https://github.com/bamr87/it-journey/issues/847)) ([e347ef7](https://github.com/bamr87/it-journey/commit/e347ef7c022c20a80f6d9e364e8a65fc5dd7f847))
* **quest:** add FrontendAtlas practice resource ([#674](https://github.com/bamr87/it-journey/issues/674)) ([6d35f85](https://github.com/bamr87/it-journey/commit/6d35f85c574b363985d5d66338f043ed357128a3))
* **quests:** capstone Needs GitHub + Copilot workbench callout ([b9bea79](https://github.com/bamr87/it-journey/commit/b9bea79e07c0bb840318239dbebeba6bd0fbf28f))
* **quests:** Ch I workbench Demoed locally / Needs GitHub callout ([0d8b613](https://github.com/bamr87/it-journey/commit/0d8b6134f2d6607ffb80e8e63c411ec20077ad1b))
* **quests:** Ch II workbench Demoed locally / Needs GitHub callout ([64968ed](https://github.com/bamr87/it-journey/commit/64968edb4348a377718caae93f3328ef462646a4))
* **quests:** Ch III workbench Demoed locally / Needs GitHub callout ([52f54f5](https://github.com/bamr87/it-journey/commit/52f54f5ecc2a3f77cc1d73c196e81c7e628795f4))
* **quests:** Ch IV workbench Demoed locally / Needs GitHub callout ([56c51af](https://github.com/bamr87/it-journey/commit/56c51afb73c181069ff42ae406681797d40dde5f))
* **quests:** Ch V workbench Demoed locally / Needs GitHub callout ([635d09b](https://github.com/bamr87/it-journey/commit/635d09b1a24edb26bc919f3aa682cfa4f942d77d))
* **quests:** Ch VI workbench Demoed locally / Needs GitHub callout ([28651cc](https://github.com/bamr87/it-journey/commit/28651cccbad8dc06b5d1331794f2b6d4cb200c69))
* **readme:** align README with the portfolio standard ([#827](https://github.com/bamr87/it-journey/issues/827)) ([ce8dad9](https://github.com/bamr87/it-journey/commit/ce8dad90651a4bf90a3c0c94cd145b00d3203379))
* **theme:** document the remote_theme consumption contract ([#627](https://github.com/bamr87/it-journey/issues/627)) ([b351842](https://github.com/bamr87/it-journey/commit/b351842dede750a86bd09d46e1c148ab28b48c0b))

## [Unreleased]

### Added

- **`/tags/` and `/categories/` index pages** — every tag and category chip on the site linked to `/tags/#<slug>` or `/categories/#<slug>` (2,406 links), and both pages were 404. `pages/tags.md` and `pages/categories.md` now render one anchored section per term via `_includes/content/taxonomy-index.html`: plain Liquid, GitHub Pages-safe, one sorted pass, under 1 s of build time. Collections get a tag section too, because the theme's collection badge links there
- **Bashcrawl quest hub rewrite** — `pages/_quests/0000/bashcrawl/README.md` fully rewritten with Mermaid dungeon map, chapter guide table, quick-start command, and play-mode reference; links to all 10 side-quests
- **Bashcrawl launcher script v3.0.0** — `pages/_quests/0000/bashcrawl/bash_crawl.sh` with `tutorial`/`agent` subcommands, `--quest <chamber>` flag, and 7-option interactive menu
- **10 Bashcrawl side-quests** — Full dungeon coverage: entrance, workshop, cellar, armoury, chamber, hidden-chapel, vault, scrap, rift, and agent-mode; all score 92 % on the quest validator (0 errors, 0 warnings)
- **Quest network graph data** — `assets/data/quest-network.json` and `_data/quests/network.yml` generated by `scripts/quest/build-quest-network.py` (150 nodes, 63 edges)
- **Quest dependency graph include** — `_includes/content/quest-graph.html`: JS-driven Mermaid flowchart, filterable by level ({% raw %}`{% include content/quest-graph.html level="0001" %}`{% endraw %})
- **Quest backlinks include** — `_includes/content/quest-backlinks.html`: lists quests that depend on the current page, loaded from the quest network JSON
- **Quest network builder script** — `scripts/quest/build-quest-network.py` scans all quest frontmatter and produces the node/edge JSON and YAML files
- **Quest permalink audit prompt** — `.github/prompts/quest-permalink-audit.prompt.md` for auditing and repairing quest permalink conventions
- **Quest permalink migration script** — `scripts/quest/migrate-permalinks.py` batch-migrates all quest files to canonical permalink format

- **Canonical frontmatter reference** — `.github/FRONTMATTER.md` documents the required schema for `.prompt.md` and `.instructions.md` files
- **Posts authoring standards** — `pages/_posts/README.md` documents directory layout, file naming, required frontmatter, validation tooling, link hygiene, draft lifecycle, and the cleanup metrics history (#239)
- **Posts CI workflow** — `.github/workflows/posts-markdown-lint.yml` runs `markdownlint-cli2` on PRs touching `pages/_posts/**`; supports manual `--fix` mode (#239)
- **Posts-scoped lint config** — `pages/_posts/.markdownlint.json` extends repo-root config, disabling MD025/MD036/MD040/MD060 and widening MD033 allowed elements for legitimate blog-content patterns (#239)
- **Frontmatter auto-fix script** — `scripts/validation/fix-frontmatter.py` idempotently fills missing `date` (from filename), `categories` (from folder), and `description` (from first prose paragraph) (#239)
- **External link-rot baseline** — `link-check-results/posts-external-baseline.md` catalogs 18 known-broken external links with status and remediation strategy (#239)
- **AI-generated preview images** — 11 DALL-E previews under `assets/images/previews/` for `devops/` posts that previously had empty `preview:` fields (#239)

- **New Post: `foundational-ci-cd-pipelines-github-vscode-extensions.md`** (`pages/_posts/devops/`) - Tutorial on building production-ready CI/CD pipelines for VS Code extensions with GitHub Actions, covering linting, testing, building, and automated Marketplace publishing
- **Lychee Configuration** (`.lychee.toml`) - Declarative configuration for lychee link checker with cross-run caching, performance tuning, and URL exclusions
- **Broken Links Baseline** (`link-check-results/broken_links_baseline.json`) - Baseline of known broken links for delta-based AI analysis
- **Preview Images** - Generated preview banner for the new CI/CD pipelines blog post (original + enhanced variant)

- **New Post: `terminal-bash-finance-accounting.md`** (`pages/_posts/business/`) - Comprehensive blog post targeting finance and accounting professionals, teaching terminal and bash scripting through relatable spreadsheet analogies. Includes real-world month-end automation script, Excel-to-Bash translation table, and links to Terminal Fundamentals, Bashcrawl, and Bashrun quests.

- **Resource Codex** (`pages/_quests/0000/bashcrawl/README.md`) - Added links to the Bash Cheatsheet and Complete BASH Reference in the bashcrawl quest.
- **Practical Application Section** (`pages/_docs/terminal/bash-complete-reference.md`) - Added links to interactive quests (`bashcrawl` and `bash-run`) to practice bash commands.

- **Complete BASH Reference** (`pages/_docs/terminal/bash-complete-reference.md`) - Exhaustive 4600+ line GNU Bash reference covering built-in commands, parameter expansion, arrays, string manipulation, arithmetic, conditionals, loops, functions, process control, text processing, networking, and advanced scripting techniques
- **Docs navigation entry** (`_data/navigation/docs.yml`) - Added "Complete BASH Reference" link under Terminal section
- **Cursor command** (`.cursor/commands/commit-publish.md`) - Workflow command aligned with IT-Journey commit/publish standards

- **Quest Registry** (`scripts/quest/quest_registry.py`) - New single source of truth for quest level metadata including level order, tier groupings, canonical metadata, and permalink utilities
- **Git Basics Quest Enhancement** (`pages/_quests/0000/git-basics.md`) - Major content expansion:
  - Added Mermaid diagrams: quest network position, three areas flowchart, branch lifecycle, local-remote sync, undo decision flowchart, and full quest flow
  - Added Chapter 4: "Undoing Mistakes — The Time-Travel Spells" covering restore, reset, and revert
  - Added checkpoints with validation commands and knowledge checks for Chapters 1–3
  - Replaced generic challenges with structured Implementation Challenges (Chronicle Keeper, Branch Weaver, Remote Ranger)
  - Added Boss Battle: "The Git Gauntlet" — a multi-phase capstone exercise with verification script
  - Expanded Quest Rewards with achievement badges, skills unlocked, and journey progress
  - Enhanced References section with categorized resources (documentation, interactive, quick references)

- **Quest Validation CI Workflow** (`quest-validation.yml`) - New GitHub Actions workflow for automated quest validation on PRs and pushes
- **Full Audit Report** (`test/quest-validator/full-audit-report.json`) - Comprehensive quest audit results (136 quests, 0 errors, 93.9% avg score)

- **`_includes/components/powered-by.html`** - New reusable component for displaying "Powered by" technology cards
  - Bootstrap 5 responsive card grid (1 column mobile, 3 columns desktop)
  - Graceful handling of empty/null version numbers
  - Dynamic Bootstrap icons support
- **`_includes/components/README.md`** - Documentation for the new components directory
- **`site.resources`** configuration block - External resource links for GitHub, RubyGems, Docker Hub
- **`scripts/quest/update-quest-home.py`** - Generate and inject an auto-updated quest index into `pages/_quests/home.md`.
- **`_data/navigation/README.md`** - New documentation for navigation schema with zer0-mistakes v0.17+ compatibility notes

#### Phase 5: Master Tier Quest Generation (Levels 1100-1111)
- **32 New Quests**: Complete Master Tier quest generation across 4 levels
  - **Level 1100 - Data Engineering** (5 new quests):
    - `apache-spark.md` - Big Data Processing with Spark
    - `data-quality.md` - Data Quality & Validation
    - `data-warehousing.md` - Data Warehouse Design
    - `etl-pipeline-design.md` - ETL Pipeline Architecture
    - `stream-processing.md` - Real-time Data Streams
  - **Level 1101 - Machine Learning & AI** (8 new quests):
    - `ai-ethics.md` - Responsible AI Development
    - `computer-vision.md` - Image & Video Analysis
    - `deep-learning-frameworks.md` - TensorFlow & PyTorch
    - `ml-fundamentals.md` - Machine Learning Basics
    - `mlops.md` - ML Operations & Deployment
    - `natural-language-processing.md` - NLP Fundamentals
    - `neural-networks.md` - Deep Learning Architecture
    - `python-data-science.md` - Python for Data Science
  - **Level 1110 - Architecture & Design** (7 new quests):
    - `api-gateway-patterns.md` - API Gateway Design
    - `design-patterns.md` - Software Design Patterns
    - `domain-driven-design.md` - DDD Principles
    - `event-driven-design.md` - Event-Driven Architecture
    - `microservices-architecture.md` - Microservices Design
    - `scaling-strategies.md` - Horizontal & Vertical Scaling
    - `system-design-interviews.md` - System Design Practice
  - **Level 1111 - Leadership & Innovation** (8 new quests):
    - `architecture-reviews.md` - Technical Review Process
    - `building-technical-communities.md` - Community Building
    - `career-advancement.md` - IT Career Growth
    - `innovation-rnd.md` - R&D Leadership
    - `mentorship-programs.md` - Mentoring Skills
    - `open-source-contribution.md` - OSS Contribution
    - `tech-speaking-writing.md` - Technical Communication
    - `technical-leadership.md` - Tech Lead Skills

#### Quest Validation Improvements
- **Quest Template Update**: Added `fmContentType: quest` field to `.frontmatter/templates/quests.md`
- **Validation Rules Documentation**: Added comprehensive validation rules section to `.github/instructions/quest.instructions.md` including:
  - Required frontmatter fields table
  - Enhanced fields table
  - Content structure validation requirements
  - Difficulty level guidelines
  - Binary level system reference
  - Validation commands and score thresholds
  - Common issues and fixes guide

#### Phase 4: Expert Tier Quest Generation (Phases 1-4 Complete)
- **72 New Placeholder Quests**: Complete quest generation across 4 phases
  - **Phase 2 - Apprentice Tier** (Levels 0000-0011): 17 quests
    - Level 0000: `terminal-fundamentals.md`, `git-basics.md`, `markdown-mastery.md`
    - Level 0001: `github-pages-basics.md`, `jekyll-fundamentals.md`, `liquid-templating.md`, `yaml-configuration.md`, `git-workflow-mastery.md`
    - Level 0010: `advanced-markdown.md`, `css-styling-basics.md`, `javascript-fundamentals.md`, `bootstrap-framework.md`
    - Level 0011: `advanced-git-workflows.md`, `jekyll-plugins.md`, `seo-optimization.md`, `analytics-integration.md`, `custom-domains.md`
  - **Phase 3 - Journeyman Tier** (Levels 0100-0111): 36 quests
    - Level 0100: `container-fundamentals.md`, `docker-compose-orchestration.md`
    - Level 0101: 8 CI/CD quests (`cicd-fundamentals.md`, `github-actions-basics.md`, `testing-integration.md`, etc.)
    - Level 0110 (NEW): 8 database quests (`database-fundamentals.md`, `sql-mastery.md`, `data-modeling.md`, etc.)
    - Level 0111 (NEW): 7 API quests (`api-fundamentals.md`, `rest-principles.md`, `api-authentication.md`, etc.)
  - **Phase 4 - Expert Tier** (Levels 1000-1011): 19 quests
    - Level 1000 (NEW): 6 cloud quests (`cloud-computing-fundamentals.md`, `aws-essentials.md`, `infrastructure-as-code.md`)
    - Level 1001 (NEW): 4 Kubernetes quests (`kubernetes-fundamentals.md`, `k8s-pods-workloads.md`, `k8s-services-networking.md`, `k8s-config-secrets.md`)
    - Level 1010: 5 monitoring quests (`monitoring-fundamentals.md`, `prometheus-grafana.md`, `elk-stack.md`, `distributed-tracing.md`, `alerting-systems.md`)
    - Level 1011: 5 security quests (`security-fundamentals.md`, `threat-modeling.md`, `secure-coding.md`, `penetration-testing.md`, `compliance-standards.md`)

#### Quest Infrastructure & Automation
- **Quest Generation Script**: `scripts/generate-placeholder-quest.sh` - Automated quest file generation from templates
- **Quest Validator**: `scripts/validate-quest-network.py` - Python-based frontmatter and network validation
- **Quest Tools Wrapper**: `scripts/quest-tools.sh` - Docker wrapper for validation tools
- **Quest Templates**: `pages/_quests/templates/` directory with `main-quest-template.md` and `level-readme-template.md`
- **Docker Validation Environment**: Multi-service setup in `docker-compose.yml` with `quest-validator` and `quest-network-validator` services
- **Python Dependencies**: `scripts/requirements.txt` for PyYAML and validation tools

#### Quest Documentation
- **QUEST_BUILD_PLAN.md**: 14-week roadmap for complete quest system (6 phases, 97 quests)
- **PHASE1_COMPLETE.md**: Infrastructure phase documentation
- **PHASE2_COMPLETE.md**: Apprentice Tier (17 quests) completion summary
- **PHASE3_COMPLETE.md**: Journeyman Tier (36 quests) completion summary
- **PHASE4_COMPLETE.md**: Expert Tier (19 quests) completion summary with technical coverage breakdown
- **VALIDATION_FIXES_SUMMARY.md**: Documentation of 44 frontmatter validation fixes across 58 original quests

#### Other Additions
- Preview images for various quests in `assets/images/previews/`
- **README.md files**: Added README.md to all level directories (0000, 0001, 0010, 0011, 0100, 0101, 1010, 1011, 1100, 1110)
- **inventory/README.md**: New directory for learner progress tracking (future feature)
- **tools/README.md**: Collection documentation for cross-level tool quests
- **Directory Structure section**: Added comprehensive structure documentation to main quests README.md
- **Binary Level System table**: Complete 16-level table (0000-1111) with status indicators and reserved levels

### Changed

- **Normalized quest permalinks** — All 173 quest files migrated to canonical `/quests/XXXX/[side-quests/]slug/` hierarchy; old URLs preserved in `redirect_from:` for backward compatibility
- **Quest validator updated** — `test/quest-validator/quest_validator.py` now enforces the canonical permalink regex and validates `dir-level` consistency
- **Quest CI workflow updated** — `full-audit` job now regenerates and drift-checks `quest-network.json` on every scheduled or manual run
- **AGENTS.md and copilot-instructions.md updated** — Quest permalink convention documented as canonical gotcha with migration commands

- **Level 0000 README** — Updated Bashcrawl cross-reference link from stale `/quests/0000/bashcrawl/` to canonical `/quests/0000/bashcrawl/`

- **`.github/` instructions and prompts slashed** — `.github/instructions/*.md` and `.github/prompts/*.md` compressed ~70%: removed generic AI-padding, duplicate examples, and motivational filler; kept only actionable rules and one canonical example per concept. All files tightened to ≤200 lines.
- **`.github/instructions/DONTREADME.md` removed** — 235-line fantasy filler with no inbound references; superseded by tightened instruction set.
- **Posts mass cleanup** (8-phase, #239):
  - Files: 124 → 86 (+ 34 stub/draft posts moved to `pages/_drafts/`)
  - Frontmatter valid: 73/124 (59%) → 86/86 (100%)
  - Frontmatter errors: 102 → 0
  - SEO score (avg): 54.5 → 65.5
  - Markdownlint issues: 1,790 → 21 (98.8% reduction)
  - Internal links: 0/287 broken (verified via `lychee --offline --base _site`)
- **Posts directory layout** — All posts now reside in 13 kebab-case category folders (e.g. `ai-machine-learning/`, `creative-experimental/`); previous folder names with spaces and `&` renamed via `git mv` to preserve history
- **Frontmatter normalized** — Auto-filled `date`, `categories`, and `description` across the collection per `posts.instructions.md` schema

- **Layout Rename: `journals` → `articles`** - Renamed layout references across all post instructions, prompt templates, SEO templates, documentation standards, architecture docs, and quest content for consistency with `_config.yml` default
- **Dev Performance: Incremental Builds** (`_config_dev.yml`) - Added incremental build support, reduced plugin set, disabled preview image generation during development for faster iteration
- **Docker Dev Environment** (`docker-compose.yml`) - Added `--incremental` flag to Jekyll serve command and persistent `jekyll-cache` volume for faster rebuilds
- **Preview Generator** (`_plugins/preview_generator.rb`) - Skip preview generation during incremental builds to avoid full rebuild overhead
- **Quest YAML Formatting** (`pages/_quests/0101/jekyll-quest-tracking.md`) - Normalized YAML indentation and quoting for consistency
- **Post Metadata** (`pages/_posts/devops/2026-03-07-foundational-ci-cd-pipelines-github-vscode-extensions.md`) - Updated lastmod, removed duplicate layout field

- **Link Health Guardian v3.0** (`scripts/validation/link-checker.py`) - Major rewrite:
  - Dual engine support: lychee (primary, via `.lychee.toml`) or curl (fallback)
  - Persistent caching via `.lycheecache` for cross-run URL skip
  - Incremental `--changed-only` mode for fast PR checks
  - Delta-only AI analysis (only new broken links sent to AI)
  - Multi-provider AI support (OpenAI, Anthropic, or none via `--ai-provider`)
  - `--include-site` flag for opt-in `_site/` scanning
  - Timing instrumentation for performance tracking
- **Link Checker Workflow** (`.github/workflows/link-checker.yml`) - Simplified and optimized:
  - Added `pull_request` trigger with fast incremental check (changed files only, no AI)
  - Removed redundant Friday schedule (keep Monday only)
  - Added AI provider selection (OpenAI, Anthropic, or none)
  - Removed obsolete input options (timeout, ai-analysis toggle)
- **Preview Image Generator Plugin** (`_plugins/preview_image_generator.rb`) - Fixed `has_preview?` to reject non-path strings (text descriptions) and added multi-candidate file path checking for both absolute and relative paths
- **Preview Image Script** (`scripts/generation/generate-preview-images.sh`) - Added `--enhance` mode for AI-powered image improvement with configurable model, fidelity, and format options; fixed `PROJECT_ROOT` path resolution
- **Scripts README** (`scripts/README.md`) - Updated Link Health Guardian documentation for v3.0 features, configuration options, and dual-engine architecture
- **Guardian Script** (`test/hyperlink-guardian/scripts/guardian.sh`) - Marked as deprecated in favor of `link-checker.py --engine curl`

- **Consolidated Bash Cheatsheets** (`pages/_notes/cheetsheets/bash-cheatsheet.md`) - Merged duplicate bash cheatsheets into a single file and updated frontmatter with related quests.
- **Bashcrawl Quest Enhancement** (`pages/_quests/0000/bashcrawl/README.md`) - Upgraded to a main quest with enhanced frontmatter (`level: '0000'`, `quest_type: main_quest`), added quest dependencies, and updated the setup guide to clone from `bamr87/bashcrawl`.
- **Bash-run Side Quest** (`pages/_quests/0000/bash-run.md`) - Updated frontmatter to correctly point to `bashcrawl` as its parent/required quest and added resource links.

- **Quests home page** (`pages/_quests/home.md`) - Added `mermaid: true` front matter to enable Mermaid diagram rendering
- **Docs library index** (`pages/_docs/index.md`) - Added Terminal section listing available reference guides

- **CI/CD Token Standardization** - Renamed `PAT_TOKEN` secret to `GITHUB_PAT` across all workflows and documentation for consistency:
  - `ai-content-review.yml` — 3 references updated
  - `dependency-checker.yml` — 2 references updated (also switched checkout token from `GITHUB_TOKEN` to `GITHUB_PAT` for write permissions)
  - `frontmatter-validation.yml` — 2 references updated
  - `action-triggers.md` quest — 1 reference updated
  - Blog posts updated to reflect new token naming
  - `PRD.md` — Issue descriptions updated

- **Quest Validator v2.0.0** (`test/quest-validator/quest_validator.py`) - Major upgrade:
  - Added placeholder content detection (brackets, TODO/TBD, lorem ipsum)
  - Added `--exclude-drafts` and `--fail-threshold` CLI options
  - Enhanced permalink validation supporting multiple valid patterns
  - Improved scoring with complete vs placeholder quest classification
  - Added JSON report output support for CI integration
- **Placeholder Dependency Remover** (`scripts/quest/remove-placeholder-deps.py`) - Improved regex patterns to dynamically match any level (e.g., `level-\d{4}-side-quest-\d+`) instead of hardcoded level lists
- **Quest Frontmatter Enhancements** (93 quest files across all levels) - Comprehensive frontmatter improvements:
  - Level 0000 quests: Added `quest_line`, `quest_arc`, `quest_dependencies`, `quest_relationships`, `learning_paths`, structured `prerequisites` (knowledge/system requirements), structured `rewards` (badges/skills/progression points), expanded quest objectives and content sections
  - Levels 0001–1111 quests: Removed placeholder dependency values (`side-quest-1`, `alternative-path`, `continuation`) replaced with empty arrays for accurate relationship tracking

- **`_config.yml`** - Updated `powered_by` configuration:
  - Removed Algolia (not currently in use)
  - Updated jQuery version to 3.7
  - Updated MathJax version to 3.2
  - Added Docker to powered_by list
  - Fixed jQuery capitalization

- **`pages/_quests/home.md`** - Added auto-generated quest index section with markers and refreshed `lastmod`.

- **Quest README**: Updated `pages/_quests/README.md`:
  - Removed "Coming Soon" labels from levels 1101 and 1111
  - Added links to all new quests in levels 1100-1111
  - Updated quest counts and completion status

#### Quest System Status Update
- **Total Quests**: 162 quests (130 previous + 32 new)
- **Levels Complete**: 16 of 16 levels (100%) ✅
- **Phases Complete**: 5 of 6 phases (83%)
  - Phase 5: Master Tier ✅ (NEW)

#### Quest Frontmatter Standardization
- **44 Frontmatter Validation Fixes**: Systematic fixes across 58 original quest files
  - Added missing `level` field to all quests following binary format (0000-1111)
  - Added missing `quest_type` field (main_quest, side_quest, bonus_quest, epic_quest, reference)
  - Added missing `difficulty` field (🟢 Easy, 🟡 Medium, 🔴 Hard, ⚔️ Epic, 📚 Reference)
  - Added missing `estimated_time` field with proper format
  - Standardized `permalink` field structure
  - Added missing `title` and `description` fields
  - Fixed invalid difficulty values and quest types
  - Fixed invalid level formats to 4-digit binary

#### Docker Infrastructure Updates
- **Dockerfile**: Added Python 3.11 venv setup at `/opt/venv` for quest validation
- **docker-compose.yml**: Added multi-service validation environment
  - `quest-validator` service for individual quest validation
  - `quest-network-validator` service for network-wide validation
  - Shared volume mounts for scripts and quest directories

#### Quest System Status
- **Total Quests**: 130 quests (58 original + 72 generated)
- **Levels Complete**: 12 of 16 levels (75%)
  - Original levels: 0000, 0001, 0010, 0011, 0100, 0101, 1100, 1110
  - New levels: 0110, 0111, 1000, 1001, 1010, 1011
- **Phases Complete**: 4 of 6 phases (67%)
  - Phase 1: Infrastructure ✅
  - Phase 2: Apprentice Tier ✅
  - Phase 3: Journeyman Tier ✅
  - Phase 4: Expert Tier ✅
  - Phase 5: Master Tier (pending)
  - Phase 6: Polish & Integration (pending)

#### Major Quest Reorganization
  - `init_world/` → `0000/` (Foundation & Init World)
  - `lvl_000/` → `0000/` (merged with init_world content)
  - `lvl_001/` → `0001/` (Journeyman Challenges)
  - `lvl_0010/` → `0010/` (Terminal Enhancement)
  - `frontend/` → `0100/` (Frontend & Docker)
  - Tool quests → `tools/` directory
  - Quest examples → `codex/` directory
- **File Naming**: Removed date prefixes from all quest files (e.g., `2024-05-28-bash-run.md` → `bash-run.md`)
- **Code Files**: Moved script/code examples from level root directories to subdirectories (`scripts/`, `examples/`)
- **Updated paths**: All internal quest links updated to new binary-coded paths in README.md and home.md
- Updated `scripts/lib/preview_generator.py` for enhanced preview generation
- Updated `test/quest-validator/requirements.txt` for validator dependencies

### Removed

- **Vendored preview-image generators** — `_plugins/preview_image_generator.rb`, `scripts/lib/preview_generator.py` and `scripts/generation/generate-preview-images.sh` are retired; the `zer0-image-generator` gem (`~> 0.6`, `bundle exec jekyll preview-images`) covers every option they had, and `preview_images:` in `_config.yml` is its one config block. The `_config_dev.yml` / `_config_ci.yml` `preview_images:` overrides went with the plugin that read them.

- **Empty Duplicate Post** (`pages/_posts/2025-07-10-github-actions-authentication-fix-2025-07-10.md`) - Removed empty duplicate of existing post in `devops/` subdirectory

- Legacy directory structure (`init_world/`, `lvl_000/`, `lvl_001/`, `lvl_0010/`, `frontend/`, `examples/`)
- Date prefixes from 75+ quest files
- Duplicate `0000/tools/` directory (consolidated to root `tools/`)

### Fixed

- **Quest preview paths** — 164 quests used `preview: images/previews/…` without a leading slash, which the theme joined onto `/assets` as `/assetsimages/previews/…` (404 for the hero background and `og:image`). They now start with `/images/`, like the rest of the site, and so does the SEO frontmatter template
- **Homepage stats and preview images** — the stats row rendered `0` until a scroll-triggered count-up ran, so no-JS visitors, screenshots, and anyone who had not scrolled it into view saw four zeros. Real values are now rendered server-side (quests = non-draft `fmContentType: quest` floored to tens, levels/tiers from `_data/quests/`), and the count-up is skipped for reduced motion. The tier cards and gallery referenced 8 `.png` previews that only exist as `.webp` (12 broken images per load); they now point at the `.webp` files
- **Quest nav copy and missing page headings** — the quest trail said "No prerequisite" right above each quest's own "Quest Prerequisites" list. It now reads "No prior experience needed" on level 0000 quests (13, including hello-noob) and "No required quest" elsewhere (101). `/search/` and `/sitemap/` had no `h1` (axe `page-has-heading-one`); their headings are now `h1`
- **173 quest files** with non-canonical permalink formats (`/quests/level-XXXX-slug/`, `/quests/side-quest-slug/`) migrated to `^/quests/[01]{4}/[side-quests/]slug/$` format

- **Broken Jekyll docs link** — `https://jekyllrb.com/docs/deployment/methods/` → `https://jekyllrb.com/docs/deployment/` in `devops/2025-11-17-deploying-jekyll-sites-to-azure-cloud.md` (#239)

- **Link Check Results** - Cleaned up oversized `lychee_results.json` (reduced ~128K lines of stale data) and regenerated analysis reports

- **Bashcrawl Launcher** (`pages/_quests/0000/bashcrawl/bash_crawl.sh`) - Rewrote the script to properly clone the `bashcrawl` repository and execute `entrance.sh`, removing unreachable code and adding error handling.

- **`dependency-checker.yml`** — Replaced nested YAML-unsafe heredoc labels (`ISSUE_EOF`) with standard `EOF`, removed fragile `continue-on-error`, fixed backtick quoting in markdown code fences, removed unnecessary label creation step
- **`frontmatter-validation.yml`** — Removed unused `DateTimeEncoder` class and redundant `date` import
- **`link-checker.yml`** — Removed broken float-to-integer truncation of `success_rate` variable; bash `[[ -ge ]]` already handles integer comparison
- **`prd-sync.yml`** — Fixed YAML block scalar indentation that broke workflow parsing, removed unnecessary `issues: write` permission

- **fmContentType Field**: Added missing `fmContentType: quest` to 35 quest files:
  - All 32 new quests in levels 1100-1111
  - 3 existing quests: `edgar.md`, `sec-edgar.md`, `the-temple-of-templates.md`
- **Jekyll Build Error**: Fixed invalid `preview` field in 2 blog posts:
  - `2025-06-29-planting-seeds-software-evolution.md` - Changed text to image path
  - `2025-07-09-fixing-github-actions-bash-compatibility-ai-evolution-engine.md` - Changed text to image path

### Updated

#### Navigation Schema Migration (zer0-mistakes v0.17+)
Complete migration of all navigation files to new schema format.

- **`_data/navigation/about.yml`** - Changed `sublinks` to `children`, fixed icon format to `bi-*` prefix
- **`_data/navigation/main.yml`** - Changed `sublinks` to `children`, added Bootstrap Icons to all items
- **`_data/navigation/home.yml`** - Changed `sublinks` to `children`, fixed icon format
- **`_data/navigation/docs.yml`** - Changed `sublinks` to `children`, added icons, fixed icon prefix
- **`_data/navigation/quickstart.yml`** - Changed `sublinks` to `children`, added icons
- **`_data/navigation/posts.yml`** - Changed `sublinks` to `children`, fixed all icons to use `bi-*` format, removed empty `sublinks: []`
- **`_data/navigation/quests.yml`** - Changed `sublinks` to `children`, fixed icons to use `bi-*` format
- **`_data/navigation/notebooks.yml`** - Changed `sublinks` to `children`, fixed icon format
- **`_data/navigation/hobbies.yml`** - Changed `sublinks` to `children`, added icon

### Documentation

- **`scripts/quest/README.md`** - Added front matter and documented quest index generation script usage.

### Migration Notes

- Quest permalinks may have changed - update any external references
- Binary level directories (0000-1110) replace legacy naming convention
- Code examples now live in subdirectories within level folders

## [2.2.0] - 2026-03-21

### Added
- **Contributor Profile System** — Complete gamified RPG contributor profiles with character sheets, achievement walls, stats panels, and CSS styling (#167)
- **Contributor Quest Line** — 6 new quests: forge-your-character, avatar-forge, badge-collector, contribution-calendar, stats-dashboard, profile-themes (#168)
- **Bash-Run Quest Rewrite** — Rewrote bash-run quest (bashrun → bashcrawl) with improved educational content (#168)
- **Contributor GitHub Actions Workflow** — Automated contributor profile updates via CI/CD (#167)
- **Contributor Generation Scripts** — Makefile targets and generation scripts for contributor stats (#167)
- **Advanced Version Control Quest** — Level 1100 quest teaching semantic versioning, branch strategies, PR orchestration, and release management using real-world examples

### Changed
- **Script Relocation** — Moved `generate_statistics.rb`, `generate_statistics.sh`, `update_statistics.sh` from `_data/` to `scripts/generation/` for better project organization (#166)
- **Path References Updated** — Updated Makefile, AGENTS.md, _data/README.md, scripts/README.md, pages/stats.md, and stating-the-stats quest to use new script paths (#166)
- **Quest Validator** — Added `--config` / `-c` CLI argument to respect Jekyll `_config.yml` default values, preventing false validation failures for fields with collection-level defaults (#169)
- **YAML Anchor Handling** — Quest validator now handles YAML anchors/aliases via regex fallback parser (#169)
- **About Navigation** — Added Contributors link to about navigation menu (#167)
- **Quests README and Navigation** — Updated quest collection docs with new contributor quest line (#168)

### Removed
- **Obsolete Data Files** — Removed `_data/SOLUTION_SUMMARY.md` and `_data/github-actions-example.yml` (#166)

### Fixed
- **Quest Validator False Positives** — Skips required field errors for fields that have `_config.yml` defaults (e.g., `layout`), resolving 142/142 quest validation (#169)

## [2.5.0] - 2025-01-27

### Added

#### Quest Network Validation & Fixes (Phase 6)
Complete quest network validation and frontmatter standardization across all 147 quests.

- **`scripts/fix-quest-frontmatter.py`** - New automated frontmatter fixer script
  - Removes placeholder dependencies (unlocks_quests, prerequisites)
  - Adds missing required fields (difficulty, estimated_time, quest_type)
  - Normalizes quest_type and difficulty values to valid options
  - Dry-run mode for safe previewing
  - Fixed 284 issues across 90 files

- **`pages/_quests/lvl_0110/README.md`** - New level README (Advanced Quests I)
- **`pages/_quests/lvl_0111/README.md`** - New level README (Advanced Quests II)
- **`pages/_quests/lvl_1000/README.md`** - New level README (Expert Quests I)
- **`pages/_quests/lvl_1001/README.md`** - New level README (Expert Quests II)
- **`pages/_quests/docs/`** - New documentation directory for phase plans

#### Documentation
- **`pages/_quests/PHASE6_PLAN.md`** - Detailed Phase 6 execution plan with 5-week timeline
- **`pages/_quests/docs/PHASE1-5_COMPLETE.md`** - Archived phase completion summary
- **`pages/_quests/docs/VALIDATION_FIXES_SUMMARY.md`** - Archived validation fixes summary

### Changed

#### Quest Frontmatter Standardization (~120 files)
- Removed all placeholder `unlocks_quests` and `prerequisites` references
- Added missing `difficulty` fields with contextually appropriate values
- Added missing `estimated_time` fields
- Normalized `quest_type` values to valid options (main_quest, side_quest, epic_quest, bonus_quest, reference)
- Normalized `difficulty` values to valid options (🟢 Easy, 🟡 Medium, 🔴 Hard, ⚔️ Epic)
- Fixed duplicate frontmatter keys in `sec-edgar.md`
- Cleared broken inter-quest dependencies (314 → 0 broken deps)

#### Validation System
- **`scripts/validate-quest-network.py`** - Updated to exclude `/docs/` directory from scanning
- **`pages/_quests/QUEST_BUILD_PLAN.md`** - Updated with Phase 6 status, quest counts, and version 2.0.0

### Fixed
- **318 validation errors → 0 errors** - Complete quest network integrity
- Removed 314 broken dependency references
- Fixed invalid `quest_type` values (guide → reference, etc.)
- Fixed invalid `difficulty` values (intermediate → 🟡 Medium, etc.)
- Fixed `sec-edgar.md` missing title and duplicate description fields

### Validation Results
- Total Quests: 147
- Complete Quests: 29
- Broken Dependencies: 0
- Errors: 0
- Warnings: 444 (non-blocking orphan quests - expected during development)

## [2.4.1] - 2025-12-28

### Added
- **`_data/navigation/quests.yml`** - New navigation file for quest collection with all levels (0000-0101)
- **`_data/navigation/notebooks.yml`** - New navigation file for notes/cheatsheets collection

### Changed

#### Navigation System Alignment
- **`_data/navigation/main.yml`** - Fixed broken `/zer0/` link, reorganized sections (Quick-Start, Journey, Library, Notebook, About)
- **`_data/navigation/about.yml`** - Removed non-existent pages (`/about/approach`, `/about/license`, `/about/terms`)
- **`_data/navigation/docs.yml`** - Complete rewrite to match actual `_docs` collection content
- **`_data/navigation/hobbies.yml`** - Simplified to existing `/hobbies/` page only
- **`_data/navigation/home.yml`** - Fixed broken `/roadmap/` reference, added Journey section
- **`_data/navigation/posts.yml`** - Removed broken entries, added Business category
- **`_data/navigation/quickstart.yml`** - Removed non-existent platform-specific pages

#### Sidebar Configuration
- **`_config.yml`** - Updated sidebar nav settings: `_quests` collection uses `quests` nav, `_notes` uses `notebooks`, added `_notebooks` collection scope
- **`pages/_about/settings/_config.yml`** - Synced with main config changes

### Documentation
- **`_data/README.md`** - Added comprehensive navigation files table and sidebar modes documentation

## [2.4.0] - 2025-12-20

### Added

#### SEO & Content Automation Scripts (Ruby)
Three new Ruby automation scripts for Docker/Jekyll environment:

- **`scripts/frontmatter-validator.rb`** - Comprehensive frontmatter validation
  - Multi-type validation (posts, quests, docs, notes)
  - SEO scoring system (0-100 points)
  - JSON report export
  - CLI options for filtering and verbose output
  - Validates 343 files with 91.5% validity rate

- **`scripts/ctr-report-generator.rb`** - SEO/CTR report generation
  - Baseline metrics from Google Search Console
  - Weekly review template generation
  - Opportunities analysis for improvement
  - CSV parsing and JSON export

- **`scripts/content-freshness-check.rb`** - Content age tracking
  - Freshness categories (fresh/aging/stale/critical/unknown)
  - Content health scoring (56.2% current health)
  - Priority-ranked action items
  - Markdown and JSON report exports
  - Content-type specific thresholds

#### SEO Data & Reports
- `TODO/seo/data/frontmatter-report.json` - Full validation report (343 files)
- `TODO/seo/data/seo-metrics.json` - SEO baseline metrics
- `TODO/seo/data/freshness-report.json` - Content freshness data
- `TODO/seo/reports/weekly-review-2025-12-20.md` - Weekly review template
- `TODO/seo/reports/content-freshness-2025-12-20.md` - Freshness report

### Changed
- **TODO Status Dashboard**: Updated `TODO/STATUS.md` with Automation category at 100% completion
- **TODO README**: Updated `TODO/README.md` with completed automation scripts and usage examples
- **Scripts README**: Added comprehensive SEO Automation section with usage examples

### Documentation
- Updated `scripts/README.md` with SEO & Content Automation section
- Added usage examples for all three Ruby scripts
- Documented SEO scoring methodology and freshness thresholds

## [2.3.0] - 2025-12-20

### Added

#### Comprehensive SEO Optimization Project (4 Phases)
- **Phase 1 - Quick Wins**: Optimized 6 high-impression pages with proper titles, meta descriptions, and canonical URLs
- **Phase 2 - Systematic Quest SEO**: Updated 88 quest files with proper SEO frontmatter
  - Added descriptive titles with primary keywords (e.g., "Docker Containerization Mastery" vs "Docker Quest")
  - Added unique meta descriptions (150-160 chars) explaining learning outcomes
  - Added structured tags and keywords for discoverability
  - Fixed placeholder values like `[Descriptive Subtitle]`, `[main-tech]`, `[skill-category]`
- **Phase 3 - High-Demand Content**: Created 3 new SEO-optimized articles targeting search gaps
  - `pages/_docs/terminal/terminal-shortcuts-cheat-sheet.md` - Comprehensive terminal shortcuts reference
  - `pages/_posts/devops/2025-12-20-docker-beginners-tutorial.md` - Docker beginner tutorial
  - `pages/_posts/tools & environment/2025-12-20-essential-vscode-extensions-developers.md` - VS Code extensions guide
- **Phase 4 - Monitoring Infrastructure**: Set up tracking systems for ongoing SEO health
  - `TODO/seo/MONITORING_DASHBOARD.md` - Weekly tracking templates, GSC checklists, A/B testing log
  - `scripts/seo-tracker.py` - Python CLI for baseline reports, weekly templates, opportunity analysis
  - `TODO/seo/TRACKING.md` - Performance metrics and baseline data

#### TODO System Reorganization
- Created `TODO/STATUS.md` - Central dashboard for all project work
- Created `TODO/seo/` - Dedicated SEO project directory with structured files
- Created `TODO/templates/` - Reusable templates for different task types
- Created `TODO/ARCHIVE/` - Storage for completed project documentation
- Created `.github/instructions/todo.instructions.md` - AI agent guidelines for TODO management

### Changed
- **Roadmap Update**: Refreshed `roadmap.md` with current priorities and timeline
- **Quest Frontmatter Standardization**: All 88 quest files now follow consistent SEO-optimized format

### Removed
- Deleted obsolete TODO files: `TODO/SEO_OPTIMIZATION_PLAN.md`, `TODO/QUICK_ACTIONS.md`, `TODO/TRACKING_TEMPLATE.md`

## [2.2.0] - 2025-11-29

### Added
- **PRD Machine Docker Integration**: Added `prd-machine` service to `docker-compose.yml` for containerized PRD generation
- **New Quest**: `2025-11-29-prd-codex-mastering-product-reality-distillation.md` - Level 0011 educational quest teaching Product Requirements Documents and PRD Machine usage with fantasy RPG theme
- **PRD Machine CLI**: Python-based tool (`scripts/prd-machine/prd-machine.py`) with three commands:
  - `sync` - Generate/update PRD.md from repository signals
  - `status` - Check PRD health and freshness
  - `conflicts` - Detect and display PRD conflicts

### Changed
- **PRD Content Refactor**: Regenerated `PRD.md` to document the IT-Journey platform instead of self-referential PRD Machine documentation
- **PRD Section Generators**: Updated all section generators in `prd-machine.py` to output IT-Journey focused content (WHY, MVPs, Key Signals, etc.)

### Documentation
- Updated `pages/_quests/README.md` with new PRD Codex quest entry
- PRD Machine README at `scripts/prd-machine/README.md` provides complete usage guide
### Changed

#### Content Organization Improvements (2025-12-17)
- **Consolidated Blog Post Index**: Replaced multiple duplicate post index files with a unified `pages/posts.md`
  - Removed redundant files: `pages/_posts/2000-01-01-index.md`, `pages/_posts/README.md`
  - Removed duplicate home section files: `pages/_posts/home/2025-11-16-blog-posts-it-journey.md`, `pages/_posts/home/2025-11-16-posts.md`
  - Created new unified post index at `pages/posts.md` with improved table-based category overview
  - Enhanced structure with better organization and visual layout
  - Updated frontmatter with current timestamp and version 2.0.0

### Fixed

#### Link Health Improvements (2025-12-11)
- **Removed Broken Internal References**:
  - Removed `/zer0/` bookmark from `pages/home.md` (404 error)
  - Updated quest example in `stating-the-stats.md` from `/blog/` to `/posts/`
- **Enhanced Link Checker Configuration**:
  - Excluded `_site/preview/` directory to eliminate ~15,000 false positives
  - Excluded `work/` directory from link checking
  - Added exclusion patterns for rate-limited URLs (GitHub blob URLs, Reddit share buttons)
  - Reduced total link checks from 152K to 78K (48% reduction in noise)
  - Reduced broken link reports from 19,877 to 10,680 (46% reduction)
  - Reduced unique broken URLs from 2,173 to 1,696 (22% reduction)
- **Added Comprehensive Link Analysis Documentation**:
  - `link-check-results/ANALYSIS_SUMMARY.md` - Statistical analysis of link health
  - `link-check-results/FIXES_APPLIED.md` - Detailed documentation of fixes and remaining issues
  - `link-check-results/detailed_analysis.md` - Automated link failure analysis
  - `link-check-results/ai_analysis.md` - AI-powered link health insights

### Added

#### AI-Generated Quest Preview Images (2025-12-01)
- **107 New Preview Images**: AI-generated preview images for all quest levels using DALL-E 3
  - Level 0000-1111 README banners with consistent retro pixel art style
  - Individual quest preview images for 100+ quests
  - Images stored in `assets/images/previews/`

#### Enhanced Preview Generator Script
- **New Feature: Batch Processing** - Process multiple files with `--batch N` flag
- **New Feature: Rate Limiting** - Token bucket rate limiter for API calls (5 req/min default)
- **New Feature: Logging Support** - File logging with `--log-file` flag
- **New Feature: Interrupt Handling** - Graceful shutdown on Ctrl+C with progress preservation
- **New Feature: Progress Tracking** - Real-time progress bar and ETA during batch generation
- **New Feature: Retry Logic** - Automatic retries with exponential backoff for API failures

### Fixed

- **Jekyll Build Error**: Added `work/` directory to Jekyll exclude list to prevent symlink errors from local Python virtual environments

#### Quest Collection Layout System
- **New Layout: `quest-collection.html`** - Dynamic layout for displaying quests grouped by binary level tiers (Apprentice, Adventurer, Warrior, Master)
- **New Include: `quest-card.html`** - Reusable quest card component with data attributes for filtering
- **New Include: `quest-filters.html`** - Interactive filtering UI with JavaScript for quest type, difficulty, level, technology, and search
- **New Include: `quest-stats.html`** - Statistics display component showing quest counts by type and difficulty
- **New Include: `quest_card.html`** - Alternative quest card with BEM-style CSS classes
- **New Include: `quest_grid.html`** - Grid layout component for quest collections
- **New Include: `quest_stats.html`** - Alternative statistics component with time estimation

#### New Quest
- **Side Quest: `jekyll-quest-tracking.md`** (Level 0101, 🔴 Hard, 4-6 hours)
  - Master Jekyll's collection system by building a quest tracking interface
  - Covers: Liquid templating, JavaScript filtering, Python automation
  - Includes 5 chapters and 4 mastery challenges
  - Complete with Mermaid diagrams for quest network and implementation flow

#### Automation Scripts
- **New Script: `update_level_readmes.py`** - Python script to ensure consistent frontmatter across level README files
  - Adds missing `layout: quest-collection`, `level`, and `categories` fields
  - Uses regex to detect 4-digit binary level directories

### Changed
- **Quest Index**: Updated `pages/_quests/README.md` to use `quest-collection` layout
- **Level READMEs**: All level README files (0000-1111) updated with consistent frontmatter:
  - Added `layout: quest-collection` for dynamic quest display
  - Added `level` field matching directory name
  - Added `categories: quests` for proper collection filtering
- **Level 0101 README**: Added new Jekyll Quest Tracking side quest entry with updated Mermaid diagram

### Fixed
- **Integer/String Sorting**: Quest filters now handle mixed Integer/String level values by coercing to strings before sorting

---

## [2.1.0] - 2025-11-26

### Added
- **New Quest**: `2025-11-26-prompt-crystal-mastery-vscode-copilot-quest.md` - Comprehensive VS Code Copilot prompt engineering quest with RCTF patterns, few-shot prompting, and reusable template creation
- **New Post**: `2025-11-26-mastering-prompt-engineering-vscode-copilot.md` - Tutorial companion to the prompt engineering quest
- **New Prompt Template**: `commit-publish.prompt.md` - Complete release pipeline workflow for semantic versioning and publishing
- **Enhanced Prompt**: `draft-article.prompt.md` v2.0.0 - Major upgrade with RCTF pattern, Kaizen-driven structure, intake checklists, and quality gates
- **CRUSH Workflow System**: Added `.crush/workflows/CRUSH_WORKFLOW_SYSTEM_SUMMARY.md` documentation

### Changed
- **Documentation Reorganization**: Moved summary files from repository root to organized `/docs/` subdirectories:
  - `ABOUT_REORGANIZATION_SUMMARY.md` → `docs/architecture/`
  - `QUEST_TEMPLATE_ENHANCEMENT_SUMMARY.md` → `docs/standards/`
  - `DEPENDENCY_UPDATE_SUMMARY.md` → `docs/workflows/`
  - `LINK_CONSOLIDATION_SUMMARY.md` → `docs/workflows/`
- Updated `docs/README.md` with links to newly organized documentation (v1.1.0)
- Updated `.gitignore` to exclude log files from root directory and `logs/*.log`

### Removed
- Cleaned up repository root:
  - Removed `.seed.md` (seed content moved to proper locations)
  - Removed `.github/workflows/blank.yml` (unused workflow)
  - Removed `prompts/seed.prompt.yml` and `prompts/seed_prompt.md` (consolidated)
  - Removed `test-mermaid.html` (moved to `test/` directory)
  - Removed various log files (`add-date-prefixes.log`, `post-organization.log`)

### Fixed
- Improved `.gitignore` patterns to prevent log file accumulation in repository

## [2.0.0] - 2025-11-16

### Changed
- **BREAKING**: Weekly Post Organization workflow now creates pull requests instead of directly committing to main branch
  - This change requires manual review and approval of automated post organization changes
  - PRs are automatically labeled and assigned for review
  - Provides safety and traceability for all automated content changes

### Migration Notes
- Existing workflow behavior: Posts were automatically organized and committed to main
- New workflow behavior: Posts are organized and a PR is created for review
- Action required: Review and merge PRs created by the workflow
- No script changes required: `organize-posts.py` and `organize-posts.sh` work as-is

### Technical Details
- Workflow: `.github/workflows/organize-posts-weekly.yml`
- Implementation: Uses standard GitHub Actions (git commands + GitHub CLI)
- Branch pattern: `automated/organize-posts-{run_id}`
- PR configuration:
  - Title: `🤖 Weekly Post Organization - {run_id}`
  - Labels: `automated`, `content-organization`, `posts`
  - Assignee: `bamr87`
  - Includes: Workflow link, change summary, next steps

### Documentation
- Consolidated workflow documentation in `docs/workflows/ORGANIZE_POSTS_WORKFLOW.md`
- Includes: Process flow, implementation details, testing guide, troubleshooting
- Removed temporary documentation files from repository root

## [1.0.0] - 2025-11-16

### Initial Release
- Weekly Post Organization workflow with direct commit to main branch
- Automated organization of posts by section using frontmatter metadata
- Automated archiving of posts older than configurable threshold
- Scheduled execution every Sunday at 2 AM UTC
- Manual trigger with dry-run option

---

## Changelog Maintenance

This changelog is manually maintained. When making changes:

1. Add new entries under `[Unreleased]` section
2. Use categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`
3. Include migration notes for breaking changes
4. Link to relevant documentation
5. Move `[Unreleased]` items to a new version section when releasing

### Version Numbering

- **Major version** (X.0.0): Breaking changes that require user action
- **Minor version** (0.X.0): New features, non-breaking changes
- **Patch version** (0.0.X): Bug fixes, documentation updates

[Unreleased]: https://github.com/bamr87/it-journey/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/bamr87/it-journey/releases/tag/v2.1.0
[2.0.0]: https://github.com/bamr87/it-journey/releases/tag/v2.0.0
[1.0.0]: https://github.com/bamr87/it-journey/releases/tag/v1.0.0

## Theme Fixes (2025-12-12)

### Fixed - Theme Social Button URLs
- **Pull Request**: [zer0-mistakes#15](https://github.com/bamr87/zer0-mistakes/pull/15)
- **Branch**: `fix/social-button-urls`
- **Commit**: 866e26b

#### Changes
- Fixed social sharing buttons to use production URLs instead of localhost
- Updated `_includes/content/intro.html`: Reddit, LinkedIn, Twitter, copy link buttons
- Updated `_layouts/notebook.html`: Twitter, LinkedIn, email share buttons
- Replaced `{{ page.url | absolute_url }}` with `{{ site.url | append: page.url }}`

#### Impact
- Resolves 353 unique broken URLs (20.8% of all broken link types)
- Eliminates false positives in link health checks
- Social buttons now work correctly in all environments
- Expected 46% reduction in unique broken URL types after theme merge

#### Documentation
- Created `link-check-results/THEME_FIXES.md` with comprehensive details
- Technical implementation notes and testing procedures included
- Deployment process and expected improvements documented
