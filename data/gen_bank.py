"""Generator for data/questions.json and data/flashcards.json. Run once; do not commit."""
import json
from collections import Counter

REF = {
    "system-design": "#/ml-system-design",
    "transformers": "#/transformers",
    "ml-fundamentals": "#/ml-fundamentals",
    "llm-systems": "#/llm-systems",
    "rag": "#/rag-search",
    "recsys": "#/recsys",
    "coding": "#/coding",
    "ml-coding": "#/coding",
    "debugging": "#/debugging",
    "deep-dive": "#/project-deep-dive",
    "behavioral": "#/behavioral",
    "agent-design": "#/agent-design",
    "research": "#/transformers",
}

questions = []
counters = {}

def Q(category, difficulty, time_min, frequency, text, companies=(), label="REPRESENTATIVE PRACTICE",
      coding=False, answer_available=True, answer_ref=None, note=""):
    counters[category] = counters.get(category, 0) + 1
    qid = f"q-{category}-{counters[category]:03d}"
    src_note = note
    if companies and not note:
        src_note = "Representative practice question; not an actual candidate report."
    questions.append({
        "id": qid,
        "question": text,
        "companies": list(companies),
        "category": category,
        "difficulty": difficulty,
        "time_min": time_min,
        "frequency": frequency,
        "label": label,
        "coding": coding,
        "answer_available": answer_available,
        "answer_ref": answer_ref or REF[category],
        "source": {"url": "", "accessed": "2026-10-01", "note": src_note},
    })

# ---------------- system-design (20) ----------------
Q("system-design", "hard", 45, "high",
  "Design a real-time ETA prediction service for a ride-hailing platform: architecture, feature pipeline, training/serving skew handling, and a 50ms p99 latency budget.",
  companies=("uber",))
Q("system-design", "hard", 45, "high",
  "Design a dispatch matching system that assigns couriers to orders at city scale: constraints, objective function, batching window, and how you would evaluate it offline.",
  companies=("doordash",))
Q("system-design", "hard", 45, "high",
  "Design an ads click-through-rate prediction system from ad request to bid: training pipeline, feature store, model refresh cadence, and online serving path.")
Q("system-design", "hard", 45, "medium",
  "Design a fraud detection system for a payments platform: label latency, severe class imbalance, adversarial drift, and feedback loops from actions taken.")
Q("system-design", "hard", 45, "medium",
  "Design a large-scale LLM inference-serving platform across GPU clusters: request scheduling, autoscaling, multi-tenant isolation, and failure handling.",
  companies=("crusoe",))
Q("system-design", "hard", 45, "high",
  "Design a search relevance stack (query rewriting, retrieval, multi-stage ranking): components, offline vs online evaluation, and where an LLM fits in the pipeline.")
Q("system-design", "medium", 30, "high",
  "Design a feature store serving 10k features at under 10ms p99 with point-in-time correctness for training.")
Q("system-design", "medium", 30, "medium",
  "Design a model monitoring and drift detection system covering 200 production models: what you track, alerting thresholds, and the remediation loop.")
Q("system-design", "medium", 30, "medium",
  "Design an A/B testing platform for ML models: randomization unit, metric hierarchy, guardrails, and handling network interference.")
Q("system-design", "hard", 45, "medium",
  "Design enterprise search over 100M permissioned documents: indexing, retrieval, ranking, freshness, and access-control enforcement at query time.",
  companies=("glean",))
Q("system-design", "hard", 45, "high",
  "Design a recommendation feed for 50M DAU: candidate generation, ranking, explore/exploit, cold start, and diversity controls.")
Q("system-design", "hard", 45, "low",
  "Design a training platform for 100B-parameter models: job orchestration, checkpointing, elastic recovery from node failures, and observability.")
Q("system-design", "medium", 30, "medium",
  "Design a real-time bidding system with a 100ms auction deadline: where CTR/CVR models run and what happens on timeout.")
Q("system-design", "medium", 30, "medium",
  "Design a content-moderation pipeline combining classifiers and LLM judges at high throughput: routing, cost control, and appeal handling.")
Q("system-design", "medium", 30, "low",
  "Design a data-labeling and active-learning loop for a vision model: sampling strategy, annotator quality control, and model-in-the-loop pre-labeling.")
