from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader

loader = UnstructuredMarkdownLoader("D://LLMLearning//pxf77//README.md")
md_pages = loader.load()

print(f"载入后的变量类型为：{type(md_pages)}，",  f"该 Markdown 一共包含 {len(md_pages)} 页")

md_page = md_pages[0]
print(f"每一个元素的类型：{type(md_page)}.",
    f"该文档的描述性数据：{md_page.metadata}",
    f"查看该文档的内容:\n{md_page.page_content[0:][:200]}",
    sep="\n------\n")