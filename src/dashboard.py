import streamlit as st
import pickle
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.models import ResearchState


def load_state(filename="state.pkl"):
    with open(filename, "rb") as f:
        return pickle.load(f)
    
def build_dashboard(state: ResearchState):
    st.set_page_config(page_title="AI Agent Lead Dashboard", layout="wide")

    st.title(f"📊 {state.query}'s Lead Dashboard")
    st.markdown("Here's an auto-generated sales lead with all of the collected information and analyses. Review the fit analysis and copy the outreach message.\n\n---")

    col1, col2 = st.columns(2)

    with col1:
        st.header("🔍 Customer Info")
        st.text(f"Customer Query: {state.query}")
        st.text(f"Industry: {state.industry}")
        st.markdown(f"**Description:**\n{state.customer_desc}")

    with col2:
        st.header("🎯 Target Lead Info")
        st.text(f"Event: {state.targetEvent}")
        st.text(f"Target Lead: {state.targetLead}")
        st.text(f"Contact: {state.leadContact}")
        st.markdown(f"**Lead Description:**\n{state.lead_desc}")

    st.markdown("---")

    st.header("📌 Fit Analysis")
    st.info(state.fitAnalysis)

    st.header("📬 Outreach Email")
    st.info(state.outreachMsg)

def main():
    state = load_state()
    build_dashboard(state)

if __name__ == "__main__":
    main()
