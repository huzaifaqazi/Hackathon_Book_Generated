from loguru import logger
from ..services.llm import get_llm_response

def construct_agent_prompt(query: str, retrieved_context: list[dict], selected_text: str = None) -> (list[dict], list[dict]):
    system_message = (
        "You are a helpful AI assistant that answers questions based ONLY on the provided context from a book. "
        "Do not use any external knowledge. If the answer is not in the context, state that you cannot answer. "
        "Provide source URLs from the context for your answer."
    )

    context_str = ""
    sources = []
    
    # Build context string and collect sources from retrieved_context
    for i, chunk in enumerate(retrieved_context):
        context_str += f"--- Source {i+1} (URL: {chunk.get('source_url', 'N/A')} - Title: {chunk.get('page_title', 'N/A')}) ---\n"
        context_str += chunk.get('content', '') + "\n\n"
        sources.append({"url": chunk.get('source_url'), "title": chunk.get('page_title')})

    if selected_text:
        # If selected_text is provided, prioritize it and clear other sources
        user_message = (
            f"Here is some selected text from the book:\n\n{selected_text}\n\n"
            f"Based ONLY on this selected text, please answer the following question: {query}"
        )
        final_sources = [] # No other sources if only selected text is used
    else:
        # Otherwise, use the context built from retrieved chunks
        user_message = f"Based ONLY on the following context, please answer the question: {query}\n\nContext:\n{context_str}"
        final_sources = sources # Use collected sources from retrieved chunks
    
    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ], final_sources

def get_answer_from_agent(query: str, retrieved_context: list[dict], selected_text: str = None) -> (str, list[dict]):
    logger.info(f"Agent: Processing query: '{query}'")
    logger.info(f"Agent: Retrieved context summary: {[c.get('source_url', 'N/A') for c in retrieved_context]}")
    logger.info(f"Agent: Selected text: {selected_text[:100] if selected_text else 'N/A'}")

    messages, sources = construct_agent_prompt(query, retrieved_context, selected_text)
    logger.info(f"Agent: Constructed messages for LLM: {messages}")
    
    llm_response = get_llm_response(messages)
    logger.info(f"Agent: Raw LLM response: {llm_response}")
    return llm_response, sources

if __name__ == "__main__":
    # Example usage (requires LLM setup and context)
    from ..services.retrieval import retrieve_chunks
    test_query = "What is ROS2?"
    retrieved = retrieve_chunks(test_query)
    answer, sources = get_answer_from_agent(test_query, retrieved)
    print(f"Answer: {answer}")
    print(f"Sources: {sources}")

    # Test with selected text
    selected = "ROS 2 (Robot Operating System 2) is an open-source, meta-operating system for robots. It provides libraries and tools to help software developers create robot applications."
    answer_selected, sources_selected = get_answer_from_agent("What is it?", [], selected)
    print(f"Answer with selected text: {answer_selected}")
    print(f"Sources with selected text (should be empty as context comes from selected_text): {sources_selected}")
