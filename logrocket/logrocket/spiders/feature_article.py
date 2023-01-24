import scrapy
from ..items import LogrocketArticleItem


class FeatureArticleSpider(scrapy.Spider):
    name = 'feature_article'
    allowed_domains = ['blog.logrocket.com']
    start_urls = ['http://blog.logrocket.com/']

    def parse(self, response):
        feature_articles = response.css("section.featured-posts div.card")
        for article in feature_articles:
            article_obj = LogrocketArticleItem(
                _id=article.css("::attr('id')").extract_first(),
                heading=article.css("h2.card-title a::text").extract_first(),
                url=article.css("h2.card-title a::attr(href)").extract_first(),
                author=article.css("span.author-meta span.post-name a::text").extract_first(),
                published_on=article.css("span.author-meta span.post-date::text").extract_first(),
                read_time=article.css("span.readingtime::text").extract_first(),
            )
            yield article_obj
