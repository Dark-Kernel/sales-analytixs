import requests
from bs4 import BeautifulSoup
import csv
import logging
from typing import List, Dict
import time

class WebScraper:
    def __init__(self, base_url: str):
        """
        Initialize the web scraper with a base URL.
        
        Args:
            base_url (str): The base URL of the website to scrape
        """
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def scrape_books(self, max_pages: int = 5) -> List[Dict[str, str]]:
        """
        Scrape book information from multiple pages.
        
        Args:
            max_pages (int): Maximum number of pages to scrape
        
        Returns:
            List of dictionaries containing book information
        """
        all_books = []
        
        for page in range(1, max_pages + 1):
            try:
                url = f"{self.base_url}/catalogue/page-{page}.html" if page > 1 else self.base_url
                response = requests.get(url, headers=self.headers, timeout=10)
                
                # Raise an exception for bad HTTP responses
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                books = soup.find_all('article', class_='product_pod')
                
                if not books:
                    self.logger.warning(f"No books found on page {page}")
                    break
                
                for book in books:
                    book_info = self._extract_book_details(book)
                    if book_info:
                        all_books.append(book_info)
                
                # Respectful scraping: Add delay between requests
                time.sleep(1)
                
            except requests.RequestException as e:
                self.logger.error(f"Error scraping page {page}: {e}")
                continue
        
        return all_books

    def _extract_book_details(self, book_element) -> Dict[str, str]:
        """
        Extract detailed information for a single book.
        
        Args:
            book_element (BeautifulSoup): Beautiful Soup element for a book
        
        Returns:
            Dictionary of book details
        """
        try:
            title = book_element.h3.a['title']
            price = book_element.find('p', class_='price_color').text[1:]  # Remove £ symbol
            availability = book_element.find('p', class_='instock availability').text.strip()
            rating = book_element.find('p', class_='star-rating')['class'][1]  # Star rating
            book_url = self.base_url + '/' + book_element.h3.a['href']
            
            return {
                'Title': title,
                'Price': price,
                'Availability': availability,
                'Rating': rating,
                'URL': book_url
            }
        
        except Exception as e:
            self.logger.warning(f"Could not extract book details: {e}")
            return {}

    def save_to_csv(self, books: List[Dict[str, str]], filename: str = 'scraped_books.csv'):
        """
        Save scraped book data to a CSV file.
        
        Args:
            books (List[Dict]): List of book dictionaries
            filename (str): Output CSV filename
        """
        if not books:
            self.logger.warning("No data to save!")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = books[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for book in books:
                    writer.writerow(book)
            
            self.logger.info(f"Data saved to {filename}")
        
        except IOError as e:
            self.logger.error(f"Error saving CSV: {e}")

def main():
    base_url = 'http://books.toscrape.com'
    scraper = WebScraper(base_url)
    
    books = scraper.scrape_books(max_pages=3)
    scraper.save_to_csv(books)

if __name__ == "__main__":
    main()
