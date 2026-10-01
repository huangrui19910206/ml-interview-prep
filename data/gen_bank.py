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

# ml-fundamentals deck (12)
FC("ml-fundamentals", "BatchNorm vs LayerNorm: when is each used?",
   "BatchNorm normalizes across the batch dimension per feature - great for vision/CNNs but breaks with small or variable batch sizes and leaks batch statistics. LayerNorm normalizes across features per token, independent of batch size, which is why transformers use it. Never use BatchNorm in a transformer.")
FC("ml-fundamentals", "L1 vs L2 regularization: what is the practical difference?",
   "L2 (ridge) shrinks all weights smoothly toward zero, keeping every feature but small - good for dense signals. L1 (lasso) drives many weights exactly to zero via its diamond-shaped constraint geometry, performing feature selection. Use L1 when you suspect few features matter; L2 as the default.")
FC("ml-fundamentals", "Why does AdamW decouple weight decay?",
   "In Adam with L2 added to the loss, the decay gradient gets scaled by the adaptive denominator, so large-gradient parameters are decayed less - weight decay becomes coupled to gradient history. AdamW applies decay directly to the weights after the adaptive step, restoring the intended regularization. It is the standard for transformer training.")
FC("ml-fundamentals", "Bias-variance tradeoff in one paragraph?",
   "Expected error decomposes into bias^2 (error from wrong model assumptions), variance (error from sensitivity to training data), and irreducible noise. Simple models underfit (high bias); complex models overfit (high variance). More data reduces variance; better model class or features reduce bias.")
FC("ml-fundamentals", "ROC-AUC vs PR-AUC: which for imbalanced data?",
   "ROC-AUC measures ranking quality across all thresholds but is dominated by the abundant negative class - it looks optimistic at 1% positives. PR-AUC focuses on the positive class (precision vs recall) and is far more informative for fraud/disease detection. Report PR-AUC (and calibrated thresholds) for imbalanced problems.")
FC("ml-fundamentals", "Why cross-entropy instead of MSE for classification?",
   "MSE with sigmoid/softmax saturates: when the model is confidently wrong, gradients vanish and learning stalls. Cross-entropy's gradient is proportional to (prediction - target), staying strong exactly when the model is wrong. It is also the negative log-likelihood, matching probabilistic modeling.")
FC("ml-fundamentals", "What does dropout do at test time?",
   "At training, dropout randomly zeroes activations with probability p, forcing redundancy. At test time dropout is off, so activations must be scaled by (1-p) - or equivalently use inverted dropout (scale by 1/(1-p) during training) - to keep expected magnitudes consistent. Forgetting the scaling silently shifts every downstream layer's input distribution.")
FC("ml-fundamentals", "What is gradient clipping and when do you need it?",
   "Clipping rescales the gradient norm to a max threshold when it exceeds it, preventing single explosive updates from destroying training. It is essential in RNNs and sometimes transformers with spikes; but if you clip constantly, you are masking a deeper bug (bad LR, data corruption, loss scale).")
FC("ml-fundamentals", "MLE vs MAP: what is the difference?",
   "MLE picks parameters maximizing the data likelihood P(data|theta). MAP maximizes P(theta|data), proportional to likelihood times prior P(theta) - equivalently MLE with a regularization term from the log-prior. They disagree whenever the prior is informative, e.g., L2-regularized logistic regression is MAP with a Gaussian prior.")
FC("ml-fundamentals", "What is label smoothing and why use it?",
   "Label smoothing replaces hard 0/1 targets with soft targets (e.g., 0.1/K for wrong classes), penalizing overconfident predictions. It improves calibration and generalization slightly, and is standard in machine translation and pretraining. Do not use it when you need well-calibrated probabilities for decision thresholds without recalibration.")
