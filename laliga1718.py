import urllib.request
import gzip
from bs4 import BeautifulSoup

class Prem_Team(object):

	def __init__(self, team_name, pts, proj_pts, PoR, PoUCL, PoP):
		self.team_name = team_name
		self.pts = pts
		self.proj_pts = proj_pts
		self.PoR = PoR
		self.PoUCL = PoUCL
		self.PoP = PoP

	def dump(self):
		return {
			'name': self.team_name,
			'points': self.pts,
			'proj_points': self.proj_pts,
			'percent_relegation': self.PoR,
			'percent_champions_league': self.PoUCL,
			'percent_league_win': self.PoP
		}

url = "https://projects.fivethirtyeight.com/soccer-predictions/la-liga/"
response = urllib.request.urlopen(url) 
# html of the page
html = gzip.decompress(response.read())
html_tree = BeautifulSoup(html, 'html.parser')

team_rows = html_tree.find(id='forecast-table').find('tbody').select('tr')

teams = []
for row in team_rows:
	percentages = row.find_all("td", class_="pct")
	teams.append(Prem_Team(
			team_name = row['data-str'],
			pts = int(row.select_one("td.team").select_one("div.team-div").select_one("div.name").select_one("span.record").getText()[:-3]),
			proj_pts = float(row.select("td.num.record.drop-3")[-1].getText()),
			PoR = float(percentages[0]['data-val']),
			PoUCL = float(percentages[1]['data-val']),
			PoP = float(percentages[2]['data-val'])
		))

for team in teams:
	print(team.dump())


