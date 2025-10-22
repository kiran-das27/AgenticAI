import streamlit as st
from src.gen_insurance_tool.crew import GenInsuranceTool

st.set_page_config(page_title="📈 Insurance Policy Advisor")

st.title("📋 Insurance Policy Recommendation")

# --- 1. Take user inputs
st.sidebar.header("User Input")
budget = st.sidebar.number_input("Annual Premium Budget (₹)", value=50000)
policy_term = st.sidebar.slider("Policy Term (Years)", 5, 30, 15)
goal = st.sidebar.text_input("Financial Goal", value="Retirement planning")

if st.button("Run Insurance Advisor 🚀"):
    with st.spinner("Running AI Agents..."):

        # --- 2. Prepare inputs for crew
        inputs = {
            "budget": budget,
            "term": policy_term,
            "goal": goal
        }

        # --- 3. Run Crew
        result = GenInsuranceTool().crew().kickoff(inputs=inputs)

        # --- 4. Display result
        st.subheader("🧠 Final Recommendation")
        st.markdown(result, unsafe_allow_html=True)

        # --- 5. Save to file
        output_path = "terminal_output.md"
        with open(output_path, "w") as f:
            f.write(result.raw)

        # --- 6. Download button
        with open(output_path, "rb") as file:
            st.download_button(
                label="📥 Download Report as Markdown",
                data=file,
                file_name="terminal_output.md",
                mime="text/markdown"
            )
