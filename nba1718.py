import urllib.request
import gzip
from bs4 import BeautifulSoup

class NBA_Team(object):

	def __init__(self, team_name, conference, record, proj_record, PoP, PoF, PoC):
		self.team_name = team_name
		self.record = record
		self.proj_record = proj_record
		self.conference = conference
		self.PoP = PoP
		self.PoF = PoF
		self.PoC = PoC

	def dump(self):
		return {
			'name': self.team_name,
			'record': self.record,
			'proj_record': self.proj_record,
			'conference': self.conference,
			'percent_playoffs': self.PoP,
			'percent_finals': self.PoF,
			'percent_championship': self.PoC
		}

url = "https://projects.fivethirtyeight.com/2018-nba-predictions/"
response = urllib.request.urlopen(url) 
# html of the page
html = gzip.decompress(response.read())
html_tree = BeautifulSoup(html, 'html.parser')

team_rows = html_tree.find(id='standings-table').find('tbody').select('tr')

teams = []
for row in team_rows:
	name_and_record = row.select_one("td.team")
	teams.append(NBA_Team(
			team_name = name_and_record['data-str'],
			record = name_and_record.select_one("span.record.desktop").getText(),
			conference = row.select_one("td.conference").getText(),
			proj_record = row.select_one("td.proj-rec").getText(),
			PoP = float(row.select_one("td.pct.div")['data-val']),
			PoF = float(row.select_one("td.pct.top-seed")['data-val']),
			PoC = float(row.find("td", class_="pct")['data-val'])
		))


