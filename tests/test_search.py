from api.search import Index

texts = [
    "This is a sample document about a dog.",
    "This is a sample document about a cat.",
    "Cat cat super cat more cat kitty cat.",
    "Diggity dog diggity dog deputy dog.",
]

def test_search():
    index = Index(texts)
    indices = index.search("cat")
    assert indices == [2, 1]

    indices = index.search("dog")
    assert indices == [3, 0]

def test_search_no_match():
    index = Index(texts)
    indices = index.search("asdf")
    assert indices == []
