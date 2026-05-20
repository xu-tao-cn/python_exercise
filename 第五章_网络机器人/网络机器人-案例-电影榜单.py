from lxml import html
import csv
import requests

TMDB_BASE_URL = "https://www.themoviedb.org"
TMDB_TOP_URL = "https://www.themoviedb.org/movie/top-rated"

def main():
    # 发送请求,获取高分电影榜单
    response = requests.get(TMDB_TOP_URL,timeout=60)
    # 解析数据获取电影列表
    document = html.fromstring(response.text)
    movie_list = document.xpath("/html/body/div[1]/main/section/div/div/div/div[2]/div[2]/div/section/div/div/div[1]/div")
    print(movie_list)
    # 遍历榜单,获取数据
    for movie in movie_list[0]:
        movie_url = movie.xpath("./div/div/div/a/@href")
        if movie_url:
            movie_info_url = TMDB_BASE_URL + movie_url[1]
            print(movie_info_url)


if __name__ == '__main__':
    main()
