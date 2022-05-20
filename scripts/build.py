import pandas as pd
import yaml

abbr = {"Segunda": "seg",
        "Terça": "ter",
        "Quarta": "qua",
        "Quinta": "qui",
        "Sexta": "sex"}

schedule = pd.read_csv("organizacao.csv", dtype=str)

rooms_for_a_day = {}

currRoom = None

currDay = None

days = []

for i, row in schedule.iterrows():
    
    if (i == 0) or (not pd.isna(row["Dia"])):

        currDay  = row["Dia"]
        currRoom = row["Local"].strip()

        # If is changing the day and is not the first row, then flush
        # all the information about the rooms to the current day
        if i > 0:

            day["rooms"] = list(rooms_for_a_day.values())

            days.append(day)

        # Create a new day
        day = {"name": row["Dia semana"],
               "abbr": abbr[row["Dia semana"]],
               "date": row["Dia"],
               "rooms": []}

    # Update information about the rooms
    if (not pd.isna(row["Local"])) and (row["Local"] != currRoom):

        currRoom = row["Local"].strip()
        
    if currRoom not in rooms_for_a_day:

        rooms_for_a_day[currRoom] = {"name": currRoom,
                                     "talks": []}

    # Create a talk in that room
    rooms_for_a_day[currRoom]["talks"].append(
        {"name": row["Titulo"].strip(),
         "time_start": row["Inicio"],
         "time_end":   row["Fim"]}
        )

day["rooms"] = list(rooms_for_a_day.values())

days.append(day)

with open("../_data/program.yml", "w") as fp:

    fp.write(yaml.dump({"days": days}, allow_unicode=True))


# Generate rooms files
# ####################
rooms = pd.read_csv("salas.csv")

for i, row in rooms.iterrows():

    room = {"name": row["Nome"].strip(),
            "hide": True}
            #"live": {"absolute_url": row["Link"]}}

    with open("../_rooms/room{0:02d}.md".format(i), "w") as fp:

        fp.write("---\n")
        fp.write(yaml.dump(room, allow_unicode=True))
        fp.write("---\n")


# Generate talks files
# ####################

talks = pd.read_csv("palestras.csv")

for i, row in talks.iterrows():

    talk = {"name": row["Titulo"],
            "categories": list(map(str.strip, row["Tipo"].split(';'))),
            "speakers": list(map(str.strip, row["Palestrantes"].split(';')))
            }

    with open("../_talks/talk{0:02d}.md".format(i), "w") as fp:
    
        fp.write("---\n")
        fp.write(yaml.dump(talk, allow_unicode=True))
        fp.write("---\n\n")
        fp.write(row["Resumo"])


# Generate speakers files
# #######################

speakers = pd.read_csv("palestrantes.csv", dtype=str, keep_default_na=False)

for i, row in speakers.iterrows():

    nome = row["Nome"].strip()
    sobrenome = row["Sobrenome"].strip()
    
    speaker = {"first_name": nome,
               "last_name": sobrenome,
               "name": (nome + " " + sobrenome).strip(),
               "hide": False}

    with open("../_speakers/speaker{0:02d}.md".format(i), "w") as fp:

        fp.write("---\n")
        fp.write(yaml.dump(speaker, allow_unicode=True))
        fp.write("\n---\n\n")
        fp.write(row["Instituicao"])
