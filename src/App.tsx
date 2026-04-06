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
  experience,
  fitItems,
  heroHighlights,
  lessons,
  pipelineStages,
  proofPoints,
  services,
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
  const projectEmail = `mailto:${contactLinks.email}?subject=AI%20Systems%20Project`
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
            <small>AI Systems Engineer</small>
          </span>
        </a>

        <nav className="topbar-nav" aria-label="Primary">
          <a href="#services">Services</a>
          <a href="#case-studies">Case Studies</a>
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
              AI systems engineering for teams building serious products
            </motion.p>

            <motion.h1 variants={fadeInUp}>
              I help teams turn ambitious AI ideas into{' '}
              <span>reliable, fast, usable products</span>.
            </motion.h1>

            <motion.p className="hero-body" variants={fadeInUp}>
              I design and build AI systems with a strong focus on voice,
              clinical NLP, structured outputs, and low-latency backends. My
              role is usually to make the system clearer, more dependable, and
              more ready for real users, not just internal demos.
            </motion.p>

            <motion.p className="hero-note" variants={fadeInUp}>
              That means practical work across architecture, model selection,
              APIs, streaming behavior, deployment, and optimization.
            </motion.p>

            <motion.div className="hero-actions" variants={fadeInUp}>
              <a className="button button-primary" href={projectEmail}>
                Start a Project
              </a>
              <a className="button button-secondary" href="#case-studies">
                View Case Studies
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

        <section className="section" id="services">
          <Reveal>
            <SectionHeader
              eyebrow="How I Help"
              title="Clear technical help for teams that need more than model glue code."
              body="I work best when a company needs senior judgment as much as implementation: deciding what to build, how to ship it, and how to keep it reliable once customers depend on it."
            />
          </Reveal>

          <motion.div
            className="service-list"
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.15 }}
            variants={stagger}
          >
            {services.map((service, index) => (
              <motion.article
                className="service-row"
                key={service.title}
                variants={fadeInUp}
              >
                <div className="service-row__index">
                  {String(index + 1).padStart(2, '0')}
                </div>

                <div className="service-row__content">
                  <div>
                    <h3>{service.title}</h3>
                    <p>{service.summary}</p>
                  </div>

                  <ul>
                    {service.details.map((detail) => (
                      <li key={detail}>{detail}</li>
                    ))}
                  </ul>
                </div>
              </motion.article>
            ))}
          </motion.div>
        </section>

        <section className="section section-muted">
          <Reveal>
            <SectionHeader
              eyebrow="Best Fit"
              title="The kinds of teams I’m most useful to."
              body="If your product touches regulated workflows, live interaction, or important business operations, the engineering details start to matter very quickly."
            />
          </Reveal>

          <div className="fit-grid">
            {fitItems.map((item) => (
              <Reveal className="fit-item" key={item.title}>
                <h3>{item.title}</h3>
                <p>{item.body}</p>
              </Reveal>
            ))}
          </div>
        </section>

        <section className="section" id="case-studies">
          <Reveal>
            <SectionHeader
              eyebrow="Case Studies"
              title="Examples of the kinds of systems I’ve built."
              body="These are written in plain terms on purpose. The value is not in clever project names. It is in what the system did, how it was designed, and why it mattered in practice."
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
              title="A background across speech systems, healthcare AI, and production backend engineering."
              body="The common thread is end-to-end ownership. I am strongest when I can connect the idea, the system design, the implementation details, and the production realities."
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
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        <section className="section contact-section" id="contact">
          <Reveal>
            <SectionHeader
              eyebrow="Contact"
              title="If you’re building something ambitious, I’d be happy to look at it."
              body="The best starting point is simple: send the product idea, the current blockers, and the outcome you want. I can help with architecture, implementation, or improving a system that already exists."
            />
          </Reveal>

          <Reveal className="contact-panel">
            <div className="contact-panel__copy">
              <p>Selective consulting and implementation work for high-value AI systems.</p>
              <div className="contact-panel__actions">
                <a className="button button-primary" href={projectEmail}>
                  Email Qalab
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
                <dt>Focus</dt>
                <dd>Voice AI, clinical NLP, production backends</dd>
              </div>
              <div>
                <dt>Best for</dt>
                <dd>US and Canada startups, SaaS, and health tech teams</dd>
              </div>
            </dl>
          </Reveal>
        </section>
      </main>

      <footer className="footer">
        <p>© {year} Qalab Abbas. Built for high-trust AI systems work.</p>
        <a href={contactLinks.linkedin} target="_blank" rel="noreferrer">
          linkedin.com/in/qalabeabbas
        </a>
      </footer>
    </div>
  )
}

export default App
