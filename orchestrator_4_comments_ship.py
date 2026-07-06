from typing import TypedDict  # Imports dictionary type hinting structures to define graph state contracts.
import sys  # Provides runtime utilities to inspect or control low-level engine variables.
import requests  # Handles classic standard synchronous HTTP connection payloads across endpoints.
from langgraph.graph import StateGraph, END  # Imports state-machine workflow engines and final terminal destination constants.
from langchain_ollama import OllamaLLM  # Imports the interface wrapper to communicate with locally hosted Ollama instances.
from langchain_neo4j import Neo4jGraph  # Imports the graph connection framework tool designed specifically for Neo4j DB instances.

# ---------------------------------------------------------
# 1. INITIALIZE CONNECTION TO NEO4J INSTANCE
# ---------------------------------------------------------
NEO4J_URI = "bolt://localhost:7687"  # Configures the active bolt network connection link for your database instance.
NEO4J_USERNAME = "neo4j"  # Establishes the admin authentication username identification profile parameter.
NEO4J_PASSWORD = "MotorcycleProduction_1_30*"  # Stores the protected security key used to access target database schemas.

graph = None  # Instantiates an empty base global pointer slot for tracking the active graph engine.

def get_graph():  # Declares a safe single-instance management connector function block.
    global graph  # Points context directly to the overarching parent script scope tracking variable.
    if graph is None:  # Evaluates whether a live connection handler is currently missing.
        print("[DEBUG] Connecting to Neo4j database...", flush=True)  # Emits initial pipeline diagnostic trace verification print statements.
        graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD, enhanced_schema=False)  # Connects the driver container instance to local graph data buckets.
        print("[DEBUG] Connected to Neo4j successfully.", flush=True)  # Confirms established connection metrics inside terminal environment logging paths.
    return graph  # Returns the live connected driver instance handler tool directly back to callers.

# ---------------------------------------------------------
# 2. DEFINE LANGGRAPH MEMORY STATE
# ---------------------------------------------------------
class AgentState(TypedDict):  # Structures the memory template layout object shared fluidly between processing nodes.
    user_query: str  # Tracks original prompt strings input by humans into dashboard components.
    cypher_query: str  # Stores current operational iterations of compiled graph query search strings.
    graph_data: str  # Holds structural text payloads pulled back from active graph nodes.
    final_answer: str  # Accumulates final parsed summary explanations built by natural language generation layers.
    fallback_attempt: bool  # Keeps track of flag conditions indicating whether core structural paths have failed.
    loop_count: int  # Records state iteration numbers to defend against recursive system path freezing.

# ---------------------------------------------------------
# 3. WORKFLOW NODES WITH DEEPER CONTEXT EXTRACTION
# ---------------------------------------------------------