Q("system-design", "hard", 45, "medium",
  "Design a code-search and code-understanding system over a large monorepo to power an AI coding assistant: indexing, retrieval, and freshness on every commit.",
  companies=("factory",))
Q("system-design", "medium", 30, "medium",
  "Design an anomaly detection system for operational metrics with strict alert-fatigue constraints: detection, alerting, and feedback from on-call.")
Q("system-design", "hard", 45, "medium",
  "Design a customer-support agent platform: orchestration, tool access, guardrails, evaluation harness, and human handoff criteria.",
  companies=("sierra",))
Q("system-design", "medium", 30, "low",
  "Design a streaming feature pipeline with exactly-once semantics from Kafka to an online feature store: failure modes and backfill strategy.")
Q("system-design", "medium", 30, "high",
  "Design a vector-search service for 1B embeddings: index structure, recall/latency trade-offs, filtering, and handling embedding-version updates.")

# ---------------- transformers (18) ----------------
Q("transformers", "medium", 10, "high",
  "Derive scaled dot-product attention and explain precisely why dividing by sqrt(d_k) matters for training stability.")
Q("transformers", "medium", 10, "high",
  "Compare pre-norm vs post-norm transformer blocks: gradient flow, training stability, and why modern LLMs converged on pre-norm.")
Q("transformers", "medium", 15, "high",
  "Explain rotary positional embeddings (RoPE): the rotation construction, and why it extrapolates to longer sequences better than learned absolute embeddings.")
Q("transformers", "medium", 10, "high",
  "Why do large models use grouped-query attention (GQA)? Quantify the KV-cache memory savings relative to full multi-head attention.",
  companies=("openai",))
Q("transformers", "medium", 10, "medium",
  "Explain ALiBi positional bias: how it is constructed and what its length-extrapolation behavior looks like in practice.")
Q("transformers", "hard", 15, "medium",
  "What causes attention sinks in long-context models, and how do they affect KV-cache eviction policies?")
Q("transformers", "easy", 5, "high",
  "Derive the time and memory complexity of self-attention as a function of sequence length n, hidden size d, and number of heads h.")
Q("transformers", "medium", 10, "medium",
  "Explain SwiGLU/GeGLU gated activations: the construction and why they outperform ReLU in large language models.")
Q("transformers", "medium", 15, "high",
  "How does FlashAttention reduce HBM memory IO? Explain the tiling and recomputation idea without writing code.")
Q("transformers", "medium", 10, "medium",
  "Compare absolute, relative, and rotary positional encodings: what breaks for each when the test sequence is longer than training?")
Q("transformers", "easy", 5, "high",
  "Explain multi-head attention: why use multiple smaller heads instead of one large head of the same total dimension?")
Q("transformers", "easy", 10, "medium",
  "Contrast encoder-only, decoder-only, and encoder-decoder architectures: the attention masking in each and when you would choose each.",
  companies=("anthropic",))
Q("transformers", "easy", 5, "high",
  "Explain layer normalization in a transformer block: the formula, and why it is preferred over batch normalization here.")
Q("transformers", "hard", 15, "medium",
  "How do you extend a trained model's context length: NTK-aware RoPE scaling vs YaRN vs continued pretraining? Compare cost and quality.")
Q("transformers", "medium", 15, "high",
  "Explain mixture-of-experts routing: top-k gating, the auxiliary load-balancing loss, expert capacity, and what happens when routing collapses.")
Q("transformers", "hard", 15, "low",
  "Why do transformers struggle with length generalization on algorithmic tasks (e.g., parity, addition)? What do the known fixes change?")
Q("transformers", "hard", 15, "low",
  "Explain the residual stream view of a transformer: what does it mean, mechanistically, for an attention head to 'write' to the residual stream?")
Q("transformers", "medium", 10, "high",
  "Contrast causal masking during training with KV-cached incremental decoding at inference: what is recomputed, what is reused, and where the complexity goes.")

# ---------------- ml-fundamentals (18) ----------------
Q("ml-fundamentals", "medium", 15, "high",
  "Derive the bias-variance decomposition of expected squared error and explain how it guides model selection in practice.")
Q("ml-fundamentals", "easy", 10, "high",
  "L1 vs L2 regularization: give the geometric intuition for why L1 induces sparsity, and state when you would pick each.")
