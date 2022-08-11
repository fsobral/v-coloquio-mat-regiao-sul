import pandas as pd
import re

schedule = pd.read_csv("schedule.tsv", dtype=str, delimiter="\t")

tipos = {
    "Plenária": "palestra",
    "Minicurso": "mini",
    "Sessão Temática": "palestra",
    "Mesa Redonda": "atividade",
    "Atividade Cultural": "atividade"
    }

rnome = re.compile("[^(]+")

for i, row in schedule.iterrows():

    for spkr in row["Palestrantes"].split(";"):

        tipo = tipos[row["Tipo"].split(";")[0]]

        ativ = ""
        if tipo == "atividade":
            ativ = row["Tipo"].split(";")[0]
        
        ch = ""
        if tipo == "mini":
            ch = "4,5"
        
        name = (rnome.match(spkr)[0]).strip()
        
        s = "\\para{{{0:s}}}{{{1:s}}}{{{2:s}}}{{{3:s}}}{{{4:s}}}\n".format(
            name, row["Titulo"].strip(), tipo, ch, ativ
        )

        print(s)
        
#     if (i == 0) or (not pd.isna(row["Dia"])):

#         currDay  = row["Dia"]
#         currRoom = row["Local"].strip()

#         # Add the room to the list of rooms. In case the same room
#         # appears twice, keep the last information
#         rooms[currRoom] = {
#             "name": currRoom,
#             "hide": False
#         }

#         # If is changing the day and is not the first row, then flush
#         # all the information about the rooms to the current day
#         if i > 0:

#             day["rooms"] = list(rooms_for_a_day.values())

#             days.append(day)

#         # Create a new day
#         day = {"name": str.capitalize(row["Dia semana"]),
#                "abbr": abbr[row["Dia semana"]],
#                "date": row["Dia"],
#                "rooms": []}

#         rooms_for_a_day = {}

#     # Update information about the rooms
#     if (not pd.isna(row["Local"])) and (row["Local"] != currRoom):

#         currRoom = row["Local"].strip()

#         # Add the room to the list of rooms. In case the same room
#         # appears twice, keep the last information
#         rooms[currRoom] = {
#             "name": currRoom,
#             "hide": False
#         }
        
#     if currRoom not in rooms_for_a_day:

#         rooms_for_a_day[currRoom] = {"name": currRoom,
#                                      "talks": []}

#     # Talks
#     talk = {
#         "meta" :
#         {
#             "name": row["Titulo"],
#             "categories": list(map(str.strip, row["Tipo"].split(';'))),
#             "speakers": list(map(str.strip, row["Palestrantes"].split(';')))
#         },
#         "abstract": str(row["Resumo"]).replace("\\n", "\n")
#     }
#     # Add links to recordings
#     if not pd.isna(row["Link"]):
#         link = [
#             {"name": "Assistir gravação", "absolute_url": row["Link"],
#              "icon":"play"}
#         ]
#         talk["meta"].update({
#             "links": link,
#             "live":  link
#             })

#     talks.append(talk)

#     # Speaker

#     for name in talk["meta"]["speakers"]:
    
#         speakers[name] = {
#             "name": name,
#             "first_name": "",
#             "last_name" : name
#         }

#     # Create a talk in that room
#     rooms_for_a_day[currRoom]["talks"].append(
#         {"name": talk["meta"]["name"],
#          "time_start": row["Inicio"],
#          "time_end":   row["Fim"]}
#         )

# day["rooms"] = list(rooms_for_a_day.values())

# days.append(day)

# # Save program
# with open("../_data/program.yml", "w") as fp:

#     fp.write(yaml.dump({"days": days}, allow_unicode=True))

# # Generate rooms files
# # ####################

# for i, r in enumerate(rooms.values()):

#     with open("../_rooms/room{0:02d}.md".format(i), "w") as fp:

#         fp.write("---\n")
#         fp.write(yaml.dump(r, allow_unicode=True))
#         fp.write("---\n")


# # Generate talks files
# # ####################

# for i, t in enumerate(talks):

#     with open("../_talks/talk{0:02d}.md".format(i), "w") as fp:
    
#         fp.write("---\n")
#         fp.write(yaml.dump(t["meta"], allow_unicode=True))
#         fp.write("---\n\n")
#         fp.write(t["abstract"])

# # Generate speakers files
# # #######################

# for i, s in enumerate(speakers.values()):

#     with open("../_speakers/speaker{0:02d}.md".format(i), "w") as fp:

#         fp.write("---\n")
#         fp.write(yaml.dump(s, allow_unicode=True))
#         fp.write("\n---\n\n")
