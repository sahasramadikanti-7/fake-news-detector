import streamlit as st
from google import genai
import json
import re

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="📰",
    layout="centered"
)

# --------------------------------------------------
# GEMINI CONNECTION
# --------------------------------------------------
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #aaaaaa;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 25px;
        border-radius: 15px;
        margin-top: 20px;
    }

    .footer {
        text-align: center;
        color: #888888;
        margin-top: 40px;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    '<div class="main-title">📰 Fake News Detector</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered news credibility analysis using Gemini</div>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# INFORMATION
# --------------------------------------------------
st.info(
    "🔎 Enter a news paragraph below. The AI will analyze it "
    "and classify it as likely FAKE or likely REAL."
)

# --------------------------------------------------
# FEW-SHOT EXAMPLES
# --------------------------------------------------
examples = """
Example 1:
News: The city administration announced that public schools will remain
closed tomorrow because of severe weather conditions. The announcement
was published through the city's official communication channels.
Label: REAL

Example 2:
News: A viral social media message claims that the government will deposit
₹50,000 into every citizen's bank account if they register through a
WhatsApp link within 24 hours.
Label: FAKE

Example 3:
News: Scientists announced the successful launch of a research satellite
designed to collect environmental and atmospheric data.
Label: REAL

Example 4:
News: A viral post claims that a new mobile application can make anyone
a millionaire within 24 hours without investment or work.
Label: FAKE

Example 5:
News: A university announced that its annual examination schedule has
been published on its official website and students can check their
individual examination dates there.
Label: REAL

Example 6:
News: A social media post claims that drinking a special mixture for
three days can permanently prevent every viral infection.
Label: FAKE

Example 7:
News: The national weather department issued an advisory asking residents
in several regions to remain cautious because heavy rainfall is expected.
Label: REAL

Example 8:
News: A viral message claims that people who forward the message to
20 contacts will receive a government job automatically.
Label: FAKE

Example 9:
News: Researchers published a study describing the results of an
experiment and explained the methods and limitations of their research.
Label: REAL

Example 10:
News: An online post claims that a secret technology has been developed
that allows ordinary smartphones to read a person's thoughts from
several kilometres away.
Label: FAKE
"""

# --------------------------------------------------
# NEWS INPUT
# --------------------------------------------------
st.subheader("📝 Enter News")

news_text = st.text_area(
    "Paste your news article or paragraph:",
    height=220,
    placeholder="Example: Scientists have announced..."
)

# --------------------------------------------------
# DETECTION
# --------------------------------------------------
if st.button(
    "🔍 Detect News",
    use_container_width=True
):

    if not news_text.strip():

        st.warning("⚠️ Please enter a news paragraph first.")

    else:

        prompt = f"""
You are an AI assistant designed to analyze potentially
misleading or fake news.

Use the following 10 demonstration examples to understand
the expected classification style:

{examples}

Now analyze the following user-provided news:

"{news_text}"

Return ONLY valid JSON:

{{
    "prediction": "FAKE",
    "fake_confidence": 85,
    "real_confidence": 15,
    "reason": "Short explanation."
}}

Rules:

1. prediction must be either FAKE or REAL.
2. fake_confidence must be a number from 0 to 100.
3. real_confidence must be a number from 0 to 100.
4. fake_confidence + real_confidence must equal 100.
5. Give a short and understandable explanation.
6. Do not classify something as fake only because it sounds surprising.
7. Look for signs such as unrealistic claims, impossible statements,
   suspicious promises, fabricated information, and misleading patterns.
8. Consider whether the claim sounds like a genuine news report.
9. If there is not enough evidence to determine whether it is true,
   lower the confidence instead of giving an extreme score.
10. Do not use markdown.
11. Return only the JSON object.
"""

        with st.spinner("🤖 Analyzing the news..."):

            try:

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )

                result_text = response.text.strip()

                result_text = re.sub(
                    r"```json|```",
                    "",
                    result_text
                ).strip()

                result = json.loads(result_text)

                prediction = result["prediction"].upper()
                fake_confidence = int(result["fake_confidence"])
                real_confidence = int(result["real_confidence"])
                reason = result["reason"]

                # --------------------------------------------------
                # RESULT
                # --------------------------------------------------

                st.divider()

                st.subheader("📊 Detection Result")

                if prediction == "FAKE":

                    st.error(
                        "🚨 LIKELY FAKE NEWS"
                    )

                else:

                    st.success(
                        "✅ LIKELY REAL NEWS"
                    )

                # --------------------------------------------------
                # CONFIDENCE
                # --------------------------------------------------

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "🤥 Fake Confidence",
                        f"{fake_confidence}%"
                    )

                with col2:

                    st.metric(
                        "✅ Real Confidence",
                        f"{real_confidence}%"
                    )

                st.progress(
                    fake_confidence / 100
                )

                # --------------------------------------------------
                # EXPLANATION
                # --------------------------------------------------

                st.subheader("💡 AI Explanation")

                st.write(reason)

                # --------------------------------------------------
                # DISCLAIMER
                # --------------------------------------------------

                st.warning(
                    "⚠️ This is an AI-based assessment. "
                    "The confidence percentage is an AI estimate "
                    "and should not be treated as definitive "
                    "fact verification."
                )

            except json.JSONDecodeError:

                st.error(
                    "The AI returned an unexpected format. "
                    "Please try again."
                )

            except Exception as e:

                st.error(
                    "Something went wrong while analyzing the news."
                )

                st.code(str(e))

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    '<div class="footer">'
    'Fake News Detection Project • Powered by Streamlit + Gemini'
    '</div>',
    unsafe_allow_html=True
)