def nlu_generate_cypher(state: AgentState):  # Sets up Node 1 processing logic for translating prompts to database scripts.
    print("\n" + "="*50, flush=True)  # Visual log boundary separation indicator block.
    print("[NODE 1] Entering nlu_generate_cypher...", flush=True)  # System tracking line verification trace indicator.
    current_loops = state.get("loop_count", 0) + 1  # Increments local iteration records by one unit step.
    is_fallback = state.get("fallback_attempt", False)  # Pulls the active execution phase mode validation status.
    
    llama3 = OllamaLLM(  # Instantiates the underlying base model wrapper module driver instance.
        model="llama3.1:latest",  # Targets your locally installed Llama 3.1 model parameter file.
        temperature=0.0,  # Strips model randomness factors out entirely to force deterministic query syntax generation.
        timeout=30.0  # Safe watchdog timer limit protecting runtime execution cycles against unexpected freeze frames.
    )  # Concludes model object setup instructions.
    
    ALLOWED_SCHEMA_CONTEXT = """
    VALID NODE LABELS:
    - :Vehicle
    - :Article
    - :Annex
    - `Applicable test procedure`
    - :Requirement
    
    VALID RELATIONSHIP TYPES:
    - [:APPLICABLE_TO]
    - [:APPLIES_TO]
    - [:ASSOCIATED_WITH]
    """  # Imprints direct graph structure rule guidelines to guide structural generation choices.
    
    if is_fallback or current_loops > 1:  # Branching decision processing loop routing path.
        # CONTEXT FIX: Fallback now searches keywords and grabs connected nodes and relationship types!
        prompt = (  # Generates an ultra-strict instruction block for Llama's fallback routine.
            f"System: You are an isolated database driver. Output ONLY a raw valid fallback Cypher query string. No preamble, no markdown.\n"  # Sets absolute behavioral constraints.
            f"CRITICAL: Nodes ONLY have an 'id' property. Write a query that finds keyword nodes and returns their connections for deep context.\n"  # Mandates structural context constraints.
            f"User Question: {state['user_query']}\n\n"  # Injects user prompt parameters into instruction templates.
            f"Fallback Template to follow exactly:\n"  # Demands structural mirroring actions.
            f"MATCH (n)-[r]-(connected) WHERE lower(n.id) CONTAINS 'motorcycle' OR lower(n.id) CONTAINS 'sound' OR lower(n.id) CONTAINS 'level' RETURN n.id, type(r), connected.id LIMIT 25;"  # The precise neighborhood query string fallback format.
        )  # Finishes structural query prompt string binding setup.
    else:  # Standard target baseline execution path parameters selection block.
        prompt = (  # Constructs the default strict relationship matching instructions format layout.
            f"System: You are an isolated database driver. Output ONLY a valid Cypher statement. No explanations, no markdown.\n"  # Strips conversational headers away.
            f"--- STRICT ALLOWED SCHEMA ---\n{ALLOWED_SCHEMA_CONTEXT}\n-------------------------\n"  # Pins graph shape data to prompt maps.
            f"CRITICAL RULES:\n"  # Opens restriction listing logs.
            f"1. Every node ONLY contains the property 'id'. Fields like '.name', '.title', or '.category' DO NOT EXIST.\n"  # Denies hallucinated variables.
            f"2. Never use inline property filters like (v:Vehicle {{id: '...'}}). Always use the pattern: WHERE lower(v.id) CONTAINS 'value'.\n"  # Forces search flexibility.
            f"3. Never alter relationship names. Only use exact matches from the schema context above.\n\n"  # Enforces true graph path labels.
            f"Target Structural Example:\n"  # Shows gold standard layout templates.
            f"MATCH (v:Vehicle)-[:APPLICABLE_TO]->(t:`Applicable test procedure`)\n"  # Maps typical query design.
            f"WHERE lower(v.id) CONTAINS 'motorcycle' AND lower(t.id) CONTAINS 'sound'\n"  # Sets conditional filters.
            f"RETURN t.id LIMIT 10;\n\n"  # Sets return constraints.
            f"User Question: {state['user_query']}"  # Injects original user text into setup.
        )  # Concludes base instruction layout variable assembly.
        
    print("[NODE 1] Invoking Llama 3.1 model...", flush=True)  # Tracking log milestone tracker updates.
    try:  # Opens error interception pipeline for model query executions.
        response = llama3.invoke(prompt)  # Calls the local LLM engine to extract query text structures.
        print(f"[NODE 1] Raw Llama response captured.", flush=True)  # Debug milestone reporting log verification trace.
    except Exception as e:  # Fallback intercept trigger if Llama drops pipeline execution streams.
        print(f"[NODE 1] Llama timed out, applying hardcoded recovery.", flush=True)  # Logs system alert updates immediately.
        response = "MATCH (n)-[r]-(c) WHERE lower(n.id) CONTAINS 'sound' RETURN n.id, type(r), c.id LIMIT 10;"  # Hardcoded structural emergency bypass script.
        
    return {"cypher_query": response, "loop_count": current_loops}  # Updates graph storage values to pass forward down structural node lines.


def execute_graph_query(state: AgentState):  # Declares Node 2 execution structure block routing handling logic.
    print("\n[NODE 2] Entering execute_graph_query...", flush=True)  # Logs system milestone tracker details.
    raw_query = state["cypher_query"]  # Pulls raw unchecked model outputs from memory slots.
    
    # --- AUTOMATIC CYPHER REPAIR PIPELINE ---
    clean_query = raw_query.replace("`", "").replace("*", "").strip()  # Scrubs potential markdown formatting tricks out of strings.
    
    if "MATCH" in clean_query.upper():  # Verifies if conversational headers are present above query bodies.
        idx = clean_query.upper().find("MATCH")  # Pins precise character location offset of genuine code elements.
        clean_query = clean_query[idx:]  # Slices chat preambles out entirely to leave pure code layouts behind.
        
    if "M A T C H" in clean_query.upper() or "M  A  T  C  H" in clean_query.upper():  # Detects broken character space anomalies.
        clean_query = "".join(clean_query.split())  # Collapses wide text spacing layouts together back into word blocks.
        clean_query = clean_query.replace("MATCH", "MATCH ").replace("WHERE", " WHERE ").replace("RETURN", " RETURN ")  # Inserts syntactic single-spaces into target areas for query reading.
    
    print(f"[NODE 2] Repaired Clean Cypher: {clean_query}", flush=True)  # Prints the safe, recovered script layout ahead of DB execution.
    
    try:  # Sets up a safety net container before executing code on live infrastructure.
        db = get_graph()  # Grabs current database driver object pointers.
        results = db.query(clean_query)  # Runs clean strings directly across target database nodes.
        print(f"[NODE 2] Neo4j successfully returned records: {results}", flush=True)  # Reports record collection metrics to server screens.
        
        if not results:  # Triggers if query returns completely empty response objects.
            return {"graph_data": "None", "fallback_attempt": True, "cypher_query": clean_query}  # Toggles backup flags to rewrite queries.
        return {"graph_data": str(results), "cypher_query": clean_query}  # Delivers valid output maps down pipeline streams.
        
    except Exception as e:  # Catch loop triggered if database rejects query syntax profiles.
        print(f"[NODE 2] Neo4j error captured on query execution: {str(e)}", flush=True)  # Prints core error messages directly to dashboard server screens.
        return {"graph_data": "None", "fallback_attempt": True, "cypher_query": clean_query}  # Drops back safely into correction states to start recovery processes.


