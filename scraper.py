from scrapy.item import Item, Field

class PaperItem(Item):
    author = Field()
    name = Field()
    description = Field()
    size = Field()
