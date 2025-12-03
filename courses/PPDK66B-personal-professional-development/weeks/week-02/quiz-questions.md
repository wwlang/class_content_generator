---
metadata:
  week: 2
  topic: "Career Skills in the AI Era"
  prepares_for: "Personal Development Plan (Week 11)"
  source: "lecture-content.md"

questions:
  - id: "W2-Q1-context-eng"
    type: "multiple_choice"
    bloom_level: "remembering"
    topic: "Context Engineering"

    question: |
      According to Andrej Karpathy, what is the fundamental difference between prompt engineering and context engineering?

    options:
      - key: "A"
        text: "Prompt engineering focuses on clever phrasing while context engineering focuses on curating what AI sees in its context window"
        feedback: "Correct. Karpathy defines context engineering as the art of filling the context window with the right information, not just clever task descriptions."
        correct: true
      - key: "B"
        text: "Prompt engineering is for technical tasks while context engineering is for creative tasks"
        feedback: "Incorrect. The distinction is about how you provide information to AI, not the type of task being performed."
      - key: "C"
        text: "Context engineering requires longer prompts than prompt engineering"
        feedback: "Incorrect. The difference is about strategic information curation, not prompt length. Context engineering actually emphasizes the minimum effective dose principle."
      - key: "D"
        text: "Prompt engineering is outdated while context engineering is the same technique with a new name"
        feedback: "Incorrect. These represent fundamentally different approaches. Context engineering focuses on what information AI has access to, not just how you phrase requests."

    general_feedback: |
      <b>Context engineering</b> (the delicate art and science of filling the context window with just the right information) has replaced prompt engineering as the premium skill for working with AI. Rather than focusing on clever phrasing, context engineering emphasizes strategic curation of information. Reference: Slide 5 on the shift from prompts to context.

  - id: "W2-Q2-context-eng"
    type: "multiple_choice"
    bloom_level: "understanding"
    topic: "Context Engineering"

    question: |
      A student wants AI to help write a cover letter for a marketing internship at VinGroup. Which approach best demonstrates the Goldilocks Principle?

    options:
      - key: "A"
        text: "Instructing AI to start with 'Dear Hiring Manager' and use the word 'synergy' in the second paragraph"
        feedback: "Incorrect. This is too rigid—over-controlling specific word choices leads to robotic, obviously AI-generated output."
      - key: "B"
        text: "Asking AI to 'write a professional cover letter'"
        feedback: "Incorrect. This is too vague—AI lacks strategic direction and will produce generic, off-target content."
      - key: "C"
        text: "Providing the job description, relevant experiences, and requesting a confident but humble tone emphasizing collaboration"
        feedback: "Correct. This is 'just right'—gives AI strategic constraints and relevant information while allowing creative freedom to write naturally."
        correct: true
      - key: "D"
        text: "Giving AI complete freedom to decide tone, structure, and content without any guidance"
        feedback: "Incorrect. This is too vague. Without strategic direction, AI cannot tailor the letter to the specific opportunity and your unique fit."

    general_feedback: |
      The <b>Goldilocks Principle</b> (finding the optimal altitude between overly specific and overly general instructions) helps you avoid two extremes: over-controlling AI (brittle, robotic output) and under-guiding AI (unpredictable, generic output). The sweet spot gives AI strategic constraints with room for natural expression. Reference: Slide 6 on the Goldilocks Zone.

  - id: "W2-Q3-context-eng"
    type: "multiple_choice"
    bloom_level: "understanding"
    topic: "Context Engineering"

    question: |
      According to the Minimum Effective Dose principle, why should a student applying for a data analytics position NOT provide AI with their entire academic transcript, all course descriptions, and every extracurricular activity?

    options:
      - key: "A"
        text: "Because AI models charge based on the amount of text processed"
        feedback: "Incorrect. While some AI tools have usage limits, the principle is about effectiveness, not cost."
      - key: "B"
        text: "Because dumping everything dilutes what's important and AI struggles to identify what matters most"
        feedback: "Correct. The principle states that strategic selection is better than comprehensive dumping—more information does not equal better results."
        correct: true
      - key: "C"
        text: "Because AI models cannot process large amounts of text at once"
        feedback: "Incorrect. Modern AI models can handle large contexts, but the Attention Budget principle shows that performance degrades with larger contexts."
      - key: "D"
        text: "Because it violates academic integrity policies to share all course information with AI"
        feedback: "Incorrect. This is not related to academic integrity. The principle is about strategic curation for better AI outputs."

    general_feedback: |
      The <b>Minimum Effective Dose</b> (finding the smallest possible set of high-signal information that maximizes desired outcomes) emphasizes that more information does not equal better results. Strategic curation—selecting the 3-5 most relevant experiences—maintains your strategic control and prevents AI from being overwhelmed with diluted information. Reference: Slide 7 on Minimum Effective Dose from Anthropic's engineering team.

  - id: "W2-Q4-workslop"
    type: "multiple_choice"
    bloom_level: "remembering"
    topic: "Workslop Problem"

    question: |
      According to the HBR research by Niederhoffer et al., what percentage of workers view the sender of workslop as less capable?

    options:
      - key: "A"
        text: "22%"
        feedback: "Incorrect. 22% is the percentage who felt offended by receiving workslop, not who view the sender as less capable."
      - key: "B"
        text: "41%"
        feedback: "Incorrect. 41% is the percentage of workers who have encountered workslop, not who judge senders negatively."
      - key: "C"
        text: "50%"
        feedback: "Correct. Half of recipients view workslop senders as less capable—this reputation damage is the serious career impact of poor AI use."
        correct: true
      - key: "D"
        text: "53%"
        feedback: "Incorrect. 53% is the percentage who felt annoyed by workslop, not who judge the sender's capability."

    general_feedback: |
      <b>Workslop</b> (AI-generated content that appears polished but lacks substance, insight, or authentic human thinking) has serious consequences. When 50% of recipients view senders as less capable, using AI poorly directly damages your professional reputation. The research shows workslop destroys careers because it signals inability to exercise judgment. Reference: Slide 11 on the hidden costs of workslop.

  - id: "W2-Q5-workslop"
    type: "multiple_choice"
    bloom_level: "understanding"
    topic: "Workslop Problem"

    question: |
      Which of the following emails would most likely be identified as workslop?

    options:
      - key: "A"
        text: "'Hi Team, Our client meeting moved to 3pm Thursday. Please bring updated sales figures for Q4. Thanks, Sarah'"
        feedback: "Incorrect. This email is specific, actionable, and contains concrete information—it demonstrates human judgment and clear thinking."
      - key: "B"
        text: "'Dear Team, I hope this email finds you well. I wanted to reach out regarding the deliverables we discussed. It is important that we align on expectations and ensure all stakeholders are informed. Please advise on your availability. Best regards'"
        feedback: "Correct. This is classic workslop—superficially professional but no specific information, no clear ask, no evidence of actual thinking. Just AI-generated filler."
        correct: true
      - key: "C"
        text: "'Quick question: Did we decide on the blue or green logo for the presentation? I'm finalizing slides now. - Mike'"
        feedback: "Incorrect. This email is direct, specific, and shows active engagement with work—clear human thinking and judgment."
      - key: "D"
        text: "'Reminder: Budget proposals due Friday 5pm. Use the template in shared drive. Let me know if you have questions. - Finance Team'"
        feedback: "Incorrect. This email provides specific deadline, clear action, and helpful resource—demonstrates thoughtful communication planning."

    general_feedback: |
      <b>Workslop characteristics</b> (superficially professional formatting, generic templated language, no specific insights or original thinking, obvious lack of human judgment) make content immediately recognizable to recipients. The experience creates confusion followed by frustration, signaling the sender didn't care enough to think critically. Reference: Slide 10 on what workslop is and how recipients experience it.

  - id: "W2-Q6-workslop"
    type: "multiple_choice"
    bloom_level: "understanding"
    topic: "Workslop/Pilot-Passenger"

    question: |
      A student uses ChatGPT to write a cover letter by saying 'Write me a cover letter for this marketing job,' then copies the entire output and submits it without editing. According to the pilot vs. passenger framework, what behavior is this student demonstrating?

    options:
      - key: "A"
        text: "Pilot behavior—using AI efficiently to save time"
        feedback: "Incorrect. Pilots actively steer AI with judgment and edit outputs critically. This student is abdicating thinking to AI."
      - key: "B"
        text: "Passenger behavior—leaning on AI to avoid hard work and treating AI as a shortcut"
        feedback: "Correct. This demonstrates classic passenger behavior: copy-paste without editing, no strategic framing, treating AI as a replacement for thinking rather than a tool."
        correct: true
      - key: "C"
        text: "Context engineering—providing AI with necessary information"
        feedback: "Incorrect. The student didn't provide strategic context (job description, relevant experiences, company mission). They gave a vague prompt and accepted the output uncritically."
      - key: "D"
        text: "Appropriate AI use for academic work"
        feedback: "Incorrect. This is inappropriate AI use that produces workslop. It demonstrates no judgment, no refinement, and no authentic thinking."

    general_feedback: |
      The <b>pilot vs. passenger framework</b> (pilots actively steer AI with judgment and use it as a springboard for insight; passengers lean on AI to avoid hard work and copy-paste without editing) distinguishes effective from ineffective AI users. Passengers produce workslop that damages reputation; pilots produce enhanced work showcasing both AI capability and human judgment. Reference: Slide 12 on the two mindsets and their outcomes.

  - id: "W2-Q7-judgment"
    type: "multiple_choice"
    bloom_level: "remembering"
    topic: "Human Judgment at the Helm"

    question: |
      According to Aashna Kircher from Workday, what is the critical step civilization must take in the next three to five years?

    options:
      - key: "A"
        text: "Develop more powerful AI models"
        feedback: "Incorrect. Kircher's focus is on human skill development, not AI technological advancement."
      - key: "B"
        text: "Thoughtfully educate people about how to be good at judgment"
        feedback: "Correct. Kircher emphasizes that judgment education is a civilization-level priority for the AI era—we haven't thoughtfully enough educated people on this critical skill."
        correct: true
      - key: "C"
        text: "Regulate AI use in workplace settings"
        feedback: "Incorrect. While regulation may be discussed, Kircher's quote specifically addresses judgment education, not policy."
      - key: "D"
        text: "Replace human workers with AI systems"
        feedback: "Incorrect. This contradicts the entire concept of 'human at the helm'—humans make strategic decisions AI cannot."

    general_feedback: |
      <b>Judgment</b> (the ability to make sound decisions when there's no clear right answer, weighing tradeoffs and considering context) cannot be automated and represents the core human differentiator in the AI era. Kircher's statement that judgment education is a civilization-level priority reflects how fundamental this skill has become. Reference: Slide 14 on the shift from 'human in the loop' to 'human at the helm.'

  - id: "W2-Q8-judgment"
    type: "multiple_choice"
    bloom_level: "understanding"
    topic: "Human Judgment at the Helm"

    question: |
      Katy George from Microsoft (former McKinsey partner) identifies four key competencies employees must demonstrate to thrive. Which competency is listed first, indicating its priority?

    options:
      - key: "A"
        text: "Design-thinking mindset"
        feedback: "Incorrect. While design-thinking is the fourth competency, sound judgment is listed first, indicating its priority."
      - key: "B"
        text: "Effective delegation to AI agents"
        feedback: "Incorrect. This is the second competency. Sound judgment comes first."
      - key: "C"
        text: "Sound judgment"
        feedback: "Correct. Sound judgment is listed first—the ability to make good decisions when AI gives multiple options, identify when AI is confidently wrong, and weigh business tradeoffs."
        correct: true
      - key: "D"
        text: "Quality control over AI outputs"
        feedback: "Incorrect. This is the third competency—the workslop detector skill. Sound judgment is the foundation that enables quality control."

    general_feedback: |
      According to <b>Microsoft's hiring criteria</b> (sound judgment, effective delegation to AI agents, quality control over AI outputs, design-thinking mindset), sound judgment is the foundational competency that enables all others. As a former McKinsey partner now leading people strategy at Microsoft, George represents what top employers are actually hiring for in 2025. Reference: Slide 15 on what executives want from employees.

  - id: "W2-Q9-judgment"
    type: "multiple_choice"
    bloom_level: "understanding"
    topic: "Human Judgment at the Helm"

    question: |
      Why does the lecture emphasize developing an 'experimental mindset' where you treat yourself as a 'Chief Experimentation Officer'?

    options:
      - key: "A"
        text: "Because AI tools are unreliable and produce random results"
        feedback: "Incorrect. The emphasis is not about AI unreliability, but about continuous learning and adaptation."
      - key: "B"
        text: "Because AI tools evolve monthly and continuous experimentation is the only sustainable strategy for building judgment"
        feedback: "Correct. With no 'right way' to use AI, testing different approaches and reflecting on what produces quality vs. workslop builds judgment through repeated practice."
        correct: true
      - key: "C"
        text: "Because employers want to hire people with science backgrounds"
        feedback: "Incorrect. The experimental mindset is about learning and adaptation, not scientific training."
      - key: "D"
        text: "Because students should use as many different AI tools as possible"
        feedback: "Incorrect. The focus is on learning what works through testing and iteration, not on tool quantity."

    general_feedback: |
      The <b>experimental mindset</b> (testing different approaches with AI, reflecting on what produces quality vs. workslop, and iterating based on feedback) is essential because AI capabilities evolve constantly. No one has the perfect approach. Judgment develops through the learning cycle: form hypothesis, test with AI assistance, evaluate quality, reflect on differences, apply learning to next iteration. Reference: Slide 16 on cultivating experimental mindset and the Mentorship Program as a safe space to experiment.

  - id: "W2-Q10-ebcr"
    type: "multiple_choice"
    bloom_level: "remembering"
    topic: "EBCR Framework"

    question: |
      What are the four stages of the Explore-Build-Connect-Refine framework for AI-assisted career development?

    options:
      - key: "A"
        text: "Explore possibilities, Build skills, Connect with mentors, Refine outputs"
        feedback: "Correct. The four stages are: EXPLORE (map possibilities and surface gaps), BUILD (learn through iterative practice), CONNECT (communicate and network with purpose), REFINE (test, adapt, and verify)."
        correct: true
      - key: "B"
        text: "Evaluate options, Build resume, Contact employers, Review applications"
        feedback: "Incorrect. While these activities may occur within the framework, these are not the official stage names from the Chremos & Repetto framework."
      - key: "C"
        text: "Engage AI, Build content, Collaborate online, Reflect on results"
        feedback: "Incorrect. These are not the stages of the EBCR framework. The framework emphasizes exploration, skill building, purposeful connection, and quality control."
      - key: "D"
        text: "Experiment with AI, Brainstorm ideas, Create materials, Revise drafts"
        feedback: "Incorrect. While experimentation and revision are part of the process, these are not the four official stages of the framework."

    general_feedback: |
      The <b>EBCR Framework</b> (Explore-Build-Connect-Refine) provides a structured approach to AI-assisted career development where AI serves as a thought partner, not an answer generator. Developed by university career services directors, this framework ensures career materials reflect the authentic you, enhanced by AI capability. Reference: Slide 18 introducing the career preparation framework from Inside Higher Ed.

  - id: "W2-Q11-ebcr"
    type: "multiple_choice"
    bloom_level: "understanding"
    topic: "EBCR Framework"

    question: |
      A student asks AI: 'I've completed courses in microeconomics, data analytics, and business communication. I led a team project analyzing consumer behavior. What competencies could I claim based on these experiences?' Which stage of the EBCR framework is this student applying?

    options:
      - key: "A"
        text: "EXPLORE—using AI to infer competencies and expand awareness of skills developed through academic experiences"
        feedback: "Correct. The EXPLORE stage helps surface skills students often underestimate by having AI identify patterns in their experiences and translate academic work into professional competencies."
        correct: true
      - key: "B"
        text: "BUILD—practicing professional tasks to develop competence"
        feedback: "Incorrect. BUILD focuses on iterative practice and skill development, not on identifying existing competencies."
      - key: "C"
        text: "CONNECT—preparing for professional interactions"
        feedback: "Incorrect. CONNECT involves networking preparation and relationship building, not competency identification."
      - key: "D"
        text: "REFINE—testing and verifying quality of outputs"
        feedback: "Incorrect. REFINE applies critical quality control to completed materials, not initial competency discovery."

    general_feedback: |
      The <b>EXPLORE stage</b> (using AI to expand awareness of career options and identify skill gaps) helps students see patterns in their experiences. Activity 1 in EXPLORE involves asking AI to infer competencies—translating academic projects into professional language. For example, group presentations translate to project management, stakeholder communication, and deadline management skills. Reference: Slide 19 on EXPLORE activities and the pilot behavior of curating which experiences to highlight.

  - id: "W2-Q12-ebcr"
    type: "multiple_choice"
    bloom_level: "understanding"
    topic: "EBCR Framework"

    question: |
      Before submitting your Personal Development Plan, you ask AI to 'Review this plan as my professor would. What weaknesses or unclear arguments would you identify?' Which stage of the EBCR framework are you applying, and why is this stage critical?

    options:
      - key: "A"
        text: "BUILD—because you are developing your writing skills through practice"
        feedback: "Incorrect. While this does involve skill development, the activity of simulating critical review specifically belongs to the REFINE stage."
      - key: "B"
        text: "REFINE—because you are applying critical quality control to catch issues before they damage your grade, demonstrating pilot behavior"
        feedback: "Correct. REFINE involves simulating reviewer critiques, A/B testing approaches, and verifying quality. This is where workslop gets caught—pilots spend 50% of their time refining; passengers skip this stage."
        correct: true
      - key: "C"
        text: "EXPLORE—because you are discovering gaps in your plan"
        feedback: "Incorrect. While you may discover gaps, this activity is about quality control on completed work, which is the REFINE stage, not initial exploration."
      - key: "D"
        text: "CONNECT—because you are simulating interaction with your professor"
        feedback: "Incorrect. CONNECT focuses on networking and relationship building. Simulating critical review for quality control is a REFINE activity."

    general_feedback: |
      The <b>REFINE stage</b> (testing, adapting, and verifying quality before work represents you) is where pilots separate from passengers. Activities include simulating reviewer critiques, A/B testing narratives, identifying jargon, and verifying facts. The 30-second test asks: Would a colleague recognize this as thoughtful human work? Refinement is where your value shows—passengers skip it and submit first drafts; pilots spend half their time here. Reference: Slide 22 on REFINE activities and the critical importance of quality control before submission.
---