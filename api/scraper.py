from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup

def get_citations_needed_count(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return len(soup.find_all('span', string='citation needed'))

def get_citations_needed_report(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    report = []
    for citation in soup.find_all('span', string='citation needed'):
        paragraph = citation.find_parent('p')
        if paragraph:
            report.append(paragraph.get_text().strip())
    return '\n\n'.join(report)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = 'https://en.wikipedia.org/wiki/Job_(biblical_figure)'
        count = get_citations_needed_count(url)
        report = get_citations_needed_report(url)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        response_message = f"Citations Needed Count: {count}\n\nCitations Needed Report:\n{report}"
        self.wfile.write(response_message.encode())
        return
