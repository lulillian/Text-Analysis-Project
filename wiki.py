from mediawiki import MediaWiki

wikipedia = MediaWiki()
babson = wikipedia.page("Babson College")
print(babson.title)
print(babson.content)
