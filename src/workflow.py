from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import sys

from .models import ResearchState
from .firecrawl import FirecrawlService
from .prompts import Prompts

class Workflow:
    def __init__(self):
        self.firecrawl = FirecrawlService()
        self.llm = ChatOpenAI(model = "gpt-4o-mini", temperature=0.1)
        self.prompts = Prompts
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(ResearchState)
        graph.add_node("extract_industry", self._extract_industry)
        graph.add_node("extract_targetEvent", self._extract_targetEvent)
        graph.add_node("extract_targetLead", self._extract_targetLead)
        graph.add_node("extract_leadContact", self._extract_leadContact)
        graph.add_node("analyze_fit", self._fit_analysis)
        graph.add_node("outreachMsg", self._write_outreachMsg)
        graph.set_entry_point("extract_industry")
        graph.add_edge("extract_industry","extract_targetEvent")
        graph.add_edge("extract_targetEvent","extract_targetLead")
        graph.add_edge("extract_targetLead","extract_leadContact")
        graph.add_edge("extract_leadContact","analyze_fit")
        graph.add_edge("analyze_fit", "outreachMsg")
        graph.add_edge("outreachMsg", END)
        return graph.compile()




    def _extract_industry(self, state:ResearchState) -> Dict[str, Any]:
        print(f"Analyzing info about {state.query}")

        article_query = f"{state.query}"
        search_results = self.firecrawl.search_query(article_query, num_results = 3)

        all_content = ""
        for result in search_results.data:
            url = result.get("url", "")
            scraped=self.firecrawl.scrape_website(url)
            if scraped:
                all_content + scraped.markdown[:1500] + "\n\n"

        messages = [
            SystemMessage(content=self.prompts.COMPANY_INDUSTRY_SYSTEM),
            HumanMessage(content=self.prompts.company_industry_user(state.query, all_content))
        ] 

        messages2 = [
            SystemMessage(content=self.prompts.COMPANY_DESC_SYSTEM),
            HumanMessage(content=self.prompts.company_desc_user(state.query, all_content))
        ]

        try:
            response = self.llm.invoke(messages)
            industry = [
                industry.strip()
                for industry in response.content.strip().split("\n")
                if industry.strip()
            ]
            response2 = self.llm.invoke(messages2)
            customer_desc = [
                customer_desc.strip()
                for customer_desc in response2.content.strip().split("\n")
                if customer_desc.strip()
            ]
            #print(f"Relevant target industry: {industry[0]}")
            return {"industry": industry[0], "customer_desc":customer_desc[0]}
        except Exception as e:
            print(e)
            return {"industry": "", "customer_desc": ""}
        
    def _extract_customerInfo(self, state:ResearchState) -> Dict[str, Any]:
        article_query = f"{state.query}"
        search_results = self.firecrawl.search_query(article_query, num_results = 3)

        all_content = ""
        for result in search_results.data:
            url = result.get("url", "")
            scraped=self.firecrawl.scrape_website(url)
            if scraped:
                all_content + scraped.markdown[:1500] + "\n\n"

        messages = [
            SystemMessage(content=self.prompts.COMPANY_INDUSTRY_SYSTEM),
            HumanMessage(content=self.prompts.company_industry_user(state.query, all_content))
        ] 

        try:
            response = self.llm.invoke(messages)
            industry = [
                industry.strip()
                for industry in response.content.strip().split("\n")
                if industry.strip()
            ]
            #print(f"Relevant target industry: {industry[0]}")
            return {"industry": industry[0]}
        except Exception as e:
            print(e)
            return {"industry": ""}
        
        

    def _extract_targetEvent(self, state:ResearchState) -> Dict[str, Any]:
        if state.industry == "":
            sys.exit(1)

        print(f"Analyzing events for {state.industry} industry")

        article_query = f"Best {state.industry} conferences"
        search_results = self.firecrawl.search_query(article_query, num_results = 3)

        all_content = ""
        for result in search_results.data:
            url = result.get("url", "")
            scraped=self.firecrawl.scrape_website(url)
            if scraped:
                all_content + scraped.markdown[:1500] + "\n\n"

        messages = [
            SystemMessage(content=self.prompts.INDUSTRY_EVENTS_SYSTEM),
            HumanMessage(content=self.prompts.industry_events_user(state.industry, all_content))
        ] 

        try:
            response = self.llm.invoke(messages)
            targetEvent = [
                targetEvent.strip()
                for targetEvent in response.content.strip().split("\n")
                if targetEvent.strip()
            ]
            #print(f"Relevant target event: {targetEvent[0]}")
            return {"targetEvent": targetEvent[0]}
        except Exception as e:
            print(e)
            return {"targetEvent": ""}


    def _extract_targetLead(self, state:ResearchState) -> Dict[str, Any]:
        print(f"Analyzing participants for {state.targetEvent}")

        article_query = f"{state.targetEvent} attendee list"
        search_results = self.firecrawl.search_query(article_query, num_results = 3)

        all_content = ""
        for result in search_results.data:
            url = result.get("url", "")
            scraped=self.firecrawl.scrape_website(url)
            if scraped:
                all_content + scraped.markdown[:1500] + "\n\n"

        messages = [
            SystemMessage(content=self.prompts.EVENT_PARTICIPANTS_SYSTEM),
            HumanMessage(content=self.prompts.event_participants_user(state.targetEvent, all_content))
        ] 

        try:
            response = self.llm.invoke(messages)
            targetLead = [
                targetLead.strip()
                for targetLead in response.content.strip().split("\n")
                if targetLead.strip()
            ]
            #print(f"Relevant target lead: {targetLead[0]}")
            return {"targetLead": targetLead[0]}
        except Exception as e:
            print(e)
            return {"targetLead": ""}
        

    def _extract_leadContact(self, state:ResearchState) -> Dict[str, Any]:
        print(f"Analyzing leadership at {state.targetLead}")

        article_query = f"{state.targetLead} leadership"
        search_results = self.firecrawl.search_query(article_query, num_results = 3)

        article_query2 = f"{state.targetLead}"
        search_results2 = self.firecrawl.search_query(article_query2, num_results = 3)

        all_content = ""
        for result in search_results.data:
            url = result.get("url", "")
            scraped=self.firecrawl.scrape_website(url)
            if scraped:
                all_content + scraped.markdown[:1500] + "\n\n"

        all_content2 = ""
        for result in search_results2.data:
            url2 = result.get("url", "")
            scraped2=self.firecrawl.scrape_website(url2)
            if scraped2:
                all_content2 + scraped2.markdown[:1500] + "\n\n"

        messages = [
            SystemMessage(content=self.prompts.LEAD_CONTACT_SYSTEM),
            HumanMessage(content=self.prompts.lead_contact_user(state.targetLead, all_content))
        ] 

        messages2 = [
            SystemMessage(content=self.prompts.COMPANY_DESC_SYSTEM),
            HumanMessage(content=self.prompts.company_desc_user(state.targetLead, all_content2))
        ]

        try:
            response = self.llm.invoke(messages)
            leadContact = [
                leadContact.strip()
                for leadContact in response.content.strip().split("\n")
                if leadContact.strip()
            ]
            response2 = self.llm.invoke(messages2)
            lead_desc = [
                lead_desc.strip()
                for lead_desc in response2.content.strip().split("\n")
                if lead_desc.strip()
            ]
            #print(f"Relevant lead contact: {leadContact[0]}")
            return {"leadContact": leadContact[0], "lead_desc": lead_desc[0]}
        except Exception as e:
            print(e)
            return {"leadContact": "", "lead_desc": ""}


    def _fit_analysis(self, state:ResearchState) -> Dict[str, Any]:
        print(f"Analyzing strategic fit of {state.targetLead}")

        messages = [
            SystemMessage(content=self.prompts.FIT_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.fit_analysis_user(state.query, state.customer_desc, state.targetLead, state.lead_desc))
        ] 

        try:
            response = self.llm.invoke(messages)
            fitAnalysis = [
                fitAnalysis.strip()
                for fitAnalysis in response.content.strip().split("\n")
                if fitAnalysis.strip()
            ]
            return {"fitAnalysis": fitAnalysis[0]}
        except Exception as e:
            print(e)
            return {"fitAnalysis": ""}
        
    def _write_outreachMsg(self, state:ResearchState) -> Dict[str, Any]:
        print(f"Writing outreach message to {state.targetLead}")

        messages = [
            SystemMessage(content=self.prompts.OUTREACH_MSG_SYSTEM),
            HumanMessage(content=self.prompts.outreach_msg_user(state.query, state.customer_desc, state.targetLead, state.leadContact, state.fitAnalysis))
        ] 

        try:
            response = self.llm.invoke(messages)
            outreachMsg = [
                outreachMsg.strip()
                for outreachMsg in response.content.strip().split("\n")
                if outreachMsg.strip()
            ]
            return {"outreachMsg": outreachMsg[0]}
        except Exception as e:
            print(e)
            return {"outreachMsg": ""}

    def run(self, query:str) -> ResearchState:
        initial_state = ResearchState(
            query=query,
            customer_desc="",
            industry="",
            targetEvent="",
            targetLead="",
            lead_desc="",
            leadContact="",
            fitAnalysis="",
            outreachMsg=""
            )
        final_state = self.workflow.invoke(initial_state)
        return ResearchState(**final_state)
    
    