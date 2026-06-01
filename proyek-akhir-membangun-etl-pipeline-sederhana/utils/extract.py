import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://fashion-studio.dicoding.dev"


def fetch_page(url, session=None):
    """Mengambil konten HTML dari sebuah URL."""
    try:
        if session is None:
            session = requests.Session()
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching website: {e}")
        return None
    except Exception as e:
        print(f"An error occurred during fetching: {e}")
        return None


def parse_products(html_content, timestamp):
    """Mem-parse produk dari konten HTML satu halaman."""
    products = []
    try:
        soup = BeautifulSoup(html_content, "html.parser")

        cards = soup.find_all("div", class_="collection-card")

        for card in cards:
            try:
                details = card.find("div", class_="product-details")
                if not details:
                    continue

                # ── Title ──────────────────────────────────────────
                title_tag = details.find("h3", class_="product-title")
                title = title_tag.text.strip() if title_tag else None

                # ── Price ──────────────────────────────────────────
                # Ada dua kemungkinan:
                # 1. <span class="price">$102.15</span>  → harga normal
                # 2. <p class="price">Price Unavailable</p> → tidak tersedia
                price = None
                price_container = details.find("div", class_="price-container")
                if price_container:
                    span_price = price_container.find("span", class_="price")
                    if span_price:
                        price = span_price.text.strip()
                    else:
                        p_price = price_container.find("p", class_="price")
                        if p_price:
                            price = p_price.text.strip()

                # ── Rating, Colors, Size, Gender ───────────────────
                rating = colors = size = gender = None
                detail_paragraphs = details.find_all(
                    "p", style=lambda s: s and "color: #777" in s
                )

                for p in detail_paragraphs:
                    text = p.text.strip()
                    if "Rating" in text:
                        rating = text
                    elif "Colors" in text:
                        colors = text
                    elif "Size" in text:
                        size = text
                    elif "Gender" in text:
                        gender = text

                products.append(
                    {
                        "Title": title,
                        "Price": price,
                        "Rating": rating,
                        "Colors": colors,
                        "Size": size,
                        "Gender": gender,
                        "timestamp": timestamp,
                    }
                )

            except Exception as e:
                print(f"Error parsing a product card: {e}")
                continue

    except Exception as e:
        print(f"An error occurred during parsing: {e}")

    return products


def scrape_main(url=BASE_URL, start_page=1, total_pages=50):
    """Scraping seluruh 50 halaman dan mengembalikan list produk."""
    products = []
    timestamp = datetime.now().isoformat()

    try:
        session = requests.Session()

        for page in range(start_page, start_page + total_pages):
            # Halaman 1 → URL utama, halaman 2+ → /page2, /page3, dst
            if page == 1:
                page_url = url
            else:
                page_url = f"{url}/page{page}"

            print(f"Scraping halaman {page}: {page_url}")
            html = fetch_page(page_url, session=session)

            if html is None:
                print(f"  ⚠ Halaman {page} tidak dapat diakses, dilewati.")
                continue

            page_products = parse_products(html, timestamp)
            products.extend(page_products)
            print(f"  → {len(page_products)} produk ditemukan")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching website: {e}")
        return None
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return None

    print(f"\nTotal produk ter-scrape: {len(products)}")
    return products
