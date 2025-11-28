# Course Evaluation Survey - LMS Import Package

This package contains research-based course evaluation surveys ready for import into Moodle and Blackboard.

---

## Files Included

| File | Purpose |
|------|---------|
| `moodle_feedback_survey.xml` | Moodle Feedback activity import file |
| `blackboard_survey.txt` | Blackboard Survey upload file (tab-delimited) |
| `distribution_evaluation.md` | Research summary comparing LMS vs Google Forms |
| `Course_Evaluation_Survey.docx` | Printable/reference version of the survey |

---

## Survey Overview

**Total Items:** 25 (23 quantitative + 2 open-ended)
**Estimated Completion Time:** 8-10 minutes
**Response Scale:** 7-point Likert (research-optimized)
**Reading Level:** 6th-8th grade (ESL-accessible)

### Dimensions Covered

| Section | Focus Area | Items |
|---------|------------|-------|
| A | Course Materials and Resources | 3 |
| B | Instructor Effectiveness and Teaching Quality | 4 |
| C | Assessment and Feedback | 3 |
| D | Learning Outcomes | 3 |
| E | Course Organization and Structure | 3 |
| F | Workload | 2 |
| G | Engagement and Interaction | 3 |
| H | Overall Ratings | 2 |
| I | Open-Ended Questions | 2 |

---

## Moodle Import Instructions

### Step 1: Create a Feedback Activity
1. Turn editing on in your course
2. Click "Add an activity or resource" in the desired section
3. Select **Feedback** (not Quiz)
4. Enter a name: "Course Evaluation Survey"
5. Configure settings:
   - **Record user names:** Anonymous
   - **Allow multiple submissions:** No
   - **Enable notification:** Yes (recommended)
6. Click "Save and display"

### Step 2: Import Questions
1. In the Feedback activity, click the **Templates** tab
2. Click **Import questions**
3. Click "Choose a file" and upload `moodle_feedback_survey.xml`
4. Select **Append new items** (or Delete old items if starting fresh)
5. Click **Import from this file**

### Step 3: Configure Availability
1. Go back to Edit settings
2. Set opening and closing dates (recommend 2 weeks before course end)
3. Enable automatic completion notification

### Step 4: View Results
- Go to the Feedback activity → **Analysis** tab
- Export results to Excel for detailed scoring

---

## Blackboard Import Instructions

### For Blackboard Original:

#### Step 1: Create the Survey
1. Go to **Control Panel** → **Course Tools** → **Tests, Surveys, and Pools**
2. Click **Surveys**
3. Click **Build Survey**
4. Enter name: "Course Evaluation Survey"
5. Add description/instructions (copy from the Instructions section below)
6. Click **Submit**

#### Step 2: Upload Questions
1. On the Survey Canvas, click **Upload Questions** in the action bar
2. Click **Browse** and select `blackboard_survey.txt`
3. Click **Submit**
4. Review imported questions (all 25 should appear)

#### Step 3: Deploy the Survey
1. Go to a Content Area in your course
2. Click **Assessments** → **Survey**
3. Select your survey and configure:
   - **Make available:** Yes
   - **Anonymous:** Yes
   - Set availability dates

### For Blackboard Ultra:

#### Step 1: Create the Survey
1. In your course, click the **+** button where you want the survey
2. Select **Create** → **Test**
3. Enter title: "Course Evaluation Survey"
4. In the test settings, enable **Anonymous submissions**

#### Step 2: Import Questions
1. Click the **+** button in the test canvas
2. Select **Reuse questions** → **Upload questions**
3. Upload `blackboard_survey.txt`
4. Review and confirm imported questions

---

## Survey Instructions Text

Use this text for the survey introduction:

---

**Course Evaluation Survey**

Thank you for taking time to complete this evaluation. Your honest feedback helps us improve the course.

**This survey is anonymous.** Your responses will not affect your grade.

For each statement, select one number from 1 to 7 that best describes your experience.

**Estimated time:** 8-10 minutes

**Rating Scale for Sections A-G:**
- 1 = Strongly Disagree
- 2 = Disagree
- 3 = Slightly Disagree
- 4 = Neutral
- 5 = Slightly Agree
- 6 = Agree
- 7 = Strongly Agree

---

## Scoring Guide

### Calculating Dimension Scores

For each dimension, calculate the mean of all items in that section:

```
Dimension Score = Sum of item responses ÷ Number of items in dimension
```

### Interpreting Scores (7-point scale)

| Score Range | Interpretation | Action |
|-------------|----------------|--------|
| 6.0 - 7.0 | Excellent | Maintain current approach |
| 5.0 - 5.9 | Good | Minor refinements may help |
| 4.0 - 4.9 | Adequate | Review for improvement opportunities |
| 3.0 - 3.9 | Needs Improvement | Targeted intervention recommended |
| 1.0 - 2.9 | Critical | Significant changes required |

### Priority Dimensions

Research shows these dimensions most strongly predict student learning outcomes:
1. **Organization and Clarity (Section E)** - strongest predictor
2. **Instructor Enthusiasm (Item B2)**
3. **Feedback Quality (Section C)**
4. **Student-Instructor Rapport (Section G)**

Focus improvement efforts on these areas first.

---

## Best Practices for Administration

1. **Allocate class time:** Give students 10-15 minutes during class
2. **Send reminders:** 1 week before, 3 days before, day of deadline
3. **Explain purpose:** Tell students how feedback will be used
4. **Close the loop:** Share summary of changes made from past feedback
5. **Target 70%+ response rate** for reliable results

---

## Technical Notes

### Moodle Compatibility
- Tested with Moodle 3.x and 4.x
- Uses `multichoicerated` question type for automatic scoring
- Exports numeric values (1-7) for analysis

### Blackboard Compatibility
- Works with Blackboard Original and Ultra
- Uses MC (Multiple Choice) format for Likert items
- Uses ESS (Essay) format for open-ended questions
- Note: In surveys, correct/incorrect designations are ignored

---

## Troubleshooting

**Moodle: "Invalid XML" error**
- Ensure the file is saved with UTF-8 encoding
- Check that the file was not modified in Word (use plain text editor)

**Blackboard: Questions not importing**
- Verify the file is saved as .txt (tab-delimited)
- Check for blank lines between questions (remove them)
- Ensure file uses Windows line endings (CRLF)

**Response rates are low**
- Enable LMS pop-up reminders
- Provide in-class completion time
- Explain how feedback will be used
- Consider small incentive (e.g., 1 bonus point for class if 90% respond)

---

## Research Foundation

This survey is based on:
- **SEEQ** (Students' Evaluations of Educational Quality) - Marsh, 1982
- **IDEA Center** evaluation frameworks
- Meta-analyses of SET (Student Evaluation of Teaching) research
- Best practices from top management schools

See `distribution_evaluation.md` for full research summary and citations.
