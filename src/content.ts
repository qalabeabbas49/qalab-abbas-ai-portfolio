export type ProofPoint = {
  value: string
  label: string
  note: string
}

export type CaseStudy = {
  index: string
  title: string
  category: string
  intro: string
  whatItDid: string
  howItWorked: string
  whyItMattered: string
  highlights: string[]
  stack: string[]
}

export type ExperienceItem = {
  role: string
  company: string
  dates: string
  focus: string
  highlights: string[]
}

export type Lesson = {
  title: string
  body: string
}

export type EducationItem = {
  degree: string
  school: string
  dates: string
}

export type OpenTo = {
  roles: string[]
  regions: string[]
}

export type PipelineStage = {
  title: string
  label: string
  body: string
}

export const heroHighlights = [
  'Realtime voice AI',
  'Healthcare AI and clinical NLP',
  'Production LLM systems',
  'Adversarial audio',
  'Senior ML roles',
]

export const proofPoints: ProofPoint[] = [
  {
    value: '0.40 to 0.24',
    label: 'Mean WER, multi-model ASR selector',
    note: 'Rule-based selector across ASR options on a 70-clip synthetic Arabic, English, Hindi and Urdu set (Nuxera AI).',
  },
  {
    value: '99.95%',
    label: 'ICD-10-AM candidate recall@12',
    note: 'Up from 97.7% over 35,262 test cases at 7.8 ms p95; retrieval recall, not clinically adjudicated (Nuxera AI).',
  },
  {
    value: '92%+',
    label: 'Diarization success, low-noise audio',
    note: 'Speech-separation pipeline for overlapping speakers; about 80% in fairly noisy environments (Furence).',
  },
]

