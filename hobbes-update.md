This mermaid chart demonstrates my understanding of how Hobbes currently cooperates with humans:

```mermaid
flowchart TD
    LIVE["LIVE SITE — hazelboutique.com<br/>(PSI API · HTML · sitemap crawl)"]:::live

    %% ============ CONFIG ============
    subgraph CONFIG["config — one source of per-client truth"]
        TOML["hobbes.toml (22)<br/>golden path · secrets-by-name<br/>timezone · effort_budget"]:::tmpl
        CONFIGPY["config.py (70)<br/>golden_path() · client_meta()<br/>psi_key() · effort_budget()<br/>today()/stamp() — pinned tz"]:::py
        TOML --> CONFIGPY
    end

    %% ============ ENGINE TOOLS ============
    subgraph TOOLS["the deterministic engine — hobbes/tools/ (Python, no LLM)"]
        PSI["psi.py (358)<br/>reads: live (PSI API)<br/>writes: raw/*.psi.json + prints §A–D<br/>median-of-3, retry-resilient"]:::py
        SEO["seo.py (316)<br/>reads: live (HTML)<br/>writes: raw/*.seo.json + prints §E"]:::py
        CRAWL["crawl.py (437)<br/>reads: live (SiteOne crawl)<br/>writes: raw/crawl.json + prints §F"]:::py
        BASELINE["baseline.py (135)<br/>reads: 3 tools' stdout + baseline-template.md<br/>writes: 01-baseline.md"]:::py
        FINDINGS["evaluation.py (737)<br/>reads: raw/* directly<br/>imports the SAME extractors<br/>writes: 02-evaluation.md"]:::py
        DIFF["diff.py (241) — REVIEW-ONLY<br/>reads: 2 × 01-baseline.md<br/>writes: diff.md, honest by tier"]:::py
    end

    LIVE --> PSI
    LIVE --> SEO
    LIVE --> CRAWL
    CONFIGPY -. loaded by all tools .-> TOOLS

    %% ============ DATA DOCS ============
    BMD["01-baseline.md<br/>the ONE digest · the scorecard"]:::doc
    EMD["02-evaluation.md<br/>the problem catalog"]:::doc
    DMD["diff.md<br/>the before/after"]:::doc

    PSI -. stdout .-> BASELINE
    SEO -. stdout .-> BASELINE
    CRAWL -. stdout .-> BASELINE
    PSI -- raw --> FINDINGS
    SEO -- raw --> FINDINGS
    CRAWL -- raw --> FINDINGS
    BASELINE --> BMD
    FINDINGS --> EMD
    DIFF --> DMD
    BMD -- "this + prior" --> DIFF
    EMD -. count only .-> DIFF

    %% ============ TEMPLATES ============
    subgraph TEMPLATES["stage contracts — hobbes/templates/*.md"]
        TTMPL["baseline-template.md<br/>scorecard shape §A–G"]:::tmpl
        FTMPL["evaluation-template.md<br/>the findings contract"]:::tmpl
        PTMPL["plan-template.md<br/>group → effort → impact → leverage"]:::tmpl
        ETMPL["execute-template.md<br/>batch by budget · gates · PR before/after"]:::tmpl
        PUBTMPL["publish-template.md<br/>human-owned go-live contract"]:::tmpl
    end
    TTMPL --> BASELINE
    FTMPL -. shape .-> FINDINGS

    %% ============ STANDING CONTEXT ============
    subgraph CTX["standing context — prose, read by the agent"]
        CLAUDE["CLAUDE.md<br/>identity + THE HARD LINE<br/>(never publish/merge/spend w/o sign-off)"]:::ctx
        MISSION["MISSION.md<br/>baseline → target priorities"]:::ctx
        DEV["DEVELOPMENT.md<br/>stack + done-means gates"]:::ctx
        CONTEXTMD["CONTEXT.md<br/>client · sign-off · access"]:::ctx
        CHANGELOG["CHANGELOG.md<br/>what shipped + result"]:::ctx
    end

    %% ============ AGENT STAGES ============
    subgraph AGENT["judgment — the Claude agent (reads the catalog, never raw/)"]
        PLAN["agent · PLAN<br/>reads: 02-evaluation.md + MISSION.md<br/>writes: plan.md"]:::agent
        PLANMD["plan.md<br/>systems · rated · ordered by leverage"]:::doc
        EXEC["agent · EXECUTE<br/>reads: plan.md + 02-eval + 01-baseline + theme<br/>writes: execution.md, theme code, PR body"]:::agent
        EXECOUT["execution.md + theme code + PR body"]:::doc
        PLAN --> PLANMD --> EXEC --> EXECOUT
    end
    EMD --> PLAN
    MISSION --> PLAN
    PTMPL -. fills .-> PLAN
    EMD --> EXEC
    BMD --> EXEC
    ETMPL -. fills .-> EXEC
    CLAUDE -. steers .-> AGENT

    %% ============ PR / HUMAN / OUTPUT ============
    PR["ONE PR<br/>scorecard + findings + the code fix"]:::pr
    EXECOUT --> PR
    HUMAN["HUMAN — review → merge → publish in Shopify<br/>→ add the published label"]:::human
    PR --> HUMAN
    PUBTMPL -. contract .-> HUMAN
    HUMAN -- published label fires --> DIFF
    DMD --> COMMENT["gh pr comment — the before/after"]:::pr

    %% ============ ORCHESTRATION ============
    subgraph ORCH["the cloud runner + CLI"]
        CYCLEYML["hobbes-cycle.yml — dispatch<br/>cycle measures (no LLM), agent fixes → ONE PR"]:::orch
        REVIEWYML["hobbes-review.yml — on published label<br/>re-baseline live, diff, comment (no Claude)"]:::orch
        CLI["cli.py (111)<br/>cycle · steps · status · plan/execute · budget"]:::py
    end
    CYCLEYML -. runs .-> TOOLS
    CYCLEYML -. runs .-> AGENT
    REVIEWYML -. runs .-> DIFF
    CLI -. drives locally .-> TOOLS

    %% ============ OPERATOR GUIDES ============
    subgraph GUIDES["operator guides — engine-generic"]
        SETUP["SETUP.md — once per client<br/>(local + cloud, each error-annotated)"]:::tmpl
        BASELINEMD2["BASELINE.md — the cycle runbook<br/>(read by the agent during a cycle)"]:::ctx
    end
    BASELINEMD2 -. guides .-> AGENT

    %% ============ LEGEND ============
    subgraph LEGEND["legend"]
        L1["Python · deterministic"]:::py
        L2["Claude agent · judgment"]:::agent
        L3["human · irreversible"]:::human
        L4["output digest / doc"]:::doc
        L5["template / config"]:::tmpl
        L6["standing context"]:::ctx
        L7["workflow / orchestration"]:::orch
    end

    classDef live fill:#1f2937,color:#ffffff,stroke:#0f172a,stroke-width:2px;
    classDef py fill:#dbeafe,stroke:#2563eb,color:#1e3a8a;
    classDef raw fill:#eff6ff,stroke:#93c5fd,color:#1e40af;
    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d;
    classDef agent fill:#fef3c7,stroke:#d97706,color:#78350f;
    classDef human fill:#fce7f3,stroke:#db2777,color:#831843;
    classDef ctx fill:#f3e8ff,stroke:#9333ea,color:#581c87;
    classDef tmpl fill:#f1f5f9,stroke:#64748b,color:#334155;
    classDef pr fill:#e0e7ff,stroke:#4f46e5,color:#312e81,stroke-width:2px;
    classDef orch fill:#ffe4e6,stroke:#e11d48,color:#881337;
```

Int he future I'd imagine hobbes works as an MCP or CLI tool that you have your agent operate.

Hobbes has several sections. The first is the configuration system which serves as the single source of truth for the client. `hobbes.toml` is per-client configuration including client info, the golden path web addresses,
