# oracle-supreme-squad

> This plugin is part of the [Helix Squads Public Marketplace](https://github.com/lckx777/helix-squads-public).

## Quick install

```
claude plugin marketplace add lckx777/helix-squads-public
claude plugin install oracle-supreme-squad@helix-squads-public
```

---

# 🔮 Oracle Supreme Squad

**The most advanced AI squad for codebase analysis, bug detection, and intelligent learning.**

Beyond traditional squads - Oracle combines infinite memory, adaptive reasoning, and LSP-powered code intelligence to help you understand, fix, and improve your projects.

---

## 🎯 What Oracle Does For You

### 1. **Fix Bugs Intelligently**
Oracle doesn't just find bugs - it understands context, predicts root causes, and suggests fixes based on patterns learned from your entire codebase.

**Example:**
```bash
# Analyze a crashing feature
oracle-scanner *deep-scan ./src/payments/
oracle-prophet *detect-patterns [scanner-output]
oracle-healer *diagnose-and-fix bug="payment fails on retry"

# Oracle will:
# - Scan your payment code deeply
# - Detect anti-patterns (like missing error handling)
# - Propose a fix with tests
# - Learn from this for future bugs
```

### 2. **Learn Your Codebase Faster**
New to a project? Oracle builds a knowledge graph of your code, showing you how everything connects.

**Example:**
```bash
# Understand a complex feature
oracle-scanner *analyze ./src/auth/
oracle-architect *explain-design component="authentication flow"

# Oracle will:
# - Map all auth-related files
# - Show you the architecture patterns
# - Explain design decisions
# - Generate visual diagrams
```

### 3. **Generate Perfect Documentation**
Oracle understands your code semantically (via LSP) and generates docs that actually make sense.

**Example:**
```bash
# Document your API
oracle-scanner *scan ./api/
oracle-scribe *generate-docs format="markdown" include="examples"

# Oracle will:
# - Extract API endpoints and types
# - Generate usage examples
# - Create README with code samples
# - Update on every change
```

### 4. **Optimize Performance**
Oracle tracks costs, detects bottlenecks, and suggests optimizations based on real data.

**Example:**
```bash
# Find performance issues
oracle-scanner *profile ./src/
oracle-optimizer *find-bottlenecks threshold="100ms"

# Oracle will:
# - Profile your code execution
# - Detect slow queries/loops
# - Suggest caching strategies
# - Estimate performance gains
```

### 5. **Security Audit**
Oracle validates security best practices and detects vulnerabilities before they ship.

**Example:**
```bash
# Security check before deploy
oracle-guardian *audit ./src/ depth="deep"

# Oracle will:
# - Check OWASP Top 10 vulnerabilities
# - Detect hardcoded secrets
# - Validate input sanitization
# - Suggest security patches
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone or install via AIOS marketplace
git clone https://github.com/gutomec/oracle-supreme-squad.git
cd oracle-supreme-squad

# Validate (should show 100/100)
squads validate .
```

### Your First Oracle Session

**Scenario: Debug a failing test**

```bash
# 1. Activate Oracle
squad activate oracle-supreme-squad

# 2. Scan the failing module
oracle-scanner *deep-scan ./tests/integration/checkout.test.ts

# 3. Detect patterns and anti-patterns
oracle-prophet *analyze [scanner-output]

# 4. Oracle-critic validates findings (automatic quality gate)
# (Oracle-critic runs automatically with 9.0/10 threshold)

# 5. Get fix suggestions
oracle-healer *suggest-fix test="checkout calculates tax incorrectly"

# 6. Oracle remembers this bug pattern for next time
# (Oracle-memory consolidates learnings automatically)
```

**What you get:**
- Deep analysis of test failure
- Root cause identification
- Suggested fix with explanation
- Test cases to prevent regression
- Pattern saved for future similar bugs

---

## 💡 Real-World Use Cases

### Use Case 1: Onboarding to Legacy Code

**Problem:** You inherited a 50K line codebase with zero docs.

**Solution:**
```bash
# Build knowledge graph
oracle-scanner *full-scan ./src/
oracle-architect *map-architecture

# Generate executive summary
oracle-memory *query type="architecture" 

# Create documentation
oracle-scribe *document-codebase depth="comprehensive"
```

**Result:** Complete architecture map, design patterns identified, auto-generated docs.

---

### Use Case 2: Refactoring Safely

**Problem:** Need to refactor a critical module without breaking things.

**Solution:**
```bash
# Analyze current state
oracle-scanner *analyze ./src/billing/

# Detect dependencies
oracle-prophet *find-dependencies module="billing"

# Plan refactoring
oracle-architect *design-refactor target="billing" goal="extract-payment-service"

# Implement with LSP guidance (no regex, semantic operations)
oracle-forge *implement-refactor plan=[architect-output] mode="tdd"

# Validate quality
oracle-critic *validate threshold=9.0
```

**Result:** Safe refactor with tests, zero regressions, improved architecture.

---

### Use Case 3: Performance Optimization

**Problem:** API response times are slow but you don't know why.

**Solution:**
```bash
# Profile the code
oracle-scanner *profile ./api/ include-traces=true

# Detect bottlenecks
oracle-optimizer *analyze-performance target="api-endpoints"

# Get optimization plan
oracle-optimizer *suggest-optimizations impact="high" effort="low"

# Oracle remembers what worked
oracle-memory *query type="optimization" context="api-performance"
```

**Result:** Specific bottlenecks identified, optimization suggestions ranked by ROI.

---

### Use Case 4: Learning From Bugs

**Problem:** Same types of bugs keep appearing in your codebase.

**Solution:**
```bash
# After fixing a bug, consolidate the learning
oracle-memory *consolidate session=[current-session]

# Later, when Oracle sees similar code:
oracle-prophet *predict-issues file="./src/new-feature.ts"

# Oracle will warn: "This pattern caused bug #127 before"
```

**Result:** Oracle prevents recurring bugs by learning from history.

---

## 🧬 Key Features

### 1. **Infinite Memory**
- Never forgets patterns, bugs, or solutions
- Learns from every project you work on
- Cross-project knowledge transfer
- 3-level hierarchy: global / project / session

### 2. **Adaptive Thinking**
- Automatically adjusts reasoning depth based on complexity
- Simple tasks: instant responses
- Complex tasks: deep analysis with extended reasoning
- Saves costs by not over-thinking simple problems

### 3. **LSP-Powered Code Intelligence**
- Go-to-definition (semantic, not regex)
- Find all references
- Rename symbols safely
- Type-aware code generation
- Diagnostics integration

### 4. **Quality Gates (9.0/10 threshold)**
- Oracle-critic validates ALL outputs
- VETO power (nothing bypasses validation)
- 28% more rigorous than standard squads
- Prevents low-quality suggestions

### 5. **Self-Healing**
- Detects when plans fail
- Automatically adjusts strategy
- Learns from failures
- Improves over time

---

## 📋 Available Agents

### Perception Layer
- **oracle-scanner** 🔍 - Deep context analysis, multi-dimensional scanning
- **oracle-prophet** 🔮 - Pattern detection, evolution prediction, technical debt forecasting

### Intelligence Layer  
- **oracle-critic** ⚖️ - Rigorous validation with VETO power (9.0/10 threshold)

### Execution Layer
- **oracle-forge** ⚒️ - LSP-guided TDD implementation, type-safe code generation

### Evolution Layer
- **oracle-memory** 🧠 - Infinite memory, knowledge graphs, transfer learning

---

## 🎓 How Oracle Learns

Oracle builds a **knowledge graph** of everything it analyzes:

```
.oracle-state/
├── global/              # Cross-project learnings
│   ├── patterns/        # Design patterns catalog
│   ├── learnings/       # Bug patterns, solutions
│   └── embeddings/      # For semantic search
├── projects/            # Per-project knowledge
│   └── your-project/
│       ├── context/
│       └── decisions/
└── sessions/            # Per-session work
```

**What gets learned:**
- Patterns that work (and don't work)
- Common bugs and their fixes
- Architecture decisions and rationale
- Performance optimizations that succeeded
- Security vulnerabilities detected

**How it helps:**
- Suggests fixes based on similar past bugs
- Warns about anti-patterns you've seen before
- Recommends architectures that worked in similar projects
- Auto-completes based on your coding style

---

## ⚙️ Configuration

### LSP Integration

Oracle uses Language Server Protocol for semantic code operations.

```json
// config/lsp-config.json
{
  "lsp": {
    "languages": {
      "typescript": {
        "server": "typescript-language-server",
        "rootPatterns": ["tsconfig.json"]
      },
      "python": {
        "server": "pylsp",
        "rootPatterns": ["setup.py"]
      }
    }
  }
}
```

### Memory Settings

```json
// config/memory-config.json
{
  "memory": {
    "hierarchical": true,
    "levels": {
      "global": {
        "promotionThreshold": 0.8  // High-confidence learnings go global
      }
    },
    "compaction": {
      "strategy": "wave-compress",
      "threshold": 100000
    }
  }
}
```

### Adaptive Thinking

```json
// config/thinking-budget-config.json
{
  "thinking": {
    "adaptive": true,
    "modes": {
      "disabled": { "budget": 0 },      // Simple tasks
      "enabled": { "budget": 3000 },    // Medium complexity
      "adaptive": { "budget": 5000 }    // Complex reasoning
    }
  }
}
```

---

## 🔄 Workflows

### Oracle Insight Pipeline

Complete end-to-end codebase analysis:

```bash
squad workflow oracle-insight-pipeline context="Analyze authentication module"

# Pipeline runs:
# 1. oracle-scanner → Deep scan
# 2. oracle-prophet → Pattern detection  
# 3. oracle-critic → Quality validation
# 4. oracle-forge → Fix implementation (if needed)
# 5. oracle-memory → Learning consolidation
```

---

## 📊 Success Metrics

Oracle tracks and optimizes:

- **Quality Score:** All outputs must meet 9.0/10 threshold
- **Cost Efficiency:** Auto-suggests model downgrades when possible
- **Pattern Confidence:** Only learns from high-confidence insights (>= 0.8)
- **Fix Success Rate:** Tracks which suggestions actually worked

---

## 🆚 Oracle vs Other Squads

| Feature | Standard Squad | Oracle Supreme |
|---------|---------------|----------------|
| Quality Threshold | 7.0/10 | **9.0/10** (+28%) |
| Memory | Session-only | **Infinite** |
| Learning | None | **Cross-project** |
| LSP Integration | ❌ | **✅ Full suite** |
| Adaptive Thinking | ❌ | **✅ Auto-adjusts** |
| Code Intelligence | Regex | **Semantic (LSP)** |
| Self-Healing | ❌ | **✅ Learns from failures** |

---

## 🤝 Contributing

Oracle Supreme Squad is designed to grow smarter over time. Contributions welcome:

1. **New Patterns:** Add to `oracle-prophet` pattern catalog
2. **Bug Signatures:** Extend `oracle-healer` bug detection
3. **Optimizations:** Contribute to `oracle-optimizer` suggestions
4. **Documentation:** Improve `oracle-scribe` templates

---

## 📝 License

MIT

---

## 🔗 Links

- **Repository:** https://github.com/gutomec/oracle-supreme-squad
- **Validation:** 100/100 ✅
- **Status:** Production Ready

---

**Oracle Supreme Squad** - Because your code deserves more than guesswork. 🔮✨

*Built with advanced patterns for developers who demand excellence.*
