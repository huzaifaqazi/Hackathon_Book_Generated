from ..services.llm import get_llm_response

def construct_agent_prompt(query: str, retrieved_context: list[dict], selected_text: str = None) -> list[dict]:
    system_message = (
        "You are a helpful AI assistant that answers questions based ONLY on the provided context from a book. "
        "Do not use any external knowledge. If the answer is not in the context, state that you cannot answer. "
        "Provide source URLs from the context for your answer."
    )

    context_str = ""
    sources = []
    for i, chunk in enumerate(retrieved_context):
        context_str += f"--- Source {i+1} (URL: {chunk.get('source_url', 'N/A')} - Title: {chunk.get('page_title', 'N/A')}) ---
"
        context_str += chunk.get('content', '') + "\n\n"
        sources.append({"url": chunk.get('source_url'), "title": chunk.get('page_title')})

    if selected_text:
        user_message = (
            f"Here is some selected text from the book:\n\n{selected_text}\n\n"
            f"Based ONLY on this selected text, please answer the following question: {query}"
        )
    else:
        user_message = f"Based ONLY on the following context, please answer the question: {query}\n\nContext:\n{context_str}"
    
    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ], sources

def get_answer_from_agent(query: str, retrieved_context: list[dict], selected_text: str = None) -> (str, list[dict]):
    messages, sources = construct_agent_prompt(query, retrieved_context, selected_text)
    llm_response = get_llm_response(messages)
    return llm_response, sources

if __name__ == "__main__":
    # Example usage (requires LLM setup and context)
    # from ..services.retrieval import retrieve_chunks
    # test_query = "What is ROS2?"
    # retrieved = retrieve_chunks(test_query)
    # answer, sources = get_answer_from_agent(test_query, retrieved)
    # print(f"Answer: {answer}")
    # print(f"Sources: {sources}")

    # Test with selected text
    # selected = "ROS 2 (Robot Operating System 2) is an open-source, meta-operating system for robots. It provides libraries and tools to help software developers create robot applications."
    # answer_selected, sources_selected = get_answer_from_agent("What is it?", [], selected)
    # print(f"Answer with selected text: {answer_selected}")
    # print(f"Sources with selected text (should be empty as context comes from selected_text): {sources_selected}")

