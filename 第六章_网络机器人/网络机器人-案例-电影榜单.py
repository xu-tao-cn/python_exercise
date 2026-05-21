from lxml import html
import csv
import requests

TMDB_BASE_URL = "https://www.themoviedb.org"
TMDB_TOP_URL = "https://www.themoviedb.org/movie/top-rated"

def save_all_movies(all_movie_info):
    with open("./CSV_DATA/movie_DP_info.csv", "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["电影名", "上映年份", "上映时间", "电影标签", "电影时长", "电影评分",
                                               "电影语言", "导演", "作者", "电影简介", "电影 slogan"])
        writer.writeheader()
        for movie_info in all_movie_info:
            writer.writerow({"电影名": movie_info.get("电影名"),
                             "上映年份": movie_info.get("上映年份"),
                             "上映时间": movie_info.get("上映时间"),
                             "电影标签": movie_info.get("电影标签"),
                             "电影时长": movie_info.get("电影时长"),
                             "电影评分": movie_info.get("电影评分"),
                             "电影语言": movie_info.get("电影语言"),
                             "导演": movie_info.get("导演"),
                             "作者": movie_info.get("作者"),
                             "电影简介": movie_info.get("电影简介"),
                             "电影 slogan": movie_info.get("电影 slogan")
                             })

def get_movie_info(movie_info_url):
    document = requests.get(movie_info_url)
    movie_info = html.fromstring(document.text)
    movie_name = movie_info.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/h2/a/text()")
    movie_years = movie_info.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/h2/span/text()")
    movie_dates = movie_info.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/div/span[2]/text()")
    movie_tags = movie_info.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/div/span[3]/a/text()")
    movie_cost_times = movie_info.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/div/span[4]/text()")
    movie_scores = movie_info.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[2]/div/div/div[1]/div/div[1]/div/div/@data-percent")
    movie_languages = movie_info.xpath("/html/body/div[1]/main/section/div[3]/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()")
    movie_directors = movie_info.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()")
    movie_authors = movie_info.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[3]/ol/li[2]/p[1]/a/text()")
    movie_slogans = movie_info.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[3]/h3[1]/text()")
    movie_descriptions = movie_info.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[3]/div/p/text()")

    # print(movie_name[0])
    # print(movie_years[0])
    # print(movie_dates[0])
    # print(movie_tags)
    # print(movie_cost_times[0])
    # print(movie_scores[0])
    # print(movie_languages[0])
    # print(movie_directors)
    # print(movie_authors)
    # print(movie_slogans[0])
    # print(movie_descriptions[0])

    movie_info = {
        # strip（）去掉字符串首尾的所有空白字符(包括空格、\n、\t、\r 等)
        "电影名": movie_name[0].strip() if movie_name else "",
        "上映年份": movie_years[0].strip() if movie_years else "",
        "上映时间": movie_dates[0].strip() if movie_dates else "",
        "电影标签": movie_tags[0].strip() if movie_tags else "",
        "电影时长": movie_cost_times[0].strip() if movie_cost_times else "",
        "电影评分": movie_scores[0].strip() if movie_scores else "",
        "电影语言": movie_languages[0].strip() if movie_languages else "",
        "导演": movie_directors[0].strip() if movie_directors else "",
        "作者": movie_authors[0].strip() if movie_authors else "",
        "电影简介": movie_descriptions[0].strip() if movie_descriptions else "",
        "电影 slogan": movie_slogans[0].strip() if movie_slogans else ""
    }
    return movie_info


def main():
    all_movie_info = []
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
            # print(movie_info_url)
            movie_info = get_movie_info(movie_info_url)
            # print(movie_info)
            all_movie_info.append(movie_info)
     # 保存所有数据
    save_all_movies(all_movie_info)

if __name__ == '__main__':
    main()
