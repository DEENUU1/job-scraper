[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<br />
<div align="center">
  <h3 align="center">Job scraper</h3>

  <p align="center">
    A program that allows you to scrape job offers from many websites and save new offers in Google Sheet
    <br />
    <br />
    <a href="https://github.com/DEENUU1/tvtime-scraper/issues">Report Bug</a>
    ·
    <a href="https://github.com/DEENUU1/tvtime-scraper/issues">Request Feature</a>
  </p>
</div>

## Features

1. **Multi-Portal Job Scraper:**
   - The project is designed to scrape job postings from various job portals.
   - Implements the Strategy Pattern for scrapers, allowing flexibility in choosing the scraping method based on the website's structure.
   - Utilizes either requests + BeautifulSoup or Selenium, with Selenium capable of scrolling pages and handling pop-up windows.

2. **Data Management and Storage:**
   - Scraped data is efficiently stored to prevent duplication.
   - Integrated with Google Sheets for seamless data storage and accessibility.

3. **Customizable Scraping Parameters:**
   - Users can set specific links for supported job portals along with filters and sorting preferences for tailored scraping.
   - Time-based Filtering:
   - Provides an option to set a maximum age for job postings, preventing the scraping of listings older than the specified timeframe (e.g., not scraping job postings older than 3 days).

4. **Flexible Configuration:**
   - Users can configure the scraper to their preferences, enabling selective scraping based on categories or other criteria specified by the user.

5. **Automated Maintenance:**
   - The application handles cookie consent pop-ups automatically, ensuring uninterrupted scraping experience.

## Supported websites and url configuration
<details>
<summary><a href="https://bulldogjob.pl/">bulldogjob</a></summary>
```
CODE!
```
</details>

<details>
<summary><a href="https://pl.indeed.com/?from=gnav-jobsearch--indeedmobile">indeed</a></summary>
```
CODE!
```
</details>
<details>
<summary><a href="https://it.pracuj.pl/praca">it.pracuj.pl</a></summary>
```
CODE!
```
</details>
<details>
<summary><a href="https://pl.jooble.org/SearchResult">jooble</a></summary>
```
CODE!
```
</details>
<details>
<summary><a href="https://nofluffjobs.com/pl">nofluffjobs</a></summary>
```
CODE!
```
</details>
<details>
<summary><a href="https://www.olx.pl/praca/">olx</a></summary>
```
CODE!
```
</details>
<details>
<summary><a href="https://theprotocol.it/filtry/java;t/trainee,assistant;p">theprotocol</a></summary>
```
CODE!
```
</details>
<details>
<summary><a href="https://useme.com/pl/jobs/category/programowanie-i-it,35/">useme</a></summary>
```
CODE!
```
</details>

## Commands & Examples

#### Scrape all movies/shows from each genre
```bash
python main.py list-scraper
```

#### Scrape all movies/show from the given genre
```bash
python main.py list-scraper-url <url_here>
```

for example
```bash
python main.py list-scraper-url https://www.tvtime.com/pl/genres/action
```

#### Scrape details for each movies/show in database
```bash
python main.py details-scraper
```

#### Export data to JSON
```bash
python main.py export-to-json --start_page 1 --page-limit 12
```
```json
[
    {
        "id": "df22da8c-db97-4c27-86a0-e440b2d67414",
        "title": "Wakfu",
        "genre": "AKCJA",
        "production_year": null,
        "image": "https://www.tvtime.com/_next/image?url=https%3A%2F%2Fartworks.thetvdb.com%2Fbanners%2Fv4%2Fseries%2F94121%2Fposters%2F65d88839b6802_t.jpg&w=750&q=75",
        "hours": null,
        "minutes": null,
        "url": "https://www.tvtime.com/show/94121",
        "type": "Show",
        "details": true,
        "rating": null,
        "description": "Follow Yugo and his friends Amalia, Evangelyne, Tristepin, Ruel and Az as they try to rescue the World of Twelve from destruction.",
        "keywords": "FANTASY,,RODZINNY,,ANIMACJA,,PRZYGODOWY,,AKCJA",
        "actors": [
            {
                "full_name": "G\u00e9rard Surugue",
                "image": "https://www.tvtime.com/_next/image?url=https%3A%2F%2Fartworks.thetvdb.com%2Fbanners%2Fv4%2Factor%2F621366%2Fphoto%2F65324fa2daf1c_t.jpg&w=256&q=75",
                "url": "https://www.tvtime.com/people/621366-gerard-surugue",
                "id": "f16ff459-8ccd-451e-a04b-e3bbb90d6294"
            },
            {
                "full_name": "Thomas Guitard",
                "image": "https://www.tvtime.com/_next/image?url=https%3A%2F%2Fartworks.thetvdb.com%2Fbanners%2Fv4%2Factor%2F7950847%2Fphoto%2F65c62c81bac17_t.jpg&w=256&q=75",
                "url": "https://www.tvtime.com/people/7950847-thomas-guitard",
                "id": "b6813e27-f892-4b24-bb05-023e0538856b"
            }
        ]
    },
```


By default start_page is set to 1 and page_limit to 50 so you don't need to pass this options to your command
for example
```bash
python main.py export-to-json
```


## Technologies:
- Python
  - Selenium
  - Typer
- SQLite
- Docker 


## Installation

#### Clone repository
```bash
git clone https://github.com/DEENUU1/tvtime-scraper.git
```

### Without docker
#### Install requirements
```bash
pip install -r requirements.txt
```

#### Run specified command
```bash
python main.py <command_here>
```

### With docker
#### Build image
```bash
docker build -t scraper .
```

#### Run specified command
```bash
docker run scraper <command_here>
```


## Authors

- [@DEENUU1](https://www.github.com/DEENUU1)

<!-- LICENSE -->

## License

See `LICENSE.txt` for more information.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/DEENUU1/job-scraper.svg?style=for-the-badge

[contributors-url]: https://github.com/DEENUU1/job-scraper/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/DEENUU1/job-scraper.svg?style=for-the-badge

[forks-url]: https://github.com/DEENUU1/job-scraper/network/members

[stars-shield]: https://img.shields.io/github/stars/DEENUU1/job-scraper.svg?style=for-the-badge

[stars-url]: https://github.com/DEENUU1/job-scraper/stargazers

[issues-shield]: https://img.shields.io/github/issues/DEENUU1/job-scraper.svg?style=for-the-badge

[issues-url]: https://github.com/DEENUU1/job-scraper/issues

[license-shield]: https://img.shields.io/github/license/DEENUU1/job-scraper.svg?style=for-the-badge

[license-url]: https://github.com/DEENUU1/job-scraper/blob/master/LICENSE.txt

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555

[linkedin-url]: https://linkedin.com/in/kacper-wlodarczyk

[basic]: https://github.com/DEENUU1/job-scraper/blob/main/assets/v1_2/basic.gif?raw=true

[full]: https://github.com/DEENUU1/job-scraper/blob/main/assets/v1_2/full.gif?raw=true

[search]: https://github.com/DEENUU1/job-scraper/blob/main/assets/v1_2/search.gif?raw=true
