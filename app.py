from flask import Flask, render_template, jsonify, request, redirect, url_for
from load_corpus import load_from_tsv
from models import Sentence, Word
import csv
import uuid
import os


app = Flask(__name__)
corpus = load_from_tsv("data/kubeo_corpus.tsv")

#página raiz
@app.route("/")
def index():
    #Lista dos dados do template
    sentences_data = []

    #Percorre cada item do dicionário de frases; sentence_id é o key do Dicionário, sentence_obj é o conteúdo
    for sentence_id, sentence_obj in corpus.sentences.items():
        
        #Gera o HTML formatado da frase atual a partir do objeto Sentence
        html_content = sentence_obj.render_html()
        
        #Cria uma tupla com os IDs e o HTML resultante
        data_tuple = (sentence_id, html_content)
        
        # Adiciona a tupla na lista de dados
        sentences_data.append(data_tuple)

    #Retorna a lista de dados para o Flask renderizar a partir do template
    return render_template("index.html", sentences=sentences_data)

@app.route("/sentence/<sid>")
def sentence_view(sid):
    #busca a frase pela ID no dicionário
    s = corpus.sentences.get(sid)
    #caso não encontrado, emite erro
    if not s:
        return "Frase não encontrada.", 404
    #senão, retorna a instância de Sentence
    return render_template("sentence.html", sid=sid, sentence=s)

@app.route("/api/word/<word_id>")
def api_word(word_id):
    w = corpus.words.get(word_id)
    if not w:
        return jsonify({"Erro":"Palavra não encontrada."}), 404
    return jsonify({
        "id": w.id,
        "form": w.form,
        "lemma": w.lemma,
        "pos": w.pos,
        "glosa_ptbr": w.glosa_ptbr,
        "propriedades": w.propriedades,
        "sentence_id": w.sentence_id,
        "word_index": w.word_index
    })

@app.route("/word/<word_id>")
def word_details(word_id):
    #Busca a palavra no dicionário global do corpus
    w = corpus.words.get(word_id)
    
    #Se não achar, retorna erro
    if not w:
        return "Palavra não encontrada.", 404
    
    #Renderiza o novo template passando o objeto word
    return render_template("word.html", word=w)

@app.route("/search")
def search():
    q = request.args.get("q", "").strip() #limpando o texto do request
    results = []
    
    if q:
        #padronizando em caixa baixa
        q_lower = q.lower()

        for sentence_id, sentence in corpus.sentences.items():
            for w in sentence.words:
                
                form_match = (w.form).lower() == q_lower
                lemma_match = (w.lemma).lower() == q_lower
                glosa_match = (w.glosa_ptbr).lower() == q_lower

                if form_match or lemma_match or glosa_match:
                    results.append({"sid": sentence_id, "snippet": sentence.render_html()})
                    break #Break para evitar duplicatas quando houver mais de uma ocorrência da palavra na mesma frase

    return render_template("search.html", q=q, results=results)

@app.route("/add", methods=["GET", "POST"])
def add_sentence():
    if request.method == "POST":
        #Gera um novo ID para a frase (s10, s11...)
        #Pega o maior número existente e soma 1
        existing_ids = [int(sid[1:]) for sid in corpus.sentences.keys() if sid.startswith('s') and sid[1:].isdigit()]
        new_sid_num = max(existing_ids) + 1 if existing_ids else 1
        new_sid = f"s{new_sid_num}"

        
        forms = request.form.getlist('kubeo_form[]')
        lemmas = request.form.getlist('lemma[]')
        pos_tags = request.form.getlist('pos[]')
        glosses = request.form.getlist('glosa_ptbr[]')

        # Propiedades de nomes
        genders = request.form.getlist('gender[]')
        numbers = request.form.getlist('number[]')
        countables = request.form.getlist('countable[]')
        # Props de verbos
        moods = request.form.getlist('mood[]')
        tenses = request.form.getlist('tense[]')
        aspects = request.form.getlist('aspect[]')
        persons = request.form.getlist('person[]')

        #Armazenamento de palavras obtidas
        new_words = []
        #Linhas do TSV
        tsv_rows = []

        existing_word_ids = [int(wid) for wid in corpus.words.keys() if wid.isdigit()]
        # Pega o maior ID atual, ou começa do 0 se estiver vazio
        next_word_id = max(existing_word_ids) + 1 if existing_word_ids else 1
        
        for i, form in enumerate(forms):
            if not form.strip(): continue # Pula campos vazios não preenchidos

            new_word_id = str(next_word_id)
            next_word_id += 1 #Incrementa o ID para a próxima palavra
            
            # Cria o objeto Word com os dados da iteração atual
            w = Word(
                id=new_word_id,
                form=form,
                lemma=lemmas[i],
                pos=pos_tags[i],
                glosa_ptbr=glosses[i],
                propriedades={
                    "gender": genders[i],
                    "number": numbers[i],
                    "countable": countables[i],
                    "mood": moods[i],
                    "tense": tenses[i],
                    "aspect": aspects[i],
                    "person": persons[i]
                },
                sentence_id=new_sid,
                word_index=i
            )
            new_words.append(w)

            #Adiciona o struct de dados
            tsv_rows.append({
                'id': new_word_id,
                'sentence_id': new_sid,
                'word_index': i,
                'kubeo_form': form,
                'lemma': lemmas[i],
                'pos': pos_tags[i],
                'glosa_ptbr': glosses[i],
                'gender': genders[i],
                'number': numbers[i],
                'countable': countables[i],
                'notes': ''
            })

        #Atualizar o corpus em memória
        if new_words:
            new_sentence = Sentence(id=new_sid, words=new_words)
            corpus.add_sentence(new_sentence)

            #Persistir dados no TSV
            file_path = "data/kubeo_corpus.tsv"
            file_exists = os.path.isfile(file_path)
            
            fieldnames = ['id', 'sentence_id', 'word_index', 'kubeo_form', 'lemma',
                          'pos', 'morph_class', 'glosa_ptbr', 'gender', 'number',
                          'countable', 'mood', 'tense', 'aspect', 'person', 'notes']

            with open(file_path, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='\t') #Dicionário para TSV
                
                if not file_exists:
                    writer.writeheader()
                writer.writerows(tsv_rows)

            return redirect(url_for('sentence_view', sid=new_sid))

    return render_template("add_sentence.html")

if __name__ == "__main__":
    app.run(debug=True)