FC("ml-fundamentals", "Why standardize features for gradient descent but not for trees?",
   "Gradient descent converges slowly when features have wildly different scales because the loss surface becomes an elongated valley - one learning rate cannot suit all directions. Tree splits only compare values within a single feature, so monotonic rescaling changes nothing. Distance-based methods (k-NN, SVM, k-means) need scaling too.")
FC("ml-fundamentals", "What is early stopping really regularizing?",
   "Early stopping halts training when validation loss stops improving, which limits how far weights can travel from initialization - effectively constraining model complexity like a norm penalty. Choose patience from the noise level of your validation curve (larger patience for noisy small validation sets), and always keep the best checkpoint, not the last.")

# llm-systems deck (12)
FC("llm-systems", "Prefill vs decode: what is the difference?",
   "Prefill processes the whole prompt in one parallel pass - compute-bound, like training. Decode generates one token at a time, each step loading the entire model weights and KV cache from HBM - memory-bandwidth-bound with tiny arithmetic intensity. This is why batching and KV-cache efficiency dominate serving optimization.")
FC("llm-systems", "Tensor vs pipeline vs data parallelism?",
   "Tensor parallelism shards individual layers across GPUs (needs fast NVLink, used within a node). Pipeline parallelism assigns whole layers to different GPUs (tolerates slower interconnect but suffers pipeline bubbles). Data parallelism replicates the model and splits the batch (needs the full model to fit on one GPU). 70B serving typically combines TP within a node and PP across nodes.")
FC("llm-systems", "What is continuous batching?",
   "Instead of waiting for a whole batch to finish, the server inserts new requests into the batch at each decoding step as soon as slots free up (vLLM/Orca style). This keeps the GPU saturated despite variable output lengths and raises throughput 3-10x over static batching. Scheduling policy (prefill vs decode priority) remains the hard part.")
FC("llm-systems", "What problem does PagedAttention solve?",
   "KV cache for variable-length sequences fragments GPU memory - naive contiguous allocation wastes space (internal fragmentation) and pre-allocation wastes more. PagedAttention stores KV cache in fixed-size blocks (pages) with a block table, like OS virtual memory, nearly eliminating waste and enabling larger batches.")
FC("llm-systems", "How does speculative decoding work?",
   "A small draft model generates k candidate tokens cheaply; the large target model verifies them in one parallel forward pass, accepting tokens that match its distribution. Accepted tokens are 'free' - speedup comes when the draft is accurate enough that most tokens are accepted. Gains are largest on easy, predictable text and small batch sizes.")
FC("llm-systems", "What are TTFT and TPOT?",
   "TTFT (time to first token) measures prefill + scheduling latency - what the user feels before streaming starts. TPOT (time per output token) measures decode speed - what governs streaming smoothness. Optimizing batching trades them off: bigger batches raise throughput but inflate both TTFT and TPOT.")
FC("llm-systems", "GPTQ/AWQ vs FP8 quantization: the tradeoff?",
   "GPTQ/AWQ are 4-bit weight-only methods: they shrink memory (so bigger batches fit) with small accuracy loss, but compute stays in FP16 - great for memory-bound decoding. FP8 quantizes weights and activations for actual faster math on Hopper GPUs, giving true compute speedups but needing hardware support and more careful calibration.")
FC("llm-systems", "What is disaggregated prefill/decode serving?",
   "Split the fleet into prefill-optimized pools (compute-heavy, high parallelism) and decode-optimized pools (memory-bandwidth-heavy), transferring KV cache between them per request. It raises utilization of both phases substantially, at the cost of KV-transfer latency over the network - worthwhile at scale (used by DistServe, Splitwise).")
FC("llm-systems", "Temperature vs top-p vs top-k sampling?",
   "Temperature rescales logits before softmax: <1 sharpens (greedy-like), >1 flattens (creative). Top-k keeps only the k most likely tokens. Top-p (nucleus) keeps the smallest set whose cumulative probability exceeds p, adapting to the distribution's entropy. In practice: temperature ~0.7 + top-p ~0.9 for chat; temperature 0 for factual/extraction tasks.")
