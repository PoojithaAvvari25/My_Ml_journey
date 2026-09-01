from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import ShellTool
##duckduckgo search tool-->Buillt-in
# search_tool = DuckDuckGoSearchRun()
# results=search_tool.invoke('top news in india today ')
# print(results)

#shell tool--->Built-in
shell_tool=ShellTool()
results = shell_tool.invoke("dir")
print(results)
print(shell_tool.name)#prints name of tool
print(shell_tool.description)#prints doc string provided in fn
print(shell_tool.args)#prints names,types of arguments 

