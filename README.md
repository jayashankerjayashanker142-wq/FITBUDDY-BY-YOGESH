# 💪 FitBuddy – AI Fitness Plan Generator
### Generative AI with Google | Built using Gemini Models

---

## 1. Abstract
FitBuddy is a web application that uses Google's **Gemini** generative AI models to create personalised fitness and nutrition plans. The user enters basic details (age, height, weight, goal, fitness level, equipment, diet preference, health issues). The app calculates **BMI, BMR and TDEE**, sends a structured prompt to Gemini, and returns a complete plan: weekly workout schedule, warm-up/cool-down, sample meal plan, progression and recovery tips. Users can also ask FitBuddy to modify the plan in natural language.

## 2. Problem Statement
Personal trainers and dieticians are expensive, and generic online plans ignore individual needs. There is a need for an accessible, instant, personalised fitness guide.

## 3. Objectives
- Generate personalised workout + diet plans using Generative AI.
- Calculate health metrics (BMI, BMR, TDEE) automatically.
- Provide an easy, interactive UI (Streamlit).
- Allow conversational plan editing and plan download.
- Include safety guardrails and disclaimers.

## 4. Technologies Used
| Component | Tool |
|---|---|
| Language | Python 3.10+ |
| Generative AI | Google Gemini (`gemini-2.5-flash`) via Google AI Studio API |
| SDK | `google-genai` |
| Frontend / UI | Streamlit |
| Formulas | BMI, Mifflin-St Jeor (BMR), Activity multiplier (TDEE) |

## 5. System Architecture / Workflow
```
User Input (Streamlit form)
        │
        ▼
Health Metrics Calculation (BMI, BMR, TDEE)
        │
        ▼
Prompt Engineering (profile + rules + output format)
        │
        ▼
Gemini Model (Google AI Studio API)
        │
        ▼
Generated Plan (Markdown) ──► Display ──► Download / Modify
```

## 6. Key Formulas
- **BMI** = weight(kg) / height(m)²
- **BMR (Mifflin-St Jeor)** = 10×weight + 6.25×height − 5×age + 5 (male) or −161 (female)
- **TDEE** = BMR × activity factor (1.2 to 1.725)

## 7. Prompt Engineering Approach
- Role prompting ("You are FitBuddy, a fitness & nutrition coach").
- Structured user profile injected into the prompt.
- Fixed output format (tables, sections) for consistent results.
- Safety rules (no extreme diets, adapt to injuries, advise doctor consultation).
- Follow-up prompt reuses the existing plan for editing (context-aware refinement).

## 8. How to Run (Step by Step)

1. **Install Python 3.10+** from python.org.
2. **Get a free Gemini API key**: open https://aistudio.google.com/apikey → *Create API key*.
3. Open a terminal inside the `FitBuddy` folder and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. *(Optional)* Set the key as an environment variable so you don't need to type it:
   - Windows (CMD): `set GEMINI_API_KEY=your_key`
   - Windows (PowerShell): `$env:GEMINI_API_KEY="your_key"`
   - Mac/Linux: `export GEMINI_API_KEY=your_key`
5. Run the app:
   ```bash
   streamlit run app.py
   ```
6. The browser opens at `http://localhost:8501`. Paste the API key in the sidebar (if not set), fill the form and click **Generate My Plan**.

### Run on Google Colab (no installation)
```python
!pip install streamlit google-genai
# upload app.py, then:
!streamlit run app.py & npx localtunnel --port 8501
```

## 9. Features
- Personalised workout + meal plan
- BMI / BMR / TDEE dashboard
- Supports home, dumbbell and gym setups
- Vegetarian / Non-veg / Vegan / Eggetarian diets
- Injury-aware suggestions
- Natural-language plan tweaking
- Download plan as Markdown

## 10. Limitations
- Output is AI generated and not a substitute for medical advice.
- Needs internet and a valid API key.
- Free-tier API has rate limits.

## 11. Future Scope
- Progress tracking with charts
- Image-based food calorie estimation using Gemini multimodal input
- Voice assistant, wearable (Fitbit/Google Fit) integration
- PDF export, multi-language support, mobile app

## 12. Conclusion
FitBuddy shows how Generative AI and Gemini models can make personalised fitness guidance accessible, fast and interactive, combining classical health formulas with LLM-based reasoning and natural-language interaction.

---

## 13. Possible Viva Questions
**Q1. What is Generative AI?** AI that creates new content (text, images, code) by learning patterns from large datasets.
**Q2. Which model did you use?** Google Gemini (`gemini-2.5-flash`) through the Google AI Studio API.
**Q3. Why Streamlit?** Quick to build Python web UIs without HTML/JS.
**Q4. What is prompt engineering?** Designing inputs (role, context, format, constraints) to get better model outputs.
**Q5. How do you ensure safety?** Safety rules in the prompt, disclaimer in the UI, advice to consult a doctor.
**Q6. What is BMR vs TDEE?** BMR = calories burned at rest; TDEE = BMR × activity level = total daily calories.
**Q7. Can it be improved?** Yes: progress tracking, multimodal food scanning, fine-tuning, wearable integration.

---
*Disclaimer: FitBuddy provides general fitness guidance only. Consult a qualified professional before starting any exercise or diet program.*
