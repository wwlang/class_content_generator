---
metadata:
  week: 6
  topic: "Visual Communication & Slide Design"
  prepares_for: "Group Presentation (Week 12)"
  source: "lecture-content.md"

questions:
  - id: "W6-Q1-ctml-assumptions"
    type: "multiple_choice"
    bloom_level: "remembering"
    topic: "Mayer's Cognitive Theory of Multimedia Learning"

    question: |
      What are the three core assumptions of Mayer's Cognitive Theory of Multimedia Learning?

    options:
      - key: "A"
        text: "Dual-Channel Processing, Limited Capacity, Active Processing"
        feedback: "Correct! These three assumptions form the foundation of how humans process multimedia: visual and auditory channels work separately, each handles limited information, and learning requires active engagement."
        correct: true

      - key: "B"
        text: "Visual Priority, Auditory Backup, Memory Storage"
        feedback: "Incorrect. Mayer's theory identifies Dual-Channel Processing, Limited Capacity, and Active Processing as the three core assumptions."

      - key: "C"
        text: "Sequential Processing, Unlimited Capacity, Passive Reception"
        feedback: "Incorrect. Mayer's theory emphasizes simultaneous dual-channel processing, limited capacity (5-7 chunks per channel), and active processing."

      - key: "D"
        text: "Single-Channel Processing, High Capacity, Automatic Learning"
        feedback: "Incorrect. The theory specifies two separate channels (Dual-Channel), each with limited capacity."

    general_feedback: |
      Mayer's <b>Cognitive Theory of Multimedia Learning</b> (framework explaining how humans learn from words and pictures) rests on three core assumptions: <b>dual-channel processing</b> (visual and auditory information processed separately), <b>limited capacity</b> (each channel holds only 5-7 chunks simultaneously), and <b>active processing</b> (learning requires deliberately selecting, organizing, and integrating information). Understanding these assumptions explains why poor slide design—like dense text with narration—overloads channels and causes comprehension failure. See Week 6 slides 7.

  - id: "W6-Q2-ctml-load-types"
    type: "multiple_choice"
    bloom_level: "remembering"
    topic: "Mayer's Cognitive Theory of Multimedia Learning"

    question: |
      What are the three types of cognitive load in Mayer's framework?

    options:
      - key: "A"
        text: "Intrinsic Load, Extraneous Load, Germane Load"
        feedback: "Correct! These three types describe different sources of cognitive effort: inherent topic complexity, wasted effort from poor design, and productive effort for understanding."
        correct: true

      - key: "B"
        text: "Visual Load, Auditory Load, Memory Load"
        feedback: "Incorrect. The three types are Intrinsic, Extraneous, and Germane—they describe the purpose of cognitive effort, not which channel is used."

      - key: "C"
        text: "Short-term Load, Long-term Load, Working Load"
        feedback: "Incorrect. These relate to memory systems. Mayer identifies Intrinsic, Extraneous, and Germane as the three load types."

      - key: "D"
        text: "Essential Load, Optional Load, Complex Load"
        feedback: "Incorrect. The framework uses Intrinsic Load, Extraneous Load, and Germane Load."

    general_feedback: |
      The three types are: <b>Intrinsic load</b> (inherent complexity of the material itself—some topics are genuinely difficult), <b>Extraneous load</b> (wasted mental effort from poor design like decorative clip art or confusing layouts), and <b>Germane load</b> (productive effort for understanding and building mental models). Good slide design minimizes extraneous load (remove distractions) and optimizes germane load (support understanding), while managing intrinsic load through techniques like <b>segmenting</b> (breaking complex content into smaller parts). See Week 6 slides 8.

  - id: "W6-Q3-ctml-load-distinction"
    type: "multiple_choice"
    bloom_level: "understanding"
    topic: "Mayer's Cognitive Theory of Multimedia Learning"

    question: |
      How do extraneous load and germane load differ in multimedia presentations?

    options:
      - key: "A"
        text: "Extraneous load is wasted effort from poor design; germane load is productive effort supporting understanding"
        feedback: "Correct! Extraneous load (decorative elements, confusing layouts) wastes cognitive resources; germane load (organizing information, building connections) builds understanding."
        correct: true

      - key: "B"
        text: "Extraneous load involves visual processing; germane load involves auditory processing"
        feedback: "Incorrect. Both types can involve either channel. The distinction is about whether the cognitive effort is productive or wasteful."

      - key: "C"
        text: "Extraneous load is always higher than germane load in bad presentations"
        feedback: "Incorrect. While bad presentations have high extraneous load, the key distinction is qualitative (wasteful vs. productive), not quantitative."

      - key: "D"
        text: "Extraneous load helps learning; germane load hinders it"
        feedback: "Incorrect. You have this reversed. Germane load supports learning; extraneous load wastes cognitive effort on design problems."

    general_feedback: |
      <b>Extraneous load</b> is unnecessary cognitive effort caused by poor design—decorative clip art forcing audiences to <b>filter</b> (separate useful from useless information) decoration from content, or confusing layouts requiring extra work to understand structure. <b>Germane load</b> is productive effort—<b>actively</b> (with deliberate mental work) selecting key information, organizing it into meaningful patterns, and integrating it with existing knowledge. Slide design should ruthlessly minimize extraneous and optimize germane. A slide with rotating animations has high extraneous; a slide with clear visual hierarchy has high germane. See Week 6 slides 8.

  - id: "W6-Q4-tufte-data-ink"
    type: "multiple_choice"
    bloom_level: "remembering"
    topic: "Tufte's Data-Ink Ratio"

    question: |
      What is Tufte's Data-Ink Ratio formula?

    options:
      - key: "A"
        text: "Data-ink ÷ Total ink used to print the graphic"
        feedback: "Correct! This formula measures what proportion of a visualization's visual elements actually convey data versus decoration."
        correct: true

      - key: "B"
        text: "Total ink ÷ Data-ink"
        feedback: "Incorrect. This would give you the inverse. The correct formula is Data-ink ÷ Total ink used."

      - key: "C"
        text: "Number of data points ÷ Chart area"
        feedback: "Incorrect. This would measure data density. The data-ink ratio is Data-ink ÷ Total ink used."

      - key: "D"
        text: "Chart complexity ÷ Viewer comprehension time"
        feedback: "Incorrect. The data-ink ratio specifically measures Data-ink ÷ Total ink used to print the graphic."

    general_feedback: |
      Tufte's <b>Data-Ink Ratio</b> = Data-ink ÷ Total ink used to print the graphic. This formula quantifies what proportion of a chart's visual elements actually display data information. A ratio of 1.0 would be ideal (every element shows data); most charts have much lower ratios due to decoration. Equivalently, the ratio equals 1 − (proportion of ink that can be erased without loss of data-information). Goal: maximize this ratio by removing 3D effects, decorative backgrounds, heavy gridlines, and ornamental borders. See Week 6 slides 13.

  - id: "W6-Q5-tufte-five-laws"
    type: "multiple_choice"
    bloom_level: "understanding"
    topic: "Tufte's Data-Ink Ratio"

    question: |
      What is the purpose of Tufte's Five Laws of Data-Ink?

    options:
      - key: "A"
        text: "To guide subtractive design by systematically removing visual elements that don't convey data"
        feedback: "Correct! The Five Laws (Above all else show the data; Maximize data-ink ratio; Erase non-data-ink; Erase redundant data-ink; Revise and edit) create a systematic process for eliminating visual waste."
        correct: true

      - key: "B"
        text: "To ensure all charts use the same visual style for consistency"
        feedback: "Incorrect. The laws focus on removing non-data elements, not standardizing appearance across charts."

      - key: "C"
        text: "To add visual interest through color and decoration"
        feedback: "Incorrect. The laws do the opposite—they eliminate decoration to maximize the proportion of ink devoted to data."

      - key: "D"
        text: "To make charts look more professional and polished"
        feedback: "Incorrect. The focus is on clarity and information density, not aesthetic polish. The laws guide removal of decorative elements."

    general_feedback: |
      Tufte's Five Laws create a <b>subtractive</b> (removing elements rather than adding) design process: (1) Above all else, show the data; (2) Maximize the data-ink ratio; (3) Erase non-data-ink (within reason); (4) Erase redundant data-ink (within reason); (5) Revise and edit continuously. This approach starts with a visualization and <b>systematically</b> (following a methodical process) removes every unnecessary element. Example: Excel's default charts have backgrounds, borders, heavy gridlines, legends, gradient fills—applying the Five Laws would eliminate most of these, leaving only data and minimal labels. See Week 6 slides 13.

  - id: "W6-Q6-chartjunk-categories"
    type: "multiple_choice"
    bloom_level: "remembering"
    topic: "Tufte's Data-Ink Ratio"

    question: |
      What are the three categories of chartjunk that Tufte identifies?

    options:
      - key: "A"
        text: "Moiré Vibration, Heavy Grids, Self-Promoting Graphics"
        feedback: "Correct! These three categories cover different types of unnecessary visual elements: optical interference patterns, overly prominent gridlines, and decorative forms overtaking data."
        correct: true

      - key: "B"
        text: "Colors, Borders, Backgrounds"
        feedback: "Incorrect. While these can be chartjunk when unnecessary, Tufte's three categories are Moiré Vibration, Heavy Grids, and Self-Promoting Graphics."

      - key: "C"
        text: "Text, Images, Shapes"
        feedback: "Incorrect. These are chart elements, not categories of chartjunk. The three categories are Moiré Vibration, Heavy Grids, and Self-Promoting Graphics."

      - key: "D"
        text: "3D Effects, Animations, Gradients"
        feedback: "Incorrect. While these can be chartjunk, Tufte's specific categories are Moiré Vibration, Heavy Grids, and Self-Promoting Graphics."

    general_feedback: |
      Tufte identifies three chartjunk categories: (1) <b>Moiré Vibration</b>—dense patterns creating optical interference, such as cross-hatching that creates visual shimmer; (2) <b>Heavy Grids</b>—overly prominent gridlines that dominate the chart area and draw more attention than the data itself; (3) <b>Self-Promoting Graphics</b> (nicknamed "Ducks" after a building shaped like a duck)—decorative forms overtaking data, such as 3D pie charts or bars shaped like money bags. All three add <b>extraneous cognitive load</b> (wasted mental effort) without conveying information. See Week 6 slides 14.

  - id: "W6-Q7-declutter-focus-finding"
    type: "multiple_choice"
    bloom_level: "understanding"
    topic: "Kellogg Declutter + Focus Technique"

    question: |
      What did Kellogg's research reveal about the effect of decluttering alone versus decluttering plus focus?

    options:
      - key: "A"
        text: "Decluttering alone improves appearance but provides no cognitive benefit; decluttering plus focus improves comprehension 2.5x"
        feedback: "Correct! This finding surprised researchers—removing chartjunk makes charts look better but doesn't help understanding. Only adding focus elements (headlines, strategic color) significantly improves comprehension."
        correct: true

      - key: "B"
        text: "Both techniques improve comprehension equally"
        feedback: "Incorrect. Decluttering alone showed no cognitive benefit. Only decluttering plus focus produced the 2.5x improvement in capturing main conclusions."

      - key: "C"
        text: "Decluttering is more effective than adding focus elements"
        feedback: "Incorrect. Decluttering alone provided no cognitive benefit. The focus technique was essential for the 2.5x comprehension improvement."

      - key: "D"
        text: "Neither technique significantly improves comprehension"
        feedback: "Incorrect. While decluttering alone showed no benefit, decluttering plus focus produced a 2.5x improvement in comprehension."

    general_feedback: |
      Kellogg's empirical research (Northwestern University, 2021) tested 24 participants viewing graphs in three conditions: cluttered, decluttered, and decluttered plus focused. Surprising finding: decluttered graphs looked better but didn't improve comprehension versus cluttered graphs. Only decluttered plus focused showed significant improvement—<b>approximately</b> (roughly, about) 2.5x better at capturing the main conclusion. This means cleaning up borders and gridlines isn't enough; you must actively guide attention through headlines and <b>strategic</b> (purposefully chosen) color highlighting. See Week 6 slides 21.

  - id: "W6-Q8-curse-expertise"
    type: "multiple_choice"
    bloom_level: "understanding"
    topic: "Kellogg Declutter + Focus Technique"

    question: |
      What is the "curse of expertise" in data presentation, and how does it relate to the need for the focus technique?

    options:
      - key: "A"
        text: "Presenters see patterns in data they assume audiences see too, but they're typically wrong; the focus technique overcomes this by explicitly guiding attention"
        feedback: "Correct! Expertise creates a blind spot—what's obvious to you after hours of analysis is invisible to first-time viewers. The focus technique solves this by actively telling audiences what to see."
        correct: true

      - key: "B"
        text: "Experts create overly complex charts that confuse audiences"
        feedback: "Incorrect. The curse isn't about complexity; it's about assuming audiences see patterns you see. The solution is guiding attention, not simplifying data."

      - key: "C"
        text: "Only experts can understand data visualizations effectively"
        feedback: "Incorrect. The curse is that experts assume their insights are obvious to others. Proper focus techniques make insights accessible to all viewers."

      - key: "D"
        text: "Presenters deliberately hide insights from audiences"
        feedback: "Incorrect. The curse isn't intentional—presenters genuinely believe insights are obvious. They need the focus technique to bridge this perception gap."

    general_feedback: |
      The <b>curse of expertise</b> (phenomenon where knowledge creates blind spots) means presenters spend hours analyzing data, making patterns obvious to them—but first-time viewers don't see these patterns. Presenters genuinely believe insights are clear ("it's obvious!"), but research shows they're typically wrong. This explains why 67% of business presentations fail to communicate their main point. Solution: Data cannot "speak for itself." Use the focus technique—add headlines stating conclusions, use color to highlight key data points. This actively guides audiences to see what you see. See Week 6 slides 20-21.

  - id: "W6-Q9-focus-techniques"
    type: "multiple_choice"
    bloom_level: "remembering"
    topic: "Kellogg Declutter + Focus Technique"

    question: |
      What are the key components of the focus technique according to Kellogg research?

    options:
      - key: "A"
        text: "Add headlines explaining trends; use color to highlight key data; limit to 1-2 colors maximum"
        feedback: "Correct! These three elements guide audience attention: headlines tell the story, color directs eyes to what matters, and color restraint prevents visual scatter."
        correct: true

      - key: "B"
        text: "Use multiple bright colors; add decorative elements; increase font sizes"
        feedback: "Incorrect. The focus technique uses strategic restraint—1-2 colors maximum, no decoration. Key elements are explanatory headlines and strategic color highlighting."

      - key: "C"
        text: "Remove all color; use only black and white; simplify to bare essentials"
        feedback: "Incorrect. The focus technique uses color strategically (1-2 colors to highlight key data), not eliminates it entirely."

      - key: "D"
        text: "Add more data points; show all possible trends; let audiences explore"
        feedback: "Incorrect. The focus technique guides audiences to specific insights through headlines and strategic color, not exploration."

    general_feedback: |
      The focus technique includes: (1) Add headlines explaining trends—not titles describing data ("Q3 Results") but headlines stating meaning ("Customer satisfaction dropped 15% in Q3"); (2) Use color to highlight key data points—color the one bar or line that matters, gray out supporting context; (3) Limit to 1-2 colors maximum—more colors create visual noise. Additionally, test with colleagues to verify your intended story comes through. The technique overcomes the curse of expertise by <b>explicitly</b> (clearly and directly) telling audiences what to see. See Week 6 slides 21-22.

  - id: "W6-Q10-mit-matrix-quadrants"
    type: "multiple_choice"
    bloom_level: "remembering"
    topic: "MIT Sloan Data Presentation Matrix"

    question: |
      In the MIT Sloan Data Presentation Matrix, what tool is recommended for explanatory purposes with sophisticated information?

    options:
      - key: "A"
        text: "Data stories and presentation decks"
        feedback: "Correct! This quadrant represents high-stakes persuasion requiring human judgment to integrate multiple data sources into a curated narrative."
        correct: true

      - key: "B"
        text: "AI chat interfaces"
        feedback: "Incorrect. AI chat interfaces are for exploratory purposes with simple information. Explanatory + sophisticated requires data stories/presentation decks."

      - key: "C"
        text: "Interactive dashboards"
        feedback: "Incorrect. Dashboards are for exploratory purposes (letting audiences discover insights). Explanatory + sophisticated requires data stories/presentation decks."

      - key: "D"
        text: "AI-infused BI tools"
        feedback: "Incorrect. These are for explanatory purposes with simple information. Explanatory + sophisticated requires data stories/presentation decks."

    general_feedback: |
      The MIT Sloan matrix (2024 framework for choosing data presentation tools) has four quadrants based on purpose and complexity: <b>Exploratory</b> (answering questions, discovering insights) vs. <b>Explanatory</b> (persuading to act); <b>Simple</b> (single metric) vs. <b>Sophisticated</b> (integrating multiple sources). Explanatory + Sophisticated = Data stories/presentation decks—human-crafted narratives for high-stakes decisions like board presentations. Example: $50M product launch decision requires curated story integrating customer data, projections, competitor analysis. AI can't provide this strategic synthesis. See Week 6 slides 18-19.

  - id: "W6-Q11-mit-distinction"
    type: "multiple_choice"
    bloom_level: "understanding"
    topic: "MIT Sloan Data Presentation Matrix"

    question: |
      What is the key distinction between dashboards and data stories according to the MIT Sloan framework?

    options:
      - key: "A"
        text: "Dashboards are for exploration; data stories are for persuasion and decision-making"
        feedback: "Correct! Dashboards let audiences discover patterns themselves (exploratory); data stories guide audiences to specific conclusions (explanatory). The purpose determines the tool."
        correct: true

      - key: "B"
        text: "Dashboards are always better than data stories for business presentations"
        feedback: "Incorrect. The framework recommends different tools for different purposes. Data stories are essential for explanatory, sophisticated presentations."

      - key: "C"
        text: "Dashboards contain more data than data stories"
        feedback: "Incorrect. The distinction isn't about data volume but purpose: exploration versus persuasion."

      - key: "D"
        text: "Data stories are outdated; dashboards should replace all presentations"
        feedback: "Incorrect. The framework (2024) argues data stories remain essential for high-stakes explanatory communication despite AI advances."

    general_feedback: |
      Dashboards are for <b>exploration</b>—audiences interact with data, filter views, discover their own insights. Appropriate when the goal is to answer "What happened?" Data stories are for <b>persuasion and decision-making</b>—presenter curates a specific narrative, integrates multiple sources, guides to a conclusion. Appropriate when the goal is "What should we do?" Example: Quarterly sales dashboard → exploration. Board presentation on new product launch → data story. Most student presentations (Week 12 Group Presentation) fall in the data story category: explanatory purpose, sophisticated integration. See Week 6 slides 18.

  - id: "W6-Q12-frameworks-integration"
    type: "multiple_choice"
    bloom_level: "understanding"
    topic: "Integration of All Frameworks"

    question: |
      How do Mayer's principles, Tufte's data-ink ratio, and the declutter-focus technique work together in effective slide design?

    options:
      - key: "A"
        text: "Mayer guides overall cognitive load management; Tufte maximizes data-ink ratio by removing chartjunk; declutter-focus adds active attention guidance"
        feedback: "Correct! The three frameworks form a comprehensive system: reduce extraneous load (Mayer), eliminate visual waste (Tufte), and guide audience attention (declutter-focus)."
        correct: true

      - key: "B"
        text: "All three frameworks say exactly the same thing about removing clutter"
        feedback: "Incorrect. While related, they address different aspects: Mayer focuses on cognitive load, Tufte on visual elements serving data, and declutter-focus on guiding attention."

      - key: "C"
        text: "The frameworks contradict each other and cannot be used together"
        feedback: "Incorrect. The frameworks complement each other, creating a comprehensive approach to visual design."

      - key: "D"
        text: "Only one framework should be applied to any given slide"
        feedback: "Incorrect. Effective slides apply all three: manage cognitive load (Mayer), maximize data-ink (Tufte), guide attention (focus)."

    general_feedback: |
      These frameworks form an <b>integrated</b> (working together as a system) design approach: (1) <b>Mayer</b> provides cognitive foundation—minimize extraneous load, optimize dual-channel processing, apply principles like Coherence and Redundancy; (2) <b>Tufte</b> provides visual clarity rules—maximize data-ink ratio, eliminate chartjunk, ensure graphical integrity; (3) <b>Declutter-focus</b> adds the active guidance layer—removing clutter improves appearance, but adding focus elements (headlines, strategic color) drives the 2.5x comprehension improvement. Together they create slides that are cognitively efficient (Mayer), visually clean (Tufte), and <b>explicitly</b> (clearly) guided (focus). See Week 6 slides 23-25.
---
