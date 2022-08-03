import pandas as pd
import datetime

def create_table(fromtsv,tomd):

    df = pd.read_csv(fromtsv, delimiter="\t")[['Nome completo', 'Instituição']]

    df['Nome completo'] = df['Nome completo'].transform(str.title)

    df.sort_values('Nome completo', inplace=True)

    today = datetime.datetime.today()
    
    with open("../inscritos/" + tomd, "w") as fp:

        fp.write(
"""---
layout: default
---

<h1 class="display-5 mb-3">
Lista de inscritos
</h1>
"""
            )
        fp.write(today.strftime("\nÚltima atualização: %d/%m/%y às %H:%M\n") +
                 '<br>\n')
# <!-- <input class="form-control" id="myInput" type="text" placeholder="Buscar..">
# <br> -->
# """
#         )
        fp.write('<div class="table-responsive">\n')
        fp.write('<table class="table table-striped">\n')
        fp.write('<thead>' +
                 '<tr><th>Nome</th><th>Instituição</th></tr>' +
                 '</thead>')
        fp.write('<tbody id="myTable">\n')
        
        for (i,r) in df.iterrows():

            fp.write('\t<tr><td>' + r['Nome completo'] + '</td><td>' +
                     r['Instituição'] + '</td></tr>\n')

        fp.write('</tbody>\n</table>\n</div>')
#         fp.write(
# """
# <script>
# $(document).ready(function(){
#   $("#myInput").on("keyup", function() {
#     var value = $(this).val().toLowerCase();
#     $("#myTable tr").filter(function() {
#       $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
#     });
#   });
# });
# </script>
# """
#             )

create_table('inscritos.tsv', 'index.md')
