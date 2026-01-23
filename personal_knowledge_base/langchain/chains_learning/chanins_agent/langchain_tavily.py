from langchain_community.tools.tavily_search import TavilySearchResults

search = TavilySearchResults(tavily_api_key="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", max_results=2)
res = search.invoke("苹果2025WWDC发布会")
print(res)