Q("ml-fundamentals", "medium", 10, "high",
  "Why does AdamW decouple weight decay from the adaptive update? Show exactly how it differs from Adam with L2 regularization added to the loss.")
Q("ml-fundamentals", "easy", 5, "medium",
  "Explain gradient clipping: what failure mode does it fix, and when is it necessary versus papering over a bug?")
Q("ml-fundamentals", "medium", 10, "high",
  "Derive the gradient of logistic regression and explain why cross-entropy is preferred over MSE for classification.")
Q("ml-fundamentals", "easy", 10, "high",
  "Explain the vanishing/exploding gradient problem in deep networks and name three concrete mitigations with their mechanisms.")
Q("ml-fundamentals", "easy", 5, "medium",
  "What is label smoothing, and how does it change the learned decision boundary and model calibration?")
Q("ml-fundamentals", "medium", 10, "medium",
  "Compare bagging vs boosting: their effects on bias and variance, and give one failure mode of each.")
Q("ml-fundamentals", "medium", 10, "high",
  "Explain ROC-AUC vs PR-AUC: which would you report for a fraud model with 1% positive rate, and why?")
Q("ml-fundamentals", "medium", 15, "medium",
  "What is the EM algorithm? Walk through the E-step and M-step for a Gaussian mixture model.")
Q("ml-fundamentals", "easy", 5, "high",
  "Explain dropout at train time vs test time: why the scaling factor, and what goes wrong if you forget it?")
Q("ml-fundamentals", "easy", 5, "low",
  "Derive why the unbiased sample variance estimator divides by n-1 instead of n.")
Q("ml-fundamentals", "easy", 5, "medium",
  "Explain early stopping as implicit regularization: how do you choose the patience and what are you actually regularizing?")
Q("ml-fundamentals", "easy", 5, "medium",
  "What is the curse of dimensionality, and how does it specifically degrade k-NN classifiers?")
Q("ml-fundamentals", "medium", 10, "medium",
  "Explain classifier calibration: compare Platt scaling, isotonic regression, and temperature scaling, including data requirements.")
Q("ml-fundamentals", "easy", 5, "medium",
  "Why do we standardize features for gradient-based optimization, and why is it largely unnecessary for tree-based models?")
Q("ml-fundamentals", "medium", 10, "medium",
  "Explain the difference between MLE and MAP estimation, and give a concrete example where they disagree.")
Q("ml-fundamentals", "easy", 10, "medium",
  "What is a learning-rate schedule, and why does warmup followed by cosine annealing work well for large models?")

# ---------------- llm-systems (15) ----------------
Q("llm-systems", "medium", 10, "high",
  "Explain the prefill vs decode phases of LLM serving: why their compute/memory profiles differ and what that implies for batching.")
Q("llm-systems", "easy", 10, "high",
  "What exactly is stored in the KV cache? Derive how its size scales with batch size, sequence length, layers, heads, and head dimension.")
Q("llm-systems", "medium", 15, "high",
  "Compare tensor parallelism, pipeline parallelism, and data parallelism for serving a 70B model: communication patterns and when each is the bottleneck.",
  companies=("crusoe",))
Q("llm-systems", "medium", 10, "high",
  "Explain continuous batching (vLLM-style): how does it improve throughput over static batching, and what scheduling problem remains?")
Q("llm-systems", "medium", 10, "medium",
  "What is PagedAttention and what KV-cache fragmentation problem does it solve?")
Q("llm-systems", "medium", 15, "medium",
  "Explain speculative decoding: the draft-model/verify loop, the acceptance criterion, and the conditions under which it actually speeds up generation.")
Q("llm-systems", "hard", 20, "medium",
  "How would you serve a 1M-token-context model: what breaks first - KV-cache memory, attention compute, or interconnect bandwidth? Quantify each.",
  companies=("xai",))
Q("llm-systems", "medium", 15, "high",
  "Quantization for LLM serving: compare GPTQ/AWQ vs dynamic INT8 vs FP8 on accuracy, throughput, and hardware constraints.")
Q("llm-systems", "hard", 15, "low",
  "Explain disaggregated prefill/decode serving: the throughput benefits and the cost of transferring KV state between pools.")
Q("llm-systems", "easy", 10, "medium",
  "How does beam search differ from stochastic sampling (temperature, top-k, top-p)? When is each decoding strategy appropriate?")
