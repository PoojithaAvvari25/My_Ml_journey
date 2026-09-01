from langchain_community.document_loaders import CSVLoader

loader = CSVLoader("electronic-card-transactions-June-2026-csv-tables.csv")
docs=loader.load() #can use lazy load also,can ask qns also in a specific row..value of an attr etc
print(len(docs))
print(docs[3])
