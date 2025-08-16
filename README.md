# Casteller: Asynchronous Prompt-Based Mentoring Platform

## Team Members
- **Mohammdreza Fakouri**  
  Medical Student, Alborz University of Medical Sciences  
  mfakouri2005@gmail.com  

## Team Mentors
- **Sina Moradi**  
  Medical Student, Alborz University of Medical Science  
  sina80mor@gmail.com  

- **Ali M. Shabestari**  
  Computer Engineering Student, Sharif University of Technology  
  ali.shabestari01@sharif.edu  

---

## 1. Problem Summary

Obtaining expert consultation remains a slow and often inefficient process. Key challenges include:

- Scheduling face-to-face or online meetings requires coordination and causes delays.
- Limited number of consultations possible in a work shift.
- Email exchanges are unreliable due to slow or absent responses.
- Difficulty in finding appropriate contact information.
- The delays are especially problematic for startups and individuals needing timely advice.

**Need:** A faster, more flexible system for expert consultation.

---

## 2. Solution Summary

**Casteller** is an asynchronous, prompt-based mentoring platform delivered via a **Telegram bot** that:

- Enables users to connect with experts quickly and flexibly.
- Avoids scheduling and cost barriers of traditional meetings.
- Offers a more integrated and responsive experience compared to email.

### Who benefits?

- **Experts**: Can consult more people and monetize their knowledge.
- **Mentees**: Save time and reduce consultation costs.

### Target users

- Professionals, entrepreneurs, students, and employees across industries.
- Fields include medical, legal, and exam preparation (e.g., university entrance exams).

### Consultation topics

- Professional development
- Business challenges
- Skill-building
- Exam strategies

### Pricing model

- Both free and premium consultations.
- Experts set their own fees, creating a balanced ecosystem encouraging participation and rewarding expertise.

---

## Key Benefits

- **Integrated Platform:** Includes a “monthly questionnaire” metric to analyze mentor activity and credibility.
- **Flexible Scheduling:** Asynchronous system fits consultations into daily routines.
- **Time Efficiency:** Rapid expert responses, eliminating rigid scheduling.
- **Cost Savings:** Removes the need for synchronous meetings.
- **Access to Top Experts:** Users submit concise queries to leading professionals with minimal cost burden.

---

## Main Goals of the Project

- Provide a streamlined, accessible mentoring platform via Telegram.
- Make expert guidance more efficient and widely available.
- Deliver timely advice especially for high-demand contexts such as university entrance exams, where it can significantly impact outcomes.

---

## Metrics for Improvement

- **User engagement:** Number of consultations per user.
- **Expert response time:** Average response time to queries.
- **User satisfaction:** Feedback scores after consultations.
- **Goal attainment:** Measurable improvements in outcomes (e.g., exam scores, business milestones).

> Example: A user can ask for *Konkur* exam strategies and receive actionable advice from an expert within minutes.

---

## Data Usage

Casteller collects and manages:

- Registration details.
- Questions and answers.
- Uploaded files.
- Ratings and feedback.
- Communication logs between mentors and mentees.

This data is used to:

- Improve matching.
- Track interactions.
- Ensure quality assurance.

Additional data sources:

- Integration with public professional profiles such as LinkedIn and Google Scholar.
- Open mentorship datasets to verify experts and improve matching accuracy.

**Privacy:**  
All sensitive data, including private messages and uploaded documents, is encrypted and access-controlled in compliance with privacy regulations to ensure user trust.

---

## Libraries and Techniques

- **Telegram interaction:** `python-telegram-bot` library for asynchronous API communication.
- **API management:** FastAPI or Flask for endpoints and session logic.
- **Data storage:** PostgreSQL or SQLite with SQLAlchemy.
- **Security:** bcrypt for password hashing.
- **Configuration:** python-dotenv.
- **Deployment:** Containerized with Docker and deployed on platforms like Heroku or AWS for scalability and reliability.

---

## Evaluation of Results

Casteller's success will be measured by:

- **Average expert response time:** Target under 5 minutes.
- **User retention:** Target 70% repeat users within three months.
- **User satisfaction rating:** Target 4.5 out of 5.

Benchmarks are based on comparable mentoring platforms and user expectations.

---

## Ethical Challenges and Societal Risks

- Ensuring user privacy rigorously.
- Preventing the spread of inaccurate or harmful advice.
- Implementing strict data protection and anonymization.
- Vetting experts with continuous quality monitoring.
- Providing clear disclaimers that consultations do not replace professional medical or legal advice, minimizing potential harm.

---

## Optional Features (Future Enhancements)

- Use machine learning and NLP technologies to transform user experience.
- Load datasets of previously asked questions/answers into a search engine to:

  - Sort results based on experts most likely to answer a user’s question.
  - Allow the user to post their question and have the system find related experts automatically.

- Display published answers by a language model to reduce spending on trivial questions.

---

# Summary

Casteller offers an innovative, asynchronous mentoring platform enabling fast, flexible, and affordable access to expert consultations. It removes traditional barriers and connects users across various fields to top experts via Telegram, improving professional development, business outcomes, and exam preparation success.

---

*For further information or inquiries, please contact the team members or mentors listed above.*