Q("llm-systems", "easy", 5, "high",
  "Explain the latency/throughput trade-off in LLM batching: define TTFT and TPOT and say which user experience each governs.")
Q("llm-systems", "medium", 15, "medium",
  "What is FSDP/ZeRO-3 sharding during training? Contrast its communication pattern with tensor parallelism used at inference.")
Q("llm-systems", "medium", 10, "low",
  "Explain prefix caching and radix-tree-based KV reuse across requests: what workloads benefit most?")
Q("llm-systems", "medium", 15, "medium",
  "How do you benchmark an LLM serving stack: which metrics, which workloads, and what are the common benchmarking pitfalls?")
Q("llm-systems", "medium", 20, "medium",
  "Design the rollout of a new model version behind a production API: canary strategy, shadow traffic, and evaluation gates before full cutover.",
  companies=("openai",))

# ---------------- rag (12) ----------------
Q("rag", "easy", 10, "high",
  "Why rerank after the initial retrieval step? Compare bi-encoder recall with cross-encoder precision and the cost trade-off.")
Q("rag", "hard", 30, "high",
  "Design a RAG pipeline over enterprise documents with access controls: chunking, indexing, retrieval, generation with citations, and permission enforcement.",
  companies=("glean",))
Q("rag", "medium", 10, "high",
  "Compare dense, sparse (BM25), and hybrid retrieval: the failure modes of each and when each wins.")
Q("rag", "medium", 10, "medium",
  "Explain query rewriting and HyDE: when does expanding the query help retrieval, and when does it hurt?")
Q("rag", "medium", 10, "high",
  "How do you chunk long documents for RAG? Trade-offs of chunk size, overlap, and structure-aware splitting.")
Q("rag", "medium", 15, "high",
  "How do you evaluate a RAG system: which metrics for the retrieval stage vs the generation stage, and how do you build a golden evaluation set?")
Q("rag", "medium", 10, "medium",
  "Explain the 'lost in the middle' problem in long-context RAG and give three concrete mitigations.")
Q("rag", "medium", 15, "medium",
  "How do you keep a RAG index fresh: incremental updates, deletions, and migrating to a new embedding model version?")
Q("rag", "medium", 10, "high",
  "Compare RAG vs fine-tuning vs prompt engineering for injecting domain knowledge into an LLM product: cost, freshness, and failure modes.")
Q("rag", "medium", 20, "medium",
  "Design grounded answer generation where every factual claim carries a citation that an auditor can verify: pipeline and failure handling.",
  companies=("sierra",))
Q("rag", "hard", 15, "low",
  "Explain late-interaction retrieval (ColBERT): index-time storage cost vs query-time quality, and when it beats bi-encoders.")
Q("rag", "medium", 15, "medium",
  "How do you handle multi-hop questions in RAG: iterative retrieval vs query decomposition? Compare the approaches.")

# ---------------- recsys (10) ----------------
Q("recsys", "medium", 20, "high",
  "Design a two-tower retrieval model for recommendations: training objective, negative sampling strategy, and how you serve it at scale.",
  companies=("uber",))
Q("recsys", "hard", 20, "medium",
  "How do you handle position bias in learning-to-rank: IPS weighting, two-tower click models, and randomization? Compare their assumptions.",
  companies=("doordash",))
Q("recsys", "easy", 10, "high",
  "Define Recall@K, NDCG, and MRR precisely, and say which you would optimize for a social feed vs a search box.")
Q("recsys", "easy", 10, "medium",
  "Explain matrix factorization vs deep collaborative filtering, and how each handles the cold-start problem.")
Q("recsys", "medium", 15, "medium",
  "How do you do exploration in production recommenders: epsilon-greedy, UCB, Thompson sampling? Trade-offs in a live system.")
Q("recsys", "medium", 15, "medium",
  "Explain DIN/DIEN-style user interest modeling: why apply attention over the user's behavior sequence instead of pooling?")
Q("recsys", "hard", 20, "medium",
  "How do you evaluate a ranking model offline: replay bias, and what does counterfactual evaluation buy you over naive replay?")
Q("recsys", "medium", 20, "medium",
  "Design a multi-task ranking model (MMoE/PLE): shared vs task-specific towers, loss weighting, and how you detect negative transfer.")