FC("llm-systems", "How does KV-cache size scale?",
   "Per token: 2 (K and V) x layers x num_kv_heads x head_dim x bytes_per_element. For a 70B-class model (80 layers, 8 KV heads via GQA, 128 head dim, FP16): ~2*80*8*128*2 bytes = ~327KB per token. A 32k context is ~10GB per sequence - this is why GQA, quantization, and eviction policies exist.")
FC("llm-systems", "What is FSDP / ZeRO-3?",
   "Fully Sharded Data Parallel shards model parameters, gradients, and optimizer states across data-parallel workers, all-gathering parameters layer by layer just in time for compute. It lets you train models far larger than one GPU's memory with near-linear scaling, at the cost of extra all-gather communication per layer.")
FC("llm-systems", "How do you benchmark LLM serving correctly?",
   "Fix the workload first: realistic prompt-length and output-length distributions, Poisson arrivals at several QPS levels. Report throughput at a fixed latency SLO (e.g., p99 TPOT), not peak tokens/sec. Common pitfalls: benchmarking with fixed short prompts, ignoring TTFT, warming up improperly, and comparing across different quantization levels silently.")

# rag-search deck (8)
FC("rag-search", "Why rerank after retrieval?",
   "Bi-encoder retrieval is fast but shallow: it compresses query and document into single vectors, losing token-level interactions. A cross-encoder reranker jointly encodes query+document pairs with full attention - far more accurate but 100x slower. The two-stage design gets cross-encoder quality at bi-encoder cost by reranking only the top 50-200 candidates.")
FC("rag-search", "Recall@K vs NDCG: what do they measure?",
   "Recall@K is the fraction of relevant documents appearing in the top K - pure coverage, ignores order. NDCG@K weights by position with logarithmic discount and handles graded relevance - it rewards putting the best documents first. Optimize recall@K for the retrieval stage (feed the reranker well) and NDCG for final ranking quality.")
FC("rag-search", "Dense vs sparse (BM25) vs hybrid retrieval?",
   "Dense embeddings capture semantics and paraphrase but miss exact rare terms and need training data. BM25 excels at exact keyword/identifier matches with zero training but fails on vocabulary mismatch. Hybrid (dense + BM25 fused via RRF or weighted sum) beats either alone on most real workloads - use hybrid as the default.")
FC("rag-search", "How should you chunk documents for RAG?",
   "Chunk size trades context completeness against retrieval precision: 200-500 tokens with small overlap is a common starting point. Structure-aware splitting (by headings, paragraphs, code blocks) beats fixed windows because it preserves semantic units. Always keep metadata (source, section, page) on each chunk for citations and filtering.")
FC("rag-search", "What is the 'lost in the middle' problem?",
   "LLMs attend best to the start and end of long contexts and underweight the middle - so relevant chunks placed mid-context get ignored. Mitigations: rerank so the best chunks sit at the edges, compress/deduplicate context, use smaller top-k, or switch to map-reduce summarization for very long inputs.")
FC("rag-search", "How do you evaluate a RAG system?",
   "Split evaluation: retrieval metrics (recall@K, MRR on a labeled query-doc set) and generation metrics (faithfulness/citation precision, answer correctness vs references). Build a golden set of real user questions with judged answers; add faithfulness checks (does every claim have a supporting chunk?) since fluency alone hides hallucinations.")
FC("rag-search", "When does query rewriting / HyDE help vs hurt?",
   "HyDE (generate a hypothetical answer, embed it) helps when the query is vague or vocabulary-mismatched with documents, since the hypothetical answer lives in document-space. It hurts when the LLM hallucinates misleading content that drags retrieval off-topic, and it adds latency - gate it to queries where plain retrieval demonstrably fails.")
