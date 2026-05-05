from langchain_openai import ChatOpenAI
from rag.vector_store import VectorStore
from db.databricks_connector import run_query

llm = ChatOpenAI(model="gpt-4o-mini")

vector_store = VectorStore()

def agent(query):
    # Step 1: PDF context
    pdf_results = vector_store.search(query)

    # Step 2: Decide if SQL needed
    sql_needed = "profit" in query or "revenue" in query

    sql_results = None
    if sql_needed:
        sql = "SELECT * FROM contracts_finance WHERE 1=1"
        sql_results = run_query(sql)

    # Step 3: Combine context
    context = {
        "pdf": pdf_results,
        "sql": sql_results
    }

    # Step 4: LLM reasoning
    prompt = f"""
You are a contract intelligence AI.

Question: {query}

PDF Data:
{pdf_results}

Finance Data:
{sql_results}

Give final business answer.
"""

    response = llm.invoke(prompt)
    return response.content