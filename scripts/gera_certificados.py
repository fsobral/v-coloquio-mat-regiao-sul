import pandas as pd
import re

from unidecode import unidecode
from datetime import datetime, timedelta

def palestras():

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


def posteres():
    
    poster = pd.read_csv("posteres.tsv", dtype=str, delimiter="\t")

    for i, row in poster.iterrows():

        name = row["Nome completo:"].strip()

        title = row["Título do trabalho aprovado:"].strip()
        
        s = "\\para{{{0:s}}}{{{1:s}}}{{{2:s}}}{{{3:s}}}{{{4:s}}}\n".format(
            name, title, "poster", "", ""
        )

        print(s)


def participacao(fulllist,attendlist,mctitle,chtot=4.5,percent=0.75):

    inscritos = pd.read_csv(fulllist, delimiter="\t")[['Nome completo', 'Endereço de e-mail']]

    inscritos['Endereço de e-mail'] = inscritos['Endereço de e-mail'].transform(str.casefold)

    inames = inscritos['Nome completo'].transform(str.strip).transform(str.casefold).transform(unidecode)

    attendees = {}

    minpart = timedelta(hours=(chtot * percent))

    r = re.compile("[^.]+$")
    rr = re.compile("^[^*@]+")
    
    for l in attendlist:
    
        atten = pd.read_csv(l, na_filter=False)

        for i, row in atten.iterrows():

            name = unidecode(row["Nome"].strip().casefold())
            surname = unidecode(row["Sobrenome"].strip().casefold())
            fullname = name + " " + surname

            email1 = ""
            email2 = ""

            if row["Enviar e-mail"] != "":
                email1 = rr.findall(row["Enviar e-mail"])[0].casefold()
                email2 = r.findall(row["Enviar e-mail"])[0].casefold()

            dtin = datetime.fromisoformat("2022-08-01 " + row["Horário de entrada"])
            dtou = datetime.fromisoformat("2022-08-01 " + row["Horário de saída"])

            part = dtou - dtin

            s = (inames == fullname)

            if sum(s) == 1:

                nid = inscritos[s].iloc[0]["Nome completo"]

            else:

                s = inames.apply(lambda x: x.startswith(name) and x.endswith(surname))

                if sum(s) == 1:

                    nid = inscritos[s].iloc[0]["Nome completo"]

                else:

                    s = inscritos["Endereço de e-mail"].apply(
                        lambda x: x.startswith(email1) and x.endswith(email2)
                    )

                    if sum(s) == 0:

                        print("{0:s} nao encontrado".format(fullname))

                        continue

                    elif sum(s) > 1:

                        ss = inames.apply(lambda x: (x.find(name) >= 0) and (x.find(surname) >= 0))

                        if sum(ss) == 1:

                            nid = inscritos[s & ss].iloc[0]["Nome completo"]

                        else:
                            
                            print("{0:s} com 2 ocorrencias!".format(fullname))

                            continue

                    else:

                        nid = inscritos[s].iloc[0]["Nome completo"]

            nid = nid.title()

            if nid not in attendees:

                attendees[nid] = part

            else:

                attendees[nid] += part

    for i in attendees.keys():

        if attendees[i] >= minpart:

            #print("{0:100s}: {1:3d}".format(i, int(100 * attendees[i].total_seconds() / (chtot * 3600))))

            cert = "\\para{{{0:s}}}{{{1:s}}}{{{2:s}}}{{{3:s}}}{{{4:s}}}\n".format(
                i, mctitle, "minipart", str(chtot), ""
            )

            print(cert)

    # for i in attendees.keys():

    #     if attendees[i] < minpart:

    #         print("{0:50s}: insuficiente ({1:f})".format(i, attendees[i].total_seconds() / (chtot * 3600)))

    # print(nid, int(part >= minpart), sum(inames == fullname),
    #       sum(inames.apply(lambda x: x.startswith(name) and x.endswith(surname))),
    #       len(inscritos[inscritos["Endereço de e-mail"].apply(
    #           lambda x: x.startswith(email1) and x.endswith(email2)
    #       )]) )


# participacao("inscritos.tsv", ["mc1-2.csv", "mc1-3.csv"],
#              "Sistemas dinâmicos: uma primeira visão",
#              chtot=3.0, percent=(0.60 * 4.5 - 1.5) / 3.0)

# participacao("inscritos.tsv", ["mc3-2.csv", "mc3-3.csv"],
#              "Uma introdução ao Cálculo Fracionário",
#              chtot=3.0, percent=(0.60 * 4.5 - 1.5) / 3.0)

# participacao("inscritos.tsv", ["mc4-2.csv", "mc4-3.csv"],
#              "Introdução à Geometria de Distâncias",
#              chtot=3.0, percent=(0.60 * 4.5 - 1.5) / 3.0)

# participacao("inscritos.tsv", ["mc5-2.csv", "mc5-3.csv"],
#              "Progressos recentes em teoria de regularidade elíptica e temas relacionados",
#              chtot=3.0, percent=(0.60 * 4.5 - 1.5) / 3.0)

# participacao("inscritos.tsv", ["mc6-2.csv", "mc6-3.csv"],
#              "Tópicos de Álgebra Homológica e aspectos computacionais",
#              chtot=3.0, percent=(0.60 * 4.5 - 1.5) / 3.0)
