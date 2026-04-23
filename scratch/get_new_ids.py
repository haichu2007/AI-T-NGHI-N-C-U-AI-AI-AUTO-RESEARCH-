import arxiv

search = arxiv.Search(
    query="cat:cs.AI OR cat:cs.LG OR cat:cs.CL OR cat:cs.CV",
    max_results=5,
    sort_by=arxiv.SortCriterion.SubmittedDate
)

new_ids = [result.get_short_id() for result in search.results()]
print(new_ids)