Q("recsys", "medium", 10, "low",
  "Explain session-based recommendation: what breaks in your modeling when user IDs are unreliable or missing?")
Q("recsys", "medium", 15, "medium",
  "How do you detect and mitigate feedback loops and popularity bias in a production recommender?")

# ---------------- coding (15) ----------------
Q("coding", "medium", 20, "high",
  "Implement an LRU cache with O(1) get and put operations. Explain your choice of underlying data structures.",
  companies=("uber",), coding=True)
Q("coding", "medium", 20, "high",
  "Merge k sorted linked lists into one sorted list. Give the optimal algorithm and analyze its time complexity.",
  coding=True)
Q("coding", "medium", 20, "medium",
  "Find the top-k frequent elements in a data stream using limited memory. Discuss the exact vs approximate trade-off.",
  coding=True)
Q("coding", "medium", 20, "medium",
  "Implement a token-bucket rate limiter that is safe for concurrent use. How do you handle clock skew?",
  coding=True)
Q("coding", "hard", 30, "medium",
  "Design a data structure supporting: add/update courier location, and query the nearest available couriers to a point. Analyze the complexity.",
  companies=("doordash",), coding=True)
Q("coding", "medium", 20, "medium",
  "Word ladder: find the shortest transformation sequence from beginWord to endWord. Explain why BFS gives the optimal answer.",
  coding=True)
Q("coding", "medium", 20, "medium",
  "Serialize and deserialize a binary tree to/from a string. Your format must handle arbitrary tree shapes.",
  coding=True)
Q("coding", "hard", 25, "medium",
  "Find the median of two sorted arrays in O(log(min(m,n))) time. Walk through the partition invariant.",
  coding=True)
Q("coding", "medium", 25, "medium",
  "Implement consistent hashing with virtual nodes. Show how keys redistribute when a node is added or removed.",
  coding=True)
Q("coding", "medium", 20, "medium",
  "Trapping rain water: derive the two-pointer O(1)-space solution from the DP formulation.",
  coding=True)
Q("coding", "medium", 20, "medium",
  "Design a time-based key-value store: set(key, value, timestamp) and get(key, timestamp) returning the latest value at or before the timestamp.",
  coding=True)
Q("coding", "easy", 15, "high",
  "Longest substring without repeating characters: implement the sliding-window solution and prove it is O(n).",
  coding=True)
Q("coding", "medium", 20, "low",
  "Implement a thread-safe bounded producer-consumer queue from primitives (locks/condition variables), no library queue.",
  coding=True)
Q("coding", "medium", 20, "medium",
  "Course schedule: detect whether all courses can be finished given prerequisites, and return one valid order. Handle cycles.",
  coding=True)
Q("coding", "medium", 25, "medium",
  "Design an autocomplete system: a trie storing query frequencies that returns top-k suggestions for a prefix, with updates.",
  coding=True)

# ---------------- ml-coding (12) ----------------
Q("ml-coding", "medium", 25, "high",
  "Implement scaled dot-product attention from scratch in NumPy, including the causal mask, without using any autograd.",
  coding=True, answer_ref="#/transformers")
Q("ml-coding", "easy", 20, "medium",
  "Implement k-means clustering from scratch and explain why the result is sensitive to initialization; implement one mitigation.",
  coding=True)
Q("ml-coding", "easy", 20, "high",
  "Implement logistic regression with batch gradient descent in NumPy, then add L2 regularization and show the gradient change.",
  coding=True)
Q("ml-coding", "hard", 30, "medium",
  "Implement byte-pair encoding training on a toy corpus: the merge loop, tokenization, and handling of unseen text.",
  coding=True, answer_ref="#/transformers")
Q("ml-coding", "medium", 25, "medium",
  "Implement beam search decoding for a toy language model given a next-token probability function; discuss the length-normalization issue.",
  coding=True, answer_ref="#/llm-systems")
Q("ml-coding", "medium", 20, "medium",
  "Implement mini-batch gradient descent with momentum on a quadratic objective and empirically compare convergence to vanilla SGD.",
  coding=True)
Q("ml-coding", "medium", 25, "high",
  "Implement multi-head attention with causal masking in PyTorch, showing the exact tensor shapes at each step.",
  coding=True, answer_ref="#/transformers")
