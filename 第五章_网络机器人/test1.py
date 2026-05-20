from lxml import html
import csv
import requests

TMDB_BASE_URL = "https://www.themoviedb.org"
TMDB_TOP_URL = "https://www.themoviedb.org/movie/top-rated"

# 主函数，定义核心逻辑
def main():
    # 1.发送请求，获取高分电影榜单数据
    response = requests.get(TMDB_TOP_URL, timeout=60)

    # 2.解析数据，获取电影列表
    document = html.fromstring(response.text)
    movie_list = document.xpath("/html/body/div[1]/main/section/div/div/div/div[2]/div[2]/div/section/div/div/div[1]/div")

    # 3.遍历电影列表，获取电影详情
    for movie in movie_list:
        movie_urls = movie.xpath("./div/div/div/a/@href")
        if movie_urls:
            # 电影详情的url
            movie_info_url = TMDB_BASE_URL + movie_urls
            print(movie_info_url)

    # 4.保存数据，保存为 csv 文件


if __name__ == '__main__':
    main()