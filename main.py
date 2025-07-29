from dotenv import load_dotenv
from src.workflow import Workflow
import os
import subprocess
import streamlit as st
import pickle

load_dotenv()

def main():
    workflow=Workflow()
    print("Lead Gen Automation Agent")

    while True:
        query = input("\nWho is the client (Ex. DuPont Tedlar Graphics & Signage Team): ").strip()
        if query.lower() in {"quit", "exit", ""}:
            break

        if query:
            result = workflow.run(query)
            """print(f"\nCustomer: {result.query}")
            print(f"\nCustomer Description: {result.customer_desc}")
            print(f"\nTarget Industry: {result.industry}")
            print(f"\nRelevant Event: {result.targetEvent}")
            print(f"\nCustomer Prospect: {result.targetLead}")
            print(f"\nProspect Description: {result.lead_desc}")
            print(f"\nProspect Contact: {result.leadContact}")
            print(f"\nFit Analysis: {result.fitAnalysis}")
            print(f"\nOutreach Message: {result.outreachMsg}")"""

            save_state(result)
            run_dashboard()

def save_state(state, filename="state.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(state, f)

def run_dashboard():
    dashboard_path = os.path.join("src", "dashboard.py")
    subprocess.run(["streamlit", "run", dashboard_path], cwd=os.path.dirname(__file__))

if __name__ == "__main__":
    main()