Q("ml-coding", "medium", 25, "low",
  "Implement a decision-tree split: compute the Gini impurity for candidate splits on one feature and grow a single level.",
  coding=True)
Q("ml-coding", "easy", 15, "high",
  "Implement temperature scaling and nucleus (top-p) sampling from raw logits in NumPy; explain what each parameter controls.",
  coding=True, answer_ref="#/llm-systems")
Q("ml-coding", "hard", 30, "medium",
  "Implement batch normalization forward and backward passes from scratch; explain the train/test behavior difference.",
  coding=True, answer_ref="#/deep-learning")
Q("ml-coding", "hard", 30, "low",
  "Implement a toy IVF index probe in NumPy: k-means coarse quantizer, inverted lists, and top-k search with nprobe.",
  coding=True, answer_ref="#/rag-search")
Q("ml-coding", "medium", 20, "medium",
  "Implement gradient accumulation to simulate a large effective batch size; explain where the equivalence with a true large batch breaks down.",
  coding=True, answer_ref="#/deep-learning")

# ---------------- debugging (10) ----------------
Q("debugging", "medium", 20, "high",
  "Your training loss diverges after 2000 steps of stable training: walk through your diagnosis checklist in order of likelihood.")
Q("debugging", "easy", 15, "high",
  "Training loss keeps dropping but validation loss plateaus: what do you check, in order, and what does each check tell you?")
Q("debugging", "hard", 30, "medium",
  "Your recommender's CTR drops 5% the day after a feature pipeline change: lay out your root-cause investigation plan.")
Q("debugging", "easy", 10, "high",
  "Loss is NaN on the very first training step: enumerate the possible causes and the fastest check for each.")
Q("debugging", "medium", 20, "medium",
  "You suspect your LLM fine-tune memorized the evaluation set: how do you detect contamination and what do you do about it?")
Q("debugging", "medium", 20, "medium",
  "Inference p99 latency spiked right after a model update: describe your debugging plan from metrics down to code.")
Q("debugging", "medium", 20, "medium",
  "Embedding retrieval recall dropped after a re-index: what could have changed, and how do you bisect the regression?")
Q("debugging", "hard", 30, "low",
  "An A/B test reads neutral on the primary metric but revenue dipped: how do you investigate the metric divergence?")
Q("debugging", "hard", 25, "medium",
  "Distributed training hangs at the same step on 64 GPUs every run: how do you find the straggler or the deadlock?")
Q("debugging", "medium", 15, "medium",
  "Gradients are all zero in the first layer but nonzero in later layers: what does that signature tell you, and what do you check?")

# ---------------- deep-dive (8) ----------------
Q("deep-dive", "hard", 30, "high",
  "Walk me through your most complex ML project end to end: problem framing, data, modeling choices, deployment, and measured impact.",
  companies=("uber",))
Q("deep-dive", "hard", 30, "high",
  "Tell me about a time your model worked offline but failed online: what was the training-serving skew and how did you fix it?")
Q("deep-dive", "hard", 30, "medium",
  "Describe a ranking system you built: how you designed the objective, engineered features, and evaluated before launch.",
  companies=("doordash",))
Q("deep-dive", "medium", 20, "high",
  "What is the hardest technical trade-off you made on an ML project, what did you choose, and what would you do differently now?")
Q("deep-dive", "hard", 30, "medium",
  "Describe a large-scale training or serving system you built: where were the bottlenecks and how did you remove them?",
  companies=("crusoe",))
Q("deep-dive", "medium", 20, "medium",
  "Tell me about a project where you had to simplify the model to ship on time: what did you cut and why was it safe to cut?")
Q("deep-dive", "hard", 30, "medium",
  "Walk through an ML system where latency was the binding constraint: your full optimization stack from model to serving.",
  companies=("factory",))
Q("deep-dive", "medium", 20, "medium",
  "Describe a time you disagreed with a stakeholder about the right ML approach: how did you resolve it and what was the outcome?")

# ---------------- behavioral (8) ----------------
Q("behavioral", "medium", 15, "high",
  "Tell me about a time you influenced a technical decision without having formal authority over it.")
Q("behavioral", "medium", 15, "high",
  "Describe a real conflict with a teammate or manager: what happened, what you did, and the outcome.")
Q("behavioral", "medium", 15, "high",
  "Tell me about your biggest failure as an ML engineer and what you concretely changed afterward.")
