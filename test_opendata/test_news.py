# Новости
import pytest
import requests


# Новости
@pytest.mark.parametrize("num", ["0", "1", "2", "3", "4"])
def test_news(num):
    news = "https://torgi.gov.ru/new/public/news/reg?categ="
    news_all = requests.get(news + num, timeout=10)
    assert news_all.status_code == 200


all_news = [str(i) for i in range(1, 252)]


@pytest.mark.parametrize("num_lot", all_news)
def test_all_news(num_lot):
    url_news = "https://torgi.gov.ru/new/public/news/detail/"
    news_result = requests.get(url_news + num_lot, timeout=10)
    assert news_result.status_code == 200


@pytest.mark.parametrize("num_lot_404", [str(int(all_news[-1]) + 1), "0", "word"])
def test_all_news_404(num_lot_404):
    url_news = "https://torgi.gov.ru/new/public/news/detail/"
    news_result = requests.get(url_news + num_lot_404, timeout=10)
    assert news_result.status_code == 404
   