FC("rag-search", "RAG vs fine-tuning for domain knowledge?",
   "RAG: cheap, fresh (update the index, not the model), cites sources; fails when knowledge needs deep reasoning integration or the retriever misses. Fine-tuning: bakes knowledge into weights for fluent use, but expensive, goes stale, and risks hallucination without citations. Default to RAG for factual knowledge; fine-tune for style, format, and behavior.")

# system-design deck (8)
FC("system-design", "Sketch the canonical ML system design answer structure.",
   "1) Clarify: problem, scale, latency/throughput SLOs, offline vs online. 2) Data: sources, labels, feature pipeline. 3) Training: objective, model choice, evaluation. 4) Serving: architecture, caching, fallbacks. 5) Feedback loop: logging, monitoring, retraining triggers. 6) Trade-offs and failure modes. Hit all six and you cover what interviewers score.")
FC("system-design", "Training-serving skew: what causes it and how do you detect it?",
   "Causes: features computed differently offline vs online, label definitions drifting, data leakage in training, population shift. Detect with shadow serving (compare offline-replay predictions to live), feature-distribution monitors, and prediction-drift alerts. Fix by unifying feature code paths (one feature store, point-in-time correctness).")
FC("system-design", "How do you design an ML A/B test correctly?",
   "Randomize at the right unit (user, not request, to avoid interference), pre-register primary vs guardrail metrics, size the test from minimum detectable effect and variance, run long enough to cover weekly cycles, and watch for novelty effects and network interference. For models, also shadow-test before the live experiment.")
FC("system-design", "Online vs offline evaluation for ranking models?",
   "Offline (replay on logged data) is fast and cheap but suffers presentation bias - you only observe feedback on what was shown. Counterfactual/IPS estimators partially correct this. Online A/B tests measure true causal impact but are slow and risky. Mature teams gate launches on offline metrics, then confirm with online experiments.")
FC("system-design", "What belongs in a feature store and why?",
   "A feature store centralizes feature definitions so training and serving compute identical values (killing skew), provides point-in-time-correct historical values for training, and serves low-latency online lookups. Without one, every team reimplements pipelines and skew bugs multiply.")
FC("system-design", "How do you handle cold start in recommenders?",
   "New users: onboarding signals, popularity priors, explore-heavy bandits, demographic/contextual fallbacks. New items: content-based features, embedding via item metadata, exploration budgets to gather initial interactions. Measure time-to-first-good-recommendation as the key metric.")
FC("system-design", "What do you monitor for a production ML model?",
   "Four layers: (1) input feature distributions and null rates (data drift), (2) prediction distribution and calibration drift, (3) business metrics the model drives, (4) system health (latency, error rate, fallback rate). Alert on statistically significant shifts with enough volume to avoid noise, and always keep a human-readable dashboard per model.")
FC("system-design", "Explore vs exploit in production: practical approaches?",
   "Epsilon-greedy is the simple baseline (x% random traffic). UCB/Thompson sampling direct exploration toward uncertain items and converge faster. In practice: explore in a dedicated slice or via interleaving, measure with counterfactual estimators, and bound business risk with guardrails - never explore on revenue-critical surfaces without limits.")

# misc deck (6)
FC("misc", "What is RLHF in one minute?",
   "Three stages: (1) supervised fine-tuning on demonstrations, (2) train a reward model on human preference comparisons, (3) optimize the policy against the reward model with PPO (KL-regularized to stay near the SFT model). DPO skips the explicit reward model by optimizing preferences directly. Failure modes: reward hacking, sycophancy, mode collapse.")
FC("misc", "What are neural scaling laws (Chinchilla)?",
   "For a fixed compute budget, loss is minimized by scaling parameters and training tokens together - roughly 20 tokens per parameter. Most earlier models were undertrained (too big, too few tokens). Practical takeaway: given FLOPs, do not just grow the model; grow the data proportionally, and prefer smaller models trained longer for inference efficiency.")