Q("behavioral", "easy", 10, "high",
  "Why this company and this role? Tailor your answer to the interviewer's team and the problems they own.")
Q("behavioral", "medium", 15, "medium",
  "Tell me about a time you had to deliver under an unreasonable deadline: what did you scope down and how did you communicate it?")
Q("behavioral", "medium", 15, "medium",
  "Describe how you mentor junior engineers, with one concrete example and what changed for the mentee.")
Q("behavioral", "medium", 15, "medium",
  "Tell me about a time you pushed back on a product request because it was bad for ML quality: how did you make the case?")
Q("behavioral", "easy", 10, "low",
  "Where do you see your technical growth over the next two years, and what are you doing about it now?")

# ---------------- agent-design (8) ----------------
Q("agent-design", "hard", 45, "high",
  "Design an AI customer-support agent: tool use, guardrails, evaluation harness, escalation criteria for human handoff, and cost controls.",
  companies=("sierra",))
Q("agent-design", "hard", 45, "medium",
  "Design a coding agent over a large repo: repository understanding, planning, sandboxed tool execution, and a verification loop before proposing changes.",
  companies=("factory",))
Q("agent-design", "medium", 15, "medium",
  "Compare ReAct, plan-and-execute, and multi-agent orchestration: the failure mode of each and when each wins.")
Q("agent-design", "medium", 20, "high",
  "How do you evaluate an AI agent: task success rate, trajectory-level metrics, and the pitfalls of LLM-as-judge?")
Q("agent-design", "medium", 15, "medium",
  "Explain tool-calling reliability in agents: schema validation, retries, idempotency, and recovery when a tool call fails mid-trajectory.")
Q("agent-design", "medium", 15, "medium",
  "How do you bound an agent's cost and latency in production: step limits, model routing across steps, and caching?")
Q("agent-design", "medium", 20, "medium",
  "Design memory for a long-running agent: short-term context management, long-term memory store, and retrieval into the prompt.")
Q("agent-design", "medium", 15, "high",
  "What are the security risks of agents with tool access? Explain prompt-injection attack surfaces and concrete defenses.")

# ---------------- research (6) ----------------
Q("research", "hard", 30, "high",
  "Explain RLHF end to end: reward modeling from preferences, PPO vs DPO, and the known failure modes (reward hacking, mode collapse).",
  companies=("openai",), answer_ref="#/llm-systems")
Q("research", "medium", 20, "medium",
  "What is constitutional AI, and how does it differ from standard RLHF in practice - data, training loop, and limitations?",
  companies=("anthropic",), answer_ref="#/llm-systems")
Q("research", "hard", 30, "low",
  "Explain the key ideas behind AlphaFold 2's Evoformer: why pair representations, and what does the structure module add?",
  companies=("google-deepmind",), answer_ref="#/deep-learning")
Q("research", "medium", 20, "medium",
  "What do neural scaling laws (Chinchilla) say about compute-optimal training? Derive the parameter/token trade-off for a fixed FLOPs budget.",
  companies=("xai",), answer_ref="#/llm-systems")
Q("research", "hard", 25, "medium",
  "Explain direct preference optimization (DPO): derive it from the RLHF objective and state its assumptions and failure modes.",
  answer_ref="#/llm-systems")
Q("research", "hard", 25, "low",
  "What is the superposition hypothesis in mechanistic interpretability, and why does it matter for AI safety work?",
  companies=("anthropic",), answer_ref="#/transformers")

# ---------------- flashcards ----------------
flashcards = []
fcn = 0

def FC(deck, front, back, tags=None):
    global fcn
    fcn += 1
    flashcards.append({
        "id": f"fc-{fcn:03d}",
        "front": front,
        "back": back,
        "tags": tags or [deck],
        "deck": deck,
    })

# transformers deck (15)
FC("transformers", "Why divide attention logits by sqrt(d_k)?",
   "Without scaling, dot products grow with dimension d_k, pushing softmax into saturated regions with near-zero gradients. Dividing by sqrt(d_k) keeps the logits' variance near 1 (assuming unit-variance q/k), so attention weights stay diffuse early in training and gradients flow.")
