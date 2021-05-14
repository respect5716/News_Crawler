# News Crawler



## Objectives

지정된 검색어로 뉴스 수집 후 Dropbox에 업로드하는 프로그램



## Execute

1. Make config file

```
vim config.json

{
	"TIME": "20:00",
	"DROPBOX_TOKEN": "{dropbox access token}",
	"QUERY": {
		"domain1": ["query1", "query2", "query3"],
		"domain2": ["query1", "query2", "query3"]
	}
}
```



2. Build docker container

```
sudo docker run -d respect5716/news-crawler:1
```