FC("misc", "ReAct vs plan-and-execute agents?",
   "ReAct interleaves reasoning and acting step by step - flexible and simple, but myopic on long tasks and prone to loops. Plan-and-execute first drafts a full plan, then executes steps - better for long horizons but brittle when the plan is wrong. Multi-agent splits roles (planner, worker, critic) - most capable but hardest to debug and most expensive.")
FC("misc", "How do you evaluate an AI agent reliably?",
   "Measure end-task success rate on realistic tasks first - it is the only metric that matters. Add trajectory metrics (steps taken, tool-call accuracy, cost) for diagnosis. LLM-as-judge is useful for open-ended tasks but biased (verbosity, position) - calibrate judges against human labels and never let the judge be the same model family unexamined.")
FC("misc", "What is prompt injection and how do you defend?",
   "Prompt injection smuggles instructions into data the agent reads (webpages, documents, tool outputs), hijacking its behavior. Defenses in depth: separate data from instructions (structured tool schemas, not free text), least-privilege tool access, human confirmation for irreversible actions, output validation, and monitoring for anomalous tool-use patterns. No single defense is sufficient.")
FC("misc", "STAR format for behavioral questions?",
   "Situation (one sentence of context), Task (your responsibility), Action (what YOU did - 70% of the answer, concrete verbs), Result (quantified outcome). Keep it under 2 minutes, end with what you learned. Prepare 6-8 stories covering leadership, conflict, failure, ambiguity, and technical depth - reuse them across questions.")

# ---------------- write + validate ----------------
import pathlib
DATA = pathlib.Path(__file__).resolve().parent
(DATA / "questions.json").write_text(json.dumps(questions, indent=2, ensure_ascii=False) + "\n")
(DATA / "flashcards.json").write_text(json.dumps(flashcards, indent=2, ensure_ascii=False) + "\n")

# validation
CATEGORIES = {"coding","ml-coding","ml-fundamentals","transformers","llm-systems","system-design",
              "agent-design","rag","recsys","debugging","deep-dive","behavioral","research"}
DIFFS = {"easy","medium","hard"}
FREQS = {"high","medium","low"}
LABELS = {"VERIFIED","REPORTED","REPRESENTATIVE PRACTICE"}
QREQ = {"id","question","companies","category","difficulty","time_min","frequency","label",
        "coding","answer_available","answer_ref","source"}
ids = set()
for q in questions:
    assert set(q) == QREQ, f"bad keys {q['id']}: {set(q)^QREQ}"
    assert q["id"] not in ids, f"dup id {q['id']}"; ids.add(q["id"])
    assert q["category"] in CATEGORIES, q["id"]
    assert q["difficulty"] in DIFFS, q["id"]
    assert q["frequency"] in FREQS, q["id"]
    assert q["label"] in LABELS, q["id"]
    assert isinstance(q["time_min"], int) and q["time_min"] > 0
    assert isinstance(q["coding"], bool) and isinstance(q["answer_available"], bool)
    assert q["answer_ref"].startswith("#/"), q["id"]
    assert set(q["source"]) == {"url","accessed","note"}
    assert len(q["question"]) > 40, q["id"]
    if q["label"] == "VERIFIED":
        assert q["source"]["url"], q["id"]

fids = set()
for f in flashcards:
    assert set(f) == {"id","front","back","tags","deck"}, f["id"]
    assert f["id"] not in fids; fids.add(f["id"])
    assert len(f["back"].split(". ")) >= 2 or f["back"].count(".") >= 2, f["id"]
    assert f["deck"] in f["tags"], f["id"]

print("questions:", len(questions))
print("per-category:", dict(sorted(Counter(q["category"] for q in questions).items())))
print("company-tagged:", sum(1 for q in questions if q["companies"]))
print("label counts:", dict(Counter(q["label"] for q in questions)))
print("flashcards:", len(flashcards))
print("per-deck:", dict(sorted(Counter(f["deck"] for f in flashcards).items())))