FC("transformers", "Pre-norm vs post-norm: which do modern LLMs use and why?",
   "Pre-norm (norm before attention/MLP inside the residual branch). Post-norm places the norm on the main path, which shrinks gradients in deep stacks and makes training unstable without careful warmup. Pre-norm gives cleaner gradient flow, so virtually all modern LLMs use it.")
FC("transformers", "How does RoPE encode position?",
   "Rotary Position Embedding rotates each pair of query/key dimensions by an angle proportional to the token position, with frequencies decaying geometrically across dimensions. Relative position emerges from the dot product of rotated vectors, and it extrapolates to longer sequences better than learned absolute embeddings.")
FC("transformers", "What is grouped-query attention (GQA) and why use it?",
   "GQA shares one key/value head across a group of query heads - a middle ground between MHA and MQA. It cuts KV-cache memory roughly by the group size with minimal quality loss, which is why Llama-2-70B and most open models adopted it.")
FC("transformers", "What is the KV cache and what does it store?",
   "During autoregressive decoding, the keys and values of all previous tokens are cached so each new token only computes attention against cached K/V instead of recomputing them. It stores two tensors per layer of shape (batch, heads, seq_len, head_dim); memory grows linearly with sequence length.")
FC("transformers", "How does FlashAttention speed up attention?",
   "It tiles Q/K/V blocks to fit in SRAM, computes exact softmax via online rescaling, and recomputes attention in the backward pass instead of materializing the N x N matrix in HBM. The win is IO-awareness: attention is memory-bound, so avoiding HBM traffic gives 2-4x speedups with identical numerics.")
FC("transformers", "What is an attention sink?",
   "In long-context models, the first few tokens attract disproportionately high attention mass regardless of content - they act as a 'sink' the model uses to dump excess attention probability. This matters for KV-cache eviction: dropping initial tokens (as naive sliding windows do) degrades quality badly.")
FC("transformers", "Self-attention time and memory complexity?",
   "Time O(n^2 * d) and memory O(n^2) for the attention matrix with sequence length n and hidden size d (per head work is O(n^2 * d/h) across h heads). This quadratic scaling in n is what motivates FlashAttention, sparsity, and linear-attention variants.")
FC("transformers", "Why do LLMs use SwiGLU instead of ReLU?",
   "SwiGLU is a gated activation: (xW) * silu(xV). The multiplicative gate gives the FFN more expressive capacity per parameter than ReLU, and empirically it improves perplexity at the same compute. Most modern LLMs (Llama, PaLM) use it with the FFN hidden size scaled to ~8/3 * d to match parameter count.")
FC("transformers", "Why multiple attention heads instead of one big head?",
   "Multiple heads let the model attend to different representation subspaces and positional patterns simultaneously (e.g., one head tracks syntax, another coreference). A single head of the same total size can only express one attention distribution per token pair; heads add representational diversity, not just capacity.")
FC("transformers", "What is ALiBi?",
   "Attention with Linear Biases adds a fixed linear penalty to attention scores proportional to token distance, with a different slope per head. No learned position parameters at all. It extrapolates to longer sequences than trained on, though RoPE-based methods have largely superseded it.")
FC("transformers", "How do you extend a model's context length after pretraining?",
   "Three routes: (1) NTK-aware RoPE scaling - adjust rotary base frequencies, cheap but approximate; (2) YaRN - temperature-style interpolation of RoPE, better quality; (3) continued pretraining on long sequences, most expensive but highest quality. All need long-context eval to verify.")
FC("transformers", "What is the residual stream?",
   "The residual stream is the running sum that every attention head and MLP block reads from and adds to. Mechanistic interpretability views the model as heads 'writing' information (e.g., copying a name, moving a fact) into this shared channel and later layers reading it - it makes credit assignment across layers analyzable.")
FC("transformers", "MoE routing: what is the load-balancing loss for?",
   "Top-k gating routes each token to a few experts, but without constraint the router collapses onto a few popular experts. The auxiliary load-balancing loss penalizes uneven expert utilization, keeping all experts trained. Too strong a weight hurts specialization; too weak causes collapse and wasted capacity.")
FC("transformers", "Causal masking in training vs KV-cached decoding?",
   "In training, a lower-triangular mask lets all positions compute in parallel while preserving autoregressiveness. At inference, the KV cache stores past keys/values so each step only processes the new token - O(n) per step instead of O(n^2). The mask logic is equivalent; the compute pattern is incremental.")
