import {
  useEffect,
  useState,
  type CSSProperties,
  type MouseEvent as ReactMouseEvent,
  type ReactNode,
} from 'react'
import { motion } from 'framer-motion'
import './App.css'
import {
  caseStudies,
  contactLinks,
  education,
  experience,
  heroHighlights,
  lessons,
  openTo,
  pipelineStages,
  proofPoints,
} from './content'

const revealTransition = {
  duration: 0.8,
  ease: [0.22, 1, 0.36, 1] as const,
}

const fadeInUp = {
  hidden: { opacity: 0, y: 32 },
  show: {
    opacity: 1,
    y: 0,
    transition: revealTransition,
  },
}

const stagger = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.12,
      delayChildren: 0.08,
    },
  },
}

const signalNodes = [
  { label: 'Audio Input', x: '18%', y: '28%' },
  { label: 'Reasoning', x: '78%', y: '24%' },
  { label: 'Structured Output', x: '80%', y: '74%' },
  { label: 'Deployment Layer', x: '20%', y: '76%' },
]

type SectionHeaderProps = {
  eyebrow: string
  title: string
  body: string
}

type RevealProps = {
  children: ReactNode
  className?: string
}

type TagProps = {
  children: ReactNode
}

function SectionHeader({ eyebrow, title, body }: SectionHeaderProps) {
  return (
    <div className="section-header">
      <p className="section-eyebrow">{eyebrow}</p>
      <h2>{title}</h2>
      <p className="section-copy">{body}</p>
    </div>
  )
}

function Reveal({ children, className }: RevealProps) {
  return (
    <motion.div
      className={className}
      initial="hidden"
      whileInView="show"
      viewport={{ once: true, amount: 0.2 }}
      variants={fadeInUp}
    >
      {children}
    </motion.div>
  )
}

function Tag({ children }: TagProps) {
  return <span className="tag">{children}</span>
}

