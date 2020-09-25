#!/usr/bin/env python3
import sys
import json


def parse_folder(folder):
    output = ""
    for child in folder:
        # Si dossier
        if 'children' in child:
            # ajouter le texte
            output += "<DT><H3 ADD_DATE=\"000\" LAST_MODIFIED=\"000\">Nouveau dossier</H3>\n".format(
                child['dateAdded'],
                child['lastModified'],
                child['title']
            )
            output += "<DL><p>\n"
            output += parse_folder(child['children']) # ajouter les favoris du dossier
            output += "</DL><p>\n"
        # Si favori 
        else:
            output += "<DT><A HREF=\"{}\" ADD_DATE=\"{}\" ICON=\"{}\">{}</A>\n".format(
                child['uri'],
                child['dateAdded'],
                child['iconuri'],
                child['title']
            )


def generate_output(toolbar):
    output = "<!DOCTYPE NETSCAPE-Bookmark-file-1>\n"
    output += "<META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html; charset=UTF-8\">\n"
    output += "<TITLE>Bookmarks</TITLE>\n"
    output += "<H1>Bookmarks</H1>\n"
    output += "<DL><p>\n"
    output += "<DT><H3 ADD_DATE=\"{}\" LAST_MODIFIED=\"{}\" PERSONAL_TOOLBAR_FOLDER=\"true\">Favoris</H3>\n".format(
        toolbar['dateAdded'],
        toolbar['lastModified']
    )
    output += "<DL><p>\n"

    # PARSAGE de la toolbar
    output += parse_folder(toolbar['children'])
    
    output += "</DL><p>\n"
    output += "</DL><p>\n"



args = sys.argv
file_name = args[1]
output_name = file_name.split(".")[0] + "_out.html"

file = open(file_name, 'r')
parsed_json = json.load(file)
file.close

toolbar = [child for child in parsed_json['children'] if child['guid'] == 'toolbar_____'][0]

output = generate_output(toolbar)
output_file = open(output_name, 'w')
output_file.write(output)
output_file.close