export const caseStudies: CaseStudy[] = [
  {
    index: '01',
    title: 'Ambient medical scribe for Arabic and English clinics',
    category: 'Healthcare AI / Clinical NLP',
    intro:
      'A system designed to listen to real doctor-patient conversations and turn them into structured clinical documentation with minimal delay.',
    whatItDid:
      'It captured conversations continuously, produced running transcripts, and generated a structured medical note shortly after the session ended so clinicians could spend less time documenting by hand.',
    howItWorked:
      'I designed a chunked transcription pipeline with medical Arabic adaptation, incremental transcript storage, final transcript consolidation, and GPT-based note generation tuned for structured outputs.',
    whyItMattered:
      'This made the system useful in actual clinical workflows, where terminology is domain-specific, latency is visible, and privacy and auditability cannot be treated as afterthoughts.',
    highlights: [
      'Supports Arabic and English with coverage across 28 Arabic dialects',
      'Continuous chunk processing across roughly 45 to 47 second segments',
      'Final structured note generated in under 15 seconds after session end',
      'Designed for real clinical environments rather than clean demo audio',
    ],
    stack: ['Whisper', 'GPT-OSS-20B', 'FastAPI', 'Uvicorn', 'Docker'],
  },
  {
    index: '02',
    title: 'Low-latency voice assistant pipeline',
    category: 'Realtime Voice / Streaming Systems',
    intro:
      'A realtime conversational system built to remove the dead air and awkward pacing that make many voice agents feel artificial.',
    whatItDid:
      'It accepted live audio, streamed reasoning and response generation, buffered speech intelligently, and played output fast enough to preserve a natural conversational rhythm.',
    howItWorked:
      'I combined streaming ASR, low-latency LLM integration, sentence-based buffering, and realtime playback so each stage supported the overall interaction instead of slowing it down.',
    whyItMattered:
      'In voice systems, user trust disappears quickly when every reply feels delayed. This system was built around interaction quality, not just model output quality.',
    highlights: [
      'Streaming response loop designed for natural turn-taking',
      'Sentence-level buffering for smoother TTS handoff',
      'Continuous audio playback with low perceived delay',
      'Latency-aware tuning across transport, buffering, and playback',
    ],
    stack: ['LiveKit', 'WebRTC', 'FastAPI', 'Streaming APIs', 'PyAudio'],
  },
  {
    index: '03',
    title: 'Self-correcting natural-language analytics engine',
    category: 'LLM Systems / Data Interfaces',
    intro:
      'A natural-language analytics system built to generate SQL, detect when it failed, and repair itself instead of leaving the user with a broken query.',
    whatItDid:
      'It translated questions into executable DuckDB SQL, ran the query, captured database feedback, and retried with corrected instructions when the first attempt was wrong.',
    howItWorked:
      'I designed an execution-aware retry loop that fed real database errors back into the prompt, which made the system more accurate without changing the underlying model.',
    whyItMattered:
      'Most NL-to-SQL demos look good until real data and edge cases appear. Treating error recovery as part of the system made it much more useful in practice.',
    highlights: [
      'DuckDB-backed execution for analytical workloads',
      'Error-aware correction loop using actual execution feedback',
      'Prompt refinement focused on syntax recovery and token efficiency',
      'Improved practical accuracy through system design, not just prompt edits',
    ],
    stack: ['DuckDB', 'Prompt engineering', 'Error handling', 'Structured retries'],
  },
  {
    index: '04',
    title: 'Speaker verification layer for multi-speaker clinical workflows',
    category: 'Speech Systems / Identity Layer',
    intro:
      'A lightweight speaker verification system designed to identify the right clinician in recordings where multiple people are speaking.',
    whatItDid:
      'It enrolled speaker profiles from short voice samples and used those profiles during real interactions to improve identity-aware transcription and speaker-linked workflow logic.',
    howItWorked:
      'I integrated enrollment, embedding extraction, and verification into the application pipeline using ECAPA-TDNN-based speaker representations and GPU-backed inference.',
    whyItMattered:
      'When a system is used in shared or noisy environments, knowing who is speaking can materially improve trust, transcript quality, and downstream automation.',
    highlights: [
      'SpeechBrain ECAPA-TDNN embeddings for speaker profiles',
      '30 to 60 second enrollment flow for each clinician',
      'GPU-backed inference for production responsiveness',
      'Designed for noisy and multi-speaker conditions',
    ],
    stack: ['SpeechBrain', 'ECAPA-TDNN', 'GPU inference', 'Audio pipelines'],
  },
  {
    index: '05',
    title: 'Multi-agent presentation generation system',
    category: 'Agentic Workflows / Structured Content',
    intro:
      'A system for generating complete presentations by splitting the job across multiple AI steps instead of forcing one model to do everything at once.',
    whatItDid:
      'It generated structure, slide content, visual planning, and export-ready output for full decks, making the results more coherent and easier to control than one-shot generation.',
    howItWorked:
      'I designed an agent-based workflow with structured JSON schemas, theme control, slide composition logic, and export paths for presentation formats like PPTX and PDF.',
    whyItMattered:
      'Breaking the problem into explicit stages made the output more reliable, more structured, and easier to adapt to different presentation styles or business use cases.',
    highlights: [
      'Multi-step generation across headings, content, visuals, and export',
      'Structured JSON schema for reliable slide construction',
      'Theme engine for consistent formatting across the full deck',
      'Designed for automation rather than manual slide assembly',
    ],
    stack: ['Agent workflows', 'Structured JSON', 'Theme engine', 'PPTX/PDF export'],
  },
  {
    index: '06',
    title: 'Multi-tenant voice-agent platform',
    category: 'Voice AI / Independent Project via HubAIX',
    intro:
      'Legal-intake voice agents for a legal-tech startup serving about 17 law-firm clients, built as an independent project via HubAIX. This was project work, not a job.',
    whatItDid:
      'One Node service bridges telephony media streams to a realtime LLM, with each agent’s behavior driven by per-agent database configuration.',
    howItWorked:
      'I built warm and cold call transfer with voicemail detection, localized hold audio and a return-to-agent fallback, and designed per-call identity isolation so callers on shared phone lines never merge into one contact. I added runtime voice guards and a QA harness that runs real realtime sessions against simulated callers and asserts on tool calls.',
    whyItMattered:
      'Voice agents break in small behavioral ways that unit tests miss. The harness and the runtime guards made agent behavior something the team could test and rely on.',
    highlights: [
      'Root-caused warm-transfer failures (about 20% of accepted bridges dropped within 12 seconds) and authored the fix; added voicemail detection, localized hold audio and return-to-agent fallback',
      'Found 49 distinct callers merging into one contact across 80 calls on a shared line; per-call identity isolation (shadow-mode resolver, zero-downtime index migration) verified on 11 of 11 live calls',
      'Runtime guards: forced tool calls, strict phone and email validation, speech-recognition language lock, booking-window and business-hours rules; audited three repositories for 90 verified findings, 7 critical',
      'QA harness exposed a defect: client-approved scripts were spoken only 11.3% of the time (28 offline harness tests; full suite grew to 930 tests)',
      '4-arm, 200-conversation ablation: scripts embedded in the prompt were reproduced 2-8% of the time versus 100% (80 of 80) when injected at runtime',
    ],
    stack: ['Node.js', 'Fastify', 'Twilio', 'OpenAI Realtime', 'Supabase'],
  },
  {
    index: '07',
    title: 'Realtime voice-agent pipelines',
    category: 'Voice AI / Personal Project',
    intro:
      'A personal project: voice agents backed by low-latency services that orchestrate speech recognition, LLM reasoning and speech synthesis.',
    whatItDid:
      'It runs voice agents over WebSocket streaming APIs, with ASR, LLM reasoning and TTS orchestrated by FastAPI services.',
    howItWorked:
      'I built the services with rate limiting, OpenAPI schema validation and structured logging, and set up deployment variants for cloud, VPC-restricted, hybrid and on-premise setups.',
    whyItMattered:
      'Customer constraints differ, so the same pipeline had to run under different security boundaries, with inference tuned for cost and concurrency.',
    highlights: [
      'Low-latency FastAPI services over WebSocket streaming APIs',
      'Rate limiting, OpenAPI schema validation and structured logging',
      'Cloud, VPC-restricted, hybrid and on-premise deployment variants',
      'Inference tuned for cost and concurrency',
    ],
    stack: ['LiveKit', 'Pipecat', 'FastAPI'],
  },
]

