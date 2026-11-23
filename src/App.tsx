import { useEffect, useRef, useState, type CSSProperties, type ReactNode } from 'react'
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

/* ------------------------------------------------------------------ */
/* Generated signal: a waveform and a spectrogram built from sine and  */
/* seeded noise only. It carries no data and makes no claim.           */
/* ------------------------------------------------------------------ */

const TABLE = 2048

function seeded(seed: number) {
  let s = seed
  return () => {
    s = (s + 0x6d2b79f5) | 0
    let t = Math.imul(s ^ (s >>> 15), 1 | s)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

const rand = seeded(20261123)
const NOISE_A = Float32Array.from({ length: TABLE }, () => rand())
const NOISE_B = Float32Array.from({ length: TABLE }, () => rand())

// Whole-number cycle counts make the loop seamless as it drifts.
const ENVELOPE = Float32Array.from({ length: TABLE }, (_, i) => {
  const u = i / TABLE
  const raw =
    0.55 * Math.sin(2 * Math.PI * 7 * u + 0.3) +
    0.35 * Math.sin(2 * Math.PI * 13 * u + 1.1) +
    0.25 * Math.sin(2 * Math.PI * 3 * u + 2.0) +
    0.12
  return Math.min(1, Math.pow(Math.max(0, raw), 1.15) * 1.25)
})

const PITCH = Float32Array.from({ length: TABLE }, (_, i) => {
  const u = i / TABLE
  return 0.13 + 0.035 * Math.sin(2 * Math.PI * 2 * u) + 0.02 * Math.sin(2 * Math.PI * 5 * u + 0.7)
})

type SignalColours = { ink: string; muted: string; rule: string; accent: string }

const COLUMN = 4
const CELL = 6
const BINS = 14
const PLAYHEAD = 0.78

function paintSignal(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  colours: SignalColours,
  progress: number,
  phase: number,
) {
  ctx.clearRect(0, 0, w, h)
  const waveH = h * 0.56
  const mid = waveH / 2 + 24
  const reach = progress * w
  const playheadX = w * PLAYHEAD

  ctx.globalAlpha = 1
  ctx.strokeStyle = colours.rule
  ctx.lineWidth = 1
  ctx.beginPath()
  ctx.moveTo(0, Math.round(mid) + 0.5)
  ctx.lineTo(w, Math.round(mid) + 0.5)
  ctx.stroke()

  ctx.lineWidth = 2
  ctx.lineCap = 'round'
  ctx.strokeStyle = colours.ink
  for (let x = COLUMN / 2; x < w; x += COLUMN) {
    if (x > reach) break
    const u = (x / w + phase) % 1
    const idx = Math.floor(u * TABLE) % TABLE
    const env = ENVELOPE[idx]
    const amp = env * (waveH / 2 - 24)
    const top = amp * (0.5 + 0.5 * NOISE_A[idx])
    const bottom = amp * (0.5 + 0.5 * NOISE_B[idx])
    ctx.globalAlpha = x <= playheadX ? 0.9 : 0.35
    ctx.beginPath()
    ctx.moveTo(x, mid - Math.max(top, 1))
    ctx.lineTo(x, mid + Math.max(bottom, 1))
    ctx.stroke()
  }

  const specTop = h * 0.66
  const specH = h * 0.3
  const rowH = specH / BINS
  ctx.fillStyle = colours.muted
  for (let x = 0; x < w; x += CELL) {
    if (x > reach) break
    const u = ((x + CELL / 2) / w + phase) % 1
    const idx = Math.floor(u * TABLE) % TABLE
    const env = ENVELOPE[idx]
    const pitch = PITCH[idx]
    for (let r = 0; r < BINS; r += 1) {
      const f = (r + 0.5) / BINS
      let ridge = 0
      for (let k = 1; k <= 5; k += 1) {
        const d = (f - pitch * k) / 0.05
        ridge += Math.exp(-d * d) / Math.sqrt(k)
      }
      const grain = NOISE_A[(idx + r * 53) % TABLE] * 0.14
      const value = Math.min(1, env * ridge * 0.95 + grain * (0.4 + env))
      if (value < 0.06) continue
      ctx.globalAlpha = Math.pow(value, 1.2) * (x <= playheadX ? 0.95 : 0.4)
      ctx.fillRect(x, specTop + specH - (r + 1) * rowH, CELL - 1, rowH - 1)
    }
  }

  ctx.globalAlpha = Math.min(1, progress * 1.4)
  ctx.fillStyle = colours.accent
  ctx.fillRect(Math.round(playheadX), 12, 1, h - 24)
  if (progress < 1) {
    ctx.globalAlpha = 1
    ctx.fillRect(Math.round(Math.min(reach, w - 1)), 12, 1, h - 24)
  }
  ctx.globalAlpha = 1
}

function Signal() {
  const figure = useRef<HTMLElement>(null)
  const canvas = useRef<HTMLCanvasElement>(null)
  const [reduced, setReduced] = useState(
    () => typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches,
  )
  const [held, setHeld] = useState(false)
  const progress = useRef(0)
  const phase = useRef(0.37)

  useEffect(() => {
    const query = window.matchMedia('(prefers-reduced-motion: reduce)')
    const onChange = () => setReduced(query.matches)
    query.addEventListener('change', onChange)
    return () => query.removeEventListener('change', onChange)
  }, [])

  useEffect(() => {
    const cv = canvas.current
    const fig = figure.current
    const ctx = cv?.getContext('2d')
    if (!cv || !fig || !ctx) return

    const style = getComputedStyle(cv)
    const read = (name: string) => style.getPropertyValue(name).trim()
    const colours: SignalColours = {
      ink: read('--color-ink-2'),
      muted: read('--color-muted'),
      rule: read('--color-rule-2'),
      accent: read('--color-accent'),
    }

    let w = 0
    let h = 0
    let raf = 0
    let last = 0
    const flags = { seen: false, hover: false, focus: false }

    const paint = () => paintSignal(ctx, w, h, colours, progress.current, phase.current)

    const resize = () => {
      const box = cv.getBoundingClientRect()
      const dpr = Math.min(2, window.devicePixelRatio || 1)
      w = box.width
      h = box.height
      cv.width = Math.round(w * dpr)
      cv.height = Math.round(h * dpr)
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
      paint()
    }

    const frame = (now: number) => {
      if (!last) last = now
      const dt = Math.min(0.064, (now - last) / 1000)
      if (dt >= 0.032) {
        last = now
        if (progress.current < 1) progress.current = Math.min(1, progress.current + dt / 1.6)
        phase.current = (phase.current + dt * 0.012) % 1
        paint()
      }
      raf = requestAnimationFrame(frame)
    }

    const sync = () => {
      const run = !reduced && !held && flags.seen && !flags.hover && !flags.focus
      cancelAnimationFrame(raf)
      last = 0
      if (run) raf = requestAnimationFrame(frame)
    }

    if (reduced) progress.current = 1

    const observer = new IntersectionObserver(([entry]) => {
      flags.seen = entry.isIntersecting
      sync()
    })
    const resizer = new ResizeObserver(resize)
    const on = (type: string, key: 'hover' | 'focus', value: boolean) =>
      fig.addEventListener(type, () => {
        flags[key] = value
        sync()
      })

    on('pointerenter', 'hover', true)
    on('pointerleave', 'hover', false)
    on('focusin', 'focus', true)
    on('focusout', 'focus', false)
    observer.observe(fig)
    resizer.observe(cv)
    resize()
    sync()

    return () => {
      cancelAnimationFrame(raf)
      observer.disconnect()
      resizer.disconnect()
    }
  }, [reduced, held])

  return (
    <figure className="signal" ref={figure} data-enter style={{ '--i': 4 } as CSSProperties}>
      <div className="signal__well">
        <canvas
          ref={canvas}
          className="signal__canvas"
          role="img"
          aria-label="A synthetic audio signal drawn in the browser: a waveform above a spectrogram, with a playhead."
        />
        <span className="signal__tag signal__tag--wave" aria-hidden="true">
          waveform
        </span>
        <span className="signal__tag signal__tag--spec" aria-hidden="true">
          spectrogram
        </span>
      </div>
      <figcaption className="signal__caption">
        <span>Synthetic signal, generated in your browser.</span>
        {!reduced && (
          <button
            className="btn btn--quiet btn--small"
            type="button"
            aria-pressed={held}
            onClick={() => setHeld((value) => !value)}
          >
            {held ? 'Play' : 'Pause'}
          </button>
        )}
      </figcaption>
    </figure>
  )
}

/* ------------------------------------------------------------------ */

type ItemProps = {
  children: ReactNode
  className?: string
  index?: number
}

function Item({ children, className, index = 0 }: ItemProps) {
  return (
    <div className={className} data-reveal style={{ '--i': index } as CSSProperties}>
      {children}
    </div>
  )
}

type HeadProps = {
  title: string
  body?: string
  id?: string
}

function Head({ title, body, id }: HeadProps) {
  return (
    <div className="head" data-reveal>
      <h2 id={id}>{title}</h2>
      {body && <p className="lead">{body}</p>}
    </div>
  )
}

function Tags({ items, label }: { items: string[]; label?: string }) {
  return (
    <ul className="tags" aria-label={label}>
      {items.map((item) => (
        <li key={item}>{item}</li>
      ))}
    </ul>
  )
}

function Toggle() {
  return (
    <span className="toggle" aria-hidden="true">
      <span className="toggle__closed">Read more</span>
      <span className="toggle__open">Close</span>
    </span>
  )
}

function App() {
  const year = new Date().getFullYear()
  const projectEmail = `mailto:${contactLinks.email}?subject=Role%20enquiry`
  const resumeHref = `${import.meta.env.BASE_URL}Qalab-Abbas-Senior-ML-Engineer-CV.pdf`
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    const items = Array.from(document.querySelectorAll('[data-reveal]'))
    if (!('IntersectionObserver' in window)) {
      items.forEach((item) => item.classList.add('is-in'))
      return
    }
    const observer = new IntersectionObserver(
      (entries) =>
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in')
            observer.unobserve(entry.target)
          }
        }),
      { rootMargin: '0px 0px -8% 0px' },
    )
    items.forEach((item) => observer.observe(item))
    return () => observer.disconnect()
  }, [])

  useEffect(() => {
    if (!menuOpen) return
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setMenuOpen(false)
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [menuOpen])

  return (
    <>
      <a className="skip" href="#main">
        Skip to content
      </a>

      <header className="nav-wrap">
        <div className="nav">
          <a className="brand" href="#top" aria-label="Qalab Abbas, back to the top">
            <strong>Qalab Abbas</strong>
            <small>Senior ML Engineer</small>
          </a>

          <button
            className="nav__toggle"
            type="button"
            aria-expanded={menuOpen}
            aria-controls="primary-nav"
            onClick={() => setMenuOpen((value) => !value)}
          >
            {menuOpen ? 'Close' : 'Menu'}
          </button>

          <nav
            id="primary-nav"
            className="nav__links"
            aria-label="Primary"
            data-open={menuOpen}
          >
            <a href="#experience" onClick={() => setMenuOpen(false)}>
              Experience
            </a>
            <a href="#projects" onClick={() => setMenuOpen(false)}>
              Projects
            </a>
            <a href="#about" onClick={() => setMenuOpen(false)}>
              About
            </a>
            <a href="#contact" onClick={() => setMenuOpen(false)}>
              Contact
            </a>
          </nav>
        </div>
      </header>

      <main id="main">
        <section className="hero" id="top">
          <div className="container hero__inner">
            <div className="hero__text">
              <h1 data-enter style={{ '--i': 0 } as CSSProperties}>
                Voice and clinical AI that <span className="verb">holds</span> up.
              </h1>
              <p className="lead hero__lead" data-enter style={{ '--i': 1 } as CSSProperties}>
                Senior ML engineer for production systems, open to remote roles.
              </p>
              <div className="actions" data-enter style={{ '--i': 2 } as CSSProperties}>
                <a
                  className="btn btn--primary"
                  href={resumeHref}
                  download="Qalab-Abbas-Senior-ML-Engineer-CV.pdf"
                >
                  Download CV
                </a>
                <a className="btn btn--quiet" href={projectEmail}>
                  Email me
                </a>
              </div>
            </div>
            <Signal />
          </div>
        </section>

        <section className="section proof" aria-labelledby="proof-title">
          <div className="container">
            <h2 id="proof-title" className="visually-hidden">
              Proof points
            </h2>
            <ul className="proof__list">
              {proofPoints.map((point, index) => (
                <li className="proof__item" key={point.label} data-reveal style={{ '--i': index } as CSSProperties}>
                  <p className="proof__value figure">{point.value}</p>
                  <div className="proof__text">
                    <h3>{point.label}</h3>
                    <p>{point.note}</p>
                  </div>
                </li>
              ))}
            </ul>
            <div className="focus" role="group" aria-label="Focus areas">
              <ul className="focus__list">
                {heroHighlights.map((highlight, index) => (
                  <li key={highlight} data-reveal style={{ '--i': index } as CSSProperties}>
                    <span>{highlight}</span>
                  </li>
                ))}
              </ul>
              <a className="btn btn--quiet focus__link" href="#projects">
                See projects
              </a>
            </div>
          </div>
        </section>

        <section className="chapter" id="system" aria-labelledby="system-title">
          <div className="chapter__pin">
            <div className="container">
              <Head title="Production system model" body="Idea, architecture, pipeline, deployment." id="system-title" />
              <ol className="path">
                {pipelineStages.map((stage) => (
                  <li className="path__step" key={stage.title}>
                    <h3>{stage.title}</h3>
                    <p className="path__label">{stage.label}</p>
                    <p>{stage.body}</p>
                  </li>
                ))}
              </ol>
            </div>
          </div>
        </section>

        <section className="section" id="experience">
          <div className="container">
            <Head
              title="Three roles across audio ML, healthcare AI, and speech."
              body="My current role comes first. Each one is production work, from real-time audio ML to clinical documentation and speech R&D."
            />
            <ol className="rows">
              {experience.map((item, index) => (
                <li key={`${item.company}-${item.role}`} data-reveal style={{ '--i': index } as CSSProperties}>
                  <details className="row">
                    <summary>
                      <span className="row__dates num">{item.dates}</span>
                      <span className="row__main">
                        <h3>
                          {item.role}
                          <span>{item.company}</span>
                        </h3>
                        <span className="row__focus">{item.focus}</span>
                      </span>
                      <Toggle />
                    </summary>
                    <div className="row__body">
                      <ul className="bullets">
                        {item.highlights.map((highlight) => (
                          <li key={highlight}>{highlight}</li>
                        ))}
                      </ul>
                    </div>
                  </details>
                </li>
              ))}
            </ol>
            <ol className="rows rows--edu">
              {education.map((item, index) => (
                <li key={item.degree} data-reveal style={{ '--i': index } as CSSProperties}>
                  <div className="edu">
                    <span className="row__dates num">{item.dates}</span>
                    <h3>
                      {item.degree}
                      <span>{item.school}</span>
                    </h3>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section className="section" id="projects">
          <div className="container">
            <Head
              title="What I have built."
              body="Five systems from my own work, one independent project via HubAIX, and one personal project. They are written in plain terms: what the system did, how it was designed, and why it mattered."
            />
            <ol className="rows rows--cases">
              {caseStudies.map((caseStudy, index) => (
                <li key={caseStudy.title} data-reveal style={{ '--i': Math.min(index, 3) } as CSSProperties}>
                  <details className="row case">
                    <summary>
                      <span className="row__main">
                        <h3>{caseStudy.title}</h3>
                        <span className="row__focus">{caseStudy.category}</span>
                      </span>
                      <Toggle />
                    </summary>
                    <div className="row__body case__body">
                      <p className="lead">{caseStudy.intro}</p>
                      <div className="case__story">
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
                      <div className="case__details">
                        <div>
                          <h5>Highlights</h5>
                          <ul className="bullets">
                            {caseStudy.highlights.map((highlight) => (
                              <li key={highlight}>{highlight}</li>
                            ))}
                          </ul>
                        </div>
                        <div>
                          <h5>Core tools</h5>
                          <Tags items={caseStudy.stack} />
                        </div>
                      </div>
                    </div>
                  </details>
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section className="section" id="lessons">
          <div className="container">
            <Head
              title="A few lessons that shape how I build."
              body="These ideas come from real implementation work, especially in systems where latency, edge cases, and infrastructure constraints show up quickly."
            />
            <ul className="claims">
              {lessons.map((lesson, index) => (
                <li className="claim" key={lesson.title} data-reveal style={{ '--i': index } as CSSProperties}>
                  <h3>{lesson.title}</h3>
                  <p>{lesson.body}</p>
                </li>
              ))}
            </ul>
          </div>
        </section>

        <section className="section" id="about">
          <div className="container about">
            <div className="about__main">
              <Head
                title="Speech systems, healthcare AI, and production backends."
                body="The common thread is end-to-end ownership, from the idea and system design to the implementation and the production realities."
              />
              <Item className="about__copy" index={1}>
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
              </Item>
            </div>

          </div>
        </section>

        <section className="section contact" id="contact">
          <div className="container">
            <Head
              title="Hiring for a Senior or Staff ML role? Let’s talk."
              body="Email is the quickest way to reach me. My CV has the full detail, and LinkedIn is there if you prefer to start that way."
            />
            <Item className="actions contact__actions" index={1}>
              <a
                className="btn btn--primary"
                href={resumeHref}
                download="Qalab-Abbas-Senior-ML-Engineer-CV.pdf"
              >
                Download CV
              </a>
              <a className="btn btn--quiet" href={projectEmail}>
                Email Qalab
              </a>
              <a
                className="btn btn--quiet"
                href={contactLinks.linkedin}
                target="_blank"
                rel="noreferrer"
              >
                Connect on LinkedIn
              </a>
            </Item>

            <dl className="facts">
              <Item className="facts__row" index={0}>
                <dt>Email</dt>
                <dd>
                  <a className="facts__email" href={projectEmail}>
                    {contactLinks.email}
                  </a>
                </dd>
              </Item>
              <Item className="facts__row" index={1}>
                <dt>Open to roles</dt>
                <dd>
                  <Tags items={openTo.roles} label="Open to roles" />
                </dd>
              </Item>
              <Item className="facts__row" index={2}>
                <dt>Open to regions</dt>
                <dd>
                  <Tags items={openTo.regions} label="Open to regions" />
                </dd>
              </Item>
            </dl>
          </div>
        </section>
      </main>

      <footer className="footer">
        <div className="container">
          <p className="footer__statement">Senior ML Engineer. Open to remote roles.</p>
          <div className="footer__meta">
            <p>© {year} Qalab Abbas.</p>
            <a href={contactLinks.linkedin} target="_blank" rel="noreferrer">
              linkedin.com/in/qalabeabbas
            </a>
          </div>
        </div>
      </footer>
    </>
  )
}

export default App
