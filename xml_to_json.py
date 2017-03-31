#!/usr/bin/env python

from bs4 import BeautifulSoup
import json
import sys
from pprint import pprint

files = sys.argv[1:]

for filename in files:
  with open(filename) as f:
    xml = BeautifulSoup(f.read())
    versions = []
    for page in xml.find_all("page"):
      guid = page.find("guid").string
      links = {}
      total_links = 0
      for version in page.find_all("version"):
        name = version.find("name").string
        dt = version.find("createdon").string
        ct = version.find("contenttext").string or ""
        if ct:
          content_soup = BeautifulSoup(ct)
          for link in content_soup.find_all("a", href=True):
            href = link['href']
            index = href.find("page_guid=")
            if index > 0:
              linked_guid = href[index + len("page_guid="):]
              pair_id = guid + linked_guid
              if pair_id not in links:
                links[pair_id] = {"id": pair_id, "to": linked_guid, "from": guid, "width": 0}
                links[pair_id]['width'] += 1
                total_links += 1
        versions.append({"guid": guid, "links": links, "total_links": total_links, "created_on": dt, "title": name, "length": len(ct)});
  with open(filename.replace("xml", "json"), "w") as f:
    json.dump(versions, f)