export const lessons: Lesson[] = [
  {
    title: 'Latency is multiplicative, not isolated.',
    body: 'A fast model is still a slow product when chunking, buffering, retries, transport, and playback are all designed independently. The system has to be optimized as a chain.',
  },
  {
    title: 'Structured outputs need recovery paths.',
    body: 'Validation, schema guards, and repair loops matter more than clever prompts once a system is serving real users and real edge cases.',
  },
  {
    title: 'Customer constraints shape the architecture.',
    body: 'Security boundaries, VPC restrictions, residency rules, and customer-specific integrations should influence design from day one, not after the build is finished.',
  },
]

export const experience: ExperienceItem[] = [
  {
    role: 'Senior ML Engineer',
    company: 'Augmentation Co, Remote',
    dates: 'Aug 2026 - Present',
    focus: 'Real-time audio ML and speech privacy; details confidential.',
    highlights: [
      'Own robustness evaluation for a real-time audio ML system: 100+ numbered, pre-registered experiments in about 3 months, using held-out speakers, frozen data splits, confidence intervals and a shared experiment ledger',
      'Stress-test models under realistic transmission conditions (compression, noise suppression, resampling); negative results are recorded alongside wins',
      'Optimized and exported streaming neural models for low-latency on-device inference on Apple silicon, and integrated scoring into a native macOS app (Swift)',
    ],
  },
  {
    role: 'Senior ML Engineer',
    company: 'Nuxera AI, Remote',
    dates: 'Oct 2024 - Aug 2026',
    focus:
      'Healthcare AI: clinical transcription, structured notes and EHR integration (Arabic and English).',
    highlights: [
      'Led a team of 3 engineers across a multi-repo platform (Node/TypeScript, Python, React/Next.js, Chrome extension) covering ASR, LLM note generation, clinical coding and EHR integration',
      'Built a hospital-system coding pipeline (29-field note template, embedding retrieval plus a synonym layer): 81.0% recall@12 on a 330-observation benchmark; int8 index of 10.5 MB with no measured recall loss. Raised ICD-10-AM candidate recall@12 from 97.7% to 99.95% over 35,262 test cases at 7.8 ms p95 (retrieval recall, not clinically adjudicated)',
      'Built security and compliance controls for SDAIA, ISO and SOC 2 audit readiness (audits in progress at the time): access control, audit logging and a dependency-audit gate in CI',
      'Benchmarked ASR options on a 70-clip synthetic Arabic, English, Hindi and Urdu set: a rule-based multi-model selector cut mean WER from 0.40 to 0.24 (Arabic-English code-switching 0.36 to 0.22)',
      'Designed an ASR resilience layer for clinical dictation: a guard flags script mismatch, heavy repetition, abnormal speech rate and truncation in primary-ASR output, and a cloud-hosted Whisper model gives a second opinion, with a shadow mode (verdict recorded, primary text returned), per-organization enforcement, a circuit breaker, bounded queues and deadlines',
      'Ported and benchmarked a Saudi FDA (SFDA) drug-name matcher: 43% to 92% correct on 226 mentions with an LLM picker, and a safety gate that cut wrong picks from 4 to 0 on a held-out half. Built a drug-name correction step that raised correct drug names from 157 to 215 of 411 mentions on 118 synthetic conversations',
      'Tested LoRA fine-tuning of Arabic ASR on drug names (0 to 91% on trained names, only 3-11% on unseen ones), then switched to a no-training drug-list and LLM approach that fixed 81% of failing medications with no harm on 135 control sentences',
      'Grew a clinical documentation rule engine from 16 rules to a 30-rule heart-failure library with three-state exclusions, a completeness score, contradiction checks and ICD-10-AM coding (361 reviewed synonyms); failed checks are reported explicitly',
      'Built SERA, a HIS-agnostic Manifest V3 Chrome extension published on the Chrome Web Store: records a consultation, produces a SOAP note and fills only clinician-confirmed codes through per-system adapters',
    ],
  },
  {
    role: 'Senior Machine Learning Engineer',
    company: 'Furence, Seoul',
    dates: 'Aug 2021 - Sep 2024',
    focus: 'Speaker diarization, TTS and speech enhancement.',
    highlights: [
      'Led a team of 4 researchers building speech-to-text, text-to-speech and speaker diarization systems for Woori Bank, integrated with backend services and user databases',
      'Built a speech-separation pipeline that handled overlapping speakers: 92%+ diarization success in low-noise environments and about 80% in fairly noisy ones',
      'Built noise removal and live speech emotion recognition: about 95% accuracy on two classes (good or bad) and about 88% on four (happy, sad, interested, uninterested)',
      'Built a privacy-preserving audio masking system that automatically removes personal identifiers from recordings',
      'Led development of Korean TTS models for commercial deployment and real-time speech enhancement for streaming',
    ],
  },
]

