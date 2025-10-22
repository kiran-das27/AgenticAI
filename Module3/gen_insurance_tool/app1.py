from curses import raw
import streamlit as st
import sys
import os

# Fix the import path if src is in a subfolder
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from src.gen_insurance_tool.crew import GenInsuranceTool

# Streamlit UI
st.set_page_config(page_title="Insurance Advisor", page_icon="📄")

st.title("📋 Insurance Policy Assistant")
st.markdown("Enter your details below to find the best policy.")

# Input form
with st.form("user_input_form"):
    name = st.text_input("Name", value="Kiran Das")
    age = st.number_input("Age", min_value=18, max_value=100, value=40)
    employment_type = st.selectbox("Employment Type", ["Salaried", "Self-employed", "Business Owner"])
    monthly_income = st.number_input("Monthly Income (in ₹)", min_value=0, value=100000)
    prefered_paying_for = st.selectbox("Preferred Premium Paying Term (in years)", [1, 5, 10, 15, 20])

    submitted = st.form_submit_button("Generate Policy Report")

if submitted:
    inputs = {
        'name': name,
        'age': str(age),
        'employmentType': employment_type,
        'monthlyincome': str(monthly_income),
        'preferedPayingFor': str(prefered_paying_for)
    }

    st.success("⏳ Running policy selection engine... This might take a few moments.")

    try:
        # Run the Crew and get the result
        result = GenInsuranceTool().crew().kickoff(inputs=inputs)

        # Save to file
        output_path = "terminal_output.md"
        with open(output_path, "w") as f:
            f.write(result.raw)

        st.success("✅ Report generated successfully!")

        # Display content and download button
        st.markdown("### 📄 Policy Summary")
        st.markdown(result.raw)

        with open(output_path, "rb") as file:
            st.download_button(
                label="📥 Download Report as Markdown",
                data=file,
                file_name="terminal_output.md",
                mime="text/markdown"
            )

    except Exception as e:
        st.error(f"🚫 An error occurred: {e}")
