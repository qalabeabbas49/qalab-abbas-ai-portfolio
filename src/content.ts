export type ProofPoint = {
  value: string
  label: string
  note: string
}

export type Service = {
  title: string
  summary: string
  details: string[]
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
}

export type Lesson = {
  title: string
  body: string
}

export type FitItem = {
  title: string
  body: string
}

export type PipelineStage = {
  title: string
  label: string
  body: string
}

export const heroHighlights = [
  'Real-time voice systems',
  'Clinical NLP and structured outputs',
  'Low-latency AI backends',
  'Architecture to deployment ownership',
]

export const proofPoints: ProofPoint[] = [
  {
    value: '28',
    label: 'Arabic dialects supported',
    note: 'Built for Arabic and English clinical transcription workflows instead of generic voice demos.',
  },
  {
    value: '<15s',
    label: 'To final structured note',
    note: 'Designed for rapid post-session consolidation instead of delayed batch reporting.',
  },
  {
    value: 'Realtime',
    label: 'Voice interaction focus',
    note: 'Streaming ASR, LLM, and TTS systems optimized for natural conversational flow.',
  },
  {
    value: 'Prod',
    label: 'Delivery mindset',
    note: 'Cloud, VPC-restricted, hybrid, and on-prem deployment patterns for real buyers.',
  },
]

export const services: Service[] = [
  {
    title: 'Architecture and Technical Strategy',
    summary:
      'For teams that need a clear build plan, better decisions, and fewer expensive mistakes before development scales up.',
    details: [
      'Architecture blueprints from idea through deployment',
      'Model selection based on latency, cost, and reliability constraints',
      'Failure-mode design for retries, validation, and recoverability',
    ],
  },
  {
    title: 'Voice AI Systems',
    summary:
      'Voice products that feel responsive, natural, and dependable instead of laggy or awkward.',
    details: [
      'ASR + LLM + TTS orchestration with buffering strategies',
      'LiveKit and WebRTC implementations for realtime interaction',
      'Conversation pipelines that feel human instead of staged',
    ],
  },
  {
    title: 'Clinical NLP and Structured AI Outputs',
    summary:
      'Structured AI workflows for documentation-heavy environments where clarity, traceability, and consistency matter.',
    details: [
      'Medical note generation and schema-first extraction',
      'Domain-adapted transcription pipelines for Arabic and English',
      'Audit-friendly output design for downstream systems',
    ],
  },
  {
    title: 'Optimization and Rescue Work',
    summary:
      'For AI products that already exist but feel too slow, too fragile, or too painful to deploy for serious customers.',
    details: [
      'Inference and throughput optimization on GPU-backed systems',
      'Concurrency, streaming, and queueing improvements',
      'Deployment hardening across Docker and cloud environments',
    ],
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
]

export const fitItems: FitItem[] = [
  {
    title: 'Startups moving from prototype to product',
    body: 'You already proved demand and now need architecture, deployment, and technical depth that can survive real users.',
  },
  {
    title: 'Health tech teams with documentation workflows',
    body: 'Clinical NLP, structured notes, multilingual transcription, and compliance-aware system thinking are central here.',
  },
  {
    title: 'Voice AI and call automation products',
    body: 'If interaction quality is being damaged by buffering, latency, interruption issues, or brittle pipelines, this is a strong fit.',
  },
  {
    title: 'SaaS products adding AI interfaces',
    body: 'Particularly useful for teams building retrieval, NL interfaces, decision layers, or complex LLM-backed backend workflows.',
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
    title: 'Buyer constraints shape the architecture.',
    body: 'Security boundaries, VPC restrictions, residency rules, and customer-specific integrations should influence design from day one, not after the build is finished.',
  },
]

export const experience: ExperienceItem[] = [
  {
    role: 'Senior AI Engineer',
    company: 'Nuxera AI',
    dates: 'Aug 2025 - Present',
    focus:
      'Healthcare AI systems, FastAPI services, medical note generation, ICD workflows, and production reliability.',
  },
  {
    role: 'Senior LLM Engineer',
    company: 'Spacedome',
    dates: 'Oct 2024 - Aug 2025',
    focus:
      'Voice agents, LiveKit-based realtime systems, streaming APIs, deployment customization, and latency-conscious backend design.',
  },
  {
    role: 'Senior Machine Learning Engineer',
    company: 'Furence',
    dates: 'Aug 2021 - Sep 2024',
    focus:
      'Speaker diarization, TTS, speech enhancement, privacy-focused audio systems, and production speech R&D.',
  },
  {
    role: 'Research Assistant',
    company: 'Kumoh National Institute of Technology',
    dates: 'Sep 2018 - Dec 2020',
    focus:
      'Machine learning and deep learning research, predictive systems, anomaly detection, and the technical base behind later production work.',
  },
]

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