export const education: EducationItem[] = [
  {
    degree: 'M.Sc. IT Convergence',
    school: 'Kumoh National Institute of Technology',
    dates: '2018 - 2020',
  },
  {
    degree: 'B.Eng. Electrical (Telecom)',
    school: 'NUST',
    dates: '2012 - 2016',
  },
]

export const openTo: OpenTo = {
  roles: [
    'Senior or Staff ML engineer',
    'Senior or Staff LLM engineer',
    'Senior or Staff voice-AI engineer',
    'Healthcare AI',
    'Realtime voice',
  ],
  regions: ['Remote US', 'Remote Canada', 'Remote EU', 'Pakistan', 'Full-time or contract'],
}

export const pipelineStages: PipelineStage[] = [
  {
    title: 'Capture',
    label: 'ASR / ingest',
    body: 'Streaming audio, chunk strategy, diarization, and noise handling.',
  },
  {
    title: 'Reason',
    label: 'LLM / routing',
    body: 'Structured prompting, tool use, validation, and fallback logic.',
  },
  {
    title: 'Structure',
    label: 'Outputs / policy',
    body: 'Schema-first extraction, note generation, and workflow-specific rules.',
  },
  {
    title: 'Deploy',
    label: 'Infra / reliability',
    body: 'GPU decisions, Dockerized services, observability, and secure rollout paths.',
  },
]

export const contactLinks = {
  email: 'abbaseqalab@gmail.com',
  linkedin: 'https://www.linkedin.com/in/qalabeabbas/',
}