def nlg_synthesize_response(state: AgentState):  # Opens final narrative layer node function definitions.
    print("\n[NODE 3] Entering nlg_synthesize_response...", flush=True)  # Logs execution progress reports.
    gemma2 = OllamaLLM(model="gemma-2:latest", temperature=0.0, timeout=30.0)  # Loads your high-accuracy summary model configuration profiles.
    
    data_context = state['graph_data']  # Retrieves raw target record lists collected out from databases.
    if data_context == "None" or not data_context:  # Fallback routing assessment logic checkpoint validation trace.
        data_context = "No direct paths found. However, remind the user about the relevant Sound Level entities found in the local graph ecosystem."  # Forces safe conversation directives if null records pass down.
        
    prompt = (  # Generates full professional identity mapping instructions parameters layout.
        f"You are the expert Ducati Manufacturing Compliance Assistant.\n"  # Instantiates model identity profiles tracking.
        f"Database graph relationship maps: {data_context}\n"  # Supplies pure, unfiltered relational node arrays directly to context structures.
        f"Answer the user query completely: {state['user_query']}\n"  # Re-injects target customer objective queries into window maps.
        f"Review the structural pairs (Source ID -> Relationship Type -> Target ID) found in the database data above, and provide a clear natural language breakdown explaining which regulatory test requirements apply."  # Mandates technical synthesis execution structures.
    )  # Shuts description string configurations down.
    
    try:  # Wraps terminal compilation functions within defensive catch loops.
        response = gemma2.invoke(prompt)  # Calls the summarizing local language model instance framework.
        print("[NODE 3] Gemma 2 successfully responded!", flush=True)  # Confirms text creation success metrics onto systems log outputs.
    except Exception as e:  # Breakout trigger path block if summary drivers crash down unexpectedly.
        response = f"Synthesizer timed out. Raw graph layout returned: {data_context}"  # Hands developer back base raw datasets to ensure data isn't lost.
        
    return {"final_answer": response}  # Packs response strings tightly into active graph context variables.

# ---------------------------------------------------------
# 4. WORKFLOW GRAPH ROUTING
# ---------------------------------------------------------
def route_after_db(state: AgentState):  # Evaluates active state fields to dynamically map execution routing roads.
    if state.get("loop_count", 0) >= 2:  # Safety ceiling check tracking condition limits.
        return "nlg_node"  # Escapes loops instantly to generate summary statements with available data elements.
    if state.get("graph_data") == "None":  # Triggers if prior queries generated clean zero record feedback loops.
        return "nlu_node"  # Routes workflow tracking paths backwards into Node 1 to run fallback query rules.
    return "nlg_node"  # Progresses cleanly to writing out final summary metrics if data arrays exist.

workflow = StateGraph(AgentState)  # Initializes core state machine layout blueprint tracking engine instances.
workflow.add_node("nlu_node", nlu_generate_cypher)  # Registers structural translation function modules onto structural blueprints.
workflow.add_node("db_node", execute_graph_query)  # Maps pipeline search database modules onto systemic blueprint indices.
workflow.add_node("nlg_node", nlg_synthesize_response)  # Assigns final speech synthesis nodes onto structural network routes.

workflow.set_entry_point("nlu_node")  # Locks entry parameters down onto the initial Llama generation functional segment.
workflow.add_edge("nlu_node", "db_node")  # Forges unconditional forward data roads straight from Node 1 into Node 2.
workflow.add_conditional_edges("db_node", route_after_db, {"nlu_node": "nlu_node", "nlg_node": "nlg_node"})  # Plugs intelligent routing options flags securely between data checks.
workflow.add_edge("nlg_node", END)  # Signals workflow layout termination parameters upon reaching summary goals.

app = workflow.compile()  # Processes blueprint layout architectures down into live executable program assets.

def run_ducati_agent(user_question: str) -> dict:  # Exposes a clean system interface hook function for app_10_4_comments_ship.py to use.
    initial_input = {"user_query": user_question, "fallback_attempt": False, "graph_data": "", "loop_count": 0}  # Structures the primary dictionary parameters package template.
    final_output = app.invoke(initial_input)  # Ignites workflow state machines from baseline origins to processing endpoints.
    return {  # Packages key system outcome details back out to frontend interfaces.
        "final_answer": final_output.get("final_answer", "No answer formulated."),  # Ships summary text assets straight to chat layout render blocks.
        "cypher_query": final_output.get("cypher_query", "No query compiled.")  # Provides technical query data code metrics for dropdown debug panels.
    }  # Shuts data dictionary transport objects down.