function App() {
  const year = new Date().getFullYear()
  const projectEmail = `mailto:${contactLinks.email}?subject=Role%20enquiry`
  const resumeHref = `${import.meta.env.BASE_URL}Qalab-Abbas-Senior-ML-Engineer-CV.pdf`
  const [activeStage, setActiveStage] = useState(0)
  const [pointer, setPointer] = useState({ x: 58, y: 24 })

  useEffect(() => {
    const intervalId = window.setInterval(() => {
      setActiveStage((currentStage) => (currentStage + 1) % pipelineStages.length)
    }, 2200)

    return () => window.clearInterval(intervalId)
  }, [])

  const handleHeroMove = (event: ReactMouseEvent<HTMLDivElement>) => {
    const bounds = event.currentTarget.getBoundingClientRect()
    const x = ((event.clientX - bounds.left) / bounds.width) * 100
    const y = ((event.clientY - bounds.top) / bounds.height) * 100
    setPointer({ x, y })
  }

  const heroVisualStyle = {
    '--pointer-x': `${pointer.x}%`,
    '--pointer-y': `${pointer.y}%`,
  } as CSSProperties

  return (
    <div className="site-shell">
      <div className="ambient ambient-one" aria-hidden="true" />
      <div className="ambient ambient-two" aria-hidden="true" />
      <div className="grid-overlay" aria-hidden="true" />

      <header className="topbar">
        <a className="brand" href="#top">
          <span className="brand-mark" aria-hidden="true">
            QA
          </span>
          <span>
            <strong>Qalab Abbas</strong>
            <small>Senior ML Engineer</small>
          </span>
        </a>

        <nav className="topbar-nav" aria-label="Primary">
          <a href="#experience">Experience</a>
          <a href="#projects">Projects</a>
          <a href="#about">About</a>
          <a href="#contact">Contact</a>
        </nav>
      </header>

      <main>
        <section className="hero" id="top">
          <motion.div
            className="hero-copy"
            initial="hidden"
            animate="show"
            variants={stagger}
          >
            <motion.p className="hero-kicker" variants={fadeInUp}>
              Senior ML Engineer, open to remote roles
            </motion.p>

            <motion.h1 variants={fadeInUp}>
              I build voice and clinical AI systems that{' '}
              <span>hold up in production</span>.
            </motion.h1>

            <motion.p className="hero-body" variants={fadeInUp}>
              I am a Senior ML Engineer working on voice AI, clinical NLP, and
              real-time audio ML. I am open to remote roles in the US, Canada,
              the EU, and Pakistan, full-time or contract.
            </motion.p>

            <motion.div className="hero-actions" variants={fadeInUp}>
              <a
                className="button button-primary"
                href={resumeHref}
                download="Qalab-Abbas-Senior-ML-Engineer-CV.pdf"
              >
                Download CV
              </a>
              <a className="button button-secondary" href="#projects">
                See projects
              </a>
              <a className="button button-secondary" href={projectEmail}>
                Email me
              </a>
            </motion.div>

            <motion.div className="hero-tags" variants={fadeInUp}>
              {heroHighlights.map((highlight) => (
                <Tag key={highlight}>{highlight}</Tag>
              ))}
            </motion.div>
          </motion.div>

          <motion.div
            className="hero-visual"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ ...revealTransition, delay: 0.2 }}
            onMouseMove={handleHeroMove}
            onMouseLeave={() => setPointer({ x: 58, y: 24 })}
            style={heroVisualStyle}
          >
            <div className="hero-visual__frame" aria-hidden="true" />
            <div className="hero-visual__beam" aria-hidden="true" />
            <div className="hero-visual__halo" aria-hidden="true" />

            <div className="hero-visual__header">
              <span>Production system model</span>
              <strong>Idea → Architecture → Pipeline → Deployment</strong>
            </div>

            <div className="signal-field" aria-hidden="true">
              <svg
                className="signal-field__lines"
                viewBox="0 0 100 100"
                preserveAspectRatio="none"
              >
                <path d="M18 28 C30 30, 34 38, 50 50" />
                <path d="M78 24 C68 30, 64 38, 50 50" />
                <path d="M80 74 C68 70, 62 62, 50 50" />
                <path d="M20 76 C30 70, 36 62, 50 50" />
              </svg>

              <div className="signal-core">
                <div className="signal-core__ring signal-core__ring--outer" />
                <div className="signal-core__ring signal-core__ring--inner" />
                <div className="signal-core__label">
                  <span>Live inference</span>
                  <strong>{pipelineStages[activeStage].label}</strong>
                </div>
              </div>

              {signalNodes.map((node, index) => (
                <div
                  className={`signal-node ${
                    index === activeStage ? 'signal-node--active' : ''
                  }`}
                  key={node.label}
                  style={
                    {
                      '--node-x': node.x,
                      '--node-y': node.y,
                      '--node-delay': `${index * 0.3}s`,
                    } as CSSProperties
                  }
                >
                  <span className="signal-node__dot" />
                  <span className="signal-node__label">{node.label}</span>
                </div>
              ))}

              <div className="signal-chip signal-chip--one">Streaming context</div>
              <div className="signal-chip signal-chip--two">Latency aware</div>
            </div>

            <div className="hero-visual__status">
              <span>Current flow</span>
              <strong>{pipelineStages[activeStage].title}</strong>
            </div>

            <div className="pipeline">
              {pipelineStages.map((stage, index) => (
                <div
                  className={`pipeline-stage ${
                    index === activeStage ? 'pipeline-stage--active' : ''
                  }`}
                  key={stage.title}
                >
                  <div className="pipeline-stage__meta">
                    <span>{stage.title}</span>
                    <strong>{stage.label}</strong>
                  </div>
                  <p>{stage.body}</p>
                </div>
              ))}
            </div>

            <div className="hero-visual__footer">
              <div>
                <span>Clinical documentation</span>
                <strong>Arabic and English ambient note generation</strong>
              </div>
              <div>
                <span>Voice systems</span>
                <strong>Streaming pipelines designed for real conversations</strong>
              </div>
            </div>
          </motion.div>
        </section>

        <section className="proof-strip" aria-label="Proof points">
          {proofPoints.map((point) => (
            <Reveal className="proof-point" key={point.label}>
              <p className="proof-value">{point.value}</p>
              <h2>{point.label}</h2>
              <p>{point.note}</p>
            </Reveal>
          ))}
        </section>

        <section className="section" id="experience">
          <Reveal>
            <SectionHeader
              eyebrow="Experience"
              title="Three roles across audio ML, healthcare AI, and speech."
              body="My current role comes first. Each one is production work, from real-time audio ML to clinical documentation and speech R&D."
            />
          </Reveal>

          <div className="timeline">
            {experience.map((item) => (
              <Reveal className="timeline-item" key={`${item.company}-${item.role}`}>
                <p className="timeline-item__dates">{item.dates}</p>
                <h3>
                  {item.role}
                  <span>{item.company}</span>
                </h3>
                <p>{item.focus}</p>
                <ul className="timeline-item__list">
                  {item.highlights.map((highlight) => (
                    <li key={highlight}>{highlight}</li>
                  ))}
                </ul>
              </Reveal>
            ))}
          </div>
        </section>

        <section className="section" id="projects">
          <Reveal>
            <SectionHeader
              eyebrow="Projects"
              title="What I have built."
              body="Five systems from my own work, one independent project via HubAIX, and one personal project. They are written in plain terms: what the system did, how it was designed, and why it mattered."
            />
          </Reveal>

          <div className="case-study-list">
            {caseStudies.map((caseStudy) => (
              <Reveal className="case-study" key={caseStudy.title}>
                <div className="case-study__meta">
                  <p>{caseStudy.index}</p>
                  <span>{caseStudy.category}</span>
                </div>

                <div className="case-study__body">
                  <div className="case-study__intro">
                    <h3>{caseStudy.title}</h3>
                    <p className="case-study__lead">{caseStudy.intro}</p>
                  </div>

                  <div className="case-study__story">
                    <div>
                      <h4>What it did</h4>
                      <p>{caseStudy.whatItDid}</p>
                    </div>

                    <div>
                      <h4>How it worked</h4>
                      <p>{caseStudy.howItWorked}</p>
                    </div>

                    <div>
                      <h4>Why it mattered</h4>
                      <p>{caseStudy.whyItMattered}</p>
                    </div>
                  </div>

                  <div className="case-study__details">
                    <div>
                      <h5>Highlights</h5>
                      <ul>
                        {caseStudy.highlights.map((highlight) => (
                          <li key={highlight}>{highlight}</li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h5>Core tools</h5>
                      <div className="tag-row">
                        {caseStudy.stack.map((item) => (
                          <Tag key={item}>{item}</Tag>
                        ))}
                      </div>
                    </div>
                  </div>

                </div>
              </Reveal>
            ))}
          </div>
        </section>

        <section className="section section-muted">
          <Reveal>
            <SectionHeader
              eyebrow="Production Lessons"
              title="A few lessons that shape how I build."
              body="These ideas come from real implementation work, especially in systems where latency, edge cases, and infrastructure constraints show up quickly."
            />
          </Reveal>

          <div className="lesson-grid">
            {lessons.map((lesson) => (
              <Reveal className="lesson" key={lesson.title}>
                <h3>{lesson.title}</h3>
                <p>{lesson.body}</p>
              </Reveal>
            ))}
          </div>
        </section>

        <section className="section" id="about">
          <Reveal>
            <SectionHeader
              eyebrow="About"
              title="Speech systems, healthcare AI, and production backends."
              body="The common thread is end-to-end ownership, from the idea and system design to the implementation and the production realities."
            />
          </Reveal>

          <div className="about-grid">
            <Reveal className="about-copy">
              <p>
                My strongest work sits at the intersection of AI capability and
                systems engineering. I build modular pipelines where each layer
                can be improved, replaced, or deployed under different customer
                constraints without collapsing the rest of the product.
              </p>
              <p>
                That includes realtime voice systems, medical documentation
                workflows, structured LLM outputs, streaming APIs, and
                deployment paths that account for latency, security, and cost
                from the start.
              </p>
              <p>
                I work comfortably across Asian, European and US time zones,
                with full US-hours overlap.
              </p>
            </Reveal>

            <div className="timeline">
              {education.map((item) => (
                <Reveal className="timeline-item" key={item.degree}>
                  <p className="timeline-item__dates">{item.dates}</p>
                  <h3>
                    {item.degree}
                    <span>{item.school}</span>
                  </h3>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        <section className="section contact-section" id="contact">
          <Reveal>
            <SectionHeader
              eyebrow="Contact"
              title="Hiring for a Senior or Staff ML role? Let’s talk."
              body="Email is the quickest way to reach me. My CV has the full detail, and LinkedIn is there if you prefer to start that way."
            />
          </Reveal>

          <Reveal className="contact-panel">
            <div className="contact-panel__copy">
              <p>Open to remote Senior and Staff roles in ML, LLM, and voice AI, full-time or contract.</p>
              <div className="contact-panel__actions">
                <a className="button button-primary" href={projectEmail}>
                  Email Qalab
                </a>
                <a
                  className="button button-secondary"
                  href={resumeHref}
                  download="Qalab-Abbas-Senior-ML-Engineer-CV.pdf"
                >
                  Download CV
                </a>
                <a
                  className="button button-secondary"
                  href={contactLinks.linkedin}
                  target="_blank"
                  rel="noreferrer"
                >
                  Connect on LinkedIn
                </a>
              </div>
            </div>

            <dl className="contact-details">
              <div>
                <dt>Email</dt>
                <dd>{contactLinks.email}</dd>
              </div>
              <div>
                <dt>Open to roles</dt>
                <dd>
                  <ul className="tag-row" aria-label="Open to roles">
                    {openTo.roles.map((role) => (
                      <li key={role}>
                        <Tag>{role}</Tag>
                      </li>
                    ))}
                  </ul>
                </dd>
              </div>
              <div>
                <dt>Open to regions</dt>
                <dd>
                  <ul className="tag-row" aria-label="Open to regions">
                    {openTo.regions.map((region) => (
                      <li key={region}>
                        <Tag>{region}</Tag>
                      </li>
                    ))}
                  </ul>
                </dd>
              </div>
            </dl>
          </Reveal>
        </section>
      </main>

      <footer className="footer">
        <p>© {year} Qalab Abbas. Senior ML Engineer. Open to remote roles.</p>
        <a href={contactLinks.linkedin} target="_blank" rel="noreferrer">
          linkedin.com/in/qalabeabbas
        </a>
      </footer>
    </div>
  )
}

export default App
