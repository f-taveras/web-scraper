from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

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

        query_components = parse_qs(urlparse(self.path).query)


        url = query_components.get('url', [None])[0]

        if url:
            try:
                count = get_citations_needed_count(url)
                report = get_citations_needed_report(url)
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                response_message = f"Citations Needed Count: {count}\n\nCitations Needed Report:\n{report}"
                self.wfile.write(response_message.encode())
            
            except Exception as e:
                self.send_error(500, f"Server error: {str(e)}")
        else:
            self.send_error(400, "Bad Request: Please specify a 'url' query parameter.")


        # url = 'https://en.wikipedia.org/wiki/Job_(biblical_figure)'

        # return
            
if __name__ == "__main__":
    port = 3005
    server_address = ('', port)
    httpd = HTTPServer(server_address, handler)
    print(f"Starting httpd server on {port}")
    httpd.serve_